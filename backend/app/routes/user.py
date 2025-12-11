from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.routes.auth import get_current_user
from app.schemas.auth_schemas import User as UserSchema, UserUpdate
from app.utils.logger import logger

router = APIRouter()


@router.get("/me", response_model=UserSchema)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    try:
        # Update fields if provided
        if user_update.name is not None:
            current_user.name = user_update.name
        
        if user_update.email is not None:
            # Check if email is already taken
            existing_user = db.query(User).filter(
                User.email == user_update.email,
                User.id != current_user.id
            ).first()
            
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            
            current_user.email = user_update.email
        
        db.commit()
        db.refresh(current_user)
        
        logger.info(f"User profile updated: {current_user.id}")
        return current_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating profile")


@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user statistics"""
    try:
        from app.models.dataset import Dataset
        from app.models.experiment import Experiment
        from app.models.results import Result
        
        # Count datasets
        dataset_count = db.query(Dataset).filter(Dataset.owner_id == current_user.id).count()
        
        # Count experiments
        experiment_count = db.query(Experiment).filter(Experiment.user_id == current_user.id).count()
        
        # Count completed experiments
        completed_experiments = (db.query(Experiment)
                               .filter(Experiment.user_id == current_user.id)
                               .filter(Experiment.status == "completed")
                               .count())
        
        # Get solver usage stats
        solver_stats = (db.query(Experiment.solver_type, db.func.count(Experiment.id))
                       .filter(Experiment.user_id == current_user.id)
                       .group_by(Experiment.solver_type)
                       .all())
        
        solver_usage = {solver: count for solver, count in solver_stats}
        
        # Get recent activity (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        recent_experiments = (db.query(Experiment)
                            .filter(Experiment.user_id == current_user.id)
                            .filter(Experiment.created_at >= thirty_days_ago)
                            .count())
        
        return {
            'user_id': current_user.id,
            'datasets_uploaded': dataset_count,
            'total_experiments': experiment_count,
            'completed_experiments': completed_experiments,
            'recent_experiments_30d': recent_experiments,
            'solver_usage': solver_usage,
            'success_rate': completed_experiments / experiment_count if experiment_count > 0 else 0,
            'member_since': current_user.created_at
        }
        
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics")