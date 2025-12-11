import hashlib
import json
import time
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.experiment import Experiment
from app.models.results import Result
from app.utils.logger import logger


class ExperimentTracker:
    """Track and manage optimization experiments"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_experiment(self,
                         user_id: int,
                         dataset_id: int,
                         solver_type: str,
                         constraints: Dict[str, Any],
                         solver_params: Dict[str, Any],
                         experiment_name: Optional[str] = None,
                         random_seed: Optional[int] = None) -> Experiment:
        """Create a new experiment record"""
        try:
            # Generate results hash for reproducibility
            hash_data = {
                'dataset_id': dataset_id,
                'solver_type': solver_type,
                'constraints': constraints,
                'solver_params': solver_params,
                'random_seed': random_seed
            }
            results_hash = hashlib.md5(json.dumps(hash_data, sort_keys=True).encode()).hexdigest()
            
            experiment = Experiment(
                name=experiment_name,
                user_id=user_id,
                dataset_id=dataset_id,
                solver_type=solver_type,
                constraints=constraints,
                solver_params=solver_params,
                random_seed=random_seed,
                results_hash=results_hash,
                status="pending"
            )
            
            self.db.add(experiment)
            self.db.commit()
            self.db.refresh(experiment)
            
            logger.info(f"Created experiment {experiment.id} for user {user_id}")
            return experiment
            
        except Exception as e:
            logger.error(f"Error creating experiment: {e}")
            self.db.rollback()
            raise
    
    def start_experiment(self, experiment_id: int) -> None:
        """Mark experiment as started"""
        try:
            experiment = self.db.query(Experiment).filter(Experiment.id == experiment_id).first()
            if experiment:
                experiment.status = "running"
                experiment.started_at = time.time()
                self.db.commit()
                logger.info(f"Started experiment {experiment_id}")
        except Exception as e:
            logger.error(f"Error starting experiment {experiment_id}: {e}")
            self.db.rollback()
    
    def complete_experiment(self,
                          experiment_id: int,
                          results: Dict[str, Any],
                          runtime_seconds: float,
                          error_message: Optional[str] = None) -> None:
        """Mark experiment as completed and save results"""
        try:
            experiment = self.db.query(Experiment).filter(Experiment.id == experiment_id).first()
            if not experiment:
                raise ValueError(f"Experiment {experiment_id} not found")
            
            # Update experiment
            experiment.status = "completed" if not error_message else "failed"
            experiment.completed_at = time.time()
            experiment.runtime_seconds = runtime_seconds
            experiment.error_message = error_message
            
            # Save results if successful
            if not error_message and results:
                result = Result(
                    experiment_id=experiment_id,
                    portfolio_weights=results.get('weights', {}),
                    selected_assets=results.get('selected_assets', []),
                    expected_return=results.get('metrics', {}).get('expected_return'),
                    volatility=results.get('metrics', {}).get('volatility'),
                    variance=results.get('metrics', {}).get('variance'),
                    sharpe_ratio=results.get('metrics', {}).get('sharpe_ratio'),
                    cvar_95=results.get('metrics', {}).get('cvar_95'),
                    max_drawdown=results.get('metrics', {}).get('max_drawdown'),
                    solver_metadata=results.get('solver_info', {}),
                    qubo_matrix=results.get('qubo_matrix'),
                    binary_solution=results.get('binary_solution'),
                    qaoa_circuit_depth=results.get('qaoa_circuit_depth'),
                    qaoa_energy=results.get('qaoa_energy'),
                    qaoa_shots=results.get('qaoa_shots'),
                    constraint_satisfaction=results.get('constraint_satisfaction', {})
                )
                
                self.db.add(result)
            
            self.db.commit()
            logger.info(f"Completed experiment {experiment_id} with status {experiment.status}")
            
        except Exception as e:
            logger.error(f"Error completing experiment {experiment_id}: {e}")
            self.db.rollback()
            raise
    
    def get_experiment(self, experiment_id: int) -> Optional[Experiment]:
        """Get experiment by ID"""
        return self.db.query(Experiment).filter(Experiment.id == experiment_id).first()
    
    def get_user_experiments(self, user_id: int, limit: int = 50) -> list:
        """Get experiments for a user"""
        return (self.db.query(Experiment)
                .filter(Experiment.user_id == user_id)
                .order_by(Experiment.created_at.desc())
                .limit(limit)
                .all())
    
    def get_experiment_results(self, experiment_id: int) -> Optional[Result]:
        """Get results for an experiment"""
        return self.db.query(Result).filter(Result.experiment_id == experiment_id).first()
    
    def check_reproducibility(self, results_hash: str) -> Optional[Experiment]:
        """Check if experiment with same parameters exists"""
        return (self.db.query(Experiment)
                .filter(Experiment.results_hash == results_hash)
                .filter(Experiment.status == "completed")
                .first())