# AGENTS.md — DCFL Wind Turbine Predictive Maintenance

Instructions for coding agents working in this repository.

## Project Overview

Research project: **Data-Centric Federated Learning (DCFL) for Wind Turbine Predictive Maintenance**.

- **Python 3.8+** with TensorFlow/Keras, Flower (flwr), scikit-learn, pandas, numpy
- **Federated Learning**: Flower framework (`flwr`) with 3 turbine clients (T01, T06, T07) + central test (T11)
- **Notebooks**: Jupyter notebooks for data preparation and model training in `NoteBooks/`
- **FL App**: Flower server/client app in `flower-WindPrediction/app/`
- **Article**: LaTeX manuscript in `DCFL_Article/`

## Build / Run / Deploy Commands

### Federated Learning (flower-WindPrediction/)

```bash
# Install dependencies (from flower-WindPrediction/)
pip install -e .

# Local simulation (all clients on one machine)
flwr run . --run-config num-server-rounds=10

# Docker deployment
docker compose up -d                          # start infrastructure
flwr run . local-deployment --stream          # start training
docker compose logs -f                        # view logs
docker compose down                           # stop all

# Check service status
docker compose ps
```

### Configuration

Edit `flower-WindPrediction/pyproject.toml` under `[tool.flwr.app.config]`:
- `num-server-rounds`, `local-epochs`, `batch-size`, `fraction-fit`, `use-wandb`

### Notebooks

Work in `NoteBooks/` using Jupyter. Execute cells sequentially — do not skip ahead.
Always save artifacts after training. Never overwrite without backup.

### No Formal Test/Lint Pipeline

This project has no pytest, ruff, flake8, or CI configured. Before adding tests or linting,
confirm with the user. Suggested commands if needed:

```bash
# Suggested (not yet configured)
pip install ruff && ruff check app/
pip install pytest && pytest tests/ -v
```

## Code Style

### Python

- **Imports**: stdlib → third-party → local, separated by blank lines
  ```python
  import json
  import os

  import numpy as np
  import pandas as pd
  import tensorflow as tf

  from app.task import load_model
  ```
- **Type hints**: Use for function signatures (parameters and return types)
  ```python
  def load_turbine_data(turbine_id: str, data_dir: str = None) -> tuple:
  ```
- **Docstrings**: Single-line docstrings for all public functions and classes
  ```python
  def create_windows(data, labels, window_size=144, stride=1):
      """Create windowed data from time series."""
  ```
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants
- **Strings**: Double quotes for docstrings, single or double quotes for strings (codebase uses both — prefer double)
- **Line length**: ~100 chars soft limit (no strict formatter configured)
- **Error handling**: Use explicit `try/except` with specific exceptions; avoid bare `except:`. Raise with messages:
  ```python
  raise FileNotFoundError(f"Could not find Data directory. Tried: {possible_paths}")
  ```

### Jupyter Notebooks

- Keep cell outputs committed (do not clear before committing)
- Use markdown cells for section headers and explanations
- Save training artifacts to disk in every cell that produces results
- Follow existing notebook naming: `Artical_level_data_preparation.ipynb`, `Article_level_Model_Training.ipynb`

### LaTeX (DCFL_Article/)

- Compile with `latexmk` (build artifacts in `main.aux`, `main.pdf`, etc.)
- Do not edit generated files (`.aux`, `.log`, `.fdb_latexmk`, `.fls`)

## Hard Rules (from project rules)

These are **non-negotiable** — ask for explicit override if a user instruction conflicts.

### Workflow

1. Break work into a **numbered plan** before doing anything
2. Wait for **explicit user confirmation** before executing (phrases like "go ahead", "do it" count)
3. After any experiment: **append to `Experiment_Log.md`** using the existing format (ID, Date, Description, Changes, Hypothesis, Configuration, Results, Observations)
4. Never skip the **Observations** section in experiment logs
5. Never overwrite existing experiment results without a backup

### Data Rules

- **Time-based splits only** — never shuffle SCADA data randomly
- Never fit scaler, encoder, selector, or imputer on val/test data — fit on train only, transform val/test
- Windowing is **per turbine** — never create windows across turbine boundaries
- Always preserve columns `Turbine_ID`, `Timestamp`, `Label` through all pipeline steps

### Labeling Rules

- Use a **single `Label` column** only — never create per-component columns (e.g., `Gearbox_Label`)
- Label mapping: `0 = Normal`, `1..N = component failure` (component index + 1)
- Labeling logic follows **Cell 19** of `Artical_level_data_preparation.ipynb` as source of truth

### Prohibitions

- Never shuffle time series data
- Never create multiple label columns
- Never fit preprocessing on validation or test data
- Never augment or downsample val or test data
- Never execute a plan without user confirmation
