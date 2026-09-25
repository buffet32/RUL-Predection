"""
Analyze Overestimation Bias and Error Distribution
Using validation data only
"""

import sys
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from preprocessing import preprocess_training_data, get_feature_columns
from utils import set_random_seed, split_engines_by_id, split_data_by_engines


def analyze_bias(
    data_dir: str = "../../Downloads/archive",
    random_seed: int = 42
):
    """
    Analyze prediction bias and error distribution on validation set
    
    Args:
        data_dir: Path to dataset directory
        random_seed: Random seed for reproducibility
    """
    print("=" * 80)
    print("OVERESTIMATION BIAS ANALYSIS (VALIDATION SET)")
    print("=" * 80)
    
    # Load optimized model
    models_dir = Path(__file__).parent.parent / "models"
    model = joblib.load(models_dir / "random_forest_optimized.joblib")
    scaler = joblib.load(models_dir / "scaler_optimized.joblib")
    
    print("Loaded optimized model and scaler")
    
    # Preprocess training data
    train_df = preprocess_training_data(data_dir)
    
    # Remove relative_cycle
    if 'relative_cycle' in train_df.columns:
        train_df = train_df.drop(columns=['relative_cycle'])
    
    # Get engine split (same as before)
    engine_ids = sorted(train_df['engine_id'].unique())
    engine_split = split_engines_by_id(
        engine_ids,
        train_ratio=0.7,
        val_ratio=0.15,
        test_ratio=0.15,
        seed=random_seed
    )
    
    # Split data
    train_data, val_data, test_data = split_data_by_engines(train_df, engine_split)
    
    # Get features
    feature_cols = get_feature_columns(val_data, include_engine_id=False)
    
    # Prepare validation data
    X_val = val_data[feature_cols].values
    y_val = val_data['RUL'].values
    
    # Scale and predict
    X_val_scaled = scaler.transform(X_val)
    y_val_pred = model.predict(X_val_scaled)
    
    # Calculate error
    errors = y_val_pred - y_val  # positive = overestimation
    
    print("\n" + "=" * 80)
    print("ERROR STATISTICS")
    print("=" * 80)
    
    print(f"\nMean error: {np.mean(errors):.4f}")
    print(f"Median error: {np.median(errors):.4f}")
    print(f"Std error: {np.std(errors):.4f}")
    print(f"Mean absolute error: {np.mean(np.abs(errors)):.4f}")
    
    print(f"\nOverestimation rate: {np.mean(errors > 0):.2%}")
    print(f"Underestimation rate: {np.mean(errors < 0):.2%}")
    
    # Error by RUL range
    print("\n" + "=" * 80)
    print("ERROR BY RUL RANGE")
    print("=" * 80)
    
    rul_ranges = [
        (0, 30, "Critical (0-30)"),
        (30, 60, "Warning (30-60)"),
        (60, 100, "Moderate (60-100)"),
        (100, 150, "Healthy (100-150)"),
        (150, 999, "Very Healthy (150+)")
    ]
    
    for min_rul, max_rul, label in rul_ranges:
        mask = (y_val >= min_rul) & (y_val < max_rul)
        if mask.sum() > 0:
            range_errors = errors[mask]
            print(f"\n{label}:")
            print(f"  Count: {mask.sum()}")
            print(f"  Mean error: {np.mean(range_errors):.4f}")
            print(f"  Median error: {np.median(range_errors):.4f}")
            print(f"  Std error: {np.std(range_errors):.4f}")
            print(f"  Overestimation rate: {np.mean(range_errors > 0):.2%}")
    
    # Safety margin analysis (percentiles of positive errors)
    print("\n" + "=" * 80)
    print("SAFETY MARGIN ANALYSIS (POSITIVE ERRORS ONLY)")
    print("=" * 80)
    
    positive_errors = errors[errors > 0]
    
    if len(positive_errors) > 0:
        print(f"\nPositive errors count: {len(positive_errors)}")
        print(f"50th percentile: {np.percentile(positive_errors, 50):.2f}")
        print(f"75th percentile: {np.percentile(positive_errors, 75):.2f}")
        print(f"90th percentile: {np.percentile(positive_errors, 90):.2f}")
        print(f"95th percentile: {np.percentile(positive_errors, 95):.2f}")
    
    # Create visualizations
    viz_dir = Path(__file__).parent.parent / "visualizations"
    viz_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    
    # Actual vs Predicted
    plt.figure(figsize=(10, 6))
    plt.scatter(y_val, y_val_pred, alpha=0.5, s=20)
    plt.plot([y_val.min(), y_val.max()], [y_val.min(), y_val.max()], 'r--', lw=2)
    plt.xlabel('Actual RUL')
    plt.ylabel('Predicted RUL')
    plt.title('Validation Set: Actual vs Predicted RUL (Optimized Model)')
    plt.grid(True, alpha=0.3)
    plt.savefig(viz_dir / "optimized_bias_actual_vs_predicted.png", dpi=150, bbox_inches='tight')
    print("Saved: optimized_bias_actual_vs_predicted.png")
    plt.close()
    
    # Error vs Actual RUL
    plt.figure(figsize=(10, 6))
    plt.scatter(y_val, errors, alpha=0.5, s=20)
    plt.axhline(y=0, color='r', linestyle='--', lw=2)
    plt.axhline(y=np.mean(errors), color='g', linestyle='--', lw=2, label=f'Mean: {np.mean(errors):.2f}')
    plt.xlabel('Actual RUL')
    plt.ylabel('Prediction Error (Predicted - Actual)')
    plt.title('Validation Set: Prediction Error vs Actual RUL')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(viz_dir / "optimized_bias_error_vs_rul.png", dpi=150, bbox_inches='tight')
    print("Saved: optimized_bias_error_vs_rul.png")
    plt.close()
    
    # Error distribution
    plt.figure(figsize=(10, 6))
    plt.hist(errors, bins=50, edgecolor='black', alpha=0.7)
    plt.axvline(x=0, color='r', linestyle='--', lw=2)
    plt.axvline(x=np.mean(errors), color='g', linestyle='--', lw=2, label=f'Mean: {np.mean(errors):.2f}')
    plt.xlabel('Prediction Error (Predicted - Actual)')
    plt.ylabel('Frequency')
    plt.title('Validation Set: Error Distribution')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(viz_dir / "optimized_bias_error_distribution.png", dpi=150, bbox_inches='tight')
    print("Saved: optimized_bias_error_distribution.png")
    plt.close()
    
    # Save bias analysis results
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    import json
    bias_results = {
        'mean_error': float(np.mean(errors)),
        'median_error': float(np.median(errors)),
        'std_error': float(np.std(errors)),
        'mae': float(np.mean(np.abs(errors))),
        'overestimation_rate': float(np.mean(errors > 0)),
        'underestimation_rate': float(np.mean(errors < 0)),
        'safety_margins': {
            'p50': float(np.percentile(positive_errors, 50)) if len(positive_errors) > 0 else 0,
            'p75': float(np.percentile(positive_errors, 75)) if len(positive_errors) > 0 else 0,
            'p90': float(np.percentile(positive_errors, 90)) if len(positive_errors) > 0 else 0,
            'p95': float(np.percentile(positive_errors, 95)) if len(positive_errors) > 0 else 0
        }
    }
    
    with open(results_dir / "bias_analysis.json", 'w') as f:
        json.dump(bias_results, f, indent=2)
    
    print(f"\nBias analysis saved to {results_dir / 'bias_analysis.json'}")
    
    print("\n" + "=" * 80)
    print("BIAS ANALYSIS COMPLETE")
    print("=" * 80)
    
    return bias_results


if __name__ == "__main__":
    bias_results = analyze_bias()
