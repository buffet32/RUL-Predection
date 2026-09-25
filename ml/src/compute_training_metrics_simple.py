"""
Compute training metrics for the final optimized model (simplified version)
"""

import sys
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import json

def compute_training_metrics():
    """
    Compute training metrics for the final optimized model
    """
    print("=" * 80)
    print("COMPUTING TRAINING METRICS FOR FINAL OPTIMIZED MODEL")
    print("=" * 80)
    
    # Load the final optimized model and scaler
    models_dir = Path(__file__).parent.parent.parent / "models"
    model = joblib.load(models_dir / "final_rul_model.joblib")
    scaler = joblib.load(models_dir / "preprocessing_pipeline.joblib")
    
    print("Loaded final model and scaler")
    print(f"Model parameters: n_estimators={model.n_estimators}, max_depth={model.max_depth}")
    
    # Load data directly
    import os
    data_dir = Path(os.getenv('CMAPSS_DATA_DIR', str(Path(__file__).parent.parent.parent / "data" / "archive")))
    
    # Load training data
    train_df = pd.read_csv(
        data_dir / "train_FD001.txt",
        sep=' ',
        header=None,
        engine='python'
    )
    
    # Remove empty columns (trailing whitespace)
    train_df = train_df.dropna(axis=1, how='all')
    
    # Assign column names
    column_names = ['engine_id', 'cycle', 'setting_1', 'setting_2', 'setting_3'] + [f'sensor_{i}' for i in range(1, 22)]
    train_df.columns = column_names
    
    # Remove constant sensors
    constant_sensors = ['sensor_1', 'sensor_5', 'sensor_10', 'sensor_16', 'sensor_18', 'sensor_19']
    train_df = train_df.drop(columns=constant_sensors)
    
    # Calculate RUL
    max_cycles = train_df.groupby('engine_id')['cycle'].max().reset_index()
    max_cycles.columns = ['engine_id', 'max_cycle']
    train_df = train_df.merge(max_cycles, on='engine_id')
    train_df['RUL'] = train_df['max_cycle'] - train_df['cycle']
    
    # Remove relative_cycle (data leakage)
    if 'relative_cycle' in train_df.columns:
        train_df = train_df.drop(columns=['relative_cycle'])
    train_df = train_df.drop(columns=['max_cycle'])
    
    print(f"Loaded training data: {train_df.shape}")
    
    # Get engine split (must match the split used for optimization)
    engine_ids = sorted(train_df['engine_id'].unique())
    np.random.seed(42)
    np.random.shuffle(engine_ids)
    
    n_engines = len(engine_ids)
    n_train = int(0.7 * n_engines)
    n_val = int(0.15 * n_engines)
    
    train_engines = set(engine_ids[:n_train])
    val_engines = set(engine_ids[n_train:n_train + n_val])
    test_engines = set(engine_ids[n_train + n_val:])
    
    # Split data
    train_data = train_df[train_df['engine_id'].isin(train_engines)]
    val_data = train_df[train_df['engine_id'].isin(val_engines)]
    test_data = train_df[train_df['engine_id'].isin(test_engines)]
    
    # Get features (must match model training)
    feature_cols = [
        'setting_1', 'setting_2', 'setting_3',
        'sensor_2', 'sensor_3', 'sensor_4', 'sensor_6', 'sensor_7', 'sensor_8', 'sensor_9',
        'sensor_11', 'sensor_12', 'sensor_13', 'sensor_14', 'sensor_15', 'sensor_17', 'sensor_20', 'sensor_21'
    ]
    
    print(f"Feature columns ({len(feature_cols)}):")
    print(feature_cols)
    
    # Prepare training data
    X_train = train_data[feature_cols].values
    y_train = train_data['RUL'].values
    
    # Prepare validation data
    X_val = val_data[feature_cols].values
    y_val = val_data['RUL'].values
    
    # Prepare test data
    X_test = test_data[feature_cols].values
    y_test = test_data['RUL'].values
    
    print(f"\nData shapes:")
    print(f"  X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"  X_val: {X_val.shape}, y_val: {y_val.shape}")
    print(f"  X_test: {X_test.shape}, y_test: {y_test.shape}")
    
    # Scale features
    X_train_scaled = scaler.transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Make predictions
    y_train_pred = model.predict(X_train_scaled)
    y_val_pred = model.predict(X_val_scaled)
    y_test_pred = model.predict(X_test_scaled)
    
    # Calculate metrics
    def calculate_metrics(y_true, y_pred):
        mse = np.mean((y_true - y_pred) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y_true - y_pred))
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        return {'RMSE': rmse, 'MAE': mae, 'R2': r2}
    
    train_metrics = calculate_metrics(y_train, y_train_pred)
    val_metrics = calculate_metrics(y_val, y_val_pred)
    test_metrics = calculate_metrics(y_test, y_test_pred)
    
    print("\n" + "=" * 80)
    print("COMPUTED METRICS FOR FINAL OPTIMIZED MODEL")
    print("=" * 80)
    print("\nTraining Set:")
    print(f"  RMSE: {train_metrics['RMSE']:.4f}")
    print(f"  MAE: {train_metrics['MAE']:.4f}")
    print(f"  R2: {train_metrics['R2']:.4f}")
    
    print("\nValidation Set:")
    print(f"  RMSE: {val_metrics['RMSE']:.4f}")
    print(f"  MAE: {val_metrics['MAE']:.4f}")
    print(f"  R2: {val_metrics['R2']:.4f}")
    
    print("\nInternal Test Set:")
    print(f"  RMSE: {test_metrics['RMSE']:.4f}")
    print(f"  MAE: {test_metrics['MAE']:.4f}")
    print(f"  R2: {test_metrics['R2']:.4f}")
    
    # Calculate overfitting ratios
    print("\n" + "=" * 80)
    print("OVERFITTING ANALYSIS")
    print("=" * 80)
    
    val_overfitting_ratio = val_metrics['RMSE'] / train_metrics['RMSE']
    test_overfitting_ratio = test_metrics['RMSE'] / train_metrics['RMSE']
    
    print(f"\nValidation Overfitting Ratio (val_RMSE / train_RMSE): {val_overfitting_ratio:.2f}")
    print(f"Test Overfitting Ratio (test_RMSE / train_RMSE): {test_overfitting_ratio:.2f}")
    
    print("\nInterpretation:")
    if val_overfitting_ratio < 1.5:
        print("  Healthy generalization (ratio < 1.5)")
    elif val_overfitting_ratio < 2.0:
        print("  Moderate overfitting (ratio 1.5-2.0)")
    elif val_overfitting_ratio < 3.0:
        print("  Concerning overfitting (ratio 2.0-3.0)")
    else:
        print("  Severe overfitting (ratio > 3.0)")
    
    # Save computed metrics
    results_dir = Path(__file__).parent.parent / "results"
    training_metrics = {
        'model': 'Random Forest Optimized (n_estimators=77, max_depth=9)',
        'train_metrics': train_metrics,
        'val_metrics': val_metrics,
        'test_metrics': test_metrics,
        'overfitting_ratios': {
            'val_ratio': val_overfitting_ratio,
            'test_ratio': test_overfitting_ratio
        }
    }
    
    with open(results_dir / "computed_training_metrics.json", 'w') as f:
        json.dump(training_metrics, f, indent=2)
    
    print(f"\nTraining metrics saved to {results_dir / 'computed_training_metrics.json'}")
    
    return training_metrics

if __name__ == "__main__":
    metrics = compute_training_metrics()
