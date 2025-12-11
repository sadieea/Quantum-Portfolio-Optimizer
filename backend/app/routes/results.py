import io
import csv
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.experiment import Experiment
from app.models.results import Result
from app.routes.auth import get_current_user
from app.schemas.result_schemas import (
    ResultDetail, ResultSummary, ExperimentSummary, ResultComparison
)
from app.services.experiment_tracker import ExperimentTracker
from app.utils.logger import logger

router = APIRouter()


@router.get("/{experiment_id}", response_model=ResultDetail)
async def get_result(
    experiment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed results for an experiment"""
    try:
        # Get experiment
        experiment = (db.query(Experiment)
                     .filter(Experiment.id == experiment_id)
                     .filter(Experiment.user_id == current_user.id)
                     .first())
        
        if not experiment:
            raise HTTPException(status_code=404, detail="Experiment not found")
        
        # Get results
        result = db.query(Result).filter(Result.experiment_id == experiment_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Results not found")
        
        # Format response
        portfolio_composition = {
            'weights': result.portfolio_weights,
            'selected_assets': result.selected_assets,
            'num_assets': len(result.selected_assets),
            'concentration': {}  # Could add concentration metrics
        }
        
        performance_metrics = {
            'expected_return': result.expected_return,
            'volatility': result.volatility,
            'variance': result.variance,
            'sharpe_ratio': result.sharpe_ratio,
            'cvar_95': result.cvar_95,
            'max_drawdown': result.max_drawdown
        }
        
        solver_metadata = {
            'solver_type': experiment.solver_type,
            'runtime_seconds': experiment.runtime_seconds,
            'parameters': experiment.solver_params,
            'convergence_info': result.solver_metadata
        }
        
        # Solver-specific metadata
        qubo_metadata = None
        qaoa_metadata = None
        
        if experiment.solver_type == 'qubo' and result.qubo_matrix:
            qubo_metadata = {
                'num_variables': len(result.qubo_matrix),
                'num_constraints': 0,  # Could calculate from constraints
                'penalty_coefficients': {},
                'best_energy': 0.0,  # Could extract from solver_metadata
                'num_reads': result.solver_metadata.get('num_reads', 0) if result.solver_metadata else 0
            }
        
        if experiment.solver_type == 'qaoa':
            qaoa_metadata = {
                'circuit_depth': result.qaoa_circuit_depth or 1,
                'num_parameters': (result.qaoa_circuit_depth or 1) * 2,
                'final_energy': result.qaoa_energy or 0.0,
                'shots': result.qaoa_shots or 1024,
                'convergence_history': []
            }
        
        return ResultDetail(
            id=result.id,
            experiment_id=experiment_id,
            portfolio={
                'weights': portfolio_composition['weights'],
                'selected_assets': portfolio_composition['selected_assets'],
                'num_assets': portfolio_composition['num_assets'],
                'concentration': portfolio_composition['concentration']
            },
            metrics=performance_metrics,
            solver_metadata=solver_metadata,
            qubo_metadata=qubo_metadata,
            qaoa_metadata=qaoa_metadata,
            constraint_satisfaction=result.constraint_satisfaction or {},
            created_at=result.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting result {experiment_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving result")


@router.get("/", response_model=List[ResultSummary])
async def list_results(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List recent results for the user"""
    try:
        results = (db.query(Result, Experiment)
                  .join(Experiment, Result.experiment_id == Experiment.id)
                  .filter(Experiment.user_id == current_user.id)
                  .filter(Experiment.status == "completed")
                  .order_by(Result.created_at.desc())
                  .limit(limit)
                  .all())
        
        summaries = []
        for result, experiment in results:
            summaries.append(ResultSummary(
                id=result.id,
                experiment_id=experiment.id,
                solver_type=experiment.solver_type,
                expected_return=result.expected_return,
                volatility=result.volatility,
                sharpe_ratio=result.sharpe_ratio,
                runtime_seconds=experiment.runtime_seconds,
                num_assets=len(result.selected_assets),
                created_at=result.created_at
            ))
        
        return summaries
        
    except Exception as e:
        logger.error(f"Error listing results: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving results")


@router.get("/{experiment_id}/download/csv")
async def download_csv(
    experiment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download results as CSV"""
    try:
        # Get experiment and results
        experiment = (db.query(Experiment)
                     .filter(Experiment.id == experiment_id)
                     .filter(Experiment.user_id == current_user.id)
                     .first())
        
        if not experiment:
            raise HTTPException(status_code=404, detail="Experiment not found")
        
        result = db.query(Result).filter(Result.experiment_id == experiment_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Results not found")
        
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow([
            'Asset', 'Weight', 'Expected_Return', 'Risk_Contribution'
        ])
        
        # Write data
        for asset in result.selected_assets:
            weight = result.portfolio_weights.get(asset, 0.0)
            writer.writerow([
                asset,
                f"{weight:.6f}",
                "",  # Would need to calculate individual returns
                ""   # Would need to calculate risk contribution
            ])
        
        # Add summary row
        writer.writerow([])
        writer.writerow(['Summary', '', '', ''])
        writer.writerow(['Expected Return', f"{result.expected_return:.6f}", '', ''])
        writer.writerow(['Volatility', f"{result.volatility:.6f}", '', ''])
        writer.writerow(['Sharpe Ratio', f"{result.sharpe_ratio:.6f}", '', ''])
        if result.cvar_95:
            writer.writerow(['CVaR (95%)', f"{result.cvar_95:.6f}", '', ''])
        
        output.seek(0)
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode()),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=portfolio_results_{experiment_id}.csv"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading CSV for experiment {experiment_id}: {e}")
        raise HTTPException(status_code=500, detail="Error generating CSV")


@router.get("/experiments/", response_model=List[ExperimentSummary])
async def list_experiments(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List experiments for the user"""
    try:
        from app.models.dataset import Dataset
        
        experiments = (db.query(Experiment, Dataset, Result)
                      .join(Dataset, Experiment.dataset_id == Dataset.id)
                      .outerjoin(Result, Experiment.id == Result.experiment_id)
                      .filter(Experiment.user_id == current_user.id)
                      .order_by(Experiment.created_at.desc())
                      .limit(limit)
                      .all())
        
        summaries = []
        for experiment, dataset, result in experiments:
            summaries.append(ExperimentSummary(
                id=experiment.id,
                name=experiment.name,
                solver_type=experiment.solver_type,
                dataset_name=dataset.name,
                status=experiment.status,
                runtime_seconds=experiment.runtime_seconds,
                expected_return=result.expected_return if result else None,
                volatility=result.volatility if result else None,
                sharpe_ratio=result.sharpe_ratio if result else None,
                num_assets=len(result.selected_assets) if result and result.selected_assets else None,
                created_at=experiment.created_at
            ))
        
        return summaries
        
    except Exception as e:
        logger.error(f"Error listing experiments: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving experiments")


@router.get("/experiments/{experiment_id}")
async def get_experiment_detail(
    experiment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed experiment information"""
    try:
        from app.models.dataset import Dataset
        
        experiment_data = (db.query(Experiment, Dataset)
                          .join(Dataset, Experiment.dataset_id == Dataset.id)
                          .filter(Experiment.id == experiment_id)
                          .filter(Experiment.user_id == current_user.id)
                          .first())
        
        if not experiment_data:
            raise HTTPException(status_code=404, detail="Experiment not found")
        
        experiment, dataset = experiment_data
        
        return {
            'id': experiment.id,
            'name': experiment.name,
            'solver_type': experiment.solver_type,
            'solver_params': experiment.solver_params,
            'constraints': experiment.constraints,
            'dataset': {
                'id': dataset.id,
                'name': dataset.name,
                'num_assets': dataset.num_assets
            },
            'status': experiment.status,
            'runtime_seconds': experiment.runtime_seconds,
            'error_message': experiment.error_message,
            'created_at': experiment.created_at,
            'started_at': experiment.started_at,
            'completed_at': experiment.completed_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting experiment detail {experiment_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving experiment")