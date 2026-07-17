"""windturbine-fl: A Flower / TensorFlow client for wind turbine predictive maintenance."""

import keras
import numpy as np
from app.task import load_data, load_model
from setup_wandb import init_wandb_safe, log_wandb_safe, finish_wandb_safe

from flwr.client import ClientApp, NumPyClient
from flwr.common import Array, ArrayRecord, Context, RecordDict


# Define Flower Client and client_fn
class TurbineClient(NumPyClient):
    """Wind turbine client with personalized classification head.
    
    Each turbine maintains its own classification layer locally while
    participating in federated learning for the feature extraction layers.
    """

    def __init__(self, client_state: RecordDict, data, batch_size, local_epochs, turbine_id, use_wandb=False):
        self.client_state = client_state
        self.x_train, self.y_train, self.x_test, self.y_test = data
        self.batch_size = batch_size
        self.local_epochs = local_epochs
        self.local_layer_name = "classification-head"
        self.turbine_id = turbine_id
        self.use_wandb = use_wandb
        self.wandb_run = None
        
        # Calculate class weights and unique classes (avoid duplication)
        self.unique_classes = np.unique(self.y_train)
        self.class_weights = self._calculate_class_weights()
        
        # Initialize wandb for this client if enabled
        if self.use_wandb:
            self.wandb_run = init_wandb_safe(
                project="windturbine-fl-clients",
                name=f"client_{turbine_id}",
                tags=[f"turbine_{turbine_id}", "federated_learning", "client"],
                config={
                    "turbine_id": turbine_id,
                    "batch_size": batch_size,
                    "local_epochs": local_epochs,
                    "training_samples": len(self.x_train),
                    "test_samples": len(self.x_test),
                    "unique_classes": len(self.unique_classes),
                }
            )

    def _calculate_class_weights(self):
        """Calculate class weights for this turbine to handle class imbalance."""
        class_weights = {}
        for i in range(6):  # All possible classes
            if i in self.unique_classes:
                class_count = np.sum(self.y_train == i)
                class_weights[i] = len(self.y_train) / (len(self.unique_classes) * class_count)
            else:
                class_weights[i] = 0.0
        return class_weights

    def fit(self, parameters, config):
        """Train model locally with personalized classification head."""
        
        # Get server round from config (if available)
        server_round = config.get("server_round", 0)
        
        # Instantiate model
        model = load_model(float(config["lr"]))
        
        # Apply weights from global model
        model.set_weights(parameters)
        
        # Override classification layer with this turbine's personalized weights
        self._load_layer_weights_from_state(model)
        
        # Train model with class weights
        history = model.fit(
            self.x_train,
            self.y_train,
            epochs=self.local_epochs,
            batch_size=self.batch_size,
            class_weight=self.class_weights,
            validation_data=(self.x_test, self.y_test),
            verbose=1,
        )
        
        # Save classification head to state for future rounds
        self._save_layer_weights_to_state(model)
        
        # Prepare metrics to return
        fit_metrics = {
            "loss": float(history.history["loss"][-1]),
            "accuracy": float(history.history["accuracy"][-1]),
            "val_loss": float(history.history["val_loss"][-1]),
            "val_accuracy": float(history.history["val_accuracy"][-1]),
            "turbine_id": self.turbine_id,
            "unique_classes": [int(c) for c in self.unique_classes.tolist()],
        }
        
        # Log to wandb if enabled
        if self.use_wandb and self.wandb_run is not None:
            log_wandb_safe({
                f"{self.turbine_id}_train_loss": fit_metrics["loss"],
                f"{self.turbine_id}_train_accuracy": fit_metrics["accuracy"],
                f"{self.turbine_id}_val_loss": fit_metrics["val_loss"],
                f"{self.turbine_id}_val_accuracy": fit_metrics["val_accuracy"],
                f"{self.turbine_id}_learning_rate": float(config["lr"]),
                f"{self.turbine_id}_server_round": server_round,
                f"{self.turbine_id}_num_classes": len(self.unique_classes),
            }, step=server_round)
        
        # Return locally-trained model and metrics
        return (
            model.get_weights(),
            len(self.x_train),
            fit_metrics,
        )

    def _save_layer_weights_to_state(self, model):
        """Save classification head weights to state."""
        state_dict_arrays = {}
        
        # Get weights from the classification layer (last dense layer)
        layer_name = "dense"
        for variable in model.get_layer(layer_name).trainable_variables:
            state_dict_arrays[f"{layer_name}.{variable.name}"] = Array(variable.numpy())
        
        # Add to RecordDict (replace if already exists)
        self.client_state[self.local_layer_name] = ArrayRecord(state_dict_arrays)

    def _load_layer_weights_from_state(self, model):
        """Load classification head weights from state."""
        if self.local_layer_name not in self.client_state.array_records:
            return
            
        list_weights = self.client_state[self.local_layer_name].to_numpy_ndarrays()
        
        # Apply weights to classification layer
        model.get_layer("dense").set_weights(list_weights)

    def evaluate(self, parameters, config):
        """Evaluate global model with personalized classification head."""
        
        # Get server round from config (if available)
        server_round = config.get("server_round", 0)
        
        # Instantiate model
        model = load_model()
        
        # Apply global model weights
        model.set_weights(parameters)
        
        # Override classification layer with this turbine's personalized weights
        self._load_layer_weights_from_state(model)
        
        # Evaluate
        loss, accuracy = model.evaluate(self.x_test, self.y_test, verbose=0)
        
        # Prepare evaluation metrics
        eval_metrics = {
            "accuracy": float(accuracy),
            "turbine_id": self.turbine_id,
        }
        
        # Log to wandb if enabled
        if self.use_wandb and self.wandb_run is not None:
            log_wandb_safe({
                f"{self.turbine_id}_eval_loss": float(loss),
                f"{self.turbine_id}_eval_accuracy": float(accuracy),
                f"{self.turbine_id}_eval_samples": len(self.x_test),
            }, step=server_round)
        
        return loss, len(self.x_test), eval_metrics

    def __del__(self):
        """Clean up wandb run when client is destroyed."""
        if hasattr(self, 'use_wandb') and self.use_wandb and hasattr(self, 'wandb_run') and self.wandb_run is not None:
            finish_wandb_safe()


def client_fn(context: Context):
    """Create a Flower client for a specific wind turbine."""
    
    # Ensure a new session is started
    keras.backend.clear_session()
    
    # Load config and dataset for this turbine
    partition_id = context.node_config["partition-id"]
    num_partitions = context.node_config["num-partitions"]
    
    print(f"Client starting with partition-id: {partition_id}, num-partitions: {num_partitions}")
    
    # Map partition to turbine ID
    turbine_mapping = {0: "T01", 1: "T06", 2: "T07"}
    turbine_id = turbine_mapping.get(int(partition_id), "T01")
    
    print(f"Mapped to Turbine: {turbine_id}")
    
    # Load turbine data
    data = load_data(int(partition_id), int(num_partitions))
    local_epochs = context.run_config["local-epochs"]
    batch_size = context.run_config["batch-size"]
    use_wandb = context.run_config.get("use-wandb", False)
    
    print(f"Client ready for Turbine {turbine_id} - waiting for server instructions...")
    if use_wandb:
        print(f"Wandb monitoring enabled for Turbine {turbine_id}")
    
    # Return Client instance with state persistence
    client_state = context.state
    return TurbineClient(
        client_state, 
        data, 
        batch_size, 
        local_epochs,
        turbine_id,
        use_wandb
    ).to_client()


# Flower ClientApp
app = ClientApp(
    client_fn,
)