# Wind Turbine Federated Learning System

This project implements a Federated Learning system for predictive maintenance of wind turbines using a CNN+LSTM hybrid model.

## Overview

- **4 Wind Turbines**: T01, T06, T07, T11 (each acts as a federated client)
- **Model**: CNN+LSTM hybrid for multi-class failure prediction (6 classes)
- **Framework**: Flower (flwr) for federated learning
- **Deployment**: Docker Compose for distributed setup

## Project Structure

```
windturbine-fl/
├── Data/                      # Wind turbine datasets
│   ├── turbine_T01_dataset.csv
│   ├── turbine_T06_dataset.csv
│   ├── turbine_T07_dataset.csv
│   └── turbine_T11_dataset.csv
├── fl_metrics/               # Training metrics (created automatically)
├── task.py                   # Model architecture and data processing
├── client_app.py            # FL client implementation
├── server_app.py            # FL server implementation
├── pyproject.toml           # Project configuration
├── compose.yml              # Docker Compose configuration
└── README.md                # This file
```

## Setup Instructions

### 1. Prerequisites

- WSL (Windows Subsystem for Linux) with Ubuntu
- Docker and Docker Compose installed in WSL
- Python 3.8+ (for local testing)

### 2. Data Preparation

Place your wind turbine CSV files in the `Data/` directory:

```bash
mkdir -p Data
# Copy your CSV files to the Data directory
cp /path/to/turbine_T01_dataset.csv Data/
cp /path/to/turbine_T06_dataset.csv Data/
cp /path/to/turbine_T07_dataset.csv Data/
cp /path/to/turbine_T11_dataset.csv Data/
```

### 3. Local Testing (Optional)

To test the setup locally before Docker deployment:

```bash
# Install dependencies
pip install -e .

# Run simulation mode (all clients on same machine)
flwr run . --run-config num-server-rounds=10

# Or run with Docker infrastructure
docker compose up -d  # Start infrastructure
flwr run . local-deployment --stream  # Start training
```

### 4. Docker Deployment

The proper way to run the federated learning system with Docker:

```bash
# Step 1: Start the infrastructure (SuperLink and SuperNodes)
docker compose up -d

# Step 2: Verify services are running
docker compose ps

# Step 3: Start the federated learning training
flwr run . local-deployment --stream

# View logs in another terminal
docker compose logs -f

# Stop all services when done
docker compose down
```

**Important**: `docker compose up` only starts the infrastructure. You must use `flwr run` to actually start the training process.

## Model Details

### Architecture
- **Input**: Time series windows of 144 time steps (24 hours) with 26 SCADA features
- **CNN Layers**: Extract spatial features from sensor data
- **LSTM Layers**: Capture temporal dependencies
- **Output**: 6 classes (0: Normal, 1-5: Different failure types)

### Key Features
- **Class Imbalance Handling**: Focal loss and class weights
- **Non-IID Data**: Each turbine may have different failure classes
- **Early Stopping**: Prevents overfitting during local training
- **Learning Rate Decay**: Gradual reduction across rounds

## Configuration

Edit `pyproject.toml` to adjust training parameters:

```toml
[tool.flwr.app.config]
num-server-rounds = 50    # Number of FL rounds
local-epochs = 5          # Epochs per client per round
batch-size = 32          # Batch size for training
learning-rate = 0.001    # Initial learning rate
fraction-fit = 1.0       # Fraction of clients for training
fraction-evaluate = 1.0  # Fraction of clients for evaluation
```

## Monitoring

Training metrics are saved to `fl_metrics/training_history.json` after each round, including:
- Per-turbine loss and accuracy
- Classification reports
- Aggregated metrics

## Troubleshooting

### Common Issues

1. **Memory Issues**: Reduce batch size in `pyproject.toml`
2. **Docker Permission**: Run with `sudo` if needed
3. **Port Conflicts**: Ensure ports 9091-9097 are free

### Debugging

```bash
# Check individual service logs
docker compose logs serverapp
docker compose logs clientapp-1

# Interactive debugging
docker compose run --rm clientapp-1 /bin/bash
```

## Notes on Multi-Class Classification

Each turbine may have different failure classes in their data:
- T01: Classes 0, 1
- T06: Classes 0, 2, 5
- etc.

The FL system handles this by:
1. Using a unified 6-class model across all clients
2. Applying class weights only for classes present in each client's data
3. Aggregating updates properly during federated averaging

## Future Improvements

1. Add tensorboard logging for real-time monitoring
2. Implement differential privacy
3. Add model checkpointing and recovery
4. Implement secure aggregation
5. Add automated hyperparameter tuning