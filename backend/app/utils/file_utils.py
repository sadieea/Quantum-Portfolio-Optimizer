import os
import csv
import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.config import settings
from app.utils.logger import logger


def ensure_upload_dir():
    """Ensure upload directory exists"""
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)
    return upload_path


def validate_csv_file(file: UploadFile) -> bool:
    """Validate uploaded CSV file"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    return True


def save_uploaded_file(file: UploadFile, filename: str) -> Path:
    """Save uploaded file to disk"""
    upload_dir = ensure_upload_dir()
    file_path = upload_dir / filename
    
    try:
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)
        
        logger.info(f"File saved: {file_path}")
        return file_path
    
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Error saving file")


def validate_dataset_format(file_path: Path) -> Dict[str, Any]:
    """Validate dataset format and return metadata"""
    try:
        df = pd.read_csv(file_path)
        
        # Required columns
        required_cols = ['ticker', 'date', 'adj_close']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {missing_cols}"
            )
        
        # Validate data types
        df['date'] = pd.to_datetime(df['date'])
        df['adj_close'] = pd.to_numeric(df['adj_close'])
        
        # Calculate metadata
        metadata = {
            'num_rows': len(df),
            'num_assets': df['ticker'].nunique(),
            'date_range': {
                'start': df['date'].min().isoformat(),
                'end': df['date'].max().isoformat()
            },
            'columns': list(df.columns),
            'sample_data': df.head(10).to_dict('records')
        }
        
        return metadata
        
    except Exception as e:
        logger.error(f"Error validating dataset: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid dataset format: {str(e)}")


def load_dataset(file_path: Path) -> pd.DataFrame:
    """Load and preprocess dataset"""
    try:
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(['ticker', 'date'])
        return df
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        raise HTTPException(status_code=500, detail="Error loading dataset")