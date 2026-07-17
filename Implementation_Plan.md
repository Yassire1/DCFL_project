# 📋 DCFL Project — Implementation Plan

> **Deadline:** March 20, 2026  
> **Started:** March 4, 2026  
> **Status:** In Progress  
>  
> Mark tasks as you go: `[ ]` → `[x]`

---

## Milestone 1 — Centralized Model Training (Final Clean Run)

> **Objective:** Produce the definitive centralized model results that will populate every table in Section 3 (Experiments and Results) of `main.tex`. Every experiment must be reproducible (seed=42) and every artifact (plots, metrics, model weights) must be saved.

---

### 1.1 Data Pipeline Verification

> Before training, confirm that the data preparation notebook produces correct, consistent outputs for every pipeline variant you will compare.

- [ ] **1.1.1** Run `Artical_level_data_preparation.ipynb` end-to-end and verify it produces **six datasets** (2 labeling windows × 3 post-failure configs):
  - `scada_30` — 30-day static pre-failure window
  - `scada_60` — 60-day static pre-failure window
  - `scada_dynamic` — dynamic component-specific window (60d/45d/30d)
  - Each of the above with and without post-failure window injection
- [ ] **1.1.2** For each generated dataset, verify and log:
  - Total row count matches expectations (~417K for full, less after downsampling)
  - Class distribution counts (print `value_counts` and compare with LaTeX Tables 1–3)
  - No data leakage: confirm scaler/encoder/imputer is `.fit()` on train only, `.transform()` on val/test
  - Time-based split boundaries: Train ends May 31 2017; Val = Jun–Jul 2017; Test = Aug–Oct 2017
  - No windows cross turbine boundaries
- [ ] **1.1.3** Save each dataset as `.pkl` or `.csv` to `Results and artifacts/datasets/` with clear naming

---

### 1.2 Temporal Labeling Strategy Comparison

> **Target:** Table `tab:labeling_results` (line 846 of `main.tex`)

- [ ] **1.2.1** Train the **same** 1DCNN-BiLSTM architecture (full, no simplification) three times:
  - Run A: on `scada_30` (30-day window)
  - Run B: on `scada_60` (60-day window)
  - Run C: on `scada_dynamic` (dynamic window)
  - Identical hyperparams: window=144, stride=24, epochs=60, batch=64, lr=0.001, patience=5, seed=42
- [ ] **1.2.2** For each run, record on T11 validation set:
  - Overall accuracy, Macro F1-score, Macro precision and recall
  - Per-class precision, recall, F1
  - Wall-clock training time (minutes)
- [ ] **1.2.3** Save per run: confusion matrix `.png`, ROC curves `.png`, training/validation accuracy+loss curves `.png`, classification report `.txt`
- [ ] **1.2.4** Log all three runs in `Experiment_Log.md`
- [ ] **1.2.5** Update Table `tab:labeling_results` in `main.tex` with real values

---

### 1.3 Post-Failure Window Impact Evaluation

> **Target:** Table `tab:post_failure_impact` (line 878)

- [ ] **1.3.1** Using the **best labeling strategy** from 1.2 (expected: dynamic), train the same model twice:
  - Run D: WITHOUT post-failure windows (only pre-failure labels)
  - Run E: WITH post-failure windows (detected + fallback component averages)
- [ ] **1.3.2** Record: accuracy, macro F1, total false positives (from confusion matrix), qualitative label noise assessment
- [ ] **1.3.3** Generate and save a side-by-side confusion matrix figure
- [ ] **1.3.4** Update Table `tab:post_failure_impact` in `main.tex`

---

### 1.4 Class Consolidation Ablation

> **Target:** Table `tab:class_consolidation` (line 903)

- [ ] **1.4.1** Train the same model twice:
  - Run F: Original 6-class structure (Normal + Gearbox + Transformer + Generator + Gen. Bearing + Hydraulic)
  - Run G: Consolidated 5-class structure (Generator Bearing merged into Generator)
- [ ] **1.4.2** Record: accuracy, macro F1, Class 4 recall (6-class) vs merged Generator recall (5-class), training stability (loss spikes/NaN)
- [ ] **1.4.3** Update Table `tab:class_consolidation` in `main.tex`

---

### 1.5 Feature Selection Benchmarking

> **Target:** Table `tab:feature_selection_results` (line 933)

- [ ] **1.5.1** Prepare four dataset versions (best labeling + post-failure + 5 classes):
  - All 87 features (post preliminary filtering)
  - Domain-based: 31 features
  - Statistical: 28 features (XGBoost importance + correlation + PCA)
  - Hybrid: 26 features
- [ ] **1.5.2** Train the same model on each, record: accuracy, macro F1, precision, recall, training time
- [ ] **1.5.3** Generate and save a feature importance bar chart for the hybrid approach
- [ ] **1.5.4** Update Table `tab:feature_selection_results` in `main.tex`

---

### 1.6 Stride Analysis

> **Target:** Table `tab:stride_comparison` (line 958)

- [ ] **1.6.1** Using the best pipeline config, train:
  - Run H: stride=4 (40-min resolution)
  - Run I: stride=24 (4-hour resolution)
- [ ] **1.6.2** Record: sample count, accuracy, macro F1, training time
- [ ] **1.6.3** Update Table `tab:stride_comparison` in `main.tex`

---

### 1.7 Class Imbalance Mitigation Benchmarking

> **Target:** Table `tab:balancing_results` (line 978)

- [ ] **1.7.1** Prepare four training datasets with best pipeline so far:
  - Baseline: no rebalancing, class weights only in loss
  - Downsampling only: 8-month retention + 1-month post-failure + 15% random sampling of excess normal
  - TimeGAN only: generate synthetic Class 4 (Generator) samples until 200% of original
  - Combined: downsampling then TimeGAN augmentation
- [ ] **1.7.2** Train the same model on each, record: dataset size, accuracy, macro F1, Class 4 recall, training time
- [ ] **1.7.3** Generate t-SNE or PCA visualization of TimeGAN-generated vs authentic samples
- [ ] **1.7.4** Save class distribution bar charts for each approach
- [ ] **1.7.5** Update Table `tab:balancing_results` in `main.tex`

---

### 1.8 Loss Function & Architecture Comparison

> **Target:** Tables `tab:loss_comparison` (line 1012) and `tab:architecture_comparison` (line 1033)

- [ ] **1.8.1** Loss function comparison (best pipeline + best balancing):
  - Run J: Categorical CrossEntropy + class weights
  - Run K: Categorical Focal Loss (γ=2.0, α=0.25), no class weights
- [ ] **1.8.2** Record: accuracy, macro F1, minority class recall, convergence stability
- [ ] **1.8.3** Architecture comparison — train three variants:
  - Full: 2 CNN blocks + 2 BiLSTM layers
  - Simplified CNN: 1 CNN block + 2 BiLSTM layers
  - Simplified BiLSTM: 2 CNN blocks + 1 BiLSTM layer
- [ ] **1.8.4** Record: parameter count, accuracy, macro F1, inference time (ms), model memory (MB)
- [ ] **1.8.5** Update both tables in `main.tex`

---

### 1.9 Final Test Set Evaluation

> **Target:** Table `tab:final_performance` (line 1056) — **the most important centralized result**

- [ ] **1.9.1** Using the optimal pipeline config (dynamic labeling + post-failure + 5-class + 26 features + combined balancing + CrossEntropy + full architecture), train the final model
- [ ] **1.9.2** Evaluate **once** on the held-out test set (Aug–Oct 2017, T11)
- [ ] **1.9.3** Record per-class: precision, recall, F1-score, support. Also: overall accuracy, macro avg, weighted avg
- [ ] **1.9.4** Save: confusion matrix, ROC curves (one-vs-rest with AUC), training/validation curves
- [ ] **1.9.5** Save the trained model weights (`.h5` or `.keras`) for later use in FL comparison
- [ ] **1.9.6** Update Table `tab:final_performance` in `main.tex`
- [ ] **1.9.7** Log as `EXP-011` in `Experiment_Log.md`

---

### 1.10 Ablation Study

> **Target:** Table `tab:ablation_study` (line 1171)

- [ ] **1.10.1** Run five ablation experiments, each removing ONE pipeline component:
  - Full pipeline → remove dynamic labeling (use 30-day static instead)
  - Full pipeline → remove post-failure windows
  - Full pipeline → remove class consolidation (use 6 classes)
  - Full pipeline → remove feature selection (use all 87 features)
  - Full pipeline → remove class balancing (baseline weighted loss only)
- [ ] **1.10.2** Also run one baseline: Raw data, no pipeline at all (just imputation + normalization)
- [ ] **1.10.3** Record: accuracy, macro F1, Δ accuracy, Δ macro F1 vs full pipeline
- [ ] **1.10.4** Update Table `tab:ablation_study` in `main.tex`

---

## Milestone 2 — Federated Learning Experiments

> **Objective:** Produce FL results demonstrating that federated training achieves competitive performance vs centralized training while preserving data privacy. This is the **core contribution** of the paper and currently has **zero results in the article**.

---

### 2.1 FL Infrastructure Setup

- [ ] **2.1.1** Choose FL implementation approach:
  - **Option A (recommended for speed):** Simulated FL — Python loop: partition data by turbine → train local models → average weights with `model.get_weights()` / `model.set_weights()`
  - **Option B:** Flower framework (`flwr`) with strategy server and client classes
  - **Option C:** Docker Compose (as described in article), most realistic but slowest
- [ ] **2.1.2** Create a new notebook: `NoteBooks/Article_level_FL_Training.ipynb`
- [ ] **2.1.3** Implement the FL training loop:
  - Data partitioning: split by `Turbine_ID` → 3 training clients (T01, T06, T07) + 1 evaluation turbine (T11)
  - Each client applies the full data-centric pipeline locally on its own data
  - Server initializes global model (Xavier init, seed=42)
  - Per-round: broadcast weights → local training (E=5 local epochs) → collect weight updates → aggregate → evaluate global model on T11

---

### 2.2 FedAvg Experiments

- [ ] **2.2.1** Implement FedAvg aggregation: `ω_global = Σ (n_k / Σn_j) · ω_k`
- [ ] **2.2.2** Run for 30 federated rounds, recording per round:
  - Global model accuracy on T11
  - Global model macro F1 on T11
  - Per-client local validation loss
- [ ] **2.2.3** Save: convergence curve (accuracy vs round), final confusion matrix, final ROC curves
- [ ] **2.2.4** Log as `EXP-012` in `Experiment_Log.md`

---

### 2.3 FedProx Experiments

- [ ] **2.3.1** Implement FedProx: `L_prox = L_local + (μ/2) · ||ω_local − ω_global||²` with μ=0.1
- [ ] **2.3.2** Run for 30 federated rounds with same evaluation protocol
- [ ] **2.3.3** Save same artifacts as 2.2.3
- [ ] **2.3.4** Log as `EXP-013` in `Experiment_Log.md`

---

### 2.4 Three-Model Comparison (Critical)

> The most important FL experiment — demonstrates the value of federated learning.

- [ ] **2.4.1** **Centralized model:** Train on T01+T06+T07 combined data → evaluate on T11 (reuse model from 1.9)
- [ ] **2.4.2** **Per-client local models:** Train 3 separate models (one per turbine: T01, T06, T07) → evaluate each on T11
- [ ] **2.4.3** **Global federated model:** Best FL model from 2.2 or 2.3 → evaluate on T11
- [ ] **2.4.4** Build comparison table:

  | Model | Accuracy | Macro F1 | Gearbox | Transformer | Generator | Hydraulic |
  |---|---|---|---|---|---|---|
  | Centralized | | | | | | |
  | Per-client T01 | | | | | | |
  | Per-client T06 | | | | | | |
  | Per-client T07 | | | | | | |
  | Federated (FedAvg) | | | | | | |
  | Federated (FedProx) | | | | | | |

- [ ] **2.4.5** Generate a bar chart comparing the three model types across macro F1

---

### 2.5 Per-Client Data Heterogeneity Analysis

- [ ] **2.5.1** For each client (T01, T06, T07), calculate and visualize:
  - Class distribution bar chart per turbine
  - Number of failure events per component
  - Total samples in train set
- [ ] **2.5.2** Compute non-IID degree (e.g., Jensen-Shannon divergence between class distributions)
- [ ] **2.5.3** Show how non-IID data affects per-client contribution to the global model

---

### 2.6 FL Results Integration into Article

- [ ] **2.6.1** Write a new subsection in `main.tex` under Section 3:
  - `\subsection{Federated Learning Evaluation}`
  - `\subsubsection{FedAvg vs FedProx Comparison}`
  - `\subsubsection{Centralized vs Per-Client vs Federated Comparison}`
  - `\subsubsection{Per-Client Data Heterogeneity and Contribution}`
  - `\subsubsection{Communication Efficiency Analysis}`
- [ ] **2.6.2** Add tables, figures, and interpretation text for each subsection
- [ ] **2.6.3** Reference these results from the Discussion and Conclusion sections

---

## Milestone 3 — Completing the Article Writing

> **Objective:** Write all missing sections, fix all placeholder content, produce a complete journal-ready manuscript.

---

### 3.1 Abstract

- [ ] **3.1.1** Replace the placeholder `"This paper presents..."` (line 21) with a structured abstract:
  - **Context** (1 sentence): Wind turbine PdM challenges
  - **Problem** (1 sentence): Data quality + privacy + class imbalance
  - **Approach** (2 sentences): DCFL framework with data-centric pipeline + federated learning
  - **Results** (2–3 sentences): Key numbers from centralized and FL experiments
  - **Impact** (1 sentence): Practical significance
- [ ] **3.1.2** Keep ≤250 words

---

### 3.2 Introduction — Full Rewrite

> Currently only a single "Problem Statement" paragraph. Needs complete expansion.

- [ ] **3.2.1** Write **Motivation and Context** (~2 paragraphs):
  - Global wind energy growth + maintenance cost statistics
  - Why PdM matters: unplanned downtime costs, condition-based vs time-based maintenance
  - SCADA data as the enabler for data-driven PdM
- [ ] **3.2.2** Write **Literature Review** (~4–5 paragraphs):
  - Model-centric PdM: CNN, LSTM, BiLSTM, Transformer-based approaches (cite 5–8 papers)
  - Federated learning for industrial IoT: FedAvg, FedProx, privacy-preserving ML (cite 4–5 papers)
  - Data-centric AI: Andrew Ng's paradigm, data quality for SCADA, labeling strategies (cite 3–4 papers)
  - SCADA-based WT datasets: EDP and other public datasets (cite 2–3 papers)
- [ ] **3.2.3** Write **Research Gap** (~1 paragraph):
  - No existing work combines data-centric pipeline + federated learning for WT PdM
- [ ] **3.2.4** Write **Contributions** (bulleted list, 3–5 items)
- [ ] **3.2.5** Write **Paper Organization** (1 short paragraph)

---

### 3.3 Discussion Section — New

> Entirely missing. Must be added between Results and Conclusion.

- [ ] **3.3.1** Write `\section{Discussion}` covering:
  - **Interpretation of DC results:** Why does each pipeline component contribute what it does?
  - **Federated vs Centralized trade-offs:** Performance gap analysis, non-IID impact
  - **Comparison with literature:** Position results against cited work
  - **Scalability and generalizability:** Would this work with 50+ turbines?
  - **Limitations:** Only 4 turbines, 21 failures, simulated FL, single dataset, TimeGAN quality

---

### 3.4 Conclusion and Future Work — Rewrite

> Currently a one-line placeholder (line 1207).

- [ ] **3.4.1** Write **Conclusion** (~2 paragraphs):
  - Restate problem + approach, summarize 4 key findings with numbers, state broader impact
- [ ] **3.4.2** Write **Future Work** (~1–2 paragraphs):
  - SCAFFOLD, FedNova, FedMA aggregation strategies
  - Differential privacy with formal ε-δ analysis
  - Real-time streaming FL, cross-dataset validation
  - Edge deployment benchmarking

---

### 3.5 References — Complete Overhaul

> Currently broken: one inline `\bibitem{1}`, no `.bib` file.

- [ ] **3.5.1** Create `DCFL_Article/references.bib` with proper BibTeX entries
- [ ] **3.5.2** Include minimum 25–30 references:
  - Wind turbine PdM (≥5), SCADA data processing (≥3), DL for time-series (≥5), Federated learning (≥5), Data-centric AI (≥3), TimeGAN (≥2), EDP dataset (≥2)
- [ ] **3.5.3** Replace all `\cite{1}` references in `main.tex` with proper citation keys
- [ ] **3.5.4** Add `\cite{}` commands in the Introduction literature review
- [ ] **3.5.5** Fix the duplicate `\usepackage{natbib}` (lines 7–8)
- [ ] **3.5.6** Verify `\bibliographystyle{plainnat}` compiles with all entries

---

### 3.6 Figures and Visualizations — Audit and Fix

- [ ] **3.6.1** Verify every `\includegraphics` path points to an actual file
- [ ] **3.6.2** Replace the placeholder DC Pipeline figure (line 144, caption says "exemplaire to be replaced")
- [ ] **3.6.3** Create missing figures:
  - Feature importance bar chart
  - Labeling strategies comparison (side-by-side class distributions)
  - FL convergence curves (accuracy + loss vs round)
  - Three-model comparison bar chart
  - Per-client class distribution (T01, T06, T07)
- [ ] **3.6.4** Fix all `\label{fig:placeholder}` markers (lines 69, 146, 306, 607) with unique labels

---

### 3.7 LaTeX Quality and Consistency

- [ ] **3.7.1** Remove or decide on all commented-out sections (keep, rewrite, or delete)
- [ ] **3.7.2** Fix grammar/spelling in Problem Statement (line 28): "cuz" → "because", "luck" → "lack", "complexe" → "complex"
- [ ] **3.7.3** Ensure consistent terminology:
  - "data-centric" style consistent, "1DCNN-BiLSTM" used everywhere (not "CNN-BLSTM")
  - Class numbering: after consolidation, classes are 0–4 (not 0–5)
- [ ] **3.7.4** Ensure all tables and figures are referenced in the text
- [ ] **3.7.5** Full LaTeX compilation — resolve all warnings and errors
- [ ] **3.7.6** Final proofread for flow, coherence, and academic tone

---

## Milestone 4 — Literature Review Google Sheet

> **Objective:** A structured spreadsheet cataloguing all articles relevant to the PhD subject.

- [ ] **4.1** Create a Google Sheet with columns: Title | Authors | Year | Venue | Dataset | Method | Key Contribution | Relevance to DCFL | Reading Status | Notes
- [ ] **4.2** Populate with all papers cited in the article (≥25 papers from 3.5)
- [ ] **4.3** Add 5–10 additional papers discovered during the literature review
- [ ] **4.4** Mark reading status: ✅ Read | 🟡 Skimmed | ❌ Not read
- [ ] **4.5** For each read paper, write 2–3 sentences of notes

---

## Milestone 5 — Research Gap Definition

> **Objective:** A clear, concise standalone document for the PhD committee.

- [ ] **5.1** Write a 1-page document:
  - **What exists:** Summary of current approaches (model-centric PdM, FL for IoT, data-centric AI)
  - **What is missing:** No framework combining DC optimization + FL for WT PdM
  - **How your work fills it:** DCFL framework with systematic ablation
  - **Why it matters:** Industrial deployment, privacy, rare failure detection
- [ ] **5.2** Include a gap visualization (Venn diagram or matrix)

---

## Milestone 6 — Presentation (15–20 Minutes)

> **Objective:** A clear, visually compelling slide deck for the PhD advancement committee.

### 6.1 Slide Content

- [ ] **6.1.1** Slide 1 — Title, authors, university logo, date
- [ ] **6.1.2** Slide 2 — Motivation: wind energy growth + WT maintenance costs
- [ ] **6.1.3** Slide 3 — Problem statement: 3 challenges (imbalance, dimensionality, privacy)
- [ ] **6.1.4** Slide 4 — Research gap: what exists vs what is missing (matrix visual)
- [ ] **6.1.5** Slide 5 — Our contribution: DCFL framework (3–4 bullets)
- [ ] **6.1.6** Slide 6 — DCFL architecture overview (use `Overview_DCFL.drawio.png`)
- [ ] **6.1.7** Slide 7 — EDP dataset: 4 turbines, 2 years, 21 failures
- [ ] **6.1.8** Slide 8 — DC pipeline overview (use `DC_Pipeline.png`)
- [ ] **6.1.9** Slide 9 — Temporal labeling comparison result
- [ ] **6.1.10** Slide 10 — Feature selection result (26 features vs baseline)
- [ ] **6.1.11** Slide 11 — Class imbalance mitigation result
- [ ] **6.1.12** Slide 12 — Model architecture diagram
- [ ] **6.1.13** Slide 13 — Ablation study results
- [ ] **6.1.14** Slide 14 — Centralized model final results
- [ ] **6.1.15** Slide 15 — FL results: convergence + centralized vs federated comparison
- [ ] **6.1.16** Slide 16 — Key findings (4 bullets)
- [ ] **6.1.17** Slide 17 — Difficulties encountered
- [ ] **6.1.18** Slide 18 — Next steps / Future work
- [ ] **6.1.19** Slide 19 — Q&A

### 6.2 Design and Polish

- [ ] **6.2.1** Use a clean professional template (PowerPoint or LaTeX Beamer)
- [ ] **6.2.2** Ensure all figures are high-resolution (≥300 DPI)
- [ ] **6.2.3** Slide numbers + university logo in footer

### 6.3 Rehearsal

- [ ] **6.3.1** Dry run the full presentation (time yourself: ~1 min per slide)
- [ ] **6.3.2** Prepare answers to anticipated questions:
  - "Why not use a more recent dataset?"
  - "How does FL compare to state-of-the-art centralized models?"
  - "Would this scale to 100+ turbines?"
  - "Why BiLSTM instead of Transformers?"

---

## Milestone 7 — Written Progress Report

> **Objective:** Short document (1–2 pages) synthesizing PhD progress for the committee.

- [ ] **7.1** **Section 1 — Initial Objectives** (~3 sentences): DCFL framework goal, challenges addressed, dataset
- [ ] **7.2** **Section 2 — Current Achievements** (~1 paragraph): DC pipeline, centralized model results, FL prototype, article completion %
- [ ] **7.3** **Section 3 — Key Results** (bulleted list, 3–5 items with concrete numbers)
- [ ] **7.4** **Section 4 — Difficulties Encountered** (~1 paragraph): Model collapse, limited failures, non-IID challenges, compute resources
- [ ] **7.5** **Section 5 — Next Steps** (~1 paragraph): Additional FL strategies, cross-dataset validation, real deployment
- [ ] **7.6** **Section 6 — Points Requiring Guidance** (2–3 bullets): FL scope, target journal, timeline
