# Leakage Audit Report

**Project:** AI-Based Predictive Maintenance System for Industrial Equipment  
**Phase:** 2.5 - Leakage Audit and Deployment Safety  
**Date:** August 20, 2026

---

## Executive Summary

A critical data leakage issue was identified in the current best model (Random Forest baseline). The `relative_cycle` feature uses future information (maximum engine lifetime) that would not be available during real-world deployment. This feature must be removed and the model retrained with deployment-safe features.

---

## 1. Relative Cycle Audit

### Current Implementation

The `relative_cycle` feature is calculated in `ml/src/preprocessing.py` as follows:

```python
# Calculate max cycle for each engine
max_cycles = df.groupby('engine_id')['cycle'].max().reset_index()
max_cycles.columns = ['engine_id', 'max_cycle']

# Merge back to original dataframe
df = df.merge(max_cycles, on='engine_id')

# Calculate relative cycle
df['relative_cycle'] = df['cycle'] / df['max_cycle']
```

### Formula
```
relative_cycle = current_cycle / maximum_cycle_of_engine
```

### Data Flow
1. For each engine, find the maximum cycle (failure point)
2. For each observation, divide current cycle by the engine's maximum cycle
3. Result: A normalized value from 0.0 (start) to 1.0 (failure)

---

## 2. Deployment Safety Analysis

### Classification: **NOT DEPLOYMENT SAFE**

### Why This is Data Leakage

**Training Scenario:**
- We have complete run-to-failure data for each training engine
- We know exactly when each engine failed (max_cycle)
- We can calculate relative_cycle for every training observation

**Deployment Scenario:**
- We have a running engine in operation
- We do NOT know when this engine will fail
- We do NOT know the maximum lifetime of this engine
- We CANNOT calculate relative_cycle

### The Problem

The `relative_cycle` feature requires knowledge of the future:
- It uses `max_cycle` which is the failure point
- In deployment, the failure point is unknown by definition
- If we knew the failure point, we wouldn't need to predict RUL

### Why This Feature Performed Well

The feature was the most important because it directly encodes the answer:
- `relative_cycle = 1.0` means RUL = 0 (failure imminent)
- `relative_cycle = 0.0` means RUL = max_cycle (engine just started)
- The model essentially learned to map relative_cycle to RUL

This is not prediction - it's a mathematical transformation of the target.

---

## 3. Impact on Model Performance

### Current Model Performance (with relative_cycle)
- Validation RMSE: 25.47 cycles
- Validation MAE: 18.67 cycles
- Validation R²: 0.86

### Expected Impact of Removal
- Performance will likely degrade significantly
- The model must now rely on sensor degradation patterns
- This is the correct and honest evaluation of predictive capability

---

## 4. Other Features Audit

### Safe Features (Deployment-Ready)

**Operational Settings:**
- `setting_1`, `setting_2`, `setting_3` - Available from machine controller

**Current Sensor Measurements:**
- `sensor_2`, `sensor_3`, `sensor_4`, `sensor_6`, `sensor_7`, `sensor_8`, `sensor_9`, `sensor_11`, `sensor_12`, `sensor_13`, `sensor_14`, `sensor_15`, `sensor_17`, `sensor_20`, `sensor_21` - Available from sensors

**Current Cycle:**
- `cycle` - Available from machine controller

### Potentially Unsafe Features

**Time-Series Features (if used):**
- Rolling window features - SAFE (use only past data)
- Lag features - SAFE (use only past data)
- Difference features - SAFE (use only past data)
- Degradation features - SAFE (use only past data)

**Note:** The time-series features were not selected due to overfitting, but they are deployment-safe.

---

## 5. Deployment-Safe Feature Set

### Recommended Features

1. **Operational Settings (3 features)**
   - setting_1
   - setting_2
   - setting_3

2. **Sensor Measurements (15 features)**
   - sensor_2, sensor_3, sensor_4, sensor_6, sensor_7, sensor_8, sensor_9
   - sensor_11, sensor_12, sensor_13, sensor_14, sensor_15, sensor_17, sensor_20, sensor_21

3. **Current Cycle (1 feature)**
   - cycle

**Total: 19 features**

### Alternative: Normalized Cycle (Deployment-Safe)

Instead of `relative_cycle`, we could use:
- `cycle_normalized = cycle / training_max_cycle_mean`
- Where `training_max_cycle_mean` is the average maximum cycle from training data
- This provides some normalization without using future information

However, this is not recommended as it assumes all engines have similar lifetimes, which may not be true.

---

## 6. Recommendations

### Immediate Actions

1. **Remove `relative_cycle` from the model**
   - This is a critical data leakage issue
   - The model cannot be deployed with this feature

2. **Retrain Random Forest without `relative_cycle`**
   - Use only deployment-safe features
   - Keep the same train/val/test split for fair comparison
   - Evaluate the performance degradation

3. **Document the feature set**
   - Create DEPLOYMENT_FEATURES.md
   - List all features and their real-time availability
   - Ensure no future information is used

### Long-term Considerations

1. **Feature Engineering**
   - Focus on sensor degradation patterns
   - Use rolling statistics (deployment-safe)
   - Consider domain-specific health indicators

2. **Model Evaluation**
   - The honest performance may be lower
   - This is the true predictive capability
   - Do not artificially inflate metrics with leakage

3. **Deployment Monitoring**
   - Monitor prediction quality in production
   - Track feature availability and quality
   - Implement drift detection

---

## 7. Conclusion

The current best model uses a feature (`relative_cycle`) that is **NOT deployment-safe**. This feature requires knowledge of the engine's future maximum lifetime, which is unknown during real-world operation. The model must be retrained without this feature to ensure genuine predictive capability and safe deployment.

**Status:** Critical issue found - model not deployment-ready  
**Action Required:** Retrain model with deployment-safe features  
**Expected Outcome:** Lower but honest performance metrics
