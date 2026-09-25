"""
Evaluate Deployment-Safe Model on Official FD001 Test Set
"""

import sys
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from preprocessing import preprocess_test_data, get_feature_columns, USEFUL_SENSORS


def evaluate_official_test(
    data_dir: str = "../../Downloads/archive"
):
    """
    Evaluate deployment-safe model on official FD001 test set
    
    Args:
        data_dir: Path to dataset directory
    """
    print("=" * 80)
    print("OFFICIAL FD001 TEST SET EVALUATION")
    print("=" * 80)
    
    # Load deployment-safe model
    models_dir = Path("../models")
    model = joblib.load(models_dir / "random_forest_deployment_safe.joblib")
    scaler = joblib.load(models_dir / "scaler_deployment_safe.joblib")
    
    print("Loaded deployment-safe model and scaler")
    
    # Preprocess test data
    test_df, rul_df = preprocess_test_data(data_dir)
    
    # Remove relative_cycle (data leakage feature)
    if 'relative_cycle' in test_df.columns:
        test_df = test_df.drop(columns=['relative_cycle'])
        print("Removed relative_cycle feature from test data")
    
    # Get feature columns (same as training)
    feature_cols = [
        'setting_1', 'setting_2', 'setting_3',
        'sensor_2', 'sensor_3', 'sensor_4', 'sensor_6', 'sensor_7', 'sensor_8', 'sensor_9',
        'sensor_11', 'sensor_12', 'sensor_13', 'sensor_14', 'sensor_15', 'sensor_17', 'sensor_20', 'sensor_21'
    ]
    
    print(f"\nFeature columns ({len(feature_cols)}): {feature_cols}")
    
    # Get predictions for the LAST cycle of each test engine
    print("\nGenerating predictions for last cycle of each test engine...")
    
    predictions = []
    actual_ruls = []
    engine_ids = []
    
    for engine_id in sorted(test_df['engine_id'].unique()):
        engine_data = test_df[test_df['engine_id'] == engine_id]
        
        # Get the last cycle
        last_cycle_data = engine_data.iloc[[-1]]
        
        # Extract features
        X = last_cycle_data[feature_cols].values
        
        # Scale
        X_scaled = scaler.transform(X)
        
        # Predict
        pred_rul = model.predict(X_scaled)[0]
        
        # Get actual RUL from RUL_FD001.txt
        actual_rul = rul_df.iloc[engine_id - 1]['RUL']  # engine_id is 1-indexed
        
        predictions.append(pred_rul)
        actual_ruls.append(actual_rul)
        engine_ids.append(engine_id)
    
    predictions = np.array(predictions)
    actual_ruls = np.array(actual_ruls)
    
    print(f"Generated predictions for {len(predictions)} test engines")
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(actual_ruls, predictions))
    mae = mean_absolute_error(actual_ruls, predictions)
    r2 = r2_score(actual_ruls, predictions)
    
    print("\n" + "=" * 80)
    print("OFFICIAL TEST SET METRICS")
    print("=" * 80)
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"R²: {r2:.4f}")
    
    # Error analysis by RUL range
    print("\n" + "=" * 80)
    print("ERROR ANALYSIS BY RUL RANGE")
    print("=" * 80)
    
    rul_ranges = [
        (0, 30, "Critical (0-30)"),
        (30, 60, "Warning (30-60)"),
        (60, 100, "Moderate (60-100)"),
        (100, 150, "Healthy (100-150)"),
        (150, 999, "Very Healthy (150+)")
    ]
    
    for min_rul, max_rul, label in rul_ranges:
        mask = (actual_ruls >= min_rul) & (actual_ruls < max_rul)
        if mask.sum() > 0:
            range_rmse = np.sqrt(mean_squared_error(actual_ruls[mask], predictions[mask]))
            range_mae = mean_absolute_error(actual_ruls[mask], predictions[mask])
            range_count = mask.sum()
            print(f"{label}: RMSE={range_rmse:.2f}, MAE={range_mae:.2f}, Count={range_count}")
    
    # Error analysis by engine
    print("\n" + "=" * 80)
    print("ERROR ANALYSIS BY ENGINE (Top 10 Worst)")
    print("=" * 80)
    
    errors = np.abs(predictions - actual_ruls)
    worst_indices = np.argsort(errors)[-10:][::-1]
    
    for idx in worst_indices:
        print(f"Engine {engine_ids[idx]}: Actual={actual_ruls[idx]:.1f}, Predicted={predictions[idx]:.1f}, Error={errors[idx]:.1f}")
    
    # Create visualizations
    viz_dir = Path("../visualizations")
    viz_dir.mkdir(exist_ok=True)
    
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    
    # Actual vs Predicted
    plt.figure(figsize=(10, 6))
    plt.scatter(actual_ruls, predictions, alpha=0.6, s=50)
    plt.plot([actual_ruls.min(), actual_ruls.max()], [actual_ruls.min(), actual_ruls.max()], 'r--', lw=2)
    plt.xlabel('Actual RUL')
    plt.ylabel('Predicted RUL')
    plt.title('Official Test Set: Actual vs Predicted RUL')
    plt.grid(True, alpha=0.3)
    plt.savefig(viz_dir / "official_test_predictions.png", dpi=150, bbox_inches='tight')
    print("Saved: official_test_predictions.png")
    plt.close()
    
    # Error distribution
    errors = predictions - actual_ruls
    plt.figure(figsize=(10, 6))
    plt.hist(errors, bins=30, edgecolor='black', alpha=0.7)
    plt.axvline(x=0, color='r', linestyle='--', lw=2)
    plt.axvline(x=np.mean(errors), color='g', linestyle='--', lw=2, label=f'Mean: {np.mean(errors):.2f}')
    plt.xlabel('Error (Predicted - Actual)')
    plt.ylabel('Frequency')
    plt.title('Official Test Set: Error Distribution')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(viz_dir / "official_test_error_distribution.png", dpi=150, bbox_inches='tight')
    print("Saved: official_test_error_distribution.png")
    plt.close()
    
    # Error by RUL
    plt.figure(figsize=(10, 6))
    plt.scatter(actual_ruls, errors, alpha=0.6, s=50)
    plt.axhline(y=0, color='r', linestyle='--', lw=2)
    plt.xlabel('Actual RUL')
    plt.ylabel('Error (Predicted - Actual)')
    plt.title('Official Test Set: Error vs Actual RUL')
    plt.grid(True, alpha=0.3)
    plt.savefig(viz_dir / "official_test_error_vs_rul.png", dpi=150, bbox_inches='tight')
    print("Saved: official_test_error_vs_rul.png")
    plt.close()
    
    # Per-engine error
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(engine_ids)), errors)
    plt.axhline(y=0, color='r', linestyle='--', lw=2)
    plt.xlabel('Engine ID')
    plt.ylabel('Error (Predicted - Actual)')
    plt.title('Official Test Set: Error by Engine')
    plt.xticks(range(len(engine_ids)), engine_ids, rotation=90)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(viz_dir / "official_test_error_by_engine.png", dpi=150, bbox_inches='tight')
    print("Saved: official_test_error_by_engine.png")
    plt.close()
    
    # Save results
    results = {
        'model': 'Random Forest Deployment-Safe',
        'test_set': 'Official FD001 Test Set',
        'metrics': {
            'RMSE': rmse,
            'MAE': mae,
            'R2': r2
        },
        'n_engines': len(predictions),
        'prediction_method': 'Last cycle of each test engine',
        'data_leakage_check': 'PASSED - No relative_cycle feature used'
    }
    
    results_dir = Path("../results")
    results_dir.mkdir(exist_ok=True)
    
    import json
    with open(results_dir / "official_test_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {results_dir / 'official_test_results.json'}")
    
    print("\n" + "=" * 80)
    print("OFFICIAL TEST EVALUATION COMPLETE")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    results = evaluate_official_test()
