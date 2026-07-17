#!/bin/bash

# Helper script to run FL experiments for wind turbine predictive maintenance

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running in WSL
if grep -q Microsoft /proc/version; then
    print_status "Running in WSL environment"
else
    print_warning "Not running in WSL - some features might not work as expected"
fi

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Docker
    if command -v docker &> /dev/null; then
        print_status "Docker found: $(docker --version)"
    else
        print_error "Docker not found. Please install Docker in WSL"
        exit 1
    fi
    
    # Check Docker Compose
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
        print_status "Docker Compose found"
    else
        print_error "Docker Compose not found. Please install Docker Compose"
        exit 1
    fi
    
    # Check Flower CLI
    if command -v flwr &> /dev/null; then
        print_status "Flower CLI found: $(flwr --version)"
    else
        print_error "Flower CLI not found. Please install with: pip install flwr"
        exit 1
    fi
    
    # Check data files
    print_status "Checking data files..."
    for turbine in T01 T06 T07; do
        if [ -f "Data/turbine_${turbine}_dataset.csv" ]; then
            print_status "Found turbine_${turbine}_dataset.csv"
        else
            print_error "Missing turbine_${turbine}_dataset.csv in Data directory"
            exit 1
        fi
    done
}

# Create necessary directories
setup_directories() {
    print_status "Setting up directories..."
    mkdir -p Data
    mkdir -p fl_metrics
    chmod -R 755 Data fl_metrics
}

# Clean up previous runs
cleanup() {
    print_status "Cleaning up previous runs..."
    docker compose down 2>/dev/null || true
    rm -rf fl_metrics/*
}

# Run FL experiment
run_experiment() {
    local rounds=${1:-50}
    print_status "Starting FL experiment with $rounds rounds..."
    
    # Export configuration
    export FLWR_VERSION=1.18.0
    export PROJECT_DIR=$(pwd)
    
    # Update number of rounds in pyproject.toml
    sed -i "s/num-server-rounds = .*/num-server-rounds = $rounds/" pyproject.toml
    
    # Start Docker infrastructure
    print_status "Starting Docker infrastructure..."
    docker compose up -d
    
    # Wait for services to be ready
    print_status "Waiting for services to initialize..."
    sleep 10
    
    # Check if services are running
    if ! docker compose ps | grep -q "Up"; then
        print_error "Docker services failed to start"
        return 1
    fi
    
    # Start Flower training
    print_status "Starting Flower federated learning..."
    print_status "This will run for $rounds rounds..."
    
    # Run Flower with local-deployment configuration
    flwr run . local-deployment --stream
}

# Monitor experiment
monitor_experiment() {
    print_status "Monitoring experiment..."
    
    # Check if services are running
    if ! docker compose ps | grep -q "Up"; then
        print_error "No services running"
        return 1
    fi
    
    # Watch metrics file
    if [ -f "fl_metrics/training_history.json" ]; then
        print_status "Latest metrics:"
        tail -n 50 fl_metrics/training_history.json
    else
        print_warning "No metrics file found yet"
    fi
}

# Stop experiment
stop_experiment() {
    print_status "Stopping experiment..."
    docker compose down
    print_status "Experiment stopped"
}

# Analyze results
analyze_results() {
    print_status "Analyzing results..."
    
    if [ ! -f "fl_metrics/training_history.json" ]; then
        print_error "No results found"
        return 1
    fi
    
    # Create a simple Python script to analyze results
    cat > analyze_metrics.py << 'EOF'
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load metrics
with open('fl_metrics/training_history.json', 'r') as f:
    metrics = json.load(f)

# Extract data for plotting
rounds = []
losses = []
turbine_data = {}

for round_data in metrics:
    round_num = round_data['round']
    rounds.append(round_num)
    losses.append(round_data.get('aggregated_loss', 0))
    
    # Collect per-turbine data
    for turbine_id, report in round_data.get('turbine_reports', {}).items():
        if turbine_id not in turbine_data:
            turbine_data[turbine_id] = {'rounds': [], 'accuracy': []}
        
        turbine_data[turbine_id]['rounds'].append(round_num)
        
        # Get weighted average accuracy from classification report
        if 'weighted avg' in report:
            turbine_data[turbine_id]['accuracy'].append(report['weighted avg']['precision'])

# Plot results
plt.figure(figsize=(12, 8))

# Subplot 1: Aggregated Loss
plt.subplot(2, 1, 1)
plt.plot(rounds, losses, 'b-', linewidth=2)
plt.xlabel('Round')
plt.ylabel('Aggregated Loss')
plt.title('Federated Learning Progress - Aggregated Loss')
plt.grid(True, alpha=0.3)

# Subplot 2: Per-Turbine Accuracy
plt.subplot(2, 1, 2)
for turbine_id, data in turbine_data.items():
    if data['accuracy']:  # Only plot if data exists
        plt.plot(data['rounds'], data['accuracy'], label=f'Turbine {turbine_id}', linewidth=2)

plt.xlabel('Round')
plt.ylabel('Accuracy')
plt.title('Per-Turbine Accuracy Over Rounds')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('fl_metrics/training_progress.png', dpi=300)
print("Results saved to fl_metrics/training_progress.png")

# Print final statistics
print("\nFinal Round Statistics:")
if metrics:
    final_round = metrics[-1]
    print(f"Round: {final_round['round']}")
    print(f"Aggregated Loss: {final_round.get('aggregated_loss', 'N/A'):.4f}")
    print("\nPer-Turbine Results:")
    for turbine_id, report in final_round.get('turbine_reports', {}).items():
        print(f"\n{turbine_id}:")
        if 'weighted avg' in report:
            print(f"  Precision: {report['weighted avg']['precision']:.4f}")
            print(f"  Recall: {report['weighted avg']['recall']:.4f}")
            print(f"  F1-Score: {report['weighted avg']['f1-score']:.4f}")
EOF

    python analyze_metrics.py
}

# Main menu
show_menu() {
    echo
    echo "Wind Turbine FL Experiment Manager"
    echo "=================================="
    echo "1. Check prerequisites"
    echo "2. Setup directories"
    echo "3. Clean up previous runs"
    echo "4. Run experiment (default 50 rounds)"
    echo "5. Run quick test (10 rounds)"
    echo "6. Monitor experiment"
    echo "7. Stop experiment"
    echo "8. Analyze results"
    echo "9. Full pipeline (setup + run + analyze)"
    echo "0. Exit"
    echo
}

# Main loop
main() {
    while true; do
        show_menu
        read -p "Select option: " choice
        
        case $choice in
            1) check_prerequisites ;;
            2) setup_directories ;;
            3) cleanup ;;
            4) 
                check_prerequisites
                cleanup
                print_status "Starting infrastructure..."
                docker compose up -d
                sleep 10
                print_status "Starting FL training (50 rounds)..."
                flwr run . local-deployment --stream
                ;;
            5) 
                check_prerequisites
                cleanup
                print_status "Starting infrastructure..."
                docker compose up -d
                sleep 10
                print_status "Starting FL training (10 rounds)..."
                # First update the config
                sed -i "s/num-server-rounds = .*/num-server-rounds = 10/" pyproject.toml
                flwr run . local-deployment --stream
                # Reset to default
                sed -i "s/num-server-rounds = .*/num-server-rounds = 50/" pyproject.toml
                ;;
            6) monitor_experiment ;;
            7) stop_experiment ;;
            8) analyze_results ;;
            9) 
                check_prerequisites
                setup_directories
                cleanup
                print_status "Starting infrastructure..."
                docker compose up -d
                sleep 10
                print_status "Starting FL training..."
                flwr run . local-deployment --stream
                print_status "Training completed. Analyzing results..."
                analyze_results
                ;;
            0) 
                print_status "Exiting..."
                exit 0
                ;;
            *)
                print_error "Invalid option"
                ;;
        esac
    done
}

# Run main function
main