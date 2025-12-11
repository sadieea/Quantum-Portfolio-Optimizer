from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    # Solver configuration
    solver_type = Column(String, nullable=False)  # classical, qubo, qaoa
    solver_params = Column(JSON)
    
    # Constraints
    constraints = Column(JSON)
    
    # Execution metadata
    status = Column(String, default="pending")  # pending, running, completed, failed
    runtime_seconds = Column(Float)
    random_seed = Column(Integer)
    
    # Error handling
    error_message = Column(Text)
    
    # Results hash for reproducibility
    results_hash = Column(String)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"))
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User", back_populates="experiments")
    dataset = relationship("Dataset", back_populates="experiments")
    results = relationship("Result", back_populates="experiment", uselist=False)