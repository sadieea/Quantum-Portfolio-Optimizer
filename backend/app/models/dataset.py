from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    
    # Dataset metadata
    num_assets = Column(Integer)
    num_rows = Column(Integer)
    date_range_start = Column(DateTime)
    date_range_end = Column(DateTime)
    columns = Column(JSON)
    
    # Summary statistics
    summary_stats = Column(JSON)
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="datasets")
    experiments = relationship("Experiment", back_populates="dataset")