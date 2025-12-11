import numpy as np
import time
from typing import Dict, Any
from app.utils.logger import logger
from app.utils.math_utils import normalize_weights


class MockQUBOGenerator:
    """Mock QUBO generator for development without quantum dependencies"""
    
    def __init__(self):
        self.penalty_strength = 10.0
    
    def build_qubo(self,
                   mean_returns: np.ndarray,
                   cov_matrix: np.ndarray,
                   constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Mock QUBO formulation"""
        n_assets = len(mean_returns)
        discretization = constraints.get('discretization', 10)
        
        logger.info(f"Mock QUBO: {n_assets} assets, {discretization} levels")
        
        # Mock QUBO matrix (simplified)
        mock_qubo = {(i, j): np.random.random() for i in range(n_assets) for j in range(n_assets)}
        
        return {
            'qubo_matrix': mock_qubo,
            'offset': 0.0,
            'model': None,
            'variable_mapping': {
                'assets': n_assets,
                'discretization': discretization,
                'weight_levels': np.linspace(0, 1, discretization + 1).tolist(),
                'variables': list(mock_qubo.keys())
            },
            'penalty_coefficients': {
                'asset_selection': self.penalty_strength,
                'budget': self.penalty_strength,
                'cardinality': self.penalty_strength
            }
        }
    
    def solve_qubo(self, qubo_data: Dict[str, Any], solver_params: Dict[str, Any]) -> Dict[str, Any]:
        """Mock QUBO solver using random weights"""
        try:
            # Simulate processing time
            time.sleep(1)
            
            n_assets = qubo_data['variable_mapping']['assets']
            
            # Generate random weights and normalize
            weights = np.random.random(n_assets)
            weights = normalize_weights(weights)
            
            # Apply constraints
            max_weight = 0.3  # Mock constraint
            weights = np.minimum(weights, max_weight)
            weights = normalize_weights(weights)
            
            logger.info("Mock QUBO solved with random weights")
            
            return {
                'status': 'optimal',
                'weights': weights,
                'energy': -np.random.random(),
                'binary_solution': {'mock': 'solution'},
                'solver_info': {
                    'solver': 'mock_simulated_annealing',
                    'num_reads': solver_params.get('num_reads', 1000),
                    'best_energy': -np.random.random()
                }
            }
            
        except Exception as e:
            logger.error(f"Error in mock QUBO solver: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'weights': None
            }


class MockQAOASolver:
    """Mock QAOA solver for development without quantum dependencies"""
    
    def __init__(self):
        pass
    
    def solve_qaoa(self, qubo_data: Dict[str, Any], solver_params: Dict[str, Any]) -> Dict[str, Any]:
        """Mock QAOA solver"""
        try:
            # Simulate quantum processing time
            time.sleep(2)
            
            n_assets = qubo_data['variable_mapping']['assets']
            
            # Generate random weights and normalize
            weights = np.random.random(n_assets)
            weights = normalize_weights(weights)
            
            # Apply constraints
            max_weight = 0.25  # Mock constraint
            weights = np.minimum(weights, max_weight)
            weights = normalize_weights(weights)
            
            p_layers = solver_params.get('p_layers', 1)
            shots = solver_params.get('shots', 1024)
            
            logger.info(f"Mock QAOA solved: p={p_layers}, shots={shots}")
            
            return {
                'status': 'optimal',
                'weights': weights,
                'energy': -np.random.random(),
                'bitstring': ''.join(np.random.choice(['0', '1']) for _ in range(n_assets)),
                'optimal_parameters': np.random.random(p_layers * 2),
                'solver_info': {
                    'solver': 'mock_qaoa',
                    'p_layers': p_layers,
                    'shots': shots,
                    'max_iterations': solver_params.get('max_iterations', 100),
                    'final_energy': -np.random.random()
                }
            }
            
        except Exception as e:
            logger.error(f"Error in mock QAOA solver: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'weights': None
            }