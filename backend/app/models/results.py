from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    
    # Portfolio weights and assets
    portfolio_weights = Column(JSON)  # {ticker: weight}
    selected_assets = Column(JSON)    # [ticker1, ticker2, ...]
    
    # Performance metrics
    expected_return = Column(Float)
    volatility = Column(Float)
    variance = Column(Float)
    sharpe_ratio = Column(Float)
    cvar_95 = Column(Float)
    max_drawdown = Column(Float)
    
    # Solver-specific results
    solver_metadata = Column(JSON)
    
    # QUBO-specific
    qubo_matrix = Column(JSON)
    binary_solution = Column(JSON)
    
    # QAOA-specific
    qaoa_circuit_depth = Column(Integer)
    qaoa_energy = Column(Float)
    qaoa_shots = Column(Integer)
    
    # Constraint satisfaction
    constraint_satisfaction = Column(JSON)
    
    # Foreign key
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    experiment = relationship("Experiment", back_populates="results")