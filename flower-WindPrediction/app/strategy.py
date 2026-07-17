"""windturbine-fl: Custom strategy for wind turbine federated learning."""

import json
from logging import INFO

from app.task import create_run_dir, load_model
from setup_wandb import init_wandb_safe, log_wandb_safe

from flwr.common import logger, parameters_to_ndarrays
from flwr.common.typing import UserConfig
from flwr.server.strategy import FedAvg

PROJECT_NAME = "FLOWER-WindTurbine-PredictiveMaintenance"


class WindTurbineStrategy(FedAvg):
    """Custom FedAvg strategy with advanced features for wind turbine FL.
    
    This strategy: 
    (1) saves results to the filesystem
    (2) saves checkpoints of the global model when a new best is found
    (3) logs results to W&B if enabled
    (4) tracks turbine-specific metrics
    """

    def __init__(self, run_config: UserConfig, use_wandb: bool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Store num_rounds from run_config
        self.num_rounds = run_config.get("num-server-rounds", 50)
        
        # Create a directory where to save results from this run
        self.save_path, self.run_dir = create_run_dir(run_config)
        self.use_wandb = use_wandb
        
        # Initialise W&B if set
        self.wandb_run = None
        if use_wandb:
            self.wandb_run = self._init_wandb_project()
        
        # Keep track of best accuracy
        self.best_acc_so_far = 0.0
        self.best_f1_so_far = 0.0
        
        # A dictionary to store results as they come
        self.results = {}
        
        # Track turbine participation
        self.turbine_rounds = {}

    def _init_wandb_project(self):
        """Initialize W&B project for tracking."""
        return init_wandb_safe(
            project=PROJECT_NAME, 
            name=f"{str(self.run_dir)}-ServerApp",
            config={
                "architecture": "CNN+LSTM",
                "dataset": "Wind Turbine SCADA",
                "num_turbines": 3,
                "central_test_turbine": "T11"
            }
        )

    def _store_results(self, tag: str, results_dict):
        """Store results in dictionary, then save as JSON."""
        # Update results dict
        if tag in self.results:
            self.results[tag].append(results_dict)
        else:
            self.results[tag] = [results_dict]
        
        # Save results to disk
        with open(f"{self.save_path}/results.json", "w", encoding="utf-8") as fp:
            json.dump(self.results, fp, indent=2)

    def _update_best_model(self, round, accuracy, f1_score, parameters):
        """Save model checkpoint if new best performance is found."""
        
        save_checkpoint = False
        
        # Check if accuracy improved
        if accuracy > self.best_acc_so_far:
            self.best_acc_so_far = accuracy
            save_checkpoint = True
            logger.log(INFO, "💡 New best accuracy found: %.4f", accuracy)
        
        # Check if F1 score improved
        if f1_score > self.best_f1_so_far:
            self.best_f1_so_far = f1_score
            save_checkpoint = True
            logger.log(INFO, "💡 New best F1 score found: %.4f", f1_score)
        
        if save_checkpoint:
            # Convert parameters to model weights
            ndarrays = parameters_to_ndarrays(parameters)
            model = load_model()
            model.set_weights(ndarrays)
            
            # Save the model weights
            file_name = (
                self.save_path
                / f"model_round_{round}_acc_{accuracy:.3f}_f1_{f1_score:.3f}.weights.h5"
            )
            model.save_weights(file_name)
            
            # Also save as 'best_model.weights.h5' for easy access
            best_model_path = self.save_path / "best_model.weights.h5"
            model.save_weights(best_model_path)

    def store_results_and_log(self, server_round: int, tag: str, results_dict):
        """Store results and log them to W&B if enabled."""
        # Store results
        self._store_results(
            tag=tag,
            results_dict={"round": server_round, **results_dict},
        )
        
        if self.use_wandb and self.wandb_run is not None:
            # Log to W&B with custom metrics
            wandb_dict = {f"{tag}/{k}": v for k, v in results_dict.items() 
                         if not isinstance(v, dict)}
            log_wandb_safe(wandb_dict, step=server_round)

    def aggregate_fit(self, server_round, results, failures):
        """Aggregate fit results and track turbine participation."""
        
        # Track which turbines participated
        participating_turbines = []
        for client_proxy, fit_res in results:
            if "turbine_id" in fit_res.metrics:
                turbine_id = fit_res.metrics["turbine_id"]
                participating_turbines.append(turbine_id)
                
                # Track rounds per turbine
                if turbine_id not in self.turbine_rounds:
                    self.turbine_rounds[turbine_id] = []
                self.turbine_rounds[turbine_id].append(server_round)
        
        # Log participation
        logger.log(INFO, f"Round {server_round} - Participating turbines: {participating_turbines}")
        
        # Call parent aggregation
        parameters, metrics = super().aggregate_fit(server_round, results, failures)
        
        # Store turbine-specific training metrics
        if results:
            training_metrics = {
                "num_turbines_fit": len(results),
                "participating_turbines": participating_turbines,
                "num_failures": len(failures),
            }
            
            # Add average metrics
            avg_loss = sum(fit_res.metrics.get("loss", 0) for _, fit_res in results) / len(results)
            avg_acc = sum(fit_res.metrics.get("accuracy", 0) for _, fit_res in results) / len(results)
            
            training_metrics["avg_train_loss"] = avg_loss
            training_metrics["avg_train_accuracy"] = avg_acc
            
            self.store_results_and_log(
                server_round=server_round,
                tag="federated_fit",
                results_dict=training_metrics,
            )
        
        return parameters, metrics

    def evaluate(self, server_round, parameters):
        """Run centralized evaluation on T11 dataset."""
        loss, metrics = super().evaluate(server_round, parameters)
        
        # Save model if new best central accuracy or F1 is found
        if metrics:
            self._update_best_model(
                server_round,
                metrics.get("centralized_accuracy", 0),
                metrics.get("centralized_f1_score", 0),
                parameters
            )
        
        # Store and log
        self.store_results_and_log(
            server_round=server_round,
            tag="centralized_evaluate",
            results_dict={"centralized_loss": loss, **metrics},
        )
        
        return loss, metrics

    def aggregate_evaluate(self, server_round, results, failures):
        """Aggregate results from federated evaluation."""
        loss, metrics = super().aggregate_evaluate(server_round, results, failures)
        
        # Extract turbine-specific metrics
        turbine_details = {}
        for client_proxy, eval_res in results:
            if "turbine_id" in eval_res.metrics:
                turbine_id = eval_res.metrics["turbine_id"]
                turbine_details[turbine_id] = {
                    "loss": eval_res.loss,
                    "accuracy": eval_res.metrics.get("accuracy", 0),
                    "samples": eval_res.num_examples,
                }
        
        # Add turbine details to metrics
        if metrics is None:
            metrics = {}
        metrics["turbine_details"] = turbine_details
        
        # Store and log
        self.store_results_and_log(
            server_round=server_round,
            tag="federated_evaluate",
            results_dict={
                "federated_evaluate_loss": loss,
                "num_turbines_evaluated": len(results),
                **{k: v for k, v in metrics.items() if k != "turbine_details"}
            },
        )
        
        # Log final summary at the end
        if server_round == self.num_rounds:
            self._log_final_summary()
        
        return loss, metrics

    def _log_final_summary(self):
        """Log final summary of the federated learning experiment."""
        summary = {
            "total_rounds": self.num_rounds,
            "best_centralized_accuracy": self.best_acc_so_far,
            "best_centralized_f1": self.best_f1_so_far,
            "turbine_participation": self.turbine_rounds,
            "save_path": str(self.save_path),
        }
        
        # Save summary
        with open(f"{self.save_path}/summary.json", "w", encoding="utf-8") as fp:
            json.dump(summary, fp, indent=2)
        
        logger.log(INFO, "===== Federated Learning Complete =====")
        logger.log(INFO, f"Best Accuracy: {self.best_acc_so_far:.4f}")
        logger.log(INFO, f"Best F1 Score: {self.best_f1_so_far:.4f}")
        logger.log(INFO, f"Results saved to: {self.save_path}")
        
        if self.use_wandb and self.wandb_run is not None:
            # Update wandb summary with final results
            try:
                import wandb
                wandb.summary.update(summary)
            except Exception as e:
                print(f"Failed to update wandb summary: {e}")