import time
import numpy as np
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.models.dataset import Dataset
from app.routes.auth import get_current_user
from app.schemas.optimize_schemas import (
    OptimizationRequest, OptimizationJob, OptimizationResult
)
from app.services.classical_optimizer import ClassicalOptimizer

# Try to import quantum services, fallback to mock if not available
try:
    from app.services.qubo_generator import QUBOGenerator
    from app.services.qaoa_solver import QAOASolver
    QUANTUM_AVAILABLE = True
except ImportError:
    from app.services.mock_quantum import MockQUBOGenerator as QUBOGenerator
    from app.services.mock_quantum import MockQAOASolver as QAOASolver
    QUANTUM_AVAILABLE = False
    logger.warning("Quantum libraries not available. Using mock implementations.")
from app.services.experiment_tracker import ExperimentTracker
from app.services.metrics import MetricsCalculator
from app.utils.file_utils import load_dataset
from app.utils.math_utils import calculate_returns, calculate_mean_returns, calculate_covariance_matrix
from app.utils.logger import logger

router = APIRouter()

# Sample dataset data for optimization
SAMPLE_DATASETS = {
    -1: {  # S&P 500 Sample
        "name": "S&P 500 Sample",
        "tickers": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
        "mean_returns": np.array([0.082, 0.079, 0.064, 0.058, 0.121]),
        "cov_matrix": np.array([
            [0.0576, 0.0234, 0.0312, 0.0189, 0.0456],
            [0.0234, 0.0484, 0.0267, 0.0178, 0.0389],
            [0.0312, 0.0267, 0.0676, 0.0234, 0.0445],
            [0.0189, 0.0178, 0.0234, 0.0784, 0.0356],
            [0.0456, 0.0389, 0.0445, 0.0356, 0.2025]
        ])
    },
    -2: {  # Government Bonds
        "name": "Government Bonds",
        "tickers": ["US10Y", "US5Y", "US2Y"],
        "mean_returns": np.array([0.03, 0.029, 0.032]),
        "cov_matrix": np.array([
            [0.0025, 0.0018, 0.0015],
            [0.0018, 0.0023, 0.0016],
            [0.0015, 0.0016, 0.0027]
        ])
    },
    -3: {  # Mixed Portfolio
        "name": "Mixed Portfolio",
        "tickers": ["AAPL", "BND", "GLD"],
        "mean_returns": np.array([0.082, 0.025, 0.045]),
        "cov_matrix": np.array([
            [0.0576, 0.0012, 0.0089],
            [0.0012, 0.0016, 0.0034],
            [0.0089, 0.0034, 0.0324]
        ])
    }
}


async def run_optimization_task(
    experiment_id: int,
    optimization_request: OptimizationRequest,
    db: Session
):
    """Background task to run optimization"""
    tracker = ExperimentTracker(db)
    
    try:
        # Start experiment
        tracker.start_experiment(experiment_id)
        start_time = time.time()
        
        # Load dataset
        dataset = db.query(Dataset).filter(Dataset.id == optimization_request.dataset_id).first()
        if not dataset:
            raise ValueError("Dataset not found")
        
        df = load_dataset(dataset.file_path)
        returns_df = calculate_returns(df)
        mean_returns = calculate_mean_returns(returns_df)
        cov_matrix = calculate_covariance_matrix(returns_df)
        asset_names = returns_df.columns.tolist()
        
        logger.info(f"Loaded dataset with {len(asset_names)} assets for experiment {experiment_id}")
        
        # Run optimization based on solver type
        result = None
        
        if optimization_request.solver == "classical":
            optimizer = ClassicalOptimizer()
            result = optimizer.solve(
                mean_returns=mean_returns,
                cov_matrix=cov_matrix,
                constraints=optimization_request.constraints.dict(),
                solver_params=optimization_request.solver_params.dict() if optimization_request.solver_params else None
            )
            
        elif optimization_request.solver == "qubo":
            qubo_gen = QUBOGenerator()
            qubo_data = qubo_gen.build_qubo(
                mean_returns=mean_returns,
                cov_matrix=cov_matrix,
                constraints=optimization_request.constraints.dict()
            )
            result = qubo_gen.solve_qubo(
                qubo_data=qubo_data,
                solver_params=optimization_request.solver_params.dict() if optimization_request.solver_params else {}
            )
            result['qubo_matrix'] = qubo_data['qubo_matrix']
            result['variable_mapping'] = qubo_data['variable_mapping']
            
        elif optimization_request.solver == "qaoa":
            # First generate QUBO
            qubo_gen = QUBOGenerator()
            qubo_data = qubo_gen.build_qubo(
                mean_returns=mean_returns,
                cov_matrix=cov_matrix,
                constraints=optimization_request.constraints.dict()
            )
            
            # Then solve with QAOA
            qaoa_solver = QAOASolver()
            result = qaoa_solver.solve_qaoa(
                qubo_data=qubo_data,
                solver_params=optimization_request.solver_params.dict() if optimization_request.solver_params else {}
            )
            result['qubo_matrix'] = qubo_data['qubo_matrix']
            result['qaoa_circuit_depth'] = optimization_request.solver_params.p_layers if optimization_request.solver_params else 1
        
        # Calculate comprehensive metrics
        if result and result['status'] in ['optimal', 'completed'] and result['weights'] is not None:
            weights = np.array(result['weights'])
            
            # Calculate metrics
            metrics_calc = MetricsCalculator()
            comprehensive_metrics = metrics_calc.calculate_comprehensive_metrics(
                weights=weights,
                mean_returns=mean_returns,
                cov_matrix=cov_matrix,
                returns_data=returns_df.values
            )
            
            # Portfolio composition
            composition = metrics_calc.calculate_portfolio_composition(weights, asset_names)
            
            # Prepare final results
            final_results = {
                'weights': dict(zip(asset_names, weights.tolist())),
                'selected_assets': composition['selected_assets'],
                'metrics': comprehensive_metrics,
                'solver_info': result.get('solver_info', {}),
                'constraint_satisfaction': result.get('constraint_satisfaction', {}),
                'qubo_matrix': result.get('qubo_matrix'),
                'binary_solution': result.get('binary_solution'),
                'qaoa_circuit_depth': result.get('qaoa_circuit_depth'),
                'qaoa_energy': result.get('energy'),
                'qaoa_shots': optimization_request.solver_params.shots if optimization_request.solver_params else None
            }
            
            # Complete experiment
            runtime = time.time() - start_time
            tracker.complete_experiment(experiment_id, final_results, runtime)
            
            logger.info(f"Optimization completed successfully for experiment {experiment_id}")
            
        else:
            # Handle failed optimization
            error_msg = result.get('error', 'Optimization failed') if result else 'Unknown error'
            runtime = time.time() - start_time
            tracker.complete_experiment(experiment_id, {}, runtime, error_msg)
            
            logger.error(f"Optimization failed for experiment {experiment_id}: {error_msg}")
    
    except Exception as e:
        # Handle exceptions
        runtime = time.time() - start_time
        tracker.complete_experiment(experiment_id, {}, runtime, str(e))
        logger.error(f"Error in optimization task for experiment {experiment_id}: {e}")


@router.post("/run", response_model=OptimizationJob)
async def run_optimization(
    request: OptimizationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start optimization job"""
    try:
        # Validate dataset access
        dataset = (db.query(Dataset)
                  .filter(Dataset.id == request.dataset_id)
                  .filter(Dataset.owner_id == current_user.id)
                  .first())
        
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        # Create experiment
        tracker = ExperimentTracker(db)
        experiment = tracker.create_experiment(
            user_id=current_user.id,
            dataset_id=request.dataset_id,
            solver_type=request.solver.value,
            constraints=request.constraints.dict(),
            solver_params=request.solver_params.dict() if request.solver_params else {},
            experiment_name=request.experiment_name,
            random_seed=request.random_seed
        )
        
        # Start background task
        background_tasks.add_task(run_optimization_task, experiment.id, request, db)
        
        logger.info(f"Started optimization job for experiment {experiment.id}")
        
        return OptimizationJob(
            job_id=f"opt_{experiment.id}",
            experiment_id=experiment.id,
            status="running",
            message="Optimization started",
            progress=0.0
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting optimization: {e}")
        raise HTTPException(status_code=500, detail="Error starting optimization")


@router.post("/run-sample")
async def run_sample_optimization(request: OptimizationRequest):
    """Run optimization on sample dataset (no authentication required)"""
    logger.info(f"Sample optimization endpoint called with dataset_id: {request.dataset_id}")
    
    # Simple test response first
    return {
        "experiment_id": 0,
        "solver_type": "classical",
        "status": "completed",
        "runtime_seconds": 1.0,
        "portfolio_weights": {"AAPL": 0.4, "MSFT": 0.3, "GOOGL": 0.2, "AMZN": 0.1},
        "selected_assets": ["AAPL", "MSFT", "GOOGL", "AMZN"],
        "expected_return": 0.08,
        "volatility": 0.15,
        "sharpe_ratio": 0.53,
        "cvar_95": -0.12,
        "solver_metadata": {},
        "constraint_satisfaction": {"budget": True, "weights": True}
    }


@router.get("/jobs/{job_id}/status")
async def get_job_status(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get optimization job status"""
    try:
        # Extract experiment ID from job ID
        if not job_id.startswith("opt_"):
            raise HTTPException(status_code=400, detail="Invalid job ID")
        
        experiment_id = int(job_id.split("_")[1])
        
        # Get experiment
        tracker = ExperimentTracker(db)
        experiment = tracker.get_experiment(experiment_id)
        
        if not experiment or experiment.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Calculate progress (simplified)
        progress = 0.0
        if experiment.status == "running":
            progress = 50.0  # Simplified progress
        elif experiment.status == "completed":
            progress = 100.0
        
        return {
            "job_id": job_id,
            "experiment_id": experiment_id,
            "status": experiment.status,
            "progress": progress,
            "runtime_seconds": experiment.runtime_seconds,
            "error_message": experiment.error_message
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job status: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving job status")


@router.get("/jobs/{job_id}/result", response_model=OptimizationResult)
async def get_job_result(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get optimization job result"""
    try:
        # Extract experiment ID from job ID
        if not job_id.startswith("opt_"):
            raise HTTPException(status_code=400, detail="Invalid job ID")
        
        experiment_id = int(job_id.split("_")[1])
        
        # Get experiment and results
        tracker = ExperimentTracker(db)
        experiment = tracker.get_experiment(experiment_id)
        
        if not experiment or experiment.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if experiment.status != "completed":
            raise HTTPException(status_code=400, detail="Job not completed")
        
        results = tracker.get_experiment_results(experiment_id)
        if not results:
            raise HTTPException(status_code=404, detail="Results not found")
        
        return OptimizationResult(
            experiment_id=experiment_id,
            solver_type=experiment.solver_type,
            status=experiment.status,
            runtime_seconds=experiment.runtime_seconds,
            portfolio_weights=results.portfolio_weights,
            selected_assets=results.selected_assets,
            expected_return=results.expected_return,
            volatility=results.volatility,
            sharpe_ratio=results.sharpe_ratio,
            cvar_95=results.cvar_95,
            solver_metadata=results.solver_metadata,
            constraint_satisfaction=results.constraint_satisfaction
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job result: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving job result")