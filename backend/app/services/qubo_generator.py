import numpy as np
from typing import Dict, Any, Tuple, List
from app.utils.logger import logger
from app.utils.math_utils import normalize_weights, calculate_portfolio_metrics

try:
    import pyqubo
    PYQUBO_AVAILABLE = True
except ImportError:
    PYQUBO_AVAILABLE = False
    logger.warning("PyQUBO not available. QUBO optimization will be disabled.")


class QUBOGenerator:
    """Generate QUBO formulation for portfolio optimization"""
    
    def __init__(self):
        self.penalty_strength = 10.0
    
    def build_qubo(self,
                   mean_returns: np.ndarray,
                   cov_matrix: np.ndarray,
                   constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build QUBO formulation for portfolio optimization
        """
        if not PYQUBO_AVAILABLE:
            raise ImportError("PyQUBO is not available. Please install it with: pip install pyqubo")
        
        try:
            n_assets = len(mean_returns)
            discretization = constraints.get('discretization', 10)
            risk_aversion = constraints.get('risk_aversion', 1.0)
            
            logger.info(f"Building QUBO for {n_assets} assets with {discretization} discretization levels")
            
            # Create binary variables for each asset and weight level
            # x[i][j] = 1 if asset i gets weight level j, 0 otherwise
            x = {}
            for i in range(n_assets):
                for j in range(discretization + 1):  # 0 to discretization levels
                    x[(i, j)] = pyqubo.Binary(f'x_{i}_{j}')
            
            # Weight levels (0 to max_weight_per_asset)
            max_weight = constraints.get('max_weight_per_asset', 1.0)
            weight_levels = np.linspace(0, max_weight, discretization + 1)
            
            # Objective function
            H = 0
            
            # Return term: maximize sum(mu_i * w_i)
            for i in range(n_assets):
                for j in range(discretization + 1):
                    H -= mean_returns[i] * weight_levels[j] * x[(i, j)]
            
            # Risk term: minimize risk_aversion * w^T * Sigma * w
            for i in range(n_assets):
                for k in range(n_assets):
                    for j in range(discretization + 1):
                        for l in range(discretization + 1):
                            H += risk_aversion * cov_matrix[i, k] * weight_levels[j] * weight_levels[l] * x[(i, j)] * x[(k, l)]
            
            # Constraints as penalty terms
            penalty_strength = self.penalty_strength
            
            # Constraint 1: Each asset can have only one weight level
            for i in range(n_assets):
                constraint = sum(x[(i, j)] for j in range(discretization + 1)) - 1
                H += penalty_strength * constraint**2
            
            # Constraint 2: Budget constraint
            budget = constraints.get('budget', 1.0)
            budget_constraint = sum(
                weight_levels[j] * x[(i, j)] 
                for i in range(n_assets) 
                for j in range(discretization + 1)
            ) - budget
            H += penalty_strength * budget_constraint**2
            
            # Constraint 3: Cardinality constraint (if specified)
            max_assets = constraints.get('max_assets')
            if max_assets and max_assets < n_assets:
                # Count non-zero weights
                cardinality_constraint = sum(
                    sum(x[(i, j)] for j in range(1, discretization + 1))  # j=0 means weight=0
                    for i in range(n_assets)
                ) - max_assets
                H += penalty_strength * cardinality_constraint**2
            
            # Compile QUBO
            model = H.compile()
            qubo, offset = model.to_qubo()
            
            logger.info(f"QUBO compiled: {len(qubo)} variables, offset={offset}")
            
            return {
                'qubo_matrix': qubo,
                'offset': offset,
                'model': model,
                'variable_mapping': {
                    'assets': n_assets,
                    'discretization': discretization,
                    'weight_levels': weight_levels.tolist(),
                    'variables': list(qubo.keys())
                },
                'penalty_coefficients': {
                    'asset_selection': penalty_strength,
                    'budget': penalty_strength,
                    'cardinality': penalty_strength if max_assets else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error building QUBO: {e}")
            raise
    
    def solve_qubo(self, 
                   qubo_data: Dict[str, Any],
                   solver_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Solve QUBO using simulated annealing
        """
        try:
            try:
                import neal
            except ImportError:
                raise ImportError("Neal is not available. Please install it with: pip install neal")
            
            qubo_matrix = qubo_data['qubo_matrix']
            offset = qubo_data['offset']
            model = qubo_data['model']
            
            # Create sampler
            sampler = neal.SimulatedAnnealingSampler()
            
            # Sample
            num_reads = solver_params.get('num_reads', 1000)
            response = sampler.sample_qubo(qubo_matrix, num_reads=num_reads)
            
            # Get best solution
            best_sample = response.first.sample
            best_energy = response.first.energy + offset
            
            # Decode solution
            decoded = model.decode_sample(best_sample, vartype='BINARY')
            
            # Convert to portfolio weights
            weights = self._decode_to_weights(decoded, qubo_data['variable_mapping'])
            
            logger.info(f"QUBO solved: energy={best_energy}, num_reads={num_reads}")
            
            return {
                'status': 'optimal',
                'weights': weights,
                'energy': best_energy,
                'binary_solution': best_sample,
                'solver_info': {
                    'solver': 'neal_simulated_annealing',
                    'num_reads': num_reads,
                    'best_energy': best_energy
                }
            }
            
        except Exception as e:
            logger.error(f"Error solving QUBO: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'weights': None
            }
    
    def _decode_to_weights(self, decoded_solution: Dict, variable_mapping: Dict) -> np.ndarray:
        """Convert binary solution to portfolio weights"""
        try:
            n_assets = variable_mapping['assets']
            discretization = variable_mapping['discretization']
            weight_levels = np.array(variable_mapping['weight_levels'])
            
            weights = np.zeros(n_assets)
            
            # Extract weights from binary variables
            for i in range(n_assets):
                for j in range(discretization + 1):
                    var_name = f'x_{i}_{j}'
                    if var_name in decoded_solution and decoded_solution[var_name] == 1:
                        weights[i] = weight_levels[j]
                        break
            
            # Normalize weights
            weights = normalize_weights(weights)
            
            return weights
            
        except Exception as e:
            logger.error(f"Error decoding weights: {e}")
            return np.zeros(variable_mapping['assets'])