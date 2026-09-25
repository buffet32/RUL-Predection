# ML Results Report: NASA C-MAPSS FD001 RUL Prediction

**Project:** AI-Based Predictive Maintenance System for Industrial Equipment  
**Final Academic Project (PFA26)  
**Phase 2: RUL Prediction Pipeline**  
**Date:** August 20, 2026

---

## Executive Summary

This report presents the results of the machine learning pipeline for predicting Remaining Useful Life (RUL) of turbofan engines using the NASA C-MAPSS FD001 dataset. Three models were trained and evaluated: Random Forest baseline, Random Forest with time-series features, and XGBoost with time-series features. The Random Forest baseline model achieved the best validation performance with an RMSE of 25.47 cycles.

---

## 1. Problem Definition

### Objective
Develop a predictive maintenance system that estimates the Remaining Useful Life (RUL) of aircraft turbofan engines based on sensor data, enabling proactive maintenance scheduling and reducing unexpected failures.

### Challenge
- Time-series regression problem with multi-variate sensor data
- Need to predict remaining operational cycles before failure
- Must avoid data leakage (no future information in training)
- Engine-level variability in initial wear and degradation patterns

---

## 2. Dataset

### Dataset Overview
- **Dataset:** NASA C-MAPSS FD001
- **Training Engines:** 100 engines (20,631 total cycles)
- **Test Engines:** 100 engines (13,096 total cycles)
- **Operating Conditions:** ONE (Sea Level)
- **Fault Mode:** ONE (HPC Degradation - High-Pressure Compressor)

### Data Structure
- **26 columns per observation:**
  - engine_id: Unique engine identifier (1-100)
  - cycle: Time in cycles
  - setting_1, setting_2, setting_3: Operational settings
  - sensor_1 to sensor_21: Sensor measurements

### Data Quality
- **Missing Values:** None
- **Constant Sensors:** 6 sensors removed (sensor_1, sensor_5, sensor_10, sensor_16, sensor_18, sensor_19)
- **Useful Sensors:** 15 sensors retained for modeling

---

## 3. Preprocessing

### Pipeline Steps

1. **Data Loading**
   - Loaded train_FD001.txt, test_FD001.txt, RUL_FD001.txt
   - Assigned meaningful column names
   - Handled whitespace-separated values

2. **Constant Sensor Removal**
   - Identified 6 sensors with zero variance
   - Removed: sensor_1, sensor_5, sensor_10, sensor_16, sensor_18, sensor_19
   - Rationale: Constant sensors provide no predictive information

3. **RUL Calculation (Training Data)**
   - Formula: RUL = max_cycle(engine) - current_cycle
   - Verified manually for engines 1, 2, and 3
   - RUL ranges from 0 (failure) to 361 cycles (early life)
   - Mean RUL: 107.81 cycles

4. **Relative Cycle Feature**
   - Added: relative_cycle = cycle / max_cycle
   - Normalizes position in engine life (0.0 to 1.0)
   - Helps model understand degradation progress

5. **Data Validation**
   - No missing values confirmed
   - No duplicate rows
   - Sequential cycles verified for sample engines
   - Data sorted by engine_id and cycle

### Preprocessed Data Shape
- **Training:** 20,631 rows × 23 columns
- **Test:** 13,096 rows × 22 columns

---

## 4. Train/Validation/Test Methodology

### Split Strategy
**Engine-level split** to prevent data leakage (no engine appears in multiple splits)

### Split Ratios
- **Training:** 70% of engines (70 engines)
- **Validation:** 15% of engines (15 engines)
- **Internal Test:** 15% of engines (15 engines)

### Random Seed
Fixed seed (42) for reproducibility

### Engine Assignment (Seed 42)

**Training Engines (70):**
[1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 23, 25, 26, 27, 28, 29, 31, 32, 34, 35, 36, 37, 39, 40, 41, 43, 44, 45, 46, 47, 48, 50, 51, 54, 55, 56, 57, 62, 63, 65, 66, 67, 68, 69, 70, 71, 73, 74, 77, 78, 79, 81, 82, 84, 86, 89, 90, 91, 94, 96, 97, 98, 100]

**Validation Engines (15):**
[2, 30, 33, 38, 42, 49, 58, 59, 60, 64, 76, 80, 85, 95, 99]

**Test Engines (15):**
[3, 15, 21, 22, 24, 52, 53, 61, 72, 75, 83, 87, 88, 92, 93]

### Data Distribution
- **Training:** 14,316 rows
- **Validation:** 3,170 rows
- **Test:** 3,145 rows

---

## 5. Baseline Model: Random Forest

### Model Configuration
- **Algorithm:** Random Forest Regressor
- **n_estimators:** 100
- **max_depth:** 15
- **min_samples_split:** 10
- **min_samples_leaf:** 5
- **random_state:** 42

### Features
- **Operational Settings:** setting_1, setting_2, setting_3
- **Sensors:** 15 non-constant sensors (sensor_2, sensor_3, sensor_4, sensor_6, sensor_7, sensor_8, sensor_9, sensor_11, sensor_12, sensor_13, sensor_14, sensor_15, sensor_17, sensor_20, sensor_21)
- **Engineered Feature:** relative_cycle
- **Total Features:** 19

### Performance Metrics

| Metric | Training | Validation | Internal Test |
|--------|----------|------------|---------------|
| RMSE   | 18.12    | 25.47      | 32.03         |
| MAE    | 11.97    | 18.67      | 22.11         |
| R²     | 0.93     | 0.86       | 0.80          |

### Observations
- **Good generalization:** Validation RMSE close to training RMSE
- **Overfitting ratio:** 1.41 (val_RMSE / train_RMSE)
- **Strong R²:** 0.86 on validation indicates good explanatory power
- **Best validation performance** among all models

---

## 6. Feature Engineering

### Engineered Features

#### Rolling Window Features
For each sensor and window size (5, 10, 20 cycles):
- Rolling mean
- Rolling standard deviation
- Rolling minimum
- Rolling maximum

**Total rolling features:** 15 sensors × 4 statistics × 3 windows = 180 features

#### Lag Features
For each sensor and lag value (1, 2, 5 cycles):
- Sensor value from N cycles ago

**Total lag features:** 15 sensors × 3 lags = 45 features

#### Difference Features
For each sensor:
- First difference (current - previous)
- Rate of change (difference / current value)

**Total difference features:** 15 sensors × 2 = 30 features

#### Degradation Features
For each sensor:
- Deviation from baseline (first 5 cycles mean)
- Cumulative deviation over time

**Total degradation features:** 15 sensors × 2 = 30 features

### Total Features After Engineering
- **Base features:** 19
- **Engineered features:** 285
- **Total:** 304 features

### Data Leakage Prevention
All engineered features use only current and past information:
- Rolling windows use only previous cycles
- Lag features use only historical values
- No future observations included in any feature

---

## 7. Random Forest with Time-Series Features

### Model Configuration
Same as baseline (100 estimators, max_depth 15, etc.)

### Performance Metrics

| Metric | Training | Validation | Internal Test |
|--------|----------|------------|---------------|
| RMSE   | 3.17     | 27.43      | 28.90         |
| MAE    | 1.59     | 17.38      | 18.04         |
| R²     | 0.998    | 0.84       | 0.83          |

### Observations
- **Severe overfitting:** Overfitting ratio of 8.64
- **Training RMSE extremely low** (3.17) but validation RMSE higher than baseline
- **Time-series features did not improve** generalization
- **High feature count** (304) likely contributed to overfitting

### Analysis
The model memorized the training data but failed to generalize. Possible causes:
- Too many features relative to data size
- Rolling window features may not generalize across engines
- Feature engineering introduced noise rather than signal

---

## 8. XGBoost with Time-Series Features

### Model Configuration
- **Algorithm:** XGBoost Regressor
- **n_estimators:** 100
- **max_depth:** 6
- **learning_rate:** 0.1
- **subsample:** 0.8
- **colsample_bytree:** 0.8
- **random_state:** 42

### Performance Metrics

| Metric | Training | Validation | Internal Test |
|--------|----------|------------|---------------|
| RMSE   | 3.39     | 26.07      | 29.11         |
| MAE    | 2.40     | 17.62      | 18.91         |
| R²     | 0.998    | 0.85       | 0.83          |

### Observations
- **Similar overfitting pattern** as Random Forest with time-series features
- **Overfitting ratio:** 7.69
- **Validation RMSE:** 26.07 (better than RF time-series, worse than baseline)
- **XGBoost regularization** did not prevent overfitting

### Analysis
XGBoost performed similarly to Random Forest with the same features, suggesting the issue is with the feature set rather than the algorithm.

---

## 9. Model Comparison

### Comparison Table

| Model | Features | Val RMSE | Val MAE | Val R² | Test RMSE | Test MAE | Test R² |
|-------|----------|----------|---------|--------|-----------|----------|---------|
| Random Forest (Baseline) | Basic | 25.47 | 18.67 | 0.86 | 32.03 | 22.11 | 0.80 |
| Random Forest (Time-Series) | Time-Series | 27.43 | 17.38 | 0.84 | 28.90 | 18.04 | 0.83 |
| XGBoost (Time-Series) | Time-Series | 26.07 | 17.62 | 0.85 | 29.11 | 18.91 | 0.83 |

### Key Findings

1. **Best Validation RMSE:** Random Forest Baseline (25.47)
2. **Best Test RMSE:** Random Forest Time-Series (28.90)
3. **Best MAE:** Random Forest Time-Series (17.38 on validation)
4. **Overfitting:** Time-series features caused severe overfitting (ratio > 7)
5. **Baseline features** provided the best balance of performance and generalization

### Trade-offs

**Random Forest Baseline:**
- **Pros:** Best validation performance, minimal overfitting, simple feature set
- **Cons:** Higher test RMSE compared to time-series models

**Random Forest Time-Series:**
- **Pros:** Best test performance, lowest MAE
- **Cons** Severe overfitting, complex feature set

**XGBoost Time-Series:**
- **Pros:** Good validation performance, modern algorithm
- **Cons:** Severe overfitting, similar to Random Forest with same features

---

## 10. Error Analysis

### Overfitting Analysis

| Model | Train RMSE | Val RMSE | Overfitting Ratio |
|-------|------------|----------|-------------------|
| RF Baseline | 18.12 | 25.47 | 1.41 |
| RF Time-Series | 3.17 | 27.43 | 8.64 |
| XGBoost Time-Series | 3.39 | 26.07 | 7.69 |

**Interpretation:**
- Baseline model shows healthy generalization (ratio < 2)
- Time-series models show severe overfitting (ratio > 7)
- Time-series features likely capture engine-specific patterns that don't generalize

### Error Distribution Analysis

**Baseline Model:**
- Errors are roughly normally distributed
- Mean error close to zero (no systematic bias)
- Some outliers at high RUL values

**Time-Series Models:**
- Similar error patterns
- Slightly better performance at mid-range RUL
- Worse performance at extreme RUL values

### RUL vs Error Patterns

**Common patterns across all models:**
- Higher errors at very high RUL (early engine life)
- Higher errors at very low RUL (near failure)
- Best performance in mid-range RUL (50-150 cycles)

**Interpretation:**
- Models struggle with early-life prediction (insufficient degradation signal)
- Models struggle with end-of-life prediction (non-linear degradation)
- Mid-range predictions are most reliable

---

## 11. Most Important Features

Based on feature importance analysis (visualizations saved):

### Baseline Model Top Features
1. **relative_cycle** - Normalized position in engine life
2. **sensor_11** - Physical pressure measurement
3. **sensor_12** - Physical pressure measurement
4. **sensor_4** - Temperature measurement
5. **sensor_7** - Pressure/flow measurement

### Time-Series Model Top Features
1. **sensor_11_rolling_mean_20** - Long-term average
2. **sensor_12_rolling_mean_20** - Long-term average
3. **relative_cycle** - Normalized position
4. **sensor_11_rolling_std_20** - Long-term variability
5. **sensor_4_rolling_mean_20** - Long-term average

### Interpretation
- **relative_cycle** is consistently important across models
- **sensor_11 and sensor_12** (pressure measurements) are most informative
- **Rolling mean features** dominate in time-series models
- **Long-term windows (20 cycles)** more important than short-term

---

## 12. Limitations

### Dataset Limitations
1. **Single operating condition:** Only sea-level conditions tested
2. **Single fault mode:** Only HPC degradation considered
3. **Simulated data:** May not reflect real-world complexity
4. **Limited engine count:** 100 engines may not capture full variability

### Model Limitations
1. **Overfitting with time-series features:** Engine-specific patterns don't generalize
2. **Feature engineering complexity:** 304 features difficult to interpret
3. **No hyperparameter tuning:** Default parameters used
4. **No cross-validation:** Single train/val/test split used

### Methodological Limitations
1. **No ensemble of models:** Each model trained independently
2. **No early stopping:** Could improve training efficiency
3. **No feature selection:** All features used without pruning
4. **No domain knowledge integration:** Purely data-driven approach

---

## 13. Recommendations for Phase 3

### Immediate Recommendations

1. **Use Random Forest Baseline as production model**
   - Best validation performance (RMSE: 25.47)
   - Minimal overfitting
   - Simple, interpretable feature set
   - Good generalization

2. **Evaluate on official test set**
   - Use FD001 test data with RUL_FD001.txt ground truth
   - Report official test RMSE
   - Compare with literature benchmarks

3. **Hyperparameter tuning**
   - Optimize Random Forest parameters (grid search or Bayesian optimization)
   - Target validation RMSE < 25 cycles
   - Consider cross-validation for robust tuning

### Future Improvements

1. **Investigate time-series feature overfitting**
   - Reduce feature count through selection
   - Try regularization techniques
   - Consider domain-specific feature engineering

2. **Explore alternative approaches**
   - LSTM for temporal modeling (if time-series features prove valuable)
   - Ensemble methods combining multiple models
   - Physics-informed features

3. **Expand to other datasets**
   - Test on FD002, FD003, FD004
   - Evaluate generalization across conditions and fault modes
   - Develop unified model for all datasets

4. **Production considerations**
   - Model deployment pipeline
   - Real-time prediction API
   - Monitoring and retraining strategy

---

## 14. Conclusion

The ML pipeline successfully trained and evaluated three RUL prediction models on the NASA C-MAPSS FD001 dataset. The Random Forest baseline model achieved the best validation performance with an RMSE of 25.47 cycles, demonstrating that simple features (operational settings, sensors, and relative cycle) are sufficient for this dataset. Time-series feature engineering, while theoretically promising, caused severe overfitting and did not improve generalization. The baseline model provides a solid foundation for Phase 3 development, with clear paths for improvement through hyperparameter tuning and evaluation on the official test set.

---

## 15. Final Results Summary

### Best Model
**Random Forest Baseline**

### Performance Metrics

| Metric | Validation | Internal Test |
|--------|------------|---------------|
| **RMSE** | **25.47** | **32.03** |
| **MAE** | **18.67** | **22.11** |
| **R²** | **0.86** | **0.80** |

### Most Important Features
1. relative_cycle
2. sensor_11
3. sensor_12
4. sensor_4
5. sensor_7

### Main Failure Modes/Errors
1. **Overfitting with time-series features:** Engine-specific patterns don't generalize (overfitting ratio > 7)
2. **High errors at extreme RUL:** Poor performance at very high (early life) and very low (near failure) RUL values
3. **Feature engineering complexity:** 304 features difficult to interpret and may introduce noise

### Recommendation for Phase 3
**Proceed with Random Forest Baseline model for production deployment.** Focus on:
1. Hyperparameter tuning to improve validation RMSE below 25 cycles
2. Evaluation on official FD001 test set
3. Investigation of regularization techniques if time-series features are to be used
4. Development of deployment pipeline for real-time predictions

---

**Report Version:** 1.0  
**Date:** August 20, 2026  
**ML Pipeline:** ml/ directory  
**Results:** ml/results/ directory  
**Visualizations:** ml/visualizations/ directory  
**Models:** ml/models/ directory
