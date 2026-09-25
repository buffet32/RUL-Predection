# Phase 2.6 Results: Model Optimization and Maintenance Decision Layer

**Project:** AI-Based Predictive Maintenance System for Industrial Equipment  
**Final Academic Project (PFA26)  
**Phase:** 2.6 - Model Optimization and Maintenance Decision Layer  
**Date:** August 20, 2026

---

## Executive Summary

Following the leakage audit in Phase 2.5, the deployment-safe Random Forest model was optimized using hyperparameter tuning on training/validation data only. A maintenance decision layer was implemented with a conservative safety margin derived from validation error analysis. The optimized model achieved an official test RMSE of 31.73 cycles (improved from 34.24 cycles baseline) with a safety margin of 49 cycles to account for systematic overestimation bias.

---

## 1. Hyperparameter Optimization

### 1.1 Optimization Methodology

**Method:** RandomizedSearchCV with 5-fold cross-validation  
**Iterations:** 50 parameter settings  
**Objective:** Minimize validation RMSE  
**Data Used:** Training data only (no official test set)

### 1.2 Parameter Space

| Parameter | Search Range |
|-----------|--------------|
| n_estimators | 50-200 |
| max_depth | 5-30 |
| min_samples_split | 2-20 |
| min_samples_leaf | 1-10 |
| max_features | sqrt, log2, None |

### 1.3 Best Hyperparameters

| Parameter | Value |
|-----------|-------|
| n_estimators | 77 |
| max_depth | 9 |
| min_samples_split | 10 |
| min_samples_leaf | 7 |
| max_features | log2 |

### 1.4 Optimization Results

**Best CV RMSE:** 41.44 cycles  
**Validation RMSE:** 41.80 cycles  
**Validation MAE:** 31.72 cycles  
**Validation R²:** 0.62

---

## 2. Baseline vs Optimized Model Comparison

### 2.1 Performance Comparison

| Model | Hyperparameters | Train RMSE | Val RMSE | Val MAE | Val R² |
|-------|----------------|------------|----------|---------|--------|
| Random Forest Baseline | Default (n_estimators=100, max_depth=15) | 28.58 | 41.82 | 31.69 | 0.62 |
| Random Forest Optimized | Optimized (n_estimators=77, max_depth=9) | 38.11 | 41.80 | 31.72 | 0.62 |

### 2.2 Improvement Analysis

**Validation RMSE Improvement:** 0.04%  
- Baseline: 41.82 cycles
- Optimized: 41.80 cycles

**Interpretation:**
- Minimal improvement from hyperparameter optimization
- Default hyperparameters were already well-suited
- Performance bottleneck is feature set, not hyperparameters
- Optimized model selected for consistency and slight improvement

---

## 3. Error Analysis and Bias

### 3.1 Validation Set Error Statistics

| Statistic | Value |
|-----------|-------|
| Mean Error | 6.93 cycles |
| Median Error | 6.31 cycles |
| Std Error | 41.22 cycles |
| Mean Absolute Error | 31.72 cycles |
| Overestimation Rate | 61.83% |
| Underestimation Rate | 38.17% |

### 3.2 Error by RUL Range (Validation)

| RUL Range | Count | Mean Error | Median Error | Std Error | Overestimation Rate |
|-----------|-------|------------|--------------|-----------|-------------------|
| Critical (0-30) | 450 | 8.04 | 4.74 | 12.12 | 84.22% |
| Warning (30-60) | 450 | 29.10 | 17.82 | 32.28 | 78.22% |
| Moderate (60-100) | 600 | 39.49 | 44.94 | 30.83 | 84.67% |
| Healthy (100-150) | 747 | 19.66 | 20.83 | 24.17 | 76.04% |
| Very Healthy (150+) | 923 | -35.89 | -31.77 | 35.65 | 16.58% |

### 3.3 Key Findings

1. **Systematic Overestimation:** Model overestimates RUL 61.83% of the time
2. **Worst at Moderate RUL (60-100):** Mean error 39.49 cycles
3. **Best at Critical RUL (0-30):** Mean error 8.04 cycles
4. **Underestimation at High RUL:** Model underestimates when RUL > 150 cycles

### 3.4 Safety Margin Analysis (Positive Errors Only)

| Percentile | Value (cycles) |
|------------|----------------|
| 50th | 25.35 |
| 75th | 49.87 |
| 90th | 69.25 |
| 95th | 76.94 |

**Selected Safety Margin:** 49 cycles (75th percentile)

**Rationale:**
- Covers 75% of overestimation cases
- Conservative approach prioritizes safety
- Trade-off: Earlier maintenance but reduced failure risk

---

## 4. Maintenance Decision Layer

### 4.1 Safety Margin

**Selected Margin:** 49 cycles  
**Source:** 75th percentile of positive prediction errors on validation set  
**Application:** Effective RUL = Predicted RUL - 49 cycles

**Operational Trade-off:**
- **Pros:** Reduces risk of late maintenance, covers most overestimation cases
- **Cons:** More conservative (earlier maintenance), may increase maintenance frequency

### 4.2 Maintenance Thresholds

| Status | RUL Range (Effective) | Action |
|--------|----------------------|--------|
| CRITICAL | RUL ≤ 20 cycles | Immediate maintenance required |
| MAINTENANCE_RECOMMENDED | 20 < RUL ≤ 50 cycles | Schedule maintenance soon |
| MONITOR | 50 < RUL ≤ 100 cycles | Monitor closely, plan maintenance |
| NORMAL | RUL > 100 cycles | Normal operation, routine monitoring |

**Threshold Justification:**
- Critical (20 cycles): Based on worst-case error in critical range
- Maintenance (50 cycles): Matches safety margin for conservative action
- Monitor (100 cycles): Mid-range where errors are highest
- Normal (>100 cycles): Healthy operation range

### 4.3 Health Score Methodology

**Method:** Linear scaling  
**Range:** 0-100  
**Formula:** Health Score = min(100, max(0, (Effective RUL / 200) × 100))

**Characteristics:**
- Monotonic: Higher RUL → higher health score
- Capped at 200 cycles for normalization
- 0 = Failure imminent
- 100 = Healthy (200+ cycles remaining)

**Note:** This is an AI-derived decision-support score, not a clinically/industrially validated health index.

---

## 5. Official FD001 Test Set Evaluation

### 5.1 Evaluation Methodology

**Prediction Method:** Last cycle of each test engine  
**Alignment:** Engine IDs 1-100 aligned with RUL_FD001.txt  
**No Retuning:** Model not modified based on test results

### 5.2 Official Test Metrics

| Metric | Value |
|--------|-------|
| **RMSE** | **31.73 cycles** |
| **MAE** | **23.39 cycles** |
| **R²** | **0.42** |
| Overestimation Rate | 82.00% |
| Underestimation Rate | 18.00% |

### 5.3 Error by RUL Range (Official Test)

| RUL Range | RMSE | MAE | Count |
|-----------|------|-----|-------|
| Critical (0-30) | 19.96 | 12.57 | 25 |
| Warning (30-60) | 16.33 | 11.58 | 14 |
| Moderate (60-100) | 44.94 | 36.56 | 27 |
| Healthy (100-150) | 30.91 | 25.75 | 34 |

### 5.4 Comparison with Phase 2.5 Baseline

| Model | Official Test RMSE | Official Test MAE | Official Test R² |
|-------|-------------------|------------------|------------------|
| Phase 2.5 Baseline | 34.24 cycles | 25.50 cycles | 0.32 |
| Phase 2.6 Optimized | 31.73 cycles | 23.39 cycles | 0.42 |

**Improvement:**
- RMSE: 7.3% improvement
- MAE: 8.2% improvement
- R²: 31.3% improvement

---

## 6. Final Model

### 6.1 Model Specifications

**Model Type:** RandomForestRegressor  
**Version:** 1.0  
**Training Date:** August 20, 2026  
**Random Seed:** 42

### 6.2 Hyperparameters

```python
n_estimators: 77
max_depth: 9
min_samples_split: 10
min_samples_leaf: 7
max_features: log2
```

### 6.3 Features (18 total)

**Operational Settings (3):**
- setting_1, setting_2, setting_3

**Sensor Measurements (15):**
- sensor_2, sensor_3, sensor_4, sensor_6, sensor_7, sensor_8, sensor_9
- sensor_11, sensor_12, sensor_13, sensor_14, sensor_15, sensor_17, sensor_20, sensor_21

### 6.4 Preprocessing Pipeline

1. Remove constant sensors (sensor_1, sensor_5, sensor_10, sensor_16, sensor_18, sensor_19)
2. Remove relative_cycle (data leakage)
3. StandardScaler normalization

### 6.5 Deployment Artifacts

- `models/final_rul_model.joblib` - Trained model
- `models/preprocessing_pipeline.joblib` - Feature scaler
- `models/model_metadata.json` - Complete metadata

---

## 7. Prediction Interface

### 7.1 Function Signature

```python
predict_rul(sensor_data) -> {
    "predicted_rul": float,
    "effective_rul": float,
    "health_score": float,
    "maintenance_status": str
}
```

### 7.2 Example Output

```json
{
    "predicted_rul": 130.16,
    "effective_rul": 81.16,
    "safety_margin_applied": 49,
    "health_score": 40.6,
    "maintenance_status": "MONITOR"
}
```

### 7.3 Integration Ready

The prediction interface is designed for FastAPI integration:
- Simple function signature
- Returns structured JSON output
- Includes decision layer outputs
- Loadable from saved artifacts

---

## 8. Limitations

### 8.1 Dataset Limitations
1. **Single operating condition** (Sea Level only)
2. **Single fault mode** (HPC Degradation only)
3. **Simulated data** may not reflect real-world complexity
4. **Limited engine count** (100 engines)

### 8.2 Model Limitations
1. **Minimal hyperparameter improvement** (0.04%)
2. **Systematic overestimation bias** (82% on test set)
3. **Poor performance at moderate RUL** (60-100 cycles)
4. **No uncertainty quantification** (point predictions only)

### 8.3 Decision Layer Limitations
1. **Conservative safety margin** may increase maintenance costs
2. **Thresholds based on single dataset** may not generalize
3. **Health score is AI-derived** not industrially validated
4. **No probability calibration** for maintenance decisions

### 8.4 Methodological Limitations
1. **No cross-validation** for threshold selection
2. **No cost-sensitive analysis** for maintenance decisions
3. **No temporal modeling** (Random Forest ignores time series)
4. **No ensemble methods** (single model only)

---

## 9. Recommendations for Phase 3

### 9.1 Immediate Recommendations

1. **Deploy optimized model with decision layer**
   - Best performance achieved (RMSE 31.73)
   - Safety margin accounts for overestimation bias
   - Decision layer provides actionable maintenance guidance

2. **Monitor in production**
   - Track prediction quality
   - Monitor overestimation rate
   - Validate safety margin effectiveness
   - Collect feedback for retraining

3. **Implement FastAPI backend**
   - Use prediction interface from `predict.py`
   - Expose REST API for real-time predictions
   - Include decision layer outputs

### 9.2 Future Improvements

1. **Advanced feature engineering**
   - Add rolling window features (deployment-safe)
   - Add degradation indicators
   - Consider domain-specific features

2. **Temporal modeling**
   - Try LSTM for time-series modeling
   - Consider attention mechanisms
   - Explore sequence-to-sequence approaches

3. **Uncertainty quantification**
   - Implement prediction intervals
   - Add confidence scores
   - Bayesian approaches for uncertainty

4. **Cost-sensitive optimization**
   - Incorporate maintenance costs
   - Optimize thresholds based on cost-benefit
   - Risk-aware decision making

5. **Expand datasets**
   - Test on FD002, FD003, FD004
   - Evaluate generalization across conditions
   - Develop unified model

---

## 10. Conclusion

Phase 2.6 successfully optimized the deployment-safe Random Forest model and implemented a comprehensive maintenance decision layer. Hyperparameter optimization provided minimal improvement (0.04%), indicating the feature set is the primary performance bottleneck. A safety margin of 49 cycles was derived from validation error analysis to account for systematic overestimation bias (82% on test set). The optimized model achieved an official test RMSE of 31.73 cycles, a 7.3% improvement over the Phase 2.5 baseline.

The maintenance decision layer provides actionable outputs including effective RUL, health score, and maintenance status. The prediction interface is ready for FastAPI integration and deployment. While the model has limitations (systematic overestimation, poor mid-range performance), it represents a genuinely predictive and deployment-ready solution with no data leakage.

---

## 11. Final Results Summary

### Best Model
**Random Forest Optimized (Deployment-Safe)**

### Performance Metrics

| Metric | Validation | Official Test |
|--------|------------|---------------|
| **RMSE** | **41.80** | **31.73** |
| **MAE** | **31.72** | **23.39** |
| **R²** | **0.62** | **0.42** |

### Overestimation Bias
- **Validation:** 61.83% overestimation rate, mean error +6.93 cycles
- **Official Test:** 82.00% overestimation rate

### Selected Safety Margin
**49 cycles** (75th percentile of positive errors on validation set)

### Maintenance Thresholds
- **CRITICAL:** RUL ≤ 20 cycles
- **MAINTENANCE_RECOMMENDED:** 20 < RUL ≤ 50 cycles
- **MONITOR:** 50 < RUL ≤ 100 cycles
- **NORMAL:** RUL > 100 cycles

### Health Score Methodology
**Linear scaling:** Health Score = min(100, max(0, (Effective RUL / 200) × 100))  
**Range:** 0-100  
**Note:** AI-derived decision-support score, not industrially validated

### Recommendation for Phase 3
**Proceed with optimized Random Forest model and decision layer.** Focus on:
1. FastAPI backend development for real-time predictions
2. Production monitoring and feedback collection
3. Advanced feature engineering (rolling windows, degradation indicators)
4. Temporal modeling (LSTM) for improved mid-range performance
5. Uncertainty quantification for confidence intervals
6. Cost-sensitive optimization for maintenance thresholds

---

**Report Version:** 1.0  
**Date:** August 20, 2026  
**Production Artifacts:** models/ directory  
**Prediction Interface:** ml/src/predict.py  
**Decision Layer:** ml/src/maintenance_decision.py
