"""
Compare Original vs Deployment-Safe Models
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
    Compare original (with leakage) vs deployment-safe models
    """
    print("=" * 80)
    print("MODEL COMPARISON: ORIGINAL vs DEPLOYMENT-SAFE")
    print("=" * 80)
    
    results_path = Path("../results")
    
    # Load results
    baseline_results = load_results(results_path / "baseline_results.json")
    deployment_safe_results = load_results(results_path / "deployment_safe_results.json")
    
    # Create comparison data
    comparison_data = {
        'Model': [
            'Random Forest (Original - with relative_cycle)',
            'Random Forest (Deployment-Safe - NO relative_cycle)'
        ],
        'Relative Cycle': ['YES (DATA LEAKAGE)', 'NO (DEPLOYMENT SAFE)'],
        'Deployment Safe': ['NO', 'YES'],
        'Validation RMSE': [
            baseline_results['val_metrics']['RMSE'],
            deployment_safe_results['val_metrics']['RMSE']
        ],
        'Validation MAE': [
            baseline_results['val_metrics']['MAE'],
            deployment_safe_results['val_metrics']['MAE']
        ],
        'Validation R²': [
            baseline_results['val_metrics']['R2'],
            deployment_safe_results['val_metrics']['R2']
        ],
        'Internal Test RMSE': [
            baseline_results['test_metrics']['RMSE'],
            deployment_safe_results['test_metrics']['RMSE']
        ],
        'Internal Test MAE': [
            baseline_results['test_metrics']['MAE'],
            deployment_safe_results['test_metrics']['MAE']
        ],
        'Internal Test R²': [
            baseline_results['test_metrics']['R2'],
            deployment_safe_results['test_metrics']['R2']
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    
    print("\nModel Comparison Table:")
    print(comparison_df.to_string(index=False))
    
    # Save comparison
    comparison_df.to_csv(results_path / "leakage_comparison.csv", index=False)
    print(f"\nComparison saved to {results_path / 'leakage_comparison.csv'}")
    
    # Calculate performance degradation
    val_rmse_degradation = (
        (deployment_safe_results['val_metrics']['RMSE'] - baseline_results['val_metrics']['RMSE']) / 
        baseline_results['val_metrics']['RMSE'] * 100
    )
    
    print("\n" + "=" * 80)
    print("PERFORMANCE ANALYSIS")
    print("=" * 80)
    print(f"\nValidation RMSE degradation: {val_rmse_degradation:.1f}%")
    print(f"  Original: {baseline_results['val_metrics']['RMSE']:.2f}")
    print(f"  Deployment-Safe: {deployment_safe_results['val_metrics']['RMSE']:.2f}")
    
    print("\nInterpretation:")
    print("  The performance degradation is expected and honest.")
    print("  The original model used relative_cycle which encodes the answer.")
    print("  The deployment-safe model must rely on sensor degradation patterns.")
    print("  This is the true predictive capability without data leakage.")
    
    return comparison_df


if __name__ == "__main__":
    comparison_df = compare_models()
