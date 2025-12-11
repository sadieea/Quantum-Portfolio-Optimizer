from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class DatasetBase(BaseModel):
    name: str
    description: Optional[str] = None


class DatasetCreate(DatasetBase):
    pass


class DatasetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class DatasetMetadata(BaseModel):
    num_rows: int
    num_assets: int
    date_range: Dict[str, str]
    columns: List[str]
    sample_data: List[Dict[str, Any]]


class Dataset(DatasetBase):
    id: int
    file_path: str
    file_size: Optional[int]
    num_assets: Optional[int]
    num_rows: Optional[int]
    date_range_start: Optional[datetime]
    date_range_end: Optional[datetime]
    columns: Optional[List[str]]
    summary_stats: Optional[Dict[str, Any]]
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class DatasetPreview(BaseModel):
    dataset: Dataset
    preview_data: List[Dict[str, Any]]
    summary_statistics: Dict[str, Any]
    correlation_matrix: Optional[Dict[str, Any]] = None


class DatasetUploadResponse(BaseModel):
    dataset: Dataset
    metadata: DatasetMetadata
    message: str