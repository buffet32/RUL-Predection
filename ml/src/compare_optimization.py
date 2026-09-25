"""
Compare Baseline vs Optimized Models
"""

import sys
import json
import pandas as pd
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from utils import load_results


def compare_models():
    """
    Compare baseline vs optimized deployment-safe models
    """
    print("=" * 80)
    print("BASELINE vs OPTIMIZED MODEL COMPARISON")
    print("=" * 80)
    
    results_path = Path(__file__).parent.parent / "results"
    
    # Load results
    baseline_results = load_results(results_path / "deployment_safe_results.json")
    optimized_results = load_results(results_path / "optimization_results.json")
    
    # Create comparison table
    comparison_data = {
        'Model': [
            'Random Forest Baseline (Deployment-Safe)',
            'Random Forest Optimized (Deployment-Safe)'
        ],
        'Hyperparameters': [
            'Default (n_estimators=100, max_depth=15, etc.)',
            f"Optimized (n_estimators={optimized_results['best_params']['n_estimators']}, max_depth={optimized_results['best_params']['max_depth']}, etc.)"
        ],
        'Train RMSE': [
            baseline_results['train_metrics']['RMSE'],
            'N/A (CV only)'
        ],
        'Validation RMSE': [
            baseline_results['val_metrics']['RMSE'],
            optimized_results['val_metrics']['RMSE']
        ],
        'Validation MAE': [
            baseline_results['val_metrics']['MAE'],
            optimized_results['val_metrics']['MAE']
        ],
        'Validation R²': [
            baseline_results['val_metrics']['R2'],
            optimized_results['val_metrics']['R2']
        ],
        'Best CV RMSE': [
            'N/A',
            optimized_results['best_cv_rmse']
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    
    print("\nModel Comparison Table:")
    print(comparison_df.to_string(index=False))
    
    # Calculate improvement
    baseline_val_rmse = baseline_results['val_metrics']['RMSE']
    optimized_val_rmse = optimized_results['val_metrics']['RMSE']
    improvement = ((baseline_val_rmse - optimized_val_rmse) / baseline_val_rmse) * 100
    
    print(f"\nValidation RMSE Improvement: {improvement:.2f}%")
    print(f"  Baseline: {baseline_val_rmse:.4f}")
    print(f"  Optimized: {optimized_val_rmse:.4f}")
    
    if improvement > 0:
        print(f"  Result: Optimized model is {improvement:.2f}% better")
    else:
        print(f"  Result: Baseline model is {-improvement:.2f}% better")
    
    # Save comparison
    comparison_df.to_csv(results_path / "optimization_comparison.csv", index=False)
    print(f"\nComparison saved to {results_path / 'optimization_comparison.csv'}")
    
    return comparison_df


if __name__ == "__main__":
    comparison_df = compare_models()
