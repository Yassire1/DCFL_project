# AGENTS.md — DCFL Wind Turbine Predictive Maintenance

Research project: Data-Centric Federated Learning for wind-turbine predictive maintenance (TensorFlow/Keras + Flower `flwr` + scikit-learn/pandas).

## Repo map

- `flower-WindPrediction/app/` — FL prototype: `task.py` (model + data), `client_app.py`, `server_app.py`, `strategy.py` (FedAvg + checkpointing to `outputs/`). Partition map in `task.py:132-137` / `client_app.py:193-195`: `0→T01, 1→T06, 2→T07`; `T11` is server-side central test (`server_app.py:97-99`).
- `flower-WindPrediction/Data/` — already populated (`turbine_T{01,06,07,11}_dataset.csv`). `Data/` is mounted read-only in Docker (`compose.yml`).
- `NoteBooks/Artical_level_data_preparation.ipynb` (note `Artical` typo — exact filename) — data pipeline, Cell 19 is labeling source of truth. `NoteBooks/Article_level_Model_Training.ipynb` — centralized training.
- `DCFL_Article/main.tex` (+ `test_branch.tex` scratch copy) — English journal article. Compile with `latexmk`; never edit generated `.aux/.log/.fls/.fdb_latexmk/.out`.
- `Experiment_Log.md`, `Implementation_Plan.md` — experiment history (EXP-001…EXP-010) and roadmap (deadline Mar 20, 2026).
- `sources/*.md` (background research notes), `Results and artifacts/visualizations/`, `publishing infos/` (journal cheat sheet) — read-only context, not code. `chicklist/*.png` is scratch images; ignore.

Loaded automatically via `opencode.json`: `AGENTS.md` + `.agents/rules/*.md` + `.github/instructions/*.md`. Source of truth for hard rules is `.agents/rules/contribution-rules.md` (= `.github/instructions/project-rules.instructions.md`).

## Commands

All FL commands run from `flower-WindPrediction/`:

```bash
pip install -e .
flwr run . --run-config num-server-rounds=10   # local simulation
docker compose up -d                           # start SuperLink + SuperNodes only, no training
flwr run . local-deployment --stream           # start training against Docker infra
docker compose ps; docker compose logs -f; docker compose down
```

- Config truth is `pyproject.toml [tool.flwr.app.config]` (current defaults: `num-server-rounds=3, local-epochs=1, batch-size=16, fraction-fit=1.0, use-wandb=false`). `Readme.md` shows stale values (50/5/32) — ignore it.
- `run_federated_learning.sh` is an interactive menu wrapper (prereq checks, `sed` round override, metrics plot); prefer direct `flwr` commands unless asked.
- No pytest/ruff/CI (no `tests/`, no `.github/workflows/`). Do not add test/lint infra without asking.
- Notebooks: run cells sequentially, save artifacts every step, never overwrite without backup. Keep cell outputs committed.

## Gotchas (agent would miss these)

- **`use-wandb` is broken either way.** `client_app.py:6` and `strategy.py:7` do unconditional `from setup_wandb import ...`, but no `setup_wandb` module exists in the repo (verified by search). Any `flwr run` crashes at import until that import is stubbed/removed — setting `use-wandb=false` alone does not fix it.
- **Clients keep a personalized classification head.** `client_app.py:119-139` saves/restores the final `dense` layer in `Context.state` per turbine; only feature-extraction weights are truly federated. Don't "fix" this as a bug without asking.
- **Server requires 3 clients.** `server_app.py:108-110` sets `min_fit/evaluate/available_clients=3`; Docker runs fail if any supernode/client is down, regardless of `fraction-fit`.
- **`app/task.py` diverges from research rules.** It uses `train_test_split(..., stratify=...)` random split (`task.py:118-120`) and `scaler.fit_transform` on all data (`task.py:111-112`), violating the time-based-split and fit-on-train-only rules. Do not copy this pattern into notebooks; fix only on request.
- **FL model is a stub.** `task.py:26-48` is GAP + Dense(32/16) → 6-class softmax on `(144, 26)` input for memory-efficient simulation. The real research architecture (2×CNN + 2×BiLSTM) lives in notebooks per `Implementation_Plan.md §1.8`.
- **Docker needs WSL + ports 9091–9097 free** (`Readme.md` troubleshooting); `compose.yml` pins `FLWR_VERSION=1.18.0`. `run_federated_learning.sh` rewrites `pyproject.toml` rounds via `sed` — prefer direct `flwr` commands so config isn't silently mutated.
- **Results paths differ:** strategy checkpoints go to `outputs/<date>/<time>/` (`results.json`, `summary.json`, `*.weights.h5`); `Readme.md`-era `fl_metrics/training_history.json` is stale (and `fl_metrics/` is gitignored).

## Hard rules (non-negotiable — ask for explicit override on conflict)

Workflow: numbered plan first, wait for explicit user confirmation (`go ahead`/`do it` counts); after any experiment append to `Experiment_Log.md` with ID, Date, Description, Changes, Hypothesis, Configuration, Results, **Observations** (never skip).

Data/labeling: time-based splits only (train ends May 31 2017; val Jun–Jul; test Aug–Oct 2017) — never shuffle; fit scaler/encoder/imputer on train only; windowing per turbine (never across boundaries); preserve `Turbine_ID`, `Timestamp`, `Label`; single `Label` column only (`0=Normal`, `1..N=component`), logic per Cell 19; never augment/downsample val/test; never overwrite results without backup.
