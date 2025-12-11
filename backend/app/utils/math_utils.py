import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any
from scipy import stats
from app.utils.logger import logger


def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Calculate log returns from price data"""
    try:
        # Pivot to get tickers as columns
        price_matrix = prices.pivot(index='date', columns='ticker', values='adj_close')
        
        # Calculate log returns
        returns = np.log(price_matrix / price_matrix.shift(1)).dropna()
        
        logger.info(f"Calculated returns for {len(returns.columns)} assets over {len(returns)} periods")
        return returns
        
    except Exception as e:
        logger.error(f"Error calculating returns: {e}")
        raise


def calculate_covariance_matrix(returns: pd.DataFrame) -> np.ndarray:
    """Calculate covariance matrix with optional shrinkage"""
    try:
        # Annualize (assuming daily returns)
        cov_matrix = returns.cov() * 252
        
        logger.info(f"Calculated covariance matrix: {cov_matrix.shape}")
        return cov_matrix.values
        
    except Exception as e:
        logger.error(f"Error calculating covariance matrix: {e}")
        raise


def calculate_mean_returns(returns: pd.DataFrame) -> np.ndarray:
    """Calculate annualized mean returns"""
    try:
        # Annualize (assuming daily returns)
        mean_returns = returns.mean() * 252
        
        logger.info(f"Calculated mean returns for {len(mean_returns)} assets")
        return mean_returns.values
        
    except Exception as e:
        logger.error(f"Error calculating mean returns: {e}")
        raise


def calculate_portfolio_metrics(weights: np.ndarray, mean_returns: np.ndarray, 
                              cov_matrix: np.ndarray, risk_free_rate: float = 0.02) -> Dict[str, float]:
    """Calculate portfolio performance metrics"""
    try:
        # Expected return
        portfolio_return = np.dot(weights, mean_returns)
        
        # Portfolio variance and volatility
        portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
        portfolio_volatility = np.sqrt(portfolio_variance)
        
        # Sharpe ratio
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
        
        # Maximum drawdown (simplified)
        max_drawdown = 0.0  # Would need time series for proper calculation
        
        metrics = {
            'expected_return': float(portfolio_return),
            'volatility': float(portfolio_volatility),
            'variance': float(portfolio_variance),
            'sharpe_ratio': float(sharpe_ratio),
            'max_drawdown': max_drawdown
        }
        
        logger.info(f"Calculated portfolio metrics: Return={portfolio_return:.4f}, Vol={portfolio_volatility:.4f}")
        return metrics
        
    except Exception as e:
        logger.error(f"Error calculating portfolio metrics: {e}")
        raise


def calculate_cvar(returns: np.ndarray, weights: np.ndarray, confidence_level: float = 0.95) -> float:
    """Calculate Conditional Value at Risk (CVaR)"""
    try:
        # Portfolio returns
        portfolio_returns = np.dot(returns, weights)
        
        # VaR at confidence level
        var = np.percentile(portfolio_returns, (1 - confidence_level) * 100)
        
        # CVaR (expected shortfall)
        cvar = portfolio_returns[portfolio_returns <= var].mean()
        
        logger.info(f"Calculated CVaR at {confidence_level*100}% confidence: {cvar:.4f}")
        return float(cvar)
        
    except Exception as e:
        logger.error(f"Error calculating CVaR: {e}")
        return 0.0


def normalize_weights(weights: np.ndarray) -> np.ndarray:
    """Normalize weights to sum to 1"""
    try:
        total = np.sum(weights)
        if total > 0:
            return weights / total
        else:
            return np.zeros_like(weights)
    except Exception as e:
        logger.error(f"Error normalizing weights: {e}")
        return weights