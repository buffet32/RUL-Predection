"""
Hyperparameter Optimization for Deployment-Safe Random Forest
Using ONLY training and validation data (no official test set)
"""

import sys
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from preprocessing import preprocess_training_data, get_feature_columns, USEFUL_SENSORS
from utils import set_random_seed, split_engines_by_id, split_data_by_engines, calculate_metrics


def optimize_hyperparameters(
    data_dir: str = "../../Downloads/archive",
    random_seed: int = 42,
    n_iter: int = 50
):
    """
    Optimize Random Forest hyperparameters using RandomizedSearchCV
    
    Args:
        data_dir: Path to dataset directory
        random_seed: Random seed for reproducibility
        n_iter: Number of parameter settings sampled
    """
    print("=" * 80)
    print("HYPERPARAMETER OPTIMIZATION (TRAINING/VALIDATION ONLY)")
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
    
    # Split engines at engine level (SAME SPLIT AS BEFORE)
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
    
    print(f"\nFeature columns ({len(feature_cols)}): {feature_cols}")
    
    # Prepare training data
    X_train = train_data[feature_cols].values
    y_train = train_data['RUL'].values
    
    # Prepare validation data
    X_val = val_data[feature_cols].values
    y_val = val_data['RUL'].values
    
    print(f"\nData shapes:")
    print(f"  X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"  X_val: {X_val.shape}, y_val: {y_val.shape}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    
    # Define parameter distribution
    param_distributions = {
        'n_estimators': randint(50, 200),
        'max_depth': randint(5, 30),
        'min_samples_split': randint(2, 20),
        'min_samples_leaf': randint(1, 10),
        'max_features': ['sqrt', 'log2', None]
    }
    
    print("\n" + "=" * 80)
    print("HYPERPARAMETER SEARCH")
    print("=" * 80)
    print(f"Parameter distributions:")
    print(f"  n_estimators: 50-200")
    print(f"  max_depth: 5-30")
    print(f"  min_samples_split: 2-20")
    print(f"  min_samples_leaf: 1-10")
    print(f"  max_features: sqrt, log2, None")
    print(f"\nNumber of iterations: {n_iter}")
    
    # Create RandomizedSearchCV
    rf = RandomForestRegressor(random_state=random_seed, n_jobs=-1)
    
    random_search = RandomizedSearchCV(
        rf,
        param_distributions=param_distributions,
        n_iter=n_iter,
        cv=5,
        scoring='neg_root_mean_squared_error',
        random_state=random_seed,
        n_jobs=-1,
        verbose=1
    )
    
    # Fit on training data only
    random_search.fit(X_train_scaled, y_train)
    
    print("\n" + "=" * 80)
    print("OPTIMIZATION RESULTS")
    print("=" * 80)
    
    print(f"\nBest parameters:")
    for param, value in random_search.best_params_.items():
        print(f"  {param}: {value}")
    
    print(f"\nBest CV RMSE: {-random_search.best_score_:.4f}")
    
    # Evaluate best model on validation set
    best_model = random_search.best_estimator_
    y_val_pred = best_model.predict(X_val_scaled)
    
    val_metrics = calculate_metrics(y_val, y_val_pred)
    
    print(f"\nValidation metrics with best model:")
    print(f"  RMSE: {val_metrics['RMSE']:.4f}")
    print(f"  MAE: {val_metrics['MAE']:.4f}")
    print(f"  R²: {val_metrics['R2']:.4f}")
    
    # Save best model and scaler
    models_dir = Path(__file__).parent.parent / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = models_dir / "random_forest_optimized.joblib"
    joblib.dump(best_model, model_path)
    print(f"\nOptimized model saved to {model_path}")
    
    scaler_path = models_dir / "scaler_optimized.joblib"
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved to {scaler_path}")
    
    # Save optimization results
    results = {
        'best_params': random_search.best_params_,
        'best_cv_rmse': -random_search.best_score_,
        'val_metrics': val_metrics,
        'n_iter': n_iter,
        'random_seed': random_seed,
        'feature_columns': feature_cols
    }
    
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    import json
    with open(results_dir / "optimization_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Optimization results saved to {results_dir / 'optimization_results.json'}")
    
    print("\n" + "=" * 80)
    print("OPTIMIZATION COMPLETE")
    print("=" * 80)
    
    return results, best_model, scaler


if __name__ == "__main__":
    results, best_model, scaler = optimize_hyperparameters(n_iter=50)
