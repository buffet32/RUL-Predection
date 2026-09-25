# Deployment Features Documentation

**Project:** AI-Based Predictive Maintenance System for Industrial Equipment  
**Phase:** 2.5 - Leakage Audit and Deployment Safety  
**Date:** August 20, 2026

---

## Feature Availability Analysis

This document documents every feature used by the final deployment-safe model and its real-time availability.

---

## Final Model Features

### Model: Random Forest Deployment-Safe

**Total Features:** 18

---

## Feature Table

| Feature | Available in Real Time? | Source | Explanation |
|---------|------------------------|--------|-------------|
| setting_1 | YES | Machine Controller | Operational setting 1 - affects engine performance |
| setting_2 | YES | Machine Controller | Operational setting 2 - affects engine performance |
| setting_3 | YES | Machine Controller | Operational setting 3 - affects engine performance |
| sensor_2 | YES | Sensor | Physical measurement - temperature/pressure related |
| sensor_3 | YES | Sensor | Physical measurement - temperature related |
| sensor_4 | YES | Sensor | Physical measurement - temperature related |
| sensor_6 | YES | Sensor | Physical measurement - pressure/flow related |
| sensor_7 | YES | Sensor | Physical measurement - flow rate |
| sensor_8 | YES | Sensor | Physical measurement - pressure related |
| sensor_9 | YES | Sensor | Physical measurement - pressure related |
| sensor_11 | YES | Sensor | Physical measurement - pressure (most important) |
| sensor_12 | YES | Sensor | Physical measurement - pressure (most important) |
| sensor_13 | YES | Sensor | Physical measurement - pressure related |
| sensor_14 | YES | Sensor | Physical measurement - temperature related |
| sensor_15 | YES | Sensor | Physical measurement - physical quantity |
| sensor_17 | YES | Sensor | Physical measurement - physical quantity |
| sensor_20 | YES | Sensor | Physical measurement - physical quantity |
| sensor_21 | YES | Sensor | Physical measurement - physical quantity |

---

## Excluded Features (Data Leakage)

| Feature | Available in Real Time? | Source | Explanation |
|---------|------------------------|--------|-------------|
| relative_cycle | NO | Future Lifetime | Requires knowledge of engine's maximum lifetime (failure point) - NOT AVAILABLE in deployment |
| max_cycle | NO | Future Lifetime | The actual failure cycle - unknown during operation |
| RUL | NO | Future Lifetime | The target variable - what we're trying to predict |
| engine_id | NO | Identifier | Used only for grouping, not as predictive feature |

---

## Feature Sources in Real Deployment

### Machine Controller
- **Data:** Operational settings (setting_1, setting_2, setting_3)
- **Frequency:** Available at each cycle
- **Latency:** Minimal (controller output)
- **Reliability:** High (controller telemetry)

### Sensors
- **Data:** 15 sensor measurements
- **Frequency:** Available at each cycle
- **Latency:** Minimal (sensor readings)
- **Reliability:** High (industrial-grade sensors)
- **Noise:** Present (as in training data)

---

## Data Flow in Deployment

### Prediction Request
1. **Input:** Current cycle, operational settings, sensor readings
2. **Preprocessing:** Remove constant sensors (already done in model training)
3. **Scaling:** Apply saved StandardScaler
4. **Prediction:** Random Forest model outputs RUL estimate
5. **Output:** Predicted remaining useful life in cycles

### Real-Time Feasibility
- **All features available:** YES
- **No future information required:** YES
- **No engine-specific parameters needed:** YES
- **Scalable to new engines:** YES

---

## Feature Importance (Deployment-Safe Model)

Based on feature importance analysis:

1. **sensor_11** - Pressure measurement (most important)
2. **sensor_12** - Pressure measurement (second most important)
3. **sensor_4** - Temperature measurement
4. **sensor_7** - Flow rate measurement
5. **sensor_2** - Temperature/pressure measurement

**Note:** Without `relative_cycle`, the model must rely on sensor degradation patterns to estimate RUL.

---

## Deployment Checklist

- [x] All features available in real time
- [x] No future information required
- [x] No data leakage
- [x] Model saved with scaler
- [x] Feature list documented
- [x] Prediction pipeline defined
- [x] Evaluation on official test set complete

---

## Preprocessing Pipeline

The deployment preprocessing pipeline includes:

1. **Load sensor data** from machine controller
2. **Remove constant sensors** (sensor_1, sensor_5, sensor_10, sensor_16, sensor_18, sensor_19)
3. **Select features** (18 deployment-safe features)
4. **Apply StandardScaler** (saved from training)
5. **Predict RUL** using Random Forest model

**Saved Artifacts:**
- `models/random_forest_deployment_safe.joblib` - Trained model
- `models/scaler_deployment_safe.joblib` - Feature scaler

---

## Conclusion

All 18 features used by the deployment-safe model are available in real-time from the machine controller and sensors. No future information is required, making the model genuinely predictive and deployment-ready.

**Status:** Deployment-safe model verified for real-time use
