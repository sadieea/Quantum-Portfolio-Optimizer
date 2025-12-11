from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class PerformanceMetrics(BaseModel):
    expected_return: float
    volatility: float
    variance: float
    sharpe_ratio: float
    cvar_95: Optional[float] = None
    max_drawdown: Optional[float] = None


class PortfolioComposition(BaseModel):
    weights: Dict[str, float]
    selected_assets: List[str]
    num_assets: int
    concentration: Dict[str, Any]  # sector concentration, etc.


class SolverMetadata(BaseModel):
    solver_type: str
    runtime_seconds: float
    parameters: Dict[str, Any]
    convergence_info: Optional[Dict[str, Any]] = None


class QUBOMetadata(BaseModel):
    num_variables: int
    num_constraints: int
    penalty_coefficients: Dict[str, float]
    best_energy: float
    num_reads: int


class QAOAMetadata(BaseModel):
    circuit_depth: int
    num_parameters: int
    final_energy: float
    shots: int
    convergence_history: Optional[List[float]] = None


class ResultDetail(BaseModel):
    id: int
    experiment_id: int
    
    # Portfolio composition
    portfolio: PortfolioComposition
    
    # Performance metrics
    metrics: PerformanceMetrics
    
    # Solver information
    solver_metadata: SolverMetadata
    
    # Solver-specific details
    qubo_metadata: Optional[QUBOMetadata] = None
    qaoa_metadata: Optional[QAOAMetadata] = None
    
    # Constraint satisfaction
    constraint_satisfaction: Dict[str, bool]
    
    # Timestamps
    created_at: datetime
    
    class Config:
        from_attributes = True


class ResultSummary(BaseModel):
    id: int
    experiment_id: int
    solver_type: str
    expected_return: float
    volatility: float
    sharpe_ratio: float
    runtime_seconds: float
    num_assets: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ResultComparison(BaseModel):
    classical: Optional[ResultSummary] = None
    qubo: Optional[ResultSummary] = None
    qaoa: Optional[ResultSummary] = None
    
    comparison_metrics: Dict[str, Any]
    best_performer: Optional[str] = None


class ExperimentSummary(BaseModel):
    id: int
    name: Optional[str]
    solver_type: str
    dataset_name: str
    status: str
    runtime_seconds: Optional[float]
    expected_return: Optional[float]
    volatility: Optional[float]
    sharpe_ratio: Optional[float]
    num_assets: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True