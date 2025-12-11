import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple, Optional
from app.utils.math_utils import calculate_portfolio_metrics, calculate_cvar
from app.utils.logger import logger


class MetricsCalculator:
    """Calculate portfolio performance metrics and comparisons"""
    
    def __init__(self):
        self.risk_free_rate = 0.02  # 2% annual risk-free rate
    
    def calculate_comprehensive_metrics(self,
                                      weights: np.ndarray,
                                      mean_returns: np.ndarray,
                                      cov_matrix: np.ndarray,
                                      returns_data: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """Calculate comprehensive portfolio metrics"""
        try:
            # Basic metrics
            metrics = calculate_portfolio_metrics(weights, mean_returns, cov_matrix, self.risk_free_rate)
            
            # Additional metrics if returns data available
            if returns_data is not None:
                # CVaR calculation
                cvar_95 = calculate_cvar(returns_data, weights, 0.95)
                cvar_99 = calculate_cvar(returns_data, weights, 0.99)
                
                metrics.update({
                    'cvar_95': cvar_95,
                    'cvar_99': cvar_99,
                })
                
                # Downside deviation
                portfolio_returns = np.dot(returns_data, weights)
                downside_returns = portfolio_returns[portfolio_returns < 0]
                downside_deviation = np.std(downside_returns) * np.sqrt(252) if len(downside_returns) > 0 else 0.0
                
                # Sortino ratio
                sortino_ratio = (metrics['expected_return'] - self.risk_free_rate) / downside_deviation if downside_deviation > 0 else 0.0
                
                # Maximum drawdown (simplified)
                cumulative_returns = np.cumprod(1 + portfolio_returns)
                running_max = np.maximum.accumulate(cumulative_returns)
                drawdown = (cumulative_returns - running_max) / running_max
                max_drawdown = np.min(drawdown)
                
                metrics.update({
                    'downside_deviation': downside_deviation,
                    'sortino_ratio': sortino_ratio,
                    'max_drawdown': abs(max_drawdown)
                })
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating comprehensive metrics: {e}")
            return {}
    
    def calculate_portfolio_composition(self, weights: np.ndarray, asset_names: List[str]) -> Dict[str, Any]:
        """Calculate portfolio composition metrics"""
        try:
            # Filter out zero weights
            non_zero_mask = weights > 1e-6
            active_weights = weights[non_zero_mask]
            active_assets = [asset_names[i] for i in range(len(asset_names)) if non_zero_mask[i]]
            
            composition = {
                'weights': dict(zip(asset_names, weights.tolist())),
                'selected_assets': active_assets,
                'num_assets': len(active_assets),
                'concentration': {
                    'herfindahl_index': np.sum(active_weights ** 2),
                    'max_weight': np.max(active_weights),
                    'min_weight': np.min(active_weights[active_weights > 0]) if len(active_weights) > 0 else 0,
                    'weight_std': np.std(active_weights)
                }
            }
            
            return composition
            
        except Exception as e:
            logger.error(f"Error calculating portfolio composition: {e}")
            return {}
    
    def compare_portfolios(self, portfolios: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Compare multiple portfolio solutions"""
        try:
            comparison = {
                'summary': {},
                'rankings': {},
                'best_performer': {}
            }
            
            # Extract metrics for comparison
            metrics_to_compare = ['expected_return', 'volatility', 'sharpe_ratio', 'cvar_95']
            
            for metric in metrics_to_compare:
                values = {}
                for solver, portfolio in portfolios.items():
                    if 'metrics' in portfolio and metric in portfolio['metrics']:
                        values[solver] = portfolio['metrics'][metric]
                
                if values:
                    # Rank portfolios for this metric
                    if metric in ['expected_return', 'sharpe_ratio']:
                        # Higher is better
                        ranked = sorted(values.items(), key=lambda x: x[1], reverse=True)
                    else:
                        # Lower is better (volatility, cvar)
                        ranked = sorted(values.items(), key=lambda x: x[1])
                    
                    comparison['rankings'][metric] = ranked
                    comparison['summary'][metric] = values
                    comparison['best_performer'][metric] = ranked[0][0]
            
            # Overall best performer (based on Sharpe ratio)
            if 'sharpe_ratio' in comparison['best_performer']:
                comparison['overall_best'] = comparison['best_performer']['sharpe_ratio']
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing portfolios: {e}")
            return {}
    
    def calculate_efficient_frontier(self,
                                   mean_returns: np.ndarray,
                                   cov_matrix: np.ndarray,
                                   num_points: int = 50) -> Dict[str, Any]:
        """Calculate efficient frontier points"""
        try:
            from app.services.classical_optimizer import ClassicalOptimizer
            
            optimizer = ClassicalOptimizer()
            
            # Range of risk aversion parameters
            risk_aversions = np.logspace(-2, 2, num_points)  # 0.01 to 100
            
            frontier_points = []
            
            for risk_aversion in risk_aversions:
                constraints = {
                    'budget': 1.0,
                    'risk_aversion': risk_aversion,
                    'max_weight_per_asset': 1.0,
                    'allow_short_selling': False
                }
                
                result = optimizer.solve(mean_returns, cov_matrix, constraints)
                
                if result['status'] == 'optimal' and result['metrics']:
                    frontier_points.append({
                        'risk_aversion': risk_aversion,
                        'expected_return': result['metrics']['expected_return'],
                        'volatility': result['metrics']['volatility'],
                        'sharpe_ratio': result['metrics']['sharpe_ratio']
                    })
            
            return {
                'points': frontier_points,
                'num_points': len(frontier_points)
            }
            
        except Exception as e:
            logger.error(f"Error calculating efficient frontier: {e}")
            return {'points': [], 'num_points': 0}
    
    def calculate_risk_attribution(self,
                                 weights: np.ndarray,
                                 cov_matrix: np.ndarray,
                                 asset_names: List[str]) -> Dict[str, Any]:
        """Calculate risk attribution by asset"""
        try:
            # Portfolio variance
            portfolio_var = np.dot(weights.T, np.dot(cov_matrix, weights))
            
            # Marginal contribution to risk
            marginal_contrib = np.dot(cov_matrix, weights)
            
            # Component contribution to risk
            component_contrib = weights * marginal_contrib
            
            # Risk attribution
            risk_attribution = {
                'total_risk': np.sqrt(portfolio_var),
                'asset_contributions': dict(zip(asset_names, component_contrib.tolist())),
                'percentage_contributions': dict(zip(
                    asset_names, 
                    (component_contrib / portfolio_var * 100).tolist()
                ))
            }
            
            return risk_attribution
            
        except Exception as e:
            logger.error(f"Error calculating risk attribution: {e}")
            return {}