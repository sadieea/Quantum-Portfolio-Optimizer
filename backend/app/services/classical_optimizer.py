import numpy as np
import cvxpy as cp
from typing import Dict, Any, Tuple, Optional
from app.utils.logger import logger
from app.utils.math_utils import calculate_portfolio_metrics, normalize_weights


class ClassicalOptimizer:
    """Classical portfolio optimization using CVXPY"""
    
    def __init__(self):
        self.solver_name = "ECOS"
    
    def solve(self, 
              mean_returns: np.ndarray,
              cov_matrix: np.ndarray,
              constraints: Dict[str, Any],
              solver_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Solve portfolio optimization using mean-variance framework
        """
        try:
            n_assets = len(mean_returns)
            
            # Decision variables
            weights = cp.Variable(n_assets, nonneg=True)
            
            # Objective: maximize return - risk_aversion * risk
            risk_aversion = constraints.get('risk_aversion', 1.0)
            portfolio_return = mean_returns.T @ weights
            portfolio_risk = cp.quad_form(weights, cov_matrix)
            
            objective = cp.Maximize(portfolio_return - risk_aversion * portfolio_risk)
            
            # Constraints
            constraint_list = []
            
            # Budget constraint
            budget = constraints.get('budget', 1.0)
            constraint_list.append(weights.sum() == budget)
            
            # Maximum weight per asset
            max_weight = constraints.get('max_weight_per_asset', 1.0)
            constraint_list.append(weights <= max_weight)
            
            # Cardinality constraint (if specified)
            max_assets = constraints.get('max_assets')
            if max_assets and max_assets < n_assets:
                # Use binary variables for cardinality constraint
                binary_vars = cp.Variable(n_assets, boolean=True)
                constraint_list.append(weights <= binary_vars)
                constraint_list.append(binary_vars.sum() <= max_assets)
            
            # Short selling constraint
            if not constraints.get('allow_short_selling', False):
                constraint_list.append(weights >= 0)
            
            # Create and solve problem
            problem = cp.Problem(objective, constraint_list)
            
            # Solve
            solver = solver_params.get('solver', self.solver_name) if solver_params else self.solver_name
            problem.solve(solver=solver, verbose=solver_params.get('verbose', False) if solver_params else False)
            
            if problem.status not in ["infeasible", "unbounded"]:
                optimal_weights = weights.value
                
                # Normalize weights
                optimal_weights = normalize_weights(optimal_weights)
                
                # Calculate metrics
                metrics = calculate_portfolio_metrics(optimal_weights, mean_returns, cov_matrix)
                
                # Check constraint satisfaction
                constraint_satisfaction = self._check_constraints(optimal_weights, constraints)
                
                result = {
                    'status': 'optimal',
                    'weights': optimal_weights.tolist(),
                    'objective_value': problem.value,
                    'metrics': metrics,
                    'constraint_satisfaction': constraint_satisfaction,
                    'solver_info': {
                        'solver': solver,
                        'solve_time': problem.solver_stats.solve_time if problem.solver_stats else None,
                        'num_iters': problem.solver_stats.num_iters if problem.solver_stats else None
                    }
                }
                
                logger.info(f"Classical optimization completed successfully")
                return result
                
            else:
                logger.error(f"Optimization failed with status: {problem.status}")
                return {
                    'status': 'failed',
                    'error': f"Problem status: {problem.status}",
                    'weights': None,
                    'metrics': None
                }
                
        except Exception as e:
            logger.error(f"Error in classical optimization: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'weights': None,
                'metrics': None
            }
    
    def _check_constraints(self, weights: np.ndarray, constraints: Dict[str, Any]) -> Dict[str, bool]:
        """Check if solution satisfies constraints"""
        satisfaction = {}
        
        # Budget constraint
        budget = constraints.get('budget', 1.0)
        satisfaction['budget'] = abs(weights.sum() - budget) < 1e-6
        
        # Maximum weight constraint
        max_weight = constraints.get('max_weight_per_asset', 1.0)
        satisfaction['max_weight'] = np.all(weights <= max_weight + 1e-6)
        
        # Cardinality constraint
        max_assets = constraints.get('max_assets')
        if max_assets:
            num_selected = np.sum(weights > 1e-6)
            satisfaction['cardinality'] = num_selected <= max_assets
        
        # Non-negativity (if required)
        if not constraints.get('allow_short_selling', False):
            satisfaction['non_negative'] = np.all(weights >= -1e-6)
        
        return satisfaction