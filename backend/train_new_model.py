#!/usr/bin/env python3
"""Train a new RUL prediction model on NASA C-MAPSS dataset"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

DATASET_PATH = Path("C:/Users/ULTRAPC/Downloads/archive")
MODEL_OUTPUT_PATH = Path("C:/Users/ULTRAPC/Desktop/pfa2026/models")

def load_and_prepare_data():
    """Load and prepare training data"""
    print("Loading NASA C-MAPSS training data...")

    train_file = DATASET_PATH / "train_FD001.txt"
    rul_file = DATASET_PATH / "RUL_FD001.txt"

    # Read data
    train_data = pd.read_csv(train_file, sep=r"\s+", header=None, engine="python")
    rul_data = pd.read_csv(rul_file, sep=r"\s+", header=None, engine="python")

    # Column names - match actual 26 columns
    columns = ["engine_id", "cycle", "setting_1", "setting_2", "setting_3"]
    columns += [f"sensor_{i}" for i in range(2, 22)]  # sensor_2 to sensor_21

    # Pad with extra columns if needed
    while len(columns) < train_data.shape[1]:
        columns.append(f"extra_{len(columns)}")

    train_data.columns = columns[:train_data.shape[1]]
    rul_data.columns = ["rul"]

    print(f"Loaded {len(train_data)} training samples from {train_data['engine_id'].max()} engines")

    # Calculate RUL for each sample
    rul_values = []
    for engine_id in train_data['engine_id'].unique():
        engine_data = train_data[train_data['engine_id'] == engine_id]
        max_cycle = engine_data['cycle'].max()
        engine_rul = rul_data.iloc[int(engine_id) - 1, 0]

        for _, row in engine_data.iterrows():
            cycles_remaining = max_cycle - int(row['cycle']) + engine_rul
            rul_values.append(cycles_remaining)

    train_data['rul'] = rul_values

    # Select features (exclude constant sensors and engine_id)
    feature_cols = [col for col in train_data.columns
                   if col.startswith('sensor_') or col.startswith('setting_')]
    # Remove constant sensors
    feature_cols = [col for col in feature_cols if col not in ['sensor_1', 'sensor_5', 'sensor_10', 'sensor_16', 'sensor_18', 'sensor_19']]

    X = train_data[feature_cols]
    y = train_data['rul']

    print(f"Features: {len(feature_cols)}")
    print(f"Feature columns: {feature_cols}")
    print(f"RUL range: {y.min():.1f} - {y.max():.1f}")

    return X, y, feature_cols

def train_model(X, y, feature_cols):
    """Train Random Forest model"""
    print("\n" + "="*60)
    print("TRAINING NEW MODEL")
    print("="*60)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train model
    print("\nTraining Random Forest...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    model.fit(X_train_scaled, y_train)

    # Evaluate
    print("\nEvaluating model...")
    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)

    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    train_mae = mean_absolute_error(y_train, y_pred_train)
    train_r2 = r2_score(y_train, y_pred_train)

    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
    test_mae = mean_absolute_error(y_test, y_pred_test)
    test_r2 = r2_score(y_test, y_pred_test)

    print(f"\nTraining Metrics:")
    print(f"  RMSE: {train_rmse:.2f}")
    print(f"  MAE:  {train_mae:.2f}")
    print(f"  R²:   {train_r2:.4f}")

    print(f"\nTest Metrics:")
    print(f"  RMSE: {test_rmse:.2f}")
    print(f"  MAE:  {test_mae:.2f}")
    print(f"  R²:   {test_r2:.4f}")

    # Feature importance
    importance_df = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print(f"\nTop 10 Features:")
    for idx, row in importance_df.head(10).iterrows():
        print(f"  {row['feature']:15s}: {row['importance']:.4f}")

    return model, scaler, {
        'train_rmse': float(train_rmse),
        'train_mae': float(train_mae),
        'train_r2': float(train_r2),
        'test_rmse': float(test_rmse),
        'test_mae': float(test_mae),
        'test_r2': float(test_r2),
    }

def save_model(model, scaler, metrics, feature_cols):
    """Save model, scaler, and metadata"""
    print("\n" + "="*60)
    print("SAVING MODEL")
    print("="*60)

    MODEL_OUTPUT_PATH.mkdir(exist_ok=True)

    # Save model
    model_path = MODEL_OUTPUT_PATH / "final_rul_model.joblib"
    joblib.dump(model, model_path)
    print(f"✓ Model saved: {model_path}")

    # Save scaler
    scaler_path = MODEL_OUTPUT_PATH / "preprocessing_pipeline.joblib"
    joblib.dump(scaler, scaler_path)
    print(f"✓ Scaler saved: {scaler_path}")

    # Save metadata
    metadata = {
        "model_type": "RandomForestRegressor",
        "model_version": "2.0",
        "training_date": datetime.utcnow().isoformat(),
        "training_dataset": "NASA C-MAPSS FD001",
        "features": feature_cols,
        "preprocessing": ["StandardScaler normalization"],
        "hyperparameters": {
            "n_estimators": 100,
            "max_depth": 15,
            "min_samples_split": 5,
            "min_samples_leaf": 2,
            "random_state": 42
        },
        "metrics": metrics,
        "health_score": {
            "method": "linear_scaling",
            "max_rul": 200,
            "range": "0-100"
        }
    }

    metadata_path = MODEL_OUTPUT_PATH / "model_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Metadata saved: {metadata_path}")

    print(f"\n[OK] Model training complete!")
    print(f"New model saved to {MODEL_OUTPUT_PATH}")

if __name__ == "__main__":
    print("="*60)
    print("NASA C-MAPSS RUL MODEL TRAINING")
    print("="*60)

    try:
        X, y, feature_cols = load_and_prepare_data()
        model, scaler, metrics = train_model(X, y, feature_cols)
        save_model(model, scaler, metrics, feature_cols)
        print("\n[OK] Training successful!")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
