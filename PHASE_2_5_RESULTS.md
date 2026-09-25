# Phase 2.5 Results: Leakage Audit and Official FD001 Evaluation

**Project:** AI-Based Predictive Maintenance System for Industrial Equipment  
**Final Academic Project (PFA26)  
**Phase:** 2.5 - Leakage Audit and Deployment Safety  
**Date:** August 20, 2026

---

## Executive Summary

A critical data leakage issue was identified in the Phase 2 best model. The `relative_cycle` feature used future information (maximum engine lifetime) that would not be available during real-world deployment. After removing this feature and retraining with deployment-safe features, the model's validation RMSE increased from 25.47 to 41.82 cycles (64.2% degradation). This represents the honest predictive capability without data leakage. The deployment-safe model achieved an official test RMSE of 34.24 cycles on the FD001 test set.

---

## 1. Leakage Audit

### 1.1 Relative Cycle Analysis

**Current Implementation:**
```python
relative_cycle = current_cycle / maximum_cycle_of_engine
```

**Classification:** **NOT DEPLOYMENT SAFE**

**Why This is Data Leakage:**
- Requires knowledge of the engine's future maximum lifetime (failure point)
- In deployment, the failure point is unknown by definition
- If we knew the failure point, we wouldn't need to predict RUL
- The feature essentially encodes the answer, not predictive information

**Impact:**
- This was the most important feature in the original model
- The model learned to map relative_cycle to RUL rather than predicting from sensor degradation
- Performance was artificially inflated by this leakage

### 1.2 Other Features Audit

**Safe Features (Deployment-Ready):**
- Operational settings (setting_1, setting_2, setting_3)
- Sensor measurements (15 non-constant sensors)
- Current cycle

**Unsafe Features:**
- relative_cycle - REQUIRES FUTURE INFORMATION
- max_cycle - REQUIRES FUTURE INFORMATION
- RUL - TARGET VARIABLE

---

## 2. Deployment-Safe Feature Set

### 2.1 Selected Features

**Total Features:** 18

1. **Operational Settings (3):**
   - setting_1, setting_2, setting_3

2. **Sensor Measurements (15):**
   - sensor_2, sensor_3, sensor_4, sensor_6, sensor_7, sensor_8, sensor_9
   - sensor_11, sensor_12, sensor_13, sensor_14, sensor_15, sensor_17, sensor_20, sensor_21

3. **Current Cycle (1):**
   - cycle

### 2.2 Real-Time Availability

All 18 features are available in real-time from:
- Machine controller (operational settings, cycle)
- Sensors (sensor measurements)

No future information required.

---

## 3. Model Comparison

### 3.1 Performance Comparison

| Model | Relative Cycle | Deployment Safe | Val RMSE | Val MAE | Val R² | Test RMSE | Test MAE | Test R² |
|-------|----------------|-----------------|----------|---------|--------|-----------|----------|---------|
| Random Forest (Original) | YES (DATA LEAKAGE) | NO | 25.47 | 18.67 | 0.86 | 32.03 | 22.11 | 0.80 |
| Random Forest (Deployment-Safe) | NO | YES | 41.82 | 31.69 | 0.62 | 45.74 | 33.52 | 0.58 |

### 3.2 Performance Analysis

**Validation RMSE Degradation:** 64.2%
- Original: 25.47 cycles
- Deployment-Safe: 41.82 cycles

**Interpretation:**
- The performance degradation is expected and honest
- The original model used relative_cycle which encodes the answer
- The deployment-safe model must rely on sensor degradation patterns
- This is the true predictive capability without data leakage

### 3.3 Overfitting Analysis

| Model | Train RMSE | Val RMSE | Overfitting Ratio |
|-------|------------|----------|-------------------|
| Original | 18.12 | 25.47 | 1.41 |
| Deployment-Safe | 28.58 | 41.82 | 1.46 |

Both models show similar overfitting ratios, indicating the degradation is due to feature removal, not overfitting.

---

## 4. Official FD001 Test Set Evaluation

### 4.1 Evaluation Methodology

**Prediction Method:**
- For each test engine, use the LAST cycle of sensor data
- Apply the deployment-safe model to predict RUL
- Compare with ground truth from RUL_FD001.txt
- Engine IDs aligned 1-to-1 with RUL file

**Important:**
- The official test set was NOT used during model development
- No retraining or tuning based on test results
- This represents true generalization performance

### 4.2 Official Test Metrics

| Metric | Value |
|--------|-------|
| **RMSE** | **34.24 cycles** |
| **MAE** | **25.50 cycles** |
| **R²** | **0.32** |

### 4.3 Error Analysis by RUL Range

| RUL Range | RMSE | MAE | Count |
|-----------|------|-----|-------|
| Critical (0-30) | 17.43 | 11.02 | 25 |
| Warning (30-60) | 15.13 | 10.42 | 14 |
| Moderate (60-100) | 48.38 | 40.64 | 27 |
| Healthy (100-150) | 35.66 | 30.33 | 34 |

**Key Observations:**
- **Best performance** at low RUL (0-60 cycles) - RMSE ~16 cycles
- **Worst performance** at moderate RUL (60-100 cycles) - RMSE ~48 cycles
- Model is more accurate near failure than in mid-life

### 4.4 Worst Performing Engines

Top 10 worst errors:
1. Engine 15: Error = 100.2 cycles (Actual: 83, Predicted: 183.2)
2. Engine 79: Error = 81.2 cycles (Actual: 63, Predicted: 144.2)
3. Engine 78: Error = 78.0 cycles (Actual: 107, Predicted: 185.0)
4. Engine 67: Error = 77.4 cycles (Actual: 77, Predicted: 154.4)
5. Engine 27: Error = 74.9 cycles (Actual: 66, Predicted: 140.9)

**Pattern:** Model tends to overestimate RUL (predict more remaining life than actual)

---

## 5. Final Feature List

### 5.1 Deployment-Safe Features

| Feature | Source | Real-Time Available |
|---------|--------|---------------------|
| setting_1 | Machine Controller | YES |
| setting_2 | Machine Controller | YES |
| setting_3 | Machine Controller | YES |
| sensor_2 | Sensor | YES |
| sensor_3 | Sensor | YES |
| sensor_4 | Sensor | YES |
| sensor_6 | Sensor | YES |
| sensor_7 | Sensor | YES |
| sensor_8 | Sensor | YES |
| sensor_9 | Sensor | YES |
| sensor_11 | Sensor | YES |
| sensor_12 | Sensor | YES |
| sensor_13 | Sensor | YES |
| sensor_14 | Sensor | YES |
| sensor_15 | Sensor | YES |
| sensor_17 | Sensor | YES |
| sensor_20 | Sensor | YES |
| sensor_21 | Sensor | YES |

### 5.2 Feature Importance (Deployment-Safe Model)

Based on feature importance analysis:
1. sensor_11 (pressure measurement)
2. sensor_12 (pressure measurement)
3. sensor_4 (temperature measurement)
4. sensor_7 (flow rate measurement)
5. sensor_2 (temperature/pressure measurement)

---

## 6. Final Model Selection

### 6.1 Selection Criteria

The model was selected based on:
1. **No leakage** - PASSED (relative_cycle removed)
2. **Real-time availability** - PASSED (all 18 features available)
3. **Validation performance** - RMSE 41.82 (honest performance)
4. **Internal test performance** - RMSE 45.74
5. **Official test performance** - RMSE 34.24
6. **Model stability** - Consistent overfitting ratio (1.46)
7. **Interpretability** - Random Forest provides feature importance
8. **Deployment feasibility** - All features real-time available

### 6.2 Selected Model

**Model:** Random Forest Deployment-Safe

**Reasons:**
- Only model with no data leakage
- All features available in real-time
- Reasonable performance given constraints
- Interpretable feature importance
- Stable training behavior

**Saved Artifacts:**
- `models/final_rul_model.joblib` - Trained model
- `models/preprocessing_pipeline.joblib` - Feature scaler

---

## 7. Error Analysis

### 7.1 Error Patterns

**Systematic Bias:**
- Model tends to overestimate RUL (predict more remaining life than actual)
- Average error: +2.5 cycles (predicted - actual)
- Suggests model is conservative (predicts failure later than actual)

**RUL Range Performance:**
- **Critical (0-30 cycles):** Best performance (RMSE 17.43)
- **Warning (30-60 cycles):** Good performance (RMSE 15.13)
- **Moderate (60-100 cycles):** Poor performance (RMSE 48.38)
- **Healthy (100+ cycles):** Moderate performance (RMSE 35.66)

**Interpretation:**
- Model is most accurate near failure (critical for maintenance)
- Model struggles with mid-life predictions
- Early-life predictions are moderately accurate

### 7.2 Main Failure Modes

1. **Overestimation at moderate RUL (60-100 cycles)**
   - Model predicts ~40-80 cycles more than actual
   - Could lead to delayed maintenance
   - Most concerning failure mode

2. **Engine-specific errors**
   - Some engines consistently over/under predicted
   - Suggests engine-to-engine variability not captured
   - May need engine-specific calibration

3. **Mid-life uncertainty**
   - Poor performance at 60-100 cycles
   - Degradation patterns may be non-linear
   - May need more sophisticated features

---

## 8. Limitations

### 8.1 Dataset Limitations
1. **Single operating condition** (Sea Level only)
2. **Single fault mode** (HPC Degradation only)
3. **Simulated data** may not reflect real-world complexity
4. **Limited engine count** (100 engines)

### 8.2 Model Limitations
1. **No hyperparameter tuning** - Default parameters used
2. **No feature selection** - All 18 features used
3. **No ensemble methods** - Single model only
4. **No temporal modeling** - Random Forest ignores time series nature

### 8.3 Methodological Limitations
1. **No cross-validation** - Single train/val/test split
2. **No rolling window features** - Could improve temporal modeling
3. **No domain knowledge integration** - Purely data-driven
4. **No uncertainty quantification** - Point predictions only

---

## 9. Comparison with Literature

### 9.1 C-MAPSS FD001 Benchmarks

Typical RMSE values for FD001 (from literature):
- **Linear Regression:** ~40-50 cycles
- **Random Forest:** ~30-40 cycles
- **LSTM:** ~20-30 cycles
- **CNN-LSTM:** ~15-25 cycles

### 9.2 Our Performance

**Official Test RMSE:** 34.24 cycles

**Comparison:**
- Our deployment-safe model is comparable to basic Random Forest benchmarks
- Performance is lower than state-of-the-art deep learning approaches
- However, our model is deployment-safe (no leakage)
- Many published results may use features with leakage

---

## 10. Recommendations for Phase 3

### 10.1 Immediate Recommendations

1. **Use deployment-safe model for production**
   - Only model with no data leakage
   - All features real-time available
   - Reasonable performance (RMSE 34.24)

2. **Implement safety margins**
   - Model tends to overestimate RUL
   - Apply conservative margin (e.g., subtract 20% from prediction)
   - Prioritize early maintenance over late predictions

3. **Monitor in production**
   - Track prediction quality
   - Monitor for drift
   - Collect feedback for retraining

### 10.2 Future Improvements

1. **Hyperparameter tuning**
   - Optimize Random Forest parameters
   - Target validation RMSE < 40 cycles
   - Use cross-validation for robust tuning

2. **Feature engineering**
   - Add rolling window features (deployment-safe)
   - Add degradation indicators
   - Consider domain-specific features

3. **Advanced models**
   - Try LSTM for temporal modeling
   - Consider ensemble methods
   - Explore attention mechanisms

4. **Expand datasets**
   - Test on FD002, FD003, FD004
   - Evaluate generalization across conditions
   - Develop unified model

---

## 11. Conclusion

The leakage audit revealed a critical data leakage issue in the Phase 2 best model. The `relative_cycle` feature required future information (maximum engine lifetime) that would not be available during deployment. After removing this feature and retraining with deployment-safe features, the model's validation RMSE increased from 25.47 to 41.82 cycles (64.2% degradation). This represents the honest predictive capability without data leakage.

The deployment-safe model achieved an official test RMSE of 34.24 cycles on the FD001 test set. While this performance is lower than the leaked model, it is the genuine predictive capability and is deployment-ready. The model is most accurate near failure (RMSE 17.43 at 0-30 cycles) and tends to overestimate RUL at moderate ranges (60-100 cycles).

**Final Model:** Random Forest Deployment-Safe  
**Official Test RMSE:** 34.24 cycles  
**Status:** Deployment-ready with no data leakage

---

## 12. Final Results Summary

### Best Model
**Random Forest Deployment-Safe**

### Performance Metrics

| Metric | Validation | Internal Test | Official Test |
|--------|------------|---------------|---------------|
| **RMSE** | **41.82** | **45.74** | **34.24** |
| **MAE** | **31.69** | **33.52** | **25.50** |
| **R²** | **0.62** | **0.58** | **0.32** |

### Most Important Features
1. sensor_11 (pressure measurement)
2. sensor_12 (pressure measurement)
3. sensor_4 (temperature measurement)
4. sensor_7 (flow rate measurement)
5. sensor_2 (temperature/pressure measurement)

### Main Failure Modes/Errors
1. **Overestimation at moderate RUL (60-100 cycles):** Model predicts ~40-80 cycles more than actual
2. **Engine-specific errors:** Some engines consistently over/under predicted
3. **Mid-life uncertainty:** Poor performance at 60-100 cycles (RMSE 48.38)

### Recommendation for Phase 3
**Proceed with deployment-safe Random Forest model.** Focus on:
1. Hyperparameter tuning to improve validation RMSE below 40 cycles
2. Implement safety margins to account for overestimation bias
3. Add rolling window features for temporal modeling
4. Develop deployment pipeline with FastAPI backend
5. Implement monitoring and retraining strategy

---

**Report Version:** 1.0  
**Date:** August 20, 2026  
**Leakage Audit:** LEAKAGE_AUDIT.md  
**Deployment Features:** DEPLOYMENT_FEATURES.md  
**Final Model:** models/final_rul_model.joblib  
**Preprocessing Pipeline:** models/preprocessing_pipeline.joblib
