# NASA C-MAPSS FD001 Dataset Analysis

**Project:** AI-Based Predictive Maintenance System for Industrial Equipment  
**Final Academic Project (PFA26)**  
**Dataset:** NASA C-MAPSS Turbofan Engine Degradation Dataset - FD001

---

## Executive Summary

This document provides a comprehensive analysis of the NASA C-MAPSS FD001 dataset for predictive maintenance modeling. The dataset contains simulated sensor data from turbofan engines operating under a single condition (Sea Level) with one fault mode (HPC Degradation). The analysis covers data structure, sensor characteristics, RUL calculation methodology, data leakage considerations, and recommendations for model development.

---

## 1. Dataset Overview

### 1.1 Dataset Characteristics

- **Dataset ID:** FD001
- **Training Trajectories:** 100 engines
- **Test Trajectories:** 100 engines
- **Operating Conditions:** ONE (Sea Level)
- **Fault Modes:** ONE (HPC Degradation - High-Pressure Compressor)
- **Total Training Cycles:** 20,631
- **Total Test Cycles:** 13,096

### 1.2 Experimental Scenario

The dataset consists of multivariate time series from a fleet of engines of the same type. Each engine:
- Starts with different degrees of initial wear and manufacturing variation (unknown to user)
- Operates normally at the start of each time series
- Develops a fault (HPC degradation) at some point during the series
- In the **training set**: the fault grows in magnitude until system failure
- In the **test set**: the time series ends some time prior to system failure

The data is contaminated with sensor noise, simulating real-world conditions.

---

## 2. Data Structure

### 2.1 File Structure

| File | Description | Shape |
|------|-------------|-------|
| `train_FD001.txt` | Training sensor data | (20,631 × 26) |
| `test_FD001.txt` | Test sensor data | (13,096 × 26) |
| `RUL_FD001.txt` | Ground truth RUL for test engines | (100 × 1) |

### 2.2 Column Descriptions

The data contains 26 columns per row (each row is a snapshot of data during a single operational cycle):

| Column | Name | Description |
|--------|------|-------------|
| 1 | `engine_id` | Unique identifier for each engine (1-100) |
| 2 | `cycle` | Time in cycles (operational time) |
| 3 | `setting_1` | Operational setting 1 (affects engine performance) |
| 4 | `setting_2` | Operational setting 2 (affects engine performance) |
| 5 | `setting_3` | Operational setting 3 (affects engine performance) |
| 6-26 | `sensor_1` to `sensor_21` | Various sensor measurements from engine monitoring |

### 2.3 Data Types

All columns are numeric (float64):
- `engine_id`: Integer (1-100)
- `cycle`: Integer (1-362 for training)
- `setting_1`, `setting_2`, `setting_3`: Float
- `sensor_1` to `sensor_21`: Float

---

## 3. Engine and Cycle Statistics

### 3.1 Training Set

- **Number of Engines:** 100
- **Total Cycles:** 20,631
- **Cycles per Engine:**
  - Minimum: 128 cycles
  - Maximum: 362 cycles
  - Mean: 206.31 cycles
  - Median: 199 cycles

### 3.2 Test Set

- **Number of Engines:** 100
- **Total Cycles:** 13,096
- **Cycles per Engine:**
  - Minimum: 31 cycles
  - Maximum: 303 cycles
  - Mean: 130.96 cycles
  - Median: 126 cycles

### 3.3 RUL Statistics (Test Set)

- **Minimum RUL:** 7 cycles
- **Maximum RUL:** 145 cycles
- **Mean RUL:** 75.52 cycles
- **Median RUL:** 79 cycles

---

## 4. Sensor Analysis

### 4.1 Missing Values

- **Training Set:** No missing values
- **Test Set:** No missing values

### 4.2 Constant Sensors (Zero Variance)

The following sensors have zero standard deviation and provide no useful information:

**Training Set:**
- `sensor_1` (std = 0.00)
- `sensor_5` (std = 0.00)
- `sensor_10` (std = 0.00)
- `sensor_16` (std = 0.00)
- `sensor_18` (std = 0.00)
- `sensor_19` (std = 0.00)

**Test Set:**
- Same 6 sensors are constant (consistent with training)

**Recommendation:** Remove these 6 constant sensors from modeling as they provide no information.

### 4.3 Nearly Constant Sensors (Low Variance)

**Training Set:**
- `sensor_6` (std = 0.0014)

**Test Set:**
- `sensor_6` (std = 0.0017)

**Recommendation:** Consider removing `sensor_6` or using with caution due to very low variance.

### 4.4 Sensor Distribution Statistics (Training Set)

| Sensor | Mean | Std | Min | Max | Skew |
|--------|------|-----|-----|-----|------|
| sensor_1 | 518.67 | 0.00 | 518.67 | 518.67 | 0.00 |
| sensor_2 | 642.68 | 0.50 | 641.21 | 644.53 | 0.32 |
| sensor_3 | 1590.52 | 6.13 | 1571.04 | 1616.91 | 0.31 |
| sensor_4 | 1408.93 | 9.00 | 1382.25 | 1441.49 | 0.44 |
| sensor_5 | 14.62 | 0.00 | 14.62 | 14.62 | -1.00 |
| sensor_6 | 21.61 | 0.00 | 21.60 | 21.61 | -6.92 |
| sensor_7 | 553.37 | 0.89 | 549.85 | 556.06 | -0.39 |
| sensor_8 | 2388.10 | 0.07 | 2387.90 | 2388.56 | 0.48 |
| sensor_9 | 9065.24 | 22.08 | 9021.73 | 9244.59 | 2.56 |
| sensor_10 | 1.30 | 0.00 | 1.30 | 1.30 | 0.00 |
| sensor_11 | 47.54 | 0.27 | 46.85 | 48.53 | 0.47 |
| sensor_12 | 521.41 | 0.74 | 518.69 | 523.38 | -0.44 |
| sensor_13 | 2388.10 | 0.07 | 2387.88 | 2388.56 | 0.47 |
| sensor_14 | 8143.75 | 19.08 | 8099.94 | 8293.72 | 2.37 |
| sensor_15 | 8.44 | 0.04 | 8.32 | 8.58 | 0.39 |
| sensor_16 | 0.03 | 0.00 | 0.03 | 0.03 | 0.00 |
| sensor_17 | 393.21 | 1.55 | 388.00 | 400.00 | 0.35 |
| sensor_18 | 2388.00 | 0.00 | 2388.00 | 2388.00 | 0.00 |
| sensor_19 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| sensor_20 | 38.82 | 0.18 | 38.14 | 39.43 | -0.36 |
| sensor_21 | 23.29 | 0.11 | 22.89 | 23.62 | -0.35 |

**Key Observations:**
- Sensors 9 and 14 show high positive skewness (2.56, 2.37)
- Sensors 6 shows extreme negative skewness (-6.92)
- Most sensors show relatively normal distributions
- Sensor values vary significantly in scale (e.g., sensor_9 ~9065 vs sensor_16 ~0.03)

---

## 5. RUL Calculation Methodology

### 5.1 Training Data RUL Calculation

For the training set, each engine runs until failure. The Remaining Useful Life (RUL) is calculated as:

```
RUL(cycle) = max_cycle(engine) - current_cycle
```

Where:
- `max_cycle(engine)` is the last cycle before failure for that engine
- `current_cycle` is the current operational cycle
- RUL = 0 at the last cycle (failure point)

**Training RUL Statistics:**
- Minimum: 0 cycles (at failure)
- Maximum: 361 cycles (early in engine life)
- Mean: 107.81 cycles

### 5.2 Test Data RUL Usage

For the test set:
- The time series ends BEFORE failure occurs
- `RUL_FD001.txt` provides the true remaining useful life for each test engine
- Each row in `RUL_FD001.txt` corresponds to one test engine (in order)
- The RUL value represents the number of additional cycles the engine would operate after the last recorded cycle

**Usage:**
- Model should predict RUL for the LAST cycle of each test engine
- Compare predictions with `RUL_FD001.txt` ground truth for evaluation

---

## 6. Data Leakage Analysis

### 6.1 Identified Data Leakage Risks

1. **Engine ID Leakage**
   - **Risk:** Using `engine_id` as a feature would leak information about engine-specific patterns
   - **Solution:** Do NOT use `engine_id` as a prediction feature. Use only for grouping during analysis.

2. **Cycle Number Leakage**
   - **Risk:** Direct use of absolute cycle number might leak temporal information
   - **Solution:** Use relative degradation features (e.g., cycle/max_cycle) or use cycle with caution

3. **Future Information in Training**
   - **Risk:** Using future sensor data to predict current RUL
   - **Solution:** Ensure only current and past sensor readings are used for prediction

4. **Test Set Contamination**
   - **Risk:** Same engine appearing in both train and test sets
   - **Status:** FD001 has separate engines (100 train, 100 test) - no contamination

5. **Constant Sensor Leakage**
   - **Risk:** Constant sensors provide no information but add noise
   - **Solution:** Remove 6 constant sensors (1, 5, 10, 16, 18, 19) before modeling

### 6.2 Prevention Strategies

- Remove constant sensors before feature engineering
- Use engine-based splitting for validation (not random cycle splitting)
- Implement GroupKFold cross-validation with `engine_id` as groups
- Normalize/scale sensor features due to varying scales
- Create rolling window features using only past data

---

## 7. Train/Validation/Test Methodology Recommendations

### 7.1 Recommended Approach: Engine-Based Split

For time-series predictive maintenance, split by engines (not cycles) to prevent data leakage:

- **Training Set:** 70% of engines (e.g., engines 1-70)
- **Validation Set:** 15% of engines (e.g., engines 71-85)
- **Test Set:** 15% of engines (e.g., engines 86-100)

**Advantages:**
- Prevents data leakage from same engine
- Simulates real-world scenario (predict for unseen engines)
- More robust model generalization

### 7.2 Alternative: Time-Based Split Within Engines

For each engine:
- Use early cycles (e.g., first 70%) for training
- Use later cycles (e.g., last 30%) for validation

**Advantages:**
- Simulates predicting future from past
- Uses all engine data efficiently

**Disadvantages:**
- Same engine in train/val may cause leakage
- Less realistic for unseen engine prediction

### 7.3 Cross-Validation Strategy

**Recommended:** GroupKFold with `engine_id` as groups
- Ensures same engine doesn't appear in both train and validation folds
- Provides robust performance estimates
- Standard approach for time-series with grouped data

### 7.4 Final Evaluation

- Use the provided test set (FD001 test)
- Compare predictions with `RUL_FD001.txt` ground truth
- Report multiple metrics (RMSE, MAE, accuracy within threshold)

---

## 8. ML Model Recommendations

### 8.1 Baseline Models (Start Here)

1. **Linear Regression**
   - Simple, interpretable baseline
   - Quick to implement
   - Establishes performance floor

2. **Decision Tree**
   - Handles non-linear relationships
   - Interpretable feature importance
   - No feature scaling required

### 8.2 Ensemble Methods (Recommended for Production)

1. **Random Forest**
   - Robust to noise and outliers
   - Handles non-linearities well
   - Provides feature importance
   - Good baseline for tabular sensor data

2. **Gradient Boosting (XGBoost / LightGBM)**
   - State-of-the-art for tabular data
   - Handles sensor correlations effectively
   - Excellent performance on time-series features
   - **Primary recommendation for FD001**

### 8.3 Deep Learning Approaches (For Advanced Modeling)

1. **LSTM / GRU**
   - Captures temporal dependencies
   - Suitable for sequential sensor data
   - Can learn complex degradation patterns

2. **1D CNN**
   - Efficient for time-series patterns
   - Faster training than LSTM
   - Good for local pattern detection

3. **CNN-LSTM Hybrid**
   - Combines spatial (CNN) and temporal (LSTM) features
   - State-of-the-art for many time-series tasks

4. **Transformer**
   - Attention mechanism for long-range dependencies
   - More complex but powerful
   - May be overkill for FD001 (single condition)

### 8.4 Recommendation for FD001

**Phase 1 (Baseline):**
- Start with Random Forest
- Establish performance baseline
- Understand feature importance

**Phase 2 (Optimization):**
- Implement XGBoost or LightGBM
- Tune hyperparameters
- Engineer time-series features

**Phase 3 (Advanced - if needed):**
- Implement LSTM if temporal patterns are critical
- Consider CNN-LSTM hybrid for better performance

**Note:** FD001 is the simplest dataset (single condition, single fault mode). Start with simpler models before moving to deep learning.

---

## 9. Evaluation Metrics Recommendations

### 9.1 Primary Metrics

1. **RMSE (Root Mean Squared Error)**
   - Standard metric for C-MAPSS challenge
   - Penalizes large errors more heavily
   - Sensitive to outliers
   - **Primary recommendation**

2. **MAE (Mean Absolute Error)**
   - Easy to interpret (average cycles error)
   - Less sensitive to outliers
   - Good for business communication
   - **Secondary recommendation**

### 9.2 Specialized Predictive Maintenance Metrics

1. **C-MAPSS Score Function**
   - Asymmetric metric: penalizes late predictions more
   - Formula: `exp(-error/13) - 1` for error < 0
   - Used in original NASA challenge
   - Reflects business cost (late prediction = failure)

2. **Accuracy Within Threshold**
   - Percentage of predictions within ±X cycles
   - Common thresholds: ±20, ±30 cycles
   - Practical for maintenance scheduling

### 9.3 Additional Metrics

1. **R² (R-squared)**
   - Explains variance in predictions
   - Useful for model comparison
   - Less intuitive for business stakeholders

2. **Precision/Recall for Failure Prediction**
   - Convert RUL to binary classification (e.g., RUL < 30 cycles)
   - Useful for maintenance decision-making

### 9.4 Recommended Evaluation Protocol

**Primary:** RMSE (standard for C-MAPSS benchmarking)  
**Secondary:** MAE (for interpretability)  
**Additional:** Accuracy within ±30 cycles (practical relevance)

---

## 10. Feature Engineering Recommendations

### 10.1 Basic Features

- **Remaining sensors only:** Remove 6 constant sensors (1, 5, 10, 16, 18, 19)
- **Operational settings:** Include setting_1, setting_2, setting_3
- **Relative cycle:** `cycle / max_cycle` (normalized position in engine life)

### 10.2 Time-Series Features

- **Rolling statistics:** Mean, std, min, max over windows (e.g., 5, 10, 20 cycles)
- **Lag features:** Sensor values from previous cycles (t-1, t-2, t-5)
- **Differences:** Rate of change between consecutive cycles
- **Trend features:** Slope of sensor values over recent cycles

### 10.3 Degradation Features

- **Sensor deviation from baseline:** Difference from early-life average
- **Cumulative degradation:** Sum of deviations over time
- **Health indicators:** Composite scores from multiple sensors

### 10.4 Feature Selection

- Use Random Forest feature importance
- Apply correlation analysis to remove redundant features
- Consider PCA for dimensionality reduction (if needed)

---

## 11. Data Preprocessing Pipeline

### 11.1 Recommended Steps

1. **Load data** with proper column names
2. **Remove constant sensors** (1, 5, 10, 16, 18, 19)
3. **Calculate RUL** for training data
4. **Split by engines** (train/val/test)
5. **Scale features** (StandardScaler or MinMaxScaler)
6. **Engineer time-series features** (rolling windows, lags)
7. **Handle outliers** (if necessary)
8. **Final feature selection**

### 11.2 Scaling Considerations

- Sensor values have vastly different scales (e.g., sensor_9 ~9065 vs sensor_16 ~0.03)
- Use StandardScaler for tree-based models (optional but recommended)
- Use MinMaxScaler for neural networks (required)
- Fit scaler on training data only, transform val/test

---

## 12. Key Findings Summary

### 12.1 Dataset Characteristics

- **Clean data:** No missing values
- **Simple scenario:** Single operating condition, single fault mode
- **Moderate size:** 100 train engines, 100 test engines
- **Imbalanced test RUL:** Range 7-145 cycles (mean 75.52)

### 12.2 Sensor Characteristics

- **6 constant sensors:** Must be removed (1, 5, 10, 16, 18, 19)
- **1 nearly constant sensor:** Consider removing sensor_6
- **14 useful sensors:** Provide varying information
- **High correlation expected:** Some sensors likely measure related phenomena

### 12.3 RUL Distribution

- **Training:** Linear degradation from max cycle to 0
- **Test:** Ground truth provided, range 7-145 cycles
- **Challenge:** Predict remaining cycles from partial trajectories

### 12.4 Modeling Considerations

- **Data leakage risk:** Must use engine-based splitting
- **Temporal nature:** Time-series models may outperform static models
- **Feature engineering:** Critical for good performance
- **Baseline achievable:** Simple models should provide reasonable results

---

## 13. Next Steps for Development

### 13.1 Immediate Next Phase

1. **Implement data preprocessing pipeline**
   - Remove constant sensors
   - Calculate training RUL
   - Implement engine-based train/val split

2. **Build baseline model**
   - Random Forest with basic features
   - Establish performance baseline (RMSE, MAE)

3. **Feature engineering**
   - Implement rolling window features
   - Add lag features
   - Create degradation indicators

4. **Model optimization**
   - Implement XGBoost/LightGBM
   - Hyperparameter tuning
   - Feature importance analysis

### 13.2 Advanced Development (Future)

1. **Deep learning models**
   - LSTM for temporal patterns
   - CNN-LSTM hybrid
   - Compare with ensemble methods

2. **Advanced features**
   - Domain-specific health indicators
   - Physics-informed features
   - Multi-sensor fusion

3. **Production considerations**
   - Model deployment pipeline
   - Real-time prediction API
   - Monitoring and retraining strategy

---

## 14. Technical Recommendation

### For the Next Development Phase:

**Start with a Random Forest model using:**
- 14 non-constant sensors (remove 1, 5, 10, 16, 18, 19)
- 3 operational settings
- Relative cycle feature
- Engine-based train/validation split (70/15/15)

**Expected baseline performance:** RMSE ~30-40 cycles on validation set

**Then progress to:**
- XGBoost with engineered time-series features (rolling windows, lags)
- Target RMSE: <25 cycles on validation set
- If performance plateaus, consider LSTM for temporal modeling

**This phased approach ensures:**
- Quick initial results
- Understanding of feature importance
- Efficient resource utilization
- Clear performance benchmarks

---

## 15. References

- Saxena, A., Goebel, K., Simon, D., & Eklund, N. (2008). "Damage Propagation Modeling for Aircraft Engine Run-to-Failure Simulation". Proceedings of the 1st International Conference on Prognostics and Health Management (PHM08), Denver CO, Oct 2008.
- NASA C-MAPSS Data Repository: https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/

---

**Document Version:** 1.0  
**Date:** August 20, 2026  
**Analysis Tool:** Python EDA Script (eda_analysis.py)  
**Visualizations:** Saved to `visualizations/` directory
