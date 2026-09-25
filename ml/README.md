# ML Pipeline for NASA C-MAPSS FD001 RUL Prediction

This directory contains the machine learning pipeline for predicting Remaining Useful Life (RUL) of turbofan engines using the NASA C-MAPSS FD001 dataset.

## Project Structure

```
ml/
├── data/              # Dataset files (not included, use original dataset)
├── notebooks/         # Jupyter notebooks for exploration
├── src/              # Source code
│   ├── preprocessing.py    # Data loading and preprocessing
│   ├── features.py          # Feature engineering
│   ├── utils.py             # Utility functions
│   ├── train_baseline.py    # Train Random Forest baseline
│   ├── train_xgboost.py     # Train XGBoost model
│   └── evaluate.py          # Model comparison and evaluation
├── models/           # Saved trained models
├── results/          # Training results and metrics
├── visualizations/   # Generated plots and figures
└── requirements.txt  # Python dependencies
```

## Installation

### Prerequisites

- Python 3.8 or higher
- NASA C-MAPSS FD001 dataset (place in `../../Downloads/archive/`)

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Dataset Preparation

The NASA C-MAPSS FD001 dataset should be placed in the following location:
```
../../Downloads/archive/
├── train_FD001.txt
├── test_FD001.txt
├── RUL_FD001.txt
└── readme.txt
```

If your dataset is in a different location, modify the `data_dir` parameter in the training scripts.

## Usage

### 1. Train Baseline Model

Train a Random Forest model with basic features:

```bash
python src/train_baseline.py
```

This will:
- Load and preprocess the training data
- Split engines into train/validation/test (70/15/15)
- Train a Random Forest regressor
- Generate evaluation metrics and visualizations
- Save the model to `models/random_forest_baseline.joblib`
- Save results to `results/baseline_results.json`

### 2. Train Random Forest with Time-Series Features

Train a Random Forest model with engineered time-series features:

```bash
python src/train_xgboost.py --model random_forest --features time_series
```

This adds:
- Rolling window features (mean, std, min, max for windows 5, 10, 20)
- Lag features (lags 1, 2, 5)
- Difference features (first difference, rate of change)
- Degradation features (deviation from baseline)

### 3. Train XGBoost with Time-Series Features

Train an XGBoost model with time-series features:

```bash
python src/train_xgboost.py --model xgboost --features time_series
```

### 4. Compare Models

Run the evaluation script to compare all trained models:

```bash
python src/evaluate.py
```

This generates:
- Model comparison table
- Error analysis
- Comparison visualizations

## Model Outputs

### Saved Models

- `models/random_forest_baseline.joblib` - Random Forest baseline model
- `models/scaler_baseline.joblib` - Scaler for baseline model
- `models/random_forest_ts.joblib` - Random Forest with time-series features
- `models/scaler_random_forest_ts.joblib` - Scaler for RF time-series model
- `models/xgboost_ts.joblib` - XGBoost with time-series features
- `models/scaler_xgboost_ts.joblib` - Scaler for XGBoost model

### Results Files

- `results/baseline_results.json` - Baseline model metrics
- `results/random_forest_ts_results.json` - RF time-series metrics
- `results/xgboost_ts_results.json` - XGBoost time-series metrics
- `results/model_comparison.csv` - Model comparison table
- `results/error_analysis.json` - Error analysis summary

### Visualizations

- `visualizations/rf_baseline_predictions_val.png` - Actual vs predicted RUL
- `visualizations/rf_baseline_residuals_val.png` - Residual plot
- `visualizations/rf_baseline_feature_importance.png` - Feature importance
- `visualizations/rf_baseline_error_distribution_val.png` - Error distribution
- `visualizations/rf_baseline_rul_vs_error_val.png` - RUL vs error
- Similar plots for Random Forest time-series and XGBoost models
- `visualizations/model_comparison.png` - Model comparison visualization

## Data Preprocessing

The preprocessing pipeline (`preprocessing.py`) performs:

1. **Data Loading**: Loads train, test, and RUL files with proper column names
2. **Constant Sensor Removal**: Removes 6 constant sensors (1, 5, 10, 16, 18, 19)
3. **RUL Calculation**: For training data, RUL = max_cycle - current_cycle
4. **Relative Cycle**: Adds normalized cycle feature (cycle / max_cycle)
5. **Validation**: Sanity checks for missing values, duplicates, and sequential cycles

## Feature Engineering

The feature engineering pipeline (`features.py`) creates:

### Rolling Window Features
- Rolling mean, std, min, max for each sensor
- Window sizes: 5, 10, 20 cycles

### Lag Features
- Sensor values from previous cycles
- Lag values: 1, 2, 5 cycles

### Difference Features
- First difference (current - previous)
- Rate of change (difference / current value)

### Degradation Features
- Deviation from early-life baseline (first 5 cycles)
- Cumulative deviation over time

**Important**: All features use only current and past information to prevent data leakage.

## Train/Validation/Test Split

The split is performed at the **engine level** to prevent data leakage:

- **Training**: 70 engines (70%)
- **Validation**: 15 engines (15%)
- **Internal Test**: 15 engines (15%)

No engine appears in more than one split. The split uses a fixed random seed (42) for reproducibility.

### Engine Split (Seed 42)

**Training Engines (70)**: [1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 23, 25, 26, 27, 28, 29, 31, 32, 34, 35, 36, 37, 39, 40, 41, 43, 44, 45, 46, 47, 48, 50, 51, 54, 55, 56, 57, 62, 63, 65, 66, 67, 68, 69, 70, 71, 73, 74, 77, 78, 79, 81, 82, 84, 86, 89, 90, 91, 94, 96, 97, 98, 100]

**Validation Engines (15)**: [2, 30, 33, 38, 42, 49, 58, 59, 60, 64, 76, 80, 85, 95, 99]

**Test Engines (15)**: [3, 15, 21, 22, 24, 52, 53, 61, 72, 75, 83, 87, 88, 92, 93]

## Evaluation Metrics

Models are evaluated using:

- **RMSE** (Root Mean Squared Error): Primary metric, penalizes large errors
- **MAE** (Mean Absolute Error): Interpretable average error
- **R²** (R-squared): Explains variance in predictions

## Model Hyperparameters

### Random Forest Baseline
- n_estimators: 100
- max_depth: 15
- min_samples_split: 10
- min_samples_leaf: 5

### Random Forest Time-Series
- Same as baseline

### XGBoost Time-Series
- n_estimators: 100
- max_depth: 6
- learning_rate: 0.1
- subsample: 0.8
- colsample_bytree: 0.8

## Reproducibility

All experiments use:
- Fixed random seed (42)
- Deterministic train/validation/test split
- Saved model files for exact reproduction

## Key Findings

Based on the experiments:

1. **Random Forest Baseline** achieved the best validation RMSE (25.47) with minimal overfitting
2. **Time-series features** caused significant overfitting (overfitting ratio > 7)
3. **XGBoost** performed similarly to Random Forest with time-series features
4. **Baseline features** (settings + sensors + relative_cycle) are sufficient for this dataset

## Troubleshooting

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Dataset Not Found
Check that the dataset path in the scripts matches your actual dataset location. Modify the `data_dir` parameter if needed.

### Memory Issues
If you encounter memory issues with time-series features:
- Reduce the number of rolling windows
- Reduce the number of lag features
- Use fewer engines for training

## Next Steps

For Phase 3 development:
1. Consider hyperparameter tuning for the baseline model
2. Investigate why time-series features cause overfitting
3. Try regularization techniques
4. Evaluate on the official test set (FD001 test)
5. Consider LSTM models if temporal patterns are critical

## References

- NASA C-MAPSS Dataset: https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/
- Saxena, A., Goebel, K., Simon, D., & Eklund, N. (2008). "Damage Propagation Modeling for Aircraft Engine Run-to-Failure Simulation"
