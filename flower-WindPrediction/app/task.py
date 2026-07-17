"""windturbine-fl: A Flower / TensorFlow app for wind turbine predictive maintenance."""

import json
import os
from datetime import datetime
from pathlib import Path

import tensorflow as tf
from tensorflow import keras
from keras import layers
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from flwr.common.typing import UserConfig

# Make TensorFlow log less verbose
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Configure TensorFlow
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)


def load_model(learning_rate: float = 0.001):
    """Create simple model for simulation testing (memory efficient)."""
    
    inputs = keras.Input(shape=(144, 26), name='scada_input')
    
    # Ultra-simple architecture for simulation testing
    x = layers.GlobalAveragePooling1D()(inputs)  # Reduces memory dramatically
    x = layers.Dense(32, activation='relu')(x)
    x = layers.Dropout(0.2)(x)
    x = layers.Dense(16, activation='relu')(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(6, activation='softmax')(x)
    
    model = keras.Model(inputs, outputs)
    
    optimizer = keras.optimizers.Adam(learning_rate)
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'],
    )
    
    return model


def create_windows(data, labels, window_size=144, stride=1):
    """Create windowed data from time series."""
    X_windows = []
    y_windows = []

    for i in range(0, len(data) - window_size + 1, stride):
        X_windows.append(data[i:i+window_size])
        y_windows.append(labels[i+window_size-1])

    return np.array(X_windows), np.array(y_windows)


def load_turbine_data(turbine_id: str, data_dir: str = None):
    """Load and preprocess turbine-specific SCADA data."""
    
    # Handle different environments (Docker vs local)
    if data_dir is None:
        # Try different possible paths
        possible_paths = [
            "Data",  # Local execution
            "/app/Data",  # Docker container
            "./Data",  # Relative path
            os.path.join(os.getcwd(), "Data")  # Current working directory
        ]
        
        for path in possible_paths:
            test_file = f"{path}/turbine_{turbine_id}_dataset.csv"
            if os.path.exists(test_file):
                data_dir = path
                break
        
        if data_dir is None:
            raise FileNotFoundError(f"Could not find Data directory. Tried: {possible_paths}")
    
    # Load dataset
    file_path = f"{data_dir}/turbine_{turbine_id}_dataset.csv"
    # if not os.path.exists(file_path):
    #     raise FileNotFoundError(f"Dataset file not found: {file_path}")
        
    print(f"Loading data from: {file_path}")
    df = pd.read_csv(file_path)
    
    # Convert timestamp to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Sort by timestamp
    df = df.sort_values('Timestamp')
    
    # Handle missing values
    df = df.fillna(method='ffill').fillna(method='bfill')
    
    # Separate features and target
    X = df.drop(['Label', 'Timestamp', 'Turbine_ID', 'Avg_Raindetection'], axis=1, errors='ignore')
    y = df['Label']
    
    # Print class distribution
    unique_classes, counts = np.unique(y, return_counts=True)
    print(f"Turbine {turbine_id} - Classes: {unique_classes}, Counts: {dict(zip(unique_classes, counts))}")
    
    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Create windows
    X_windowed, y_windowed = create_windows(X_scaled, y.values, window_size=144, stride=1)
    
    # Split into train/test (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X_windowed, y_windowed, test_size=0.2, random_state=42, stratify=y_windowed
    )
    
    return X_train, y_train, X_test, y_test


# Cache for loaded data
data_cache = {}


def load_data(partition_id, num_partitions):
    """Load partition data for a specific turbine."""
    
    # Map partition IDs to turbine IDs
    turbine_mapping = {
        0: "T01",
        1: "T06", 
        2: "T07"
    }
    
    turbine_id = turbine_mapping.get(partition_id, "T01")
    
    # Use cache if already loaded
    cache_key = f"turbine_{turbine_id}"
    if cache_key not in data_cache:
        print(f"Loading data for Turbine {turbine_id} (partition {partition_id})")
        x_train, y_train, x_test, y_test = load_turbine_data(turbine_id)
        data_cache[cache_key] = (x_train, y_train, x_test, y_test)
    
    return data_cache[cache_key]


def load_central_test_data(turbine_id: str = "T11", data_dir: str = None):
    """Load central test dataset (T11) for server-side evaluation."""
    
    cache_key = f"central_test_{turbine_id}"
    if cache_key not in data_cache:
        print(f"Loading central test data from Turbine {turbine_id}")
        _, _, x_test, y_test = load_turbine_data(turbine_id, data_dir)
        data_cache[cache_key] = (x_test, y_test)
    
    return data_cache[cache_key]


def create_run_dir(config: UserConfig) -> tuple[Path, str]:
    """Create a directory where to save results from this run."""
    
    # Create output directory given current timestamp
    current_time = datetime.now()
    run_dir = current_time.strftime("%Y-%m-%d/%H-%M-%S")

    # Save path is based on the current directory
    save_path = Path.cwd() / f"outputs/{run_dir}"
    save_path.mkdir(parents=True, exist_ok=False)
    
    # Save run config as json
    with open(f"{save_path}/run_config.json", "w", encoding="utf-8") as fp:
        json.dump(config, fp)
    
    return save_path, run_dir