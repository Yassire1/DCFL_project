---
trigger: always_on
---

Project contribution rules and guidelines for all agents working on the Wind Turbine Failure Prediction (DCFL) research project


# DCFL Project Rules

## Workflow

- Always break down your intended work into a numbered plan before doing anything.
- Wait for explicit user confirmation before executing any plan. Do not proceed without it.
- Exception: explicit user approval in the same prompt (e.g., "go ahead", "implement it", "do it", "apply changes now") counts as confirmation.
- After any implementation, test, or experiment: append an entry to `Experiment_Log.md` with the task name, what was done, and status (e.g., `✅ shipped`, `🔄 under verification`, `❌ failed`).
- Log every experiment to `Experiment_Log.md` using the existing format (ID, Date, Description, Changes, Hypothesis, Configuration, Results, Observations). Never skip the Observations section.
- Always use code to save artifacts from the training in every step of the notebook. Never overwrite existing artifacts without a backup.
- If a user instruction conflicts with these rules, ask for an explicit override before proceeding.

## Data Rules

- Split is **time-based only**. Never shuffle SCADA data randomly.
- For time-series data splits, use our defined split function. Do not modify it without explicit user approval.
- Never fit scaler, encoder, selector, or imputer on validation or test data; fit on train only and transform val/test.
- Windowing is **per turbine**. Never create windows across turbine boundaries.
- Always preserve columns `Turbine_ID`, `Timestamp`, `Label` through all pipeline steps.

## Labeling Rules

- Use a **single `Label` column** only. Never create per-component columns (e.g., `Gearbox_Label`).
- Label mapping: `0 = Normal`, `1..N = component failure` (component index + 1).
- Labeling logic must follow **Cell 19** of `Artical_level_data_preparation.ipynb` as source of truth.



## Hard Prohibitions

- Never shuffle time series data.
- Never create multiple label columns.
- Never fit preprocessing on validation or test data.
- Never augment or downsample val or test data.
- Never overwrite existing experiment results without a backup.
- Never skip logging to `Experiment_Log.md` after an experiment.
- Never execute a plan without user confirmation.
