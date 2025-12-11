from pydantic import BaseModel, validator
from typing import Optional, Dict, Any, List
from enum import Enum


class SolverType(str, Enum):
    CLASSICAL = "classical"
    QUBO = "qubo"
    QAOA = "qaoa"


class Constraints(BaseModel):
    budget: float = 1.0
    max_assets: Optional[int] = None
    max_weight_per_asset: float = 1.0
    risk_aversion: float = 1.0
    discretization: int = 10
    allow_short_selling: bool = False
    
    @validator('budget')
    def budget_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Budget must be positive')
        return v
    
    @validator('risk_aversion')
    def risk_aversion_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Risk aversion must be positive')
        return v


class SolverParams(BaseModel):
    # QAOA specific
    p_layers: int = 1
    learning_rate: float = 0.1
    shots: int = 1024
    max_iterations: int = 100
    
    # QUBO specific
    num_reads: int = 1000
    chain_strength: Optional[float] = None
    
    # Classical specific
    solver: str = "ECOS"
    verbose: bool = False


class OptimizationRequest(BaseModel):
    solver: SolverType
    dataset_id: int
    constraints: Constraints
    solver_params: Optional[SolverParams] = SolverParams()
    experiment_name: Optional[str] = None
    random_seed: Optional[int] = None


class OptimizationJob(BaseModel):
    job_id: str
    experiment_id: int
    status: str
    message: Optional[str] = None
    progress: Optional[float] = None
    estimated_completion: Optional[str] = None


class OptimizationResult(BaseModel):
    experiment_id: int
    solver_type: str
    status: str
    runtime_seconds: Optional[float]
    
    # Portfolio results
    portfolio_weights: Dict[str, float]
    selected_assets: List[str]
    
    # Performance metrics
    expected_return: float
    volatility: float
    sharpe_ratio: float
    cvar_95: Optional[float]
    
    # Solver-specific metadata
    solver_metadata: Dict[str, Any]
    
    # Constraint satisfaction
    constraint_satisfaction: Dict[str, bool]