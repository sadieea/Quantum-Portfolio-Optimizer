import os
import uuid
import numpy as np
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.models.dataset import Dataset
from app.routes.auth import get_current_user
from app.schemas.dataset_schemas import (
    Dataset as DatasetSchema, DatasetCreate, DatasetPreview, 
    DatasetUploadResponse, DatasetMetadata
)
from app.utils.file_utils import (
    validate_csv_file, save_uploaded_file, validate_dataset_format, load_dataset
)
from app.utils.math_utils import calculate_returns, calculate_covariance_matrix, calculate_mean_returns
from app.utils.logger import logger

router = APIRouter()


@router.post("/upload", response_model=DatasetUploadResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = None,
    description: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and validate a new dataset"""
    try:
        # Validate file
        validate_csv_file(file)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Save file
        file_path = save_uploaded_file(file, unique_filename)
        
        # Validate dataset format and get metadata
        metadata = validate_dataset_format(file_path)
        
        # Create dataset record
        dataset_name = name or file.filename
        dataset = Dataset(
            name=dataset_name,
            description=description,
            file_path=str(file_path),
            file_size=file.size,
            num_assets=metadata['num_assets'],
            num_rows=metadata['num_rows'],
            date_range_start=metadata['date_range']['start'],
            date_range_end=metadata['date_range']['end'],
            columns=metadata['columns'],
            owner_id=current_user.id
        )
        
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        
        logger.info(f"Dataset uploaded: {dataset.id} by user {current_user.id}")
        
        return DatasetUploadResponse(
            dataset=dataset,
            metadata=DatasetMetadata(**metadata),
            message="Dataset uploaded successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading dataset: {e}")
        raise HTTPException(status_code=500, detail="Error uploading dataset")


@router.get("/", response_model=List[DatasetSchema])
async def list_datasets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all datasets for the current user"""
    try:
        datasets = (db.query(Dataset)
                   .filter(Dataset.owner_id == current_user.id)
                   .order_by(Dataset.created_at.desc())
                   .all())
        
        return datasets
        
    except Exception as e:
        logger.error(f"Error listing datasets: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving datasets")


@router.get("/samples", response_model=List[DatasetSchema])
async def list_sample_datasets():
    """List available sample datasets"""
    from datetime import datetime
    
    # This would typically load from a predefined location
    sample_datasets = [
        {
            "id": -1,
            "name": "S&P 500 Sample",
            "description": "30 large-cap stocks with 5 years of daily returns",
            "file_path": "samples/sp500_sample.csv",
            "file_size": 1024000,
            "num_assets": 30,
            "num_rows": 1250,
            "date_range_start": datetime(2019, 1, 1),
            "date_range_end": datetime(2024, 1, 1),
            "columns": ["ticker", "date", "adj_close"],
            "summary_stats": {"mean_return": 0.08, "volatility": 0.15},
            "owner_id": 0,
            "created_at": datetime(2024, 1, 1),
            "updated_at": datetime(2024, 1, 1)
        },
        {
            "id": -2,
            "name": "Government Bonds",
            "description": "Treasury bonds with various maturities",
            "file_path": "samples/bonds_sample.csv",
            "file_size": 512000,
            "num_assets": 15,
            "num_rows": 1000,
            "date_range_start": datetime(2019, 1, 1),
            "date_range_end": datetime(2024, 1, 1),
            "columns": ["ticker", "date", "adj_close"],
            "summary_stats": {"mean_return": 0.03, "volatility": 0.05},
            "owner_id": 0,
            "created_at": datetime(2024, 1, 1),
            "updated_at": datetime(2024, 1, 1)
        },
        {
            "id": -3,
            "name": "Mixed Portfolio",
            "description": "Balanced mix of stocks, bonds, and commodities",
            "file_path": "samples/mixed_sample.csv",
            "file_size": 768000,
            "num_assets": 25,
            "num_rows": 1500,
            "date_range_start": datetime(2019, 1, 1),
            "date_range_end": datetime(2024, 1, 1),
            "columns": ["ticker", "date", "adj_close"],
            "summary_stats": {"mean_return": 0.06, "volatility": 0.12},
            "owner_id": 0,
            "created_at": datetime(2024, 1, 1),
            "updated_at": datetime(2024, 1, 1)
        }
    ]
    
    return sample_datasets


@router.get("/samples/{sample_id}/preview")
async def preview_sample_dataset(sample_id: int):
    """Get preview of a sample dataset"""
    try:
        # Mock sample data for preview
        sample_previews = {
            -1: {  # S&P 500 Sample
                "preview_data": [
                    {"ticker": "AAPL", "date": "2024-01-01", "adj_close": 192.53},
                    {"ticker": "MSFT", "date": "2024-01-01", "adj_close": 376.04},
                    {"ticker": "GOOGL", "date": "2024-01-01", "adj_close": 140.93},
                    {"ticker": "AMZN", "date": "2024-01-01", "adj_close": 151.94},
                    {"ticker": "TSLA", "date": "2024-01-01", "adj_close": 248.48},
                ],
                "summary_statistics": {
                    "mean_returns": {"AAPL": 0.082, "MSFT": 0.079, "GOOGL": 0.064, "AMZN": 0.058, "TSLA": 0.121},
                    "volatilities": {"AAPL": 0.24, "MSFT": 0.22, "GOOGL": 0.26, "AMZN": 0.28, "TSLA": 0.45}
                }
            },
            -2: {  # Government Bonds
                "preview_data": [
                    {"ticker": "US10Y", "date": "2024-01-01", "adj_close": 4.25},
                    {"ticker": "US5Y", "date": "2024-01-01", "adj_close": 4.15},
                    {"ticker": "US2Y", "date": "2024-01-01", "adj_close": 4.35},
                ],
                "summary_statistics": {
                    "mean_returns": {"US10Y": 0.03, "US5Y": 0.029, "US2Y": 0.032},
                    "volatilities": {"US10Y": 0.05, "US5Y": 0.048, "US2Y": 0.052}
                }
            },
            -3: {  # Mixed Portfolio
                "preview_data": [
                    {"ticker": "AAPL", "date": "2024-01-01", "adj_close": 192.53},
                    {"ticker": "BND", "date": "2024-01-01", "adj_close": 75.23},
                    {"ticker": "GLD", "date": "2024-01-01", "adj_close": 201.45},
                ],
                "summary_statistics": {
                    "mean_returns": {"AAPL": 0.082, "BND": 0.025, "GLD": 0.045},
                    "volatilities": {"AAPL": 0.24, "BND": 0.04, "GLD": 0.18}
                }
            }
        }
        
        if sample_id not in sample_previews:
            raise HTTPException(status_code=404, detail="Sample dataset not found")
        
        return sample_previews[sample_id]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error previewing sample dataset {sample_id}: {e}")
        raise HTTPException(status_code=500, detail="Error previewing sample dataset")


@router.get("/{dataset_id}", response_model=DatasetSchema)
async def get_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific dataset"""
    try:
        dataset = (db.query(Dataset)
                  .filter(Dataset.id == dataset_id)
                  .filter(Dataset.owner_id == current_user.id)
                  .first())
        
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        return dataset
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting dataset {dataset_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving dataset")


@router.get("/{dataset_id}/preview", response_model=DatasetPreview)
async def preview_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dataset preview with summary statistics"""
    try:
        dataset = (db.query(Dataset)
                  .filter(Dataset.id == dataset_id)
                  .filter(Dataset.owner_id == current_user.id)
                  .first())
        
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        # Load dataset
        df = load_dataset(dataset.file_path)
        
        # Calculate returns and statistics
        returns_df = calculate_returns(df)
        mean_returns = calculate_mean_returns(returns_df)
        cov_matrix = calculate_covariance_matrix(returns_df)
        
        # Preview data (first 50 rows)
        preview_data = df.head(50).to_dict('records')
        
        # Summary statistics
        summary_stats = {
            'mean_returns': dict(zip(returns_df.columns, mean_returns.tolist())),
            'volatilities': dict(zip(returns_df.columns, np.sqrt(np.diag(cov_matrix)).tolist())),
            'correlation_matrix': returns_df.corr().to_dict()
        }
        
        return DatasetPreview(
            dataset=dataset,
            preview_data=preview_data,
            summary_statistics=summary_stats,
            correlation_matrix=returns_df.corr().to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error previewing dataset {dataset_id}: {e}")
        raise HTTPException(status_code=500, detail="Error previewing dataset")


@router.delete("/{dataset_id}")
async def delete_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a dataset"""
    try:
        dataset = (db.query(Dataset)
                  .filter(Dataset.id == dataset_id)
                  .filter(Dataset.owner_id == current_user.id)
                  .first())
        
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        # Delete file
        try:
            os.remove(dataset.file_path)
        except OSError:
            logger.warning(f"Could not delete file: {dataset.file_path}")
        
        # Delete database record
        db.delete(dataset)
        db.commit()
        
        logger.info(f"Dataset deleted: {dataset_id} by user {current_user.id}")
        
        return {"message": "Dataset deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting dataset {dataset_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting dataset")