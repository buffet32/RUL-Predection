"""
Compute training metrics for the final optimized model
"""

import sys
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from preprocessing import preprocess_training_data, get_feature_columns
from utils import set_random_seed, split_engines_by_id, split_data_by_engines, calculate_metrics

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
    
    # Preprocess training data
    import os
    data_dir = os.getenv('CMAPSS_DATA_DIR', str(Path(__file__).parent.parent.parent / "data" / "archive"))
    train_df = preprocess_training_data(data_dir)
    
    # Remove relative_cycle (data leakage)
    if 'relative_cycle' in train_df.columns:
        train_df = train_df.drop(columns=['relative_cycle'])
        print("Removed relative_cycle feature (data leakage)")
    
    # Get engine split (must match the split used for optimization)
    engine_ids = sorted(train_df['engine_id'].unique())
    engine_split = split_engines_by_id(
        engine_ids,
        train_ratio=0.7,
        val_ratio=0.15,
        test_ratio=0.15,
        seed=42
    )
    
    # Split data
    train_data, val_data, test_data = split_data_by_engines(train_df, engine_split)
    
    # Get features
    feature_cols = get_feature_columns(train_data, include_engine_id=False)
    
    print(f"\nFeature columns ({len(feature_cols)}):")
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
    train_metrics = calculate_metrics(y_train, y_train_pred)
    val_metrics = calculate_metrics(y_val, y_val_pred)
    test_metrics = calculate_metrics(y_test, y_test_pred)
    
    print("\n" + "=" * 80)
    print("COMPUTED METRICS FOR FINAL OPTIMIZED MODEL")
    print("=" * 80)
    print("\nTraining Set:")
    print(f"  RMSE: {train_metrics['RMSE']:.4f}")
    print(f"  MAE: {train_metrics['MAE']:.4f}")
    print(f"  R²: {train_metrics['R2']:.4f}")
    
    print("\nValidation Set:")
    print(f"  RMSE: {val_metrics['RMSE']:.4f}")
    print(f"  MAE: {val_metrics['MAE']:.4f}")
    print(f"  R²: {val_metrics['R2']:.4f}")
    
    print("\nInternal Test Set:")
    print(f"  RMSE: {test_metrics['RMSE']:.4f}")
    print(f"  MAE: {test_metrics['MAE']:.4f}")
    print(f"  R²: {test_metrics['R2']:.4f}")
    
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
        print("  ✅ Healthy generalization (ratio < 1.5)")
    elif val_overfitting_ratio < 2.0:
        print("  ⚠️  Moderate overfitting (ratio 1.5-2.0)")
    elif val_overfitting_ratio < 3.0:
        print("  ❌ Concerning overfitting (ratio 2.0-3.0)")
    else:
        print("  ❌ Severe overfitting (ratio > 3.0)")
    
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
    
    import json
    with open(results_dir / "computed_training_metrics.json", 'w') as f:
        json.dump(training_metrics, f, indent=2)
    
    print(f"\nTraining metrics saved to {results_dir / 'computed_training_metrics.json'}")
    
    return training_metrics

if __name__ == "__main__":
    metrics = compute_training_metrics()
