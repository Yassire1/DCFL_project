# Dataset Reference — `Artical_level_data_preparation.ipynb` (100 cells)

> Source: EDP open-data wind farm, 2016–2017, 10-min SCADA resolution. All numbers below are committed cell outputs, not estimates.

## 1. Raw inputs (6 files → 3 tables)

| Source file | Years | Content |
|---|---|---|
| `Wind-Turbine-SCADA-signals-2016.xlsx` / `...-2017_0.xlsx` | 2016 + 2017 | Turbine SCADA signals |
| `Onsite-MetMast-SCADA-data-2016.xlsx` / `...-2017.xlsx` | 2016 + 2017 | Met-mast weather data |
| `Historical-Failure-Logbook-2016.xlsx` / `opendata-wind-failures-2017.xlsx` | 2016 + 2017 | Failure logbook |

| Concatenated table | Shape | Columns |
|---|---|---|
| `scada_concat` | ? rows × **83** (`Turbine_ID`, `Timestamp` + 81 signals) | Cell 12 |
| `scada_concat_merged` (SCADA + MetMast, left-merge on `Timestamp`) | ? rows × **123** (+40 met-mast cols) | Cell 17 |
| `failure_concat` | **28 rows** × 4 (`Turbine_ID`, `Component`, `Timestamp`, `Remarks`), 2016-03-03 → 2017-10-19, 5 turbines, 5 components | Cell 15 + Colab summary |

Failure logbook breakdown (28 events): T06-GENERATOR ×5, T09-GENERATOR_BEARING ×4, T11-HYDRAULIC_GROUP ×3, T06/T07/T09-HYDRAULIC_GROUP ×2 each, T07-GENERATOR_BEARING/TRANSFORMER ×2 each, T09-GEARBOX ×2, plus singletons (T01-GEARBOX, T01-TRANSFORMER, T06-GEARBOX, T07-GENERATOR, T09-HYDRAULIC_GROUP, T11-GENERATOR). Turbines with ≥2 failures on one component: T06, T07, T09, T11 (Cell 81).

## 2. Pipeline (cells 7–10, 19, 31–32, 34–35, 49, 51, 59–60, 98)

1. **Load** (`data_load`): `pd.read_excel`, `Timestamp` → datetime, sort by `Turbine_ID, Timestamp`.
2. **Concat** years (`concat_data`): `pd.concat(ignore_index=True)` per table.
3. **Merge** (`merge_data`): SCADA ⟕ MetMast on `Timestamp` (left join).
4. **Label** (`data_labeling`, Cell 19 — source of truth): `Label=0` default; for each failure, stamp `[failure_time − F_window, failure_time]` on that turbine with `component_index = order_of_appearance + 1`. Single `Label` column only. Run with `F_window = 30` and `60` → two datasets.
5. **Clean** (`handle_missing_values`, threshold 0.35): 2,835,408 missing total (met-mast cols ~70,883 each — met-mast starts later; `Gen_Bear_Temp_Avg` 4, `Grd_Prod_CosPhi_Avg` 4). Dropped **0 rows**; per-turbine ffill+bfill → `dropna` → **(417141, 124), 0 missing** (Cell 32).
6. **Downsample** (Cells 34–35): drop Normal samples outside any 8-month pre-failure window → 95,025 removed: **(417141, 84) → (322116, 84)** (note: this branch uses `failure_label` naming, 84-col variant).
7. **Split** (`ts_split`, Cell 49): drop last 2 months (< 2017-11-01, all-Normal, 35,056 rows) → time split test=92d / val=61d.
8. **Knowledge feature selection** (Cell 51): 29 cols = `Timestamp` + `Turbine_ID` + `Label` + **26 features** (19 SCADA + 7 met-mast — see §4).
9. **Statistical selection** (`StatisticalFeatureSelector`, Cells 59–60): 121 → 110 (zero-var) → 105 (low-var) → 105. 5 methods on DecisionTree/F1-weighted (Cell 60).
10. **Post-failure analysis** (`PostFailureAnalyzer`, Cell 98): recovery detected for 17/28 events; component windows + `generate_labels_with_post_failure()` hierarchical fallback (Cell 97–100 per EXP-010).

## 3. Label distributions

**30-day labeled set** (`scada`, 417,141 rows, Cell 24):

| Label | 0 Normal | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Count | 268,559 | 17,245 | 59,885 | 39,295 | 8,810 | 23,347 |
| Share | 64.4% | 4.1% | 14.4% | 9.4% | 2.1% | 5.6% |

**60-day file** (`scada_60`, Cell 60: 417,141 → 382,085 after dropping last 2 months; failure-class counts identical to 30-day in recorded outputs):

| Split | Rows | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|
| Full (–2mo) | 382,085 | 233,503 | 17,245 | 59,885 | 39,295 | 8,810 | 23,347 |
| Train | 294,785 | 199,634 | 8,614 | 31,984 | 30,981 | 8,631 | 14,941 |
| Val | 34,419 | 11,134 | **0** | 10,699 | 5,522 | 179 | 6,885 |
| Test | 52,881 | 22,735 | 8,631 | 17,202 | 2,792 | **0** | 1,521 |

Final shapes for selection: train (294785, 121), val (34419, 121), test (52881, 121). Label mapping = component order of appearance + 1 (Cell 19 code); class 4 has only 179 val / 0 test samples.

**Downsampled 60-day variant** (Cell 35, `failure_label`): 0: 240,877 / 3: 30,189 / 2: 25,006 / 5: 12,886 / 1: 8,641 / 4: 4,517 (322,116 rows).

## 4. Knowledge-based 26 features (Cell 51)

SCADA (19): `Gen_RPM_Avg/Std`, `Gen_Bear_Temp_Avg`, `Gen_Bear2_Temp_Avg`, `Gen_SlipRing_Temp_Avg`, `Gear_Oil_Temp_Avg`, `Gear_Bear_Temp_Avg`, `Hyd_Oil_Temp_Avg`, `Rtr_RPM_Avg/Std`, `Blds_PitchAngle_Avg`, `Prod_LatestAvg_TotActPwr`, `Grd_Prod_Pwr_Std`, `Grd_Prod_VoltPhse1/2/3_Avg`, `Amb_WindSpeed_Avg/Std`, `Nac_Direction_Avg`.
Met-mast (7): `Avg_Windspeed1`, `Var_Windspeed1`, `Avg_Windspeed2`, `Avg_Winddirection2`, `Avg_AmbientTemp`, `Avg_Humidity`, `Avg_Pressure`.

## 5. Statistical selection results (Cell 60, DT + weighted F1)

| Method | Kept | F1 |
|---|---|---|
| Feature importance | 10 | 0.2261 |
| Correlation filter | 24 (thr 0.7) | 0.2058 |
| Mutual information | 80 | 0.2189 |
| **PCA (winner)** | **60 comps** | **0.2268** |
| ICA | 50 | 0.2022 |

## 6. Post-failure recommended windows (Cell 98)

| Component | Analyzed | Mean recovery | Recommended |
|---|---|---|---|
| GEARBOX | 2 | 28.1 h | **48 h** |
| GENERATOR | 4 | 17.4 h | **36 h** |
| GENERATOR_BEARING | 1 | 4.3 h | **12 h** |
| HYDRAULIC_GROUP | 7 | 33.9 h | **72 h** |
| TRANSFORMER | 3 | 41.8 h | **96 h** |

11/28 events had no detectable recovery (all T09 + 2× T06-GENERATOR + T07 2017 events).

## 7. Saved artifacts (`.../artical_level_data_preparation/`)

- `data/scada_labeled_merged_30days.csv`, `data/scada_labeled_merged_60days.csv`
- `data/selected_scada/knowledge_selected_scada_30.csv`, `..._60.csv`
- `data/metadata/scada_class_distribution_8Months_downsamplin_60d.csv`
- `visualizations/`: `TrendAnalysis_T06_<feature>.png` (9 features), distribution plots

## 8. Caveats for continued work

- **T09 exists in SCADA + failure logs but is NOT in the FL partition map** (0→T01, 1→T06, 2→T07, test T11). Decide: exclude or 4th client.
- **Val has 0 samples of class 1; test has 0 of class 4** — per-class metrics for those splits are undefined.
- `Label` (Cells 19–24) vs `failure_label` (Cells 34–42) are two parallel labelings with different column counts (124 vs 84/85) — do not mix.
- 30-day vs 60-day failure-class counts are identical in recorded outputs — verify before citing Table `tab:labeling_results`.
- Time-series analysis (Cells 61–96) is exploratory (T06 GENERATOR trends) — no dataset changes.
- FL CSVs in `flower-WindPrediction/Data/` (`turbine_T{01,06,07,11}_dataset.csv`) are the per-turbine derivatives of this pipeline.
