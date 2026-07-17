"""windturbine-fl: A Flower / TensorFlow server for wind turbine predictive maintenance."""

from app.strategy import WindTurbineStrategy
from app.task import load_model, load_central_test_data

from flwr.common import Context, ndarrays_to_parameters
from flwr.server import ServerApp, ServerAppComponents, ServerConfig


def gen_evaluate_fn(x_test, y_test):
    """Generate the function for centralized evaluation on T11 dataset."""
    
    def evaluate(server_round, parameters_ndarrays, config):
        """Evaluate global model on centralized test set (T11)."""
        model = load_model()
        model.set_weights(parameters_ndarrays)
        loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
        
        # Additional metrics
        import numpy as np
        y_pred = model.predict(x_test, verbose=0)
        y_pred_classes = np.argmax(y_pred, axis=1)
        
        # Calculate F1 score
        from sklearn.metrics import f1_score
        f1 = f1_score(y_test, y_pred_classes, average='weighted', zero_division=0)
        
        return loss, {
            "centralized_accuracy": accuracy,
            "centralized_f1_score": f1,
            "centralized_samples": len(y_test),
        }
    
    return evaluate


def on_fit_config(server_round: int):
    """Construct config that clients receive when running fit()."""
    lr = 0.001
    # Enable learning rate decay
    if server_round > 10:
        lr *= 0.95
    if server_round > 20:
        lr *= 0.95
    return {
        "lr": lr,
        "server_round": server_round,  # Pass server round to clients for wandb logging
    }


def on_evaluate_config(server_round: int):
    """Construct config that clients receive when running evaluate()."""
    return {
        "server_round": server_round,  # Pass server round to clients for wandb logging
    }


# Define metric aggregation function
def weighted_average(metrics):
    """Aggregate metrics using weighted average."""
    
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]
    
    # Collect turbine-specific information
    turbine_info = {}
    for num_examples, m in metrics:
        if "turbine_id" in m:
            turbine_info[m["turbine_id"]] = {
                "accuracy": m["accuracy"],
                "samples": num_examples,
            }
    
    # Aggregate and return custom metrics
    return {
        "federated_evaluate_accuracy": sum(accuracies) / sum(examples) if sum(examples) > 0 else 0,
        "total_examples": sum(examples),
        "num_turbines": len(metrics),
        "turbine_metrics": turbine_info,
    }


def server_fn(context: Context):
    """Configure the server with strategy and centralized evaluation."""
    
    # Read from config
    num_rounds = context.run_config["num-server-rounds"]
    fraction_fit = context.run_config["fraction-fit"]
    fraction_eval = context.run_config["fraction-evaluate"]
    use_wandb = context.run_config.get("use-wandb", False)
    
    # Initialize model parameters
    ndarrays = load_model().get_weights()
    parameters = ndarrays_to_parameters(ndarrays)
    
    # Load T11 dataset for centralized evaluation
    print("Loading T11 dataset for centralized evaluation...")
    x_test, y_test = load_central_test_data("T11")
    print(f"Central test set: {len(x_test)} samples")
    
    # Define custom strategy with all advanced features
    strategy = WindTurbineStrategy(
        run_config=context.run_config,
        use_wandb=use_wandb,
        fraction_fit=fraction_fit,
        fraction_evaluate=fraction_eval,
        min_fit_clients=3,
        min_evaluate_clients=3,
        min_available_clients=3,
        initial_parameters=parameters,
        on_fit_config_fn=on_fit_config,
        on_evaluate_config_fn=on_evaluate_config,
        evaluate_fn=gen_evaluate_fn(x_test, y_test),
        evaluate_metrics_aggregation_fn=weighted_average,
    )
    
    config = ServerConfig(num_rounds=num_rounds)
    
    return ServerAppComponents(strategy=strategy, config=config)


# Create ServerApp
app = ServerApp(server_fn=server_fn)