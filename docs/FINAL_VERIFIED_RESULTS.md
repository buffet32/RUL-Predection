# FINAL VERIFIED RESULTS - Ground Truth from Saved Artifacts

**Project:** AI-Based Predictive Maintenance System for Industrial Equipment  
**Final Academic Project (PFA26)  
**Date:** August 21, 2026  
**Purpose:** Reconcile conflicting documentation numbers with actual saved artifacts

---

## EXECUTIVE SUMMARY

This document contains ONLY values verified directly from the saved model artifacts (JSON files and joblib models). All numbers are cited with their source file. Discrepancies in prior documentation are identified and corrected.

---

## 1. ACTUAL MODEL CONFIGURATION

### 1.1 Model Type and Version
**Source:** `models/model_metadata.json`

```json
{
  "model_type": "RandomForestRegressor",
  "model_version": "1.0",
  "training_date": "2026-08-20T14:50:41.292840",
  "random_seed": 42
}
```

**Status:** ✅ This is the model currently loaded by the backend

---

### 1.2 Final Hyperparameters (ACTUAL SAVED MODEL)
**Source:** `models/model_metadata.json` (Line 31-37)

```json
{
  "hyperparameters": {
    "max_depth": 9,
    "max_features": "log2",
    "min_samples_leaf": 7,
    "min_samples_split": 10,
    "n_estimators": 77
  }
}
```

**Source:** `ml/results/optimization_results.json` (Line 2-8)

```json
{
  "best_params": {
    "max_depth": 9,
    "max_features": "log2",
    "min_samples_leaf": 7,
    "min_samples_split": 10,
    "n_estimators": 77
  }
}
```

**CONFIRMED VALUES:**
- `n_estimators`: **77** (not 200)
- `max_depth`: **9** (not 20)
- `min_samples_split`: **10**
- `min_samples_leaf`: **7**
- `max_features`: **log2**

**❌ INCORRECT IN PRIOR DOCS:**
- "n_estimators=200/max_depth=20 from GridSearchCV" - This was never actually saved to the final model
- These values appear in some documentation but are NOT in the actual saved model

---

### 1.3 Feature Set (18 Features)
**Source:** `models/model_metadata.json` (Line 6-25)

```json
{
  "features": [
    "setting_1", "setting_2", "setting_3",
    "sensor_2", "sensor_3", "sensor_4", "sensor_6", "sensor_7", "sensor_8", "sensor_9",
    "sensor_11", "sensor_12", "sensor_13", "sensor_14", "sensor_15", "sensor_17", "sensor_20", "sensor_21"
  ]
}
```

**Source:** `ml/results/deployment_safe_results.json` (Line 113-132)

```json
{
  "feature_columns": [
    "setting_1", "setting_2", "setting_3",
    "sensor_2", "sensor_3", "sensor_4", "sensor_6", "sensor_7", "sensor_8", "sensor_9",
    "sensor_11", "sensor_12", "sensor_13", "sensor_14", "sensor_15", "sensor_17", "sensor_20", "sensor_21"
  ]
}
```

**CONFIRMED:** 18 features (3 settings + 15 sensors, NO relative_cycle)

---

### 1.4 Preprocessing Steps
**Source:** `models/model_metadata.json` (Line 26-30)

```json
{
  "preprocessing_steps": [
    "Remove constant sensors (sensor_1, sensor_5, sensor_10, sensor_16, sensor_18, sensor_19)",
    "Remove relative_cycle (data leakage)",
    "StandardScaler normalization"
  ]
}
```

**CONFIRMED:** Data leakage check PASSED

---

## 2. PERFORMANCE METRICS (VERIFIED)

### 2.1 Validation Metrics
**Source:** `models/model_metadata.json` (Line 38-42)

```json
{
  "validation_metrics": {
    "rmse": 41.79909314910572,
    "mae": 31.717317161940084,
    "r2": 0.6219475869049915
  }
}
```

**Source:** `ml/results/optimization_results.json` (Line 10-14)

```json
{
  "val_metrics": {
    "RMSE": 41.79909314910572,
    "MAE": 31.717317161940084,
    "R2": 0.6219475869049915
  }
}
```

**CONFIRMED VALIDATION METRICS:**
- **RMSE:** **41.80 cycles** (rounded from 41.799...)
- **MAE:** **31.72 cycles** (rounded from 31.717...)
- **R²:** **0.62** (rounded from 0.6219...)

---

### 2.2 Official Test Metrics (FD001)
**Source:** `models/model_metadata.json` (Line 43-47)

```json
{
  "official_test_metrics": {
    "rmse": 31.73480152309101,
    "mae": 23.391017011398937,
    "r2": 0.4168073676727069
  }
}
```

**Source:** `ml/results/optimized_official_test_results.json` (Line 4-8)

```json
{
  "metrics": {
    "RMSE": 31.73480152309101,
    "MAE": 23.391017011398937,
    "R2": 0.4168073676727069
  }
}
```

**CONFIRMED OFFICIAL TEST METRICS:**
- **RMSE:** **31.73 cycles** (rounded from 31.734...)
- **MAE:** **23.39 cycles** (rounded from 23.391...)
- **R²:** **0.42** (rounded from 0.4168...)

**❌ INCORRECT IN PRIOR DOCS:**
- "32.03 cycles" - WRONG (this was from an earlier or different run)
- "32.11 cycles" - WRONG
- "31.95 cycles" - WRONG
- The actual value is **31.73 cycles**

---

### 2.3 Internal Test Metrics (Optimized Model)
**Source:** `ml/results/computed_training_metrics.json` (computed fresh from saved model)

```json
{
  "test_metrics": {
    "RMSE": 45.4106,
    "MAE": 33.2277,
    "R2": 0.5905
  }
}
```

**CONFIRMED INTERNAL TEST METRICS:**
- **RMSE:** **45.41 cycles** (rounded from 45.4106)
- **MAE:** **33.23 cycles** (rounded from 33.2277)
- **R²:** **0.59** (rounded from 0.5905)

**Note:** The baseline model (n_estimators=100, max_depth=15) had internal test RMSE of 45.74, but the optimized model (n_estimators=77, max_depth=9) has 45.41

---

## 3. DATA LEAKAGE VERIFICATION

### 3.1 RMSE Impact of Removing relative_cycle
**Source:** `ml/results/deployment_safe_results.json` (Line 139-141)

**Deployment-Safe Model (NO relative_cycle):**
- Validation RMSE: **41.82 cycles**

**Original Model WITH relative_cycle (from PHASE_2_5_RESULTS.md):**
- Validation RMSE: **25.47 cycles**

**CONFIRMED IMPACT:**
- RMSE increased from **25.47 → 41.82 cycles** (64.2% degradation)
- This is the **CORRECT** value

**❌ INCORRECT IN PRIOR DOCS:**
- "25.47 → 25.63" - This is WRONG, never actually happened
- The correct degradation is 25.47 → 41.82

---

### 3.2 Data Leakage Check
**Source:** `models/model_metadata.json` (Line 63)

```json
{
  "data_leakage_check": "PASSED - No relative_cycle feature used"
}
```

**Source:** `ml/results/deployment_safe_results.json` (Line 154)

```json
{
  "data_leakage_check": "PASSED - No relative_cycle feature"
}
```

**CONFIRMED:** Data leakage check PASSED

---

## 4. BIAS ANALYSIS

### 4.1 Validation Set Error Statistics
**Source:** `ml/results/bias_analysis.json` (Line 1-7)

```json
{
  "mean_error": 6.92991911477406,
  "median_error": 6.314057194491086,
  "std_error": 41.220630867931966,
  "mae": 31.717317161940084,
  "overestimation_rate": 0.6182965299684543,
  "underestimation_rate": 0.38170347003154576
}
```

**CONFIRMED BIAS STATISTICS:**
- **Mean Error:** **6.93 cycles** (model overestimates)
- **Median Error:** **6.31 cycles**
- **Std Error:** **41.22 cycles**
- **MAE:** **31.72 cycles**
- **Overestimation Rate:** **61.83%**
- **Underestimation Rate:** **38.17%**

**Source:** `models/model_metadata.json` (Line 48-50)

```json
{
  "bias_analysis": {
    "mean_error": 6.92991911477406,
    "overestimation_rate": 0.6182965299684543
  }
}
```

---

### 4.2 Safety Margin Analysis
**Source:** `ml/results/bias_analysis.json` (Line 8-13)

```json
{
  "safety_margins": {
    "p50": 25.345565611229874,
    "p75": 49.86773998721253,
    "p90": 69.24876441013424,
    "p95": 76.9441019262576
  }
}
```

**CONFIRMED SAFETY MARGINS:**
- 50th percentile: **25.35 cycles**
- 75th percentile: **49.87 cycles**
- 90th percentile: **69.25 cycles**
- 95th percentile: **76.94 cycles**

---

## 5. DECISION LAYER CONFIGURATION

### 5.1 Safety Margin
**Source:** `ml/results/decision_layer_config.json` (Line 1-9)

```json
{
  "safety_margin_cycles": 49,
  "thresholds": {
    "critical": 20,
    "maintenance": 50,
    "monitor": 100
  },
  "health_score_max_rul": 200
}
```

**Source:** `models/model_metadata.json` (Line 52)

```json
{
  "safety_margin": 49
}
```

**CONFIRMED SAFETY MARGIN:** **49 cycles**

**❌ INCORRECT IN PRIOR DOCS:**
- "32 cycles" - This is WRONG
- The actual saved and used value is **49 cycles**

---

### 5.2 Maintenance Thresholds
**Source:** `ml/results/decision_layer_config.json` (Line 3-7)

```json
{
  "thresholds": {
    "critical": 20,
    "maintenance": 50,
    "monitor": 100
  }
}
```

**CONFIRMED THRESHOLDS:**
- **CRITICAL:** RUL ≤ 20 cycles
- **MAINTENANCE_RECOMMENDED:** 20 < RUL ≤ 50 cycles
- **MONITOR:** 50 < RUL ≤ 100 cycles
- **NORMAL:** RUL > 100 cycles

---

### 5.3 Health Score Configuration
**Source:** `ml/results/decision_layer_config.json` (Line 8)

```json
{
  "health_score_max_rul": 200
}
```

**Source:** `models/model_metadata.json` (Line 58-61)

```json
{
  "health_score": {
    "method": "linear_scaling",
    "max_rul": 200,
    "range": "0-100"
  }
}
```

**CONFIRMED HEALTH SCORE:**
- **Method:** Linear scaling
- **Max RUL for normalization:** 200 cycles
- **Range:** 0-100

---

## 6. BACKEND CONFIGURATION

### 6.1 Model File Paths
**Source:** `backend/app/config.py` (Line 17-20)

```python
MODEL_PATH: str = "models/final_rul_model.joblib"
SCALER_PATH: str = "models/preprocessing_pipeline.joblib"
DECISION_CONFIG_PATH: str = "ml/results/decision_layer_config.json"
```

**CONFIRMED FILES LOADED BY BACKEND:**
- **Model:** `models/final_rul_model.joblib`
- **Scaler:** `models/preprocessing_pipeline.joblib`
- **Decision Config:** `ml/results/decision_layer_config.json`

**Status:** ✅ This is the configuration currently in use by the running backend

---

## 7. TRAINING HISTORY (EXPLAINING DISCREPANCIES)

### 7.1 Multiple Training Runs Identified

Based on the artifacts, there were at least 3 training runs:

**Run 1: Deployment-Safe Baseline**
- File: `ml/results/deployment_safe_results.json`
- Hyperparameters: Default (n_estimators=100, max_depth=15)
- Validation RMSE: 41.82
- Internal Test RMSE: 45.74
- Status: Saved but NOT the final production model

**Run 2: Hyperparameter Optimization**
- File: `ml/results/optimization_results.json`
- Method: RandomizedSearchCV with 50 iterations
- Best Parameters: n_estimators=77, max_depth=9
- Validation RMSE: 41.80 (minimal improvement)
- Status: This became the final production model

**Run 3: Official Test Evaluation**
- File: `ml/results/optimized_official_test_results.json`
- Official Test RMSE: 31.73
- Status: Used the optimized model on official FD001 test set

### 7.2 Why Prior Docs Have Conflicting Numbers

**The discrepancies are due to:**

1. **Draft values from optimization exploration**: Some docs contain intermediate results from GridSearchCV exploration that were never finalized
2. **Baseline vs Optimized confusion**: Some docs report baseline numbers (41.82) while others report optimized numbers (41.80)
3. **Rounding differences**: Some docs show 31.73, others show 31.734... the exact value
4. **Outdated drafts**: Some documentation was written before the final model was selected and saved

---

## 8. CORRECTED SUMMARY (GROUND TRUTH)

### 8.1 Final Model Specifications

| Parameter | Value | Source |
|-----------|-------|--------|
| Model Type | RandomForestRegressor | model_metadata.json |
| Version | 1.0 | model_metadata.json |
| Training Date | 2026-08-20T14:50:41.292840 | model_metadata.json |
| Random Seed | 42 | model_metadata.json |
| n_estimators | **77** | model_metadata.json, optimization_results.json |
| max_depth | **9** | model_metadata.json, optimization_results.json |
| min_samples_split | **10** | model_metadata.json, optimization_results.json |
| min_samples_leaf | **7** | model_metadata.json, optimization_results.json |
| max_features | **log2** | model_metadata.json, optimization_results.json |

---

### 8.2 Performance Metrics

| Metric | Training | Validation | Internal Test | Official Test | Source |
|--------|----------|------------|---------------|---------------|--------|
| **RMSE** | **38.11** | **41.80** | **45.41** | **31.73** | computed_training_metrics.json, model_metadata.json, optimized_official_test_results.json |
| **MAE** | **26.37** | **31.72** | **33.23** | **23.39** | computed_training_metrics.json, model_metadata.json, optimized_official_test_results.json |
| **R²** | **0.69** | **0.62** | **0.59** | **0.42** | computed_training_metrics.json, model_metadata.json, optimized_official_test_results.json |

**Note:** Training metrics were computed fresh from the saved model (not in original JSON)

### 8.3 Overfitting Analysis
**Source:** `ml/results/computed_training_metrics.json`

```json
{
  "overfitting_ratios": {
    "val_ratio": 1.10,
    "test_ratio": 1.19
  }
}
```

**CONFIRMED OVERFITTING RATIOS:**
- **Validation Overfitting Ratio:** 1.10 (val_RMSE / train_RMSE)
- **Test Overfitting Ratio:** 1.19 (test_RMSE / train_RMSE)

**INTERPRETATION:**
- ✅ **Healthy generalization** (ratios < 1.5)
- The model shows minimal overfitting
- Validation and test performance are close to training performance

---

### 8.3 Data Leakage Impact

| Model | relative_cycle | Validation RMSE | Source |
|-------|----------------|-----------------|--------|
| Original (leaked) | YES | 25.47 | PHASE_2_5_RESULTS.md (historical) |
| Deployment-Safe | NO | **41.82** | deployment_safe_results.json |
| Optimized | NO | **41.80** | model_metadata.json, optimization_results.json |

**CONFIRMED:** Removing relative_cycle increased RMSE from 25.47 → 41.82

---

### 8.4 Bias Analysis

| Statistic | Value | Source |
|-----------|-------|--------|
| Mean Error | **6.93 cycles** | bias_analysis.json, model_metadata.json |
| Median Error | **6.31 cycles** | bias_analysis.json |
| Std Error | **41.22 cycles** | bias_analysis.json |
| MAE | **31.72 cycles** | bias_analysis.json |
| Overestimation Rate | **61.83%** | bias_analysis.json, model_metadata.json |
| Underestimation Rate | **38.17%** | bias_analysis.json |

---

### 8.5 Decision Layer

| Parameter | Value | Source |
|-----------|-------|--------|
| Safety Margin | **49 cycles** | decision_layer_config.json, model_metadata.json |
| Critical Threshold | **20 cycles** | decision_layer_config.json, model_metadata.json |
| Maintenance Threshold | **50 cycles** | decision_layer_config.json, model_metadata.json |
| Monitor Threshold | **100 cycles** | decision_layer_config.json, model_metadata.json |
| Health Score Max RUL | **200 cycles** | decision_layer_config.json, model_metadata.json |

---

## 9. INCORRECT VALUES IN PRIOR DOCUMENTATION

The following values from prior documentation are **INCORRECT** and should NOT be used:

### 9.1 Hyperparameters
❌ **INCORRECT:** n_estimators=200, max_depth=20 (from hypothetical GridSearchCV)
✅ **CORRECT:** n_estimators=77, max_depth=9 (from actual saved model)

### 9.2 RMSE Values
❌ **INCORRECT:** 32.03 cycles (from earlier/different run)
❌ **INCORRECT:** 32.11 cycles (from earlier/different run)
❌ **INCORRECT:** 31.95 cycles (from earlier/different run)
❌ **INCORRECT:** 25.47 → 25.63 (relative_cycle removal impact - wrong)
✅ **CORRECT:** 31.73 cycles (actual official test RMSE)
✅ **CORRECT:** 25.47 → 41.82 (actual relative_cycle removal impact)

### 9.3 Safety Margin
❌ **INCORRECT:** 32 cycles (from different analysis or hypothetical)
✅ **CORRECT:** 49 cycles (actual saved value)

### 9.4 Training Metrics
❌ **INCORRECT:** Training RMSE 28.58 cycles (from baseline model n_estimators=100, max_depth=15)
✅ **CORRECT:** Training RMSE 38.11 cycles (from optimized model n_estimators=77, max_depth=9)

### 9.5 Internal Test Metrics
❌ **INCORRECT:** Internal test RMSE 45.74 cycles (from baseline model)
✅ **CORRECT:** Internal test RMSE 45.41 cycles (from optimized model)

---

## 10. TRAINING METRICS FOR OPTIMIZED MODEL

### 10.1 Computed Training Metrics
**Source:** `ml/results/computed_training_metrics.json` (computed fresh from saved model)

**Note:** The optimization results used cross-validation and did not save training metrics. These were computed by loading the saved model and scaler and evaluating on the training set.

```json
{
  "model": "Random Forest Optimized (n_estimators=77, max_depth=9)",
  "train_metrics": {
    "RMSE": 38.1083,
    "MAE": 26.3674,
    "R2": 0.6914
  },
  "val_metrics": {
    "RMSE": 41.7991,
    "MAE": 31.7173,
    "R2": 0.6219
  },
  "test_metrics": {
    "RMSE": 45.4106,
    "MAE": 33.2277,
    "R2": 0.5905
  }
}
```

### 10.2 Overfitting Analysis
**Source:** `ml/results/computed_training_metrics.json`

```json
{
  "overfitting_ratios": {
    "val_ratio": 1.10,
    "test_ratio": 1.19
  }
}
```

**CONFIRMED OVERFITTING RATIOS:**
- **Validation Overfitting Ratio:** 1.10 (val_RMSE / train_RMSE)
- **Test Overfitting Ratio:** 1.19 (test_RMSE / train_RMSE)

**INTERPRETATION:**
- ✅ **Healthy generalization** (ratios < 1.5)
- The model shows minimal overfitting
- Validation and test performance are close to training performance
- This indicates the model generalizes well to unseen engines

**❌ INCORRECT IN PRIOR DOCS:**
- Some docs referenced baseline model training metrics (RMSE: 28.58) which were for n_estimators=100, max_depth=15
- The actual optimized model (n_estimators=77, max_depth=9) has training RMSE of 38.11

---

## 11. EXPLANATION OF RMSE/R2 DISCREPANCY

### 11.1 The Mystery
**Source:** Verified from saved artifacts

| Metric | Validation | Internal Test | Official Test |
|--------|------------|---------------|---------------|
| **RMSE** | 41.80 | 45.41 | **31.73** |
| **R²** | 0.62 | 0.59 | **0.42** |

**Question:** Why is official test RMSE (31.73) LOWER than validation (41.80) and internal test (45.41), while official test R² (0.42) is also LOWER than validation R² (0.62)?

### 11.2 Root Cause: RUL Distribution Differences
**Source:** `ml/results/rul_distribution_analysis.json`

```json
{
  "validation_rul": {
    "mean": 109.11,
    "std": 67.98,
    "min": 0,
    "max": 286,
    "median": 105.00
  },
  "official_test_rul": {
    "mean": 75.52,
    "std": 41.56,
    "min": 7,
    "max": 145,
    "median": 86.00,
    "is_capped": false
  },
  "variance_ratio": 0.37,
  "std_ratio": 0.61
}
```

**KEY FINDINGS:**
- **Validation RUL Range:** 0 to 286 cycles (high variance)
- **Official Test RUL Range:** 7 to 145 cycles (low variance)
- **Variance Ratio:** 0.37 (test set has 37% of validation variance)
- **Std Ratio:** 0.61 (test set has 61% of validation std)

### 11.3 Why This Explains Both RMSE and R²

**Lower RMSE is explained by:**
- Smaller variance in test set → smaller potential for large errors
- Maximum RUL in test set is 145 vs 286 in validation
- Shorter range of values naturally reduces absolute error magnitude

**Lower R² is explained by:**
- R² formula: R² = 1 - (SS_res / SS_tot)
- SS_tot (total sum of squares) is proportional to variance
- When variance is 37% of validation, SS_tot is much smaller
- Even with good absolute errors (low RMSE), the same SS_res yields lower R²
- The model explains less of the already-limited variance

**Mathematical explanation:**
```
R² = 1 - (SS_res / SS_tot)

If SS_tot (variance) is smaller:
- Same SS_res → lower R²
- But smaller variance also → smaller potential errors → lower RMSE
```

### 11.4 Is the Official Test Set Capped?
**Source:** `ml/results/rul_distribution_analysis.json`

**Finding:** The official test set is **NOT capped** in the traditional sense
- Max value: 145 cycles
- Only 1% of values are near the max
- The lower variance is due to the nature of the test engines, not artificial capping

**However:** The test set was designed with engines that fail earlier:
- Training/validation engines: Up to 361 cycles of life
- Official test engines: Only up to 145 cycles of life
- This creates a natural "cap" effect on the test set RUL distribution

### 11.5 Summary
The apparent paradox (lower RMSE but lower R²) is explained by the **significantly different RUL distributions**:
- Validation set has high variance (67.98 std) → higher potential RMSE but higher R² ceiling
- Official test set has low variance (41.56 std) → lower potential RMSE but lower R² ceiling
- This is a known phenomenon in RUL prediction and reflects the test set characteristics, not model performance degradation

---

## 12. FINAL VERIFICATION

### 10.1 Model File Currently in Use
**Backend Configuration:** `backend/app/config.py`
**Model Path:** `models/final_rul_model.joblib`
**Status:** ✅ This is the model loaded by the running backend

### 12.2 Verification Checklist
- ✅ Hyperparameters verified from saved model metadata
- ✅ Performance metrics verified from saved JSON files
- ✅ Training metrics computed fresh from saved model
- ✅ Overfitting ratios computed and verified as healthy
- ✅ Safety margin verified from decision layer config
- ✅ Data leakage check verified as PASSED
- ✅ Feature set verified as 18 features (no relative_cycle)
- ✅ Official test RMSE verified as 31.73 cycles
- ✅ RUL distribution analysis explains RMSE/R² discrepancy

---

## 13. DEFENSE-READY SUMMARY

For your academic defense, use ONLY these verified values:

**Final Model:** Random Forest Optimized (Deployment-Safe)
- n_estimators: 77
- max_depth: 9
- Features: 18 (3 settings + 15 sensors, NO relative_cycle)

**Performance:**
- Training RMSE: 38.11 cycles
- Validation RMSE: 41.80 cycles
- Internal Test RMSE: 45.41 cycles
- Official Test RMSE: 31.73 cycles
- Training R²: 0.69
- Validation R²: 0.62
- Internal Test R²: 0.59
- Official Test R²: 0.42

**Overfitting Analysis:**
- Validation Overfitting Ratio: 1.10 (healthy, < 1.5)
- Test Overfitting Ratio: 1.19 (healthy, < 1.5)
- Interpretation: Minimal overfitting, good generalization

**Decision Layer:**
- Safety Margin: 49 cycles
- Critical Threshold: 20 cycles
- Maintenance Threshold: 50 cycles
- Monitor Threshold: 100 cycles

**Data Leakage:**
- PASSED (relative_cycle removed)
- Performance impact: 25.47 → 41.82 validation RMSE

**Bias:**
- Overestimation Rate: 61.83%
- Mean Error: +6.93 cycles

**RMSE/R² Discrepancy Explanation:**
- Official test RMSE is lower (31.73 vs 41.80) due to lower RUL variance in test set
- Official test R² is lower (0.42 vs 0.62) due to same lower variance (variance ratio: 0.37)
- Test set RUL range: 7-145 cycles (std: 41.56)
- Validation set RUL range: 0-286 cycles (std: 67.98)
- This is a known phenomenon, not model performance degradation

---

**Report Version:** 1.1  
**Date:** August 21, 2026  
**Status:** VERIFIED from actual saved artifacts
**Updates:** Added training metrics computation and RUL distribution analysis
