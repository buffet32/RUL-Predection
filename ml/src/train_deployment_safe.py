"""
Train Deployment-Safe Random Forest Model (No Data Leakage)
"""

import sys
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from preprocessing import preprocess_training_data, get_feature_columns, USEFUL_SENSORS
from utils import (
    set_random_seed, split_engines_by_id, split_data_by_engines,
    calculate_metrics, save_results, plot_predictions, plot_residuals,
    plot_feature_importance, plot_error_distribution, plot_rul_vs_error
)


def train_deployment_safe_rf(
    data_dir: str = "../../Downloads/archive",
    random_seed: int = 42
):
    """
    Train Random Forest with deployment-safe features (NO relative_cycle)
    
    Args:
        data_dir: Path to dataset directory
        random_seed: Random seed for reproducibility
    """
    print("=" * 80)
    print("DEPLOYMENT-SAFE RANDOM FOREST TRAINING (NO DATA LEAKAGE)")
    print("=" * 80)
    
    # Set random seed
    set_random_seed(random_seed)
    
    # Preprocess training data
    train_df = preprocess_training_data(data_dir)
    
    # Remove relative_cycle (data leakage feature)
    if 'relative_cycle' in train_df.columns:
        train_df = train_df.drop(columns=['relative_cycle'])
        print("Removed relative_cycle feature (data leakage)")
    
    # Get all engine IDs
    engine_ids = sorted(train_df['engine_id'].unique())
    
    # Split engines at engine level (SAME SPLIT AS BASELINE for fair comparison)
    engine_split = split_engines_by_id(
        engine_ids,
        train_ratio=0.7,
        val_ratio=0.15,
        test_ratio=0.15,
        seed=random_seed
    )
    
    # Split data by engines
    train_data, val_data, test_data = split_data_by_engines(train_df, engine_split)
    
    # Get feature columns (exclude engine_id, cycle, max_cycle, RUL)
    feature_cols = get_feature_columns(train_data, include_engine_id=False)
    
    print(f"\nDeployment-safe feature columns ({len(feature_cols)}):")
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
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest (SAME ARCHITECTURE AS BASELINE)
    print("\n" + "=" * 80)
    print("TRAINING DEPLOYMENT-SAFE RANDOM FOREST")
    print("=" * 80)
    
    rf_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=random_seed,
        n_jobs=-1
    )
    
    rf_model.fit(X_train_scaled, y_train)
    
    print("Random Forest training complete")
    
    # Make predictions
    y_train_pred = rf_model.predict(X_train_scaled)
    y_val_pred = rf_model.predict(X_val_scaled)
    y_test_pred = rf_model.predict(X_test_scaled)
    
    # Calculate metrics
    train_metrics = calculate_metrics(y_train, y_train_pred)
    val_metrics = calculate_metrics(y_val, y_val_pred)
    test_metrics = calculate_metrics(y_test, y_test_pred)
    
    print("\n" + "=" * 80)
    print("EVALUATION METRICS")
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
    
    # Create visualizations directory
    viz_dir = Path(__file__).parent.parent / "visualizations"
    viz_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate plots
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    
    plot_predictions(
        y_val, y_val_pred,
        title="Deployment-Safe RF - Actual vs Predicted RUL (Validation)",
        save_path=viz_dir / "rf_deployment_safe_predictions_val.png"
    )
    
    plot_residuals(
        y_val, y_val_pred,
        title="Deployment-Safe RF - Residual Plot (Validation)",
        save_path=viz_dir / "rf_deployment_safe_residuals_val.png"
    )
    
    plot_feature_importance(
        feature_cols,
        rf_model.feature_importances_,
        title="Deployment-Safe RF - Feature Importance",
        top_n=20,
        save_path=viz_dir / "rf_deployment_safe_feature_importance.png"
    )
    
    plot_error_distribution(
        y_val, y_val_pred,
        title="Deployment-Safe RF - Error Distribution (Validation)",
        save_path=viz_dir / "rf_deployment_safe_error_distribution_val.png"
    )
    
    plot_rul_vs_error(
        y_val, y_val_pred,
        title="Deployment-Safe RF - RUL vs Error (Validation)",
        save_path=viz_dir / "rf_deployment_safe_rul_vs_error_val.png"
    )
    
    # Save model
    models_dir = Path(__file__).parent.parent / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = models_dir / "random_forest_deployment_safe.joblib"
    joblib.dump(rf_model, model_path)
    print(f"\nModel saved to {model_path}")
    
    # Save scaler
    scaler_path = models_dir / "scaler_deployment_safe.joblib"
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved to {scaler_path}")
    
    # Save results
    results = {
        'model': 'Random Forest Deployment-Safe',
        'features': 'deployment-safe (settings + sensors + cycle, NO relative_cycle)',
        'random_seed': random_seed,
        'engine_split': engine_split,
        'feature_columns': feature_cols,
        'train_metrics': train_metrics,
        'val_metrics': val_metrics,
        'test_metrics': test_metrics,
        'model_params': {
            'n_estimators': 100,
            'max_depth': 15,
            'min_samples_split': 10,
            'min_samples_leaf': 5
        },
        'data_leakage_check': 'PASSED - No relative_cycle feature'
    }
    
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    results_path = results_dir / "deployment_safe_results.json"
    save_results(results, results_path)
    print(f"Results saved to {results_path}")
    
    print("\n" + "=" * 80)
    print("DEPLOYMENT-SAFE TRAINING COMPLETE")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    results = train_deployment_safe_rf()
