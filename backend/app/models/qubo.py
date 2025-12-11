from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Float, Text
from sqlalchemy.sql import func
from app.database import Base


class QUBOFormulation(Base):
    __tablename__ = "qubo_formulations"

    id = Column(Integer, primary_key=True, index=True)
    
    # Problem definition
    num_variables = Column(Integer)
    num_assets = Column(Integer)
    discretization_levels = Column(Integer)
    
    # QUBO matrix (stored as JSON for smaller problems)
    qubo_matrix = Column(JSON)
    qubo_matrix_file = Column(String)  # Path to file for large matrices
    
    # Problem parameters
    risk_aversion = Column(Float)
    penalty_coefficients = Column(JSON)
    
    # Constraint encoding
    constraint_encoding = Column(JSON)
    
    # Solution
    best_solution = Column(JSON)
    best_energy = Column(Float)
    
    # Solver metadata
    solver_name = Column(String)
    solver_params = Column(JSON)
    num_reads = Column(Integer)
    
    # Associated experiment
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())