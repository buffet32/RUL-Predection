"""
Model Comparison and Error Analysis
"""

import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from utils import load_results, plot_predictions, plot_residuals, plot_error_distribution, plot_rul_vs_error


def compare_models(results_dir: str = "../results"):
    """
    Compare all trained models and create comparison table
    
    Args:
        results_dir: Path to results directory
    """
    print("=" * 80)
    print("MODEL COMPARISON")
    print("=" * 80)
    
    results_path = Path(results_dir)
    
    # Load all results
    baseline_results = load_results(results_path / "baseline_results.json")
    rf_ts_results = load_results(results_path / "random_forest_ts_results.json")
    xgb_ts_results = load_results(results_path / "xgboost_ts_results.json")
    
    # Create comparison table
    comparison_data = []
    
    for model_name, results in [
        ("Random Forest (Baseline)", baseline_results),
        ("Random Forest (Time-Series)", rf_ts_results),
        ("XGBoost (Time-Series)", xgb_ts_results)
    ]:
        comparison_data.append({
            'Model': model_name,
            'Features': results['features'],
            'Val_RMSE': results['val_metrics']['RMSE'],
            'Val_MAE': results['val_metrics']['MAE'],
            'Val_R2': results['val_metrics']['R2'],
            'Test_RMSE': results['test_metrics']['RMSE'],
            'Test_MAE': results['test_metrics']['MAE'],
            'Test_R2': results['test_metrics']['R2']
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    print("\nModel Comparison Table:")
    print(comparison_df.to_string(index=False))
    
    # Save comparison table
    comparison_df.to_csv(results_path / "model_comparison.csv", index=False)
    print(f"\nComparison table saved to {results_path / 'model_comparison.csv'}")
    
    return comparison_df


def perform_error_analysis(results_dir: str = "../results", viz_dir: str = "../visualizations"):
    """
    Perform detailed error analysis
    
    Args:
        results_dir: Path to results directory
        viz_dir: Path to visualizations directory
    """
    print("\n" + "=" * 80)
    print("ERROR ANALYSIS")
    print("=" * 80)
    
    results_path = Path(results_dir)
    viz_path = Path(viz_dir)
    viz_path.mkdir(exist_ok=True)
    
    # Load results
    baseline_results = load_results(results_path / "baseline_results.json")
    rf_ts_results = load_results(results_path / "random_forest_ts_results.json")
    xgb_ts_results = load_results(results_path / "xgboost_ts_results.json")
    
    # Analyze which model performed best
    models = [
        ("Random Forest (Baseline)", baseline_results),
        ("Random Forest (Time-Series)", rf_ts_results),
        ("XGBoost (Time-Series)", xgb_ts_results)
    ]
    
    best_val_rmse = min(m[1]['val_metrics']['RMSE'] for m in models)
    best_model = [m[0] for m in models if m[1]['val_metrics']['RMSE'] == best_val_rmse][0]
    
    print(f"\nBest model by Validation RMSE: {best_model}")
    print(f"Validation RMSE: {best_val_rmse:.4f}")
    
    # Analyze overfitting
    print("\nOverfitting Analysis:")
    for model_name, results in models:
        train_rmse = results['train_metrics']['RMSE']
        val_rmse = results['val_metrics']['RMSE']
        overfitting_ratio = val_rmse / train_rmse
        print(f"  {model_name}:")
        print(f"    Train RMSE: {train_rmse:.4f}")
        print(f"    Val RMSE: {val_rmse:.4f}")
        print(f"    Overfitting ratio: {overfitting_ratio:.2f}")
    
    # Feature importance analysis
    print("\nFeature Importance Analysis:")
    print("  Random Forest (Baseline) - Top 5 features:")
    if 'feature_columns' in baseline_results:
        # We don't have feature importance in the saved results, but we can note this
        print("    (Feature importance plot saved in visualizations)")
    
    print("\n  Random Forest (Time-Series) - Top 5 features:")
    print("    (Feature importance plot saved in visualizations)")
    
    print("\n  XGBoost (Time-Series) - Top 5 features:")
    print("    (Feature importance plot saved in visualizations)")
    
    # Create summary visualization
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # RMSE comparison
    model_names = [m[0] for m in models]
    val_rmse = [m[1]['val_metrics']['RMSE'] for m in models]
    test_rmse = [m[1]['test_metrics']['RMSE'] for m in models]
    
    x = np.arange(len(model_names))
    width = 0.35
    
    axes[0].bar(x - width/2, val_rmse, width, label='Validation', alpha=0.8)
    axes[0].bar(x + width/2, test_rmse, width, label='Test', alpha=0.8)
    axes[0].set_ylabel('RMSE')
    axes[0].set_title('RMSE Comparison')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(model_names, rotation=15, ha='right')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # MAE comparison
    val_mae = [m[1]['val_metrics']['MAE'] for m in models]
    test_mae = [m[1]['test_metrics']['MAE'] for m in models]
    
    axes[1].bar(x - width/2, val_mae, width, label='Validation', alpha=0.8)
    axes[1].bar(x + width/2, test_mae, width, label='Test', alpha=0.8)
    axes[1].set_ylabel('MAE')
    axes[1].set_title('MAE Comparison')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(model_names, rotation=15, ha='right')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # R² comparison
    val_r2 = [m[1]['val_metrics']['R2'] for m in models]
    test_r2 = [m[1]['test_metrics']['R2'] for m in models]
    
    axes[2].bar(x - width/2, val_r2, width, label='Validation', alpha=0.8)
    axes[2].bar(x + width/2, test_r2, width, label='Test', alpha=0.8)
    axes[2].set_ylabel('R²')
    axes[2].set_title('R² Comparison')
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(model_names, rotation=15, ha='right')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(viz_path / "model_comparison.png", dpi=150, bbox_inches='tight')
    print(f"\nModel comparison plot saved to {viz_path / 'model_comparison.png'}")
    plt.close()
    
    # Save error analysis summary
    error_analysis = {
        'best_model': best_model,
        'best_val_rmse': best_val_rmse,
        'overfitting_analysis': [
            {
                'model': m[0],
                'train_rmse': m[1]['train_metrics']['RMSE'],
                'val_rmse': m[1]['val_metrics']['RMSE'],
                'overfitting_ratio': m[1]['val_metrics']['RMSE'] / m[1]['train_metrics']['RMSE']
            }
            for m in models
        ]
    }
    
    with open(results_path / "error_analysis.json", 'w') as f:
        json.dump(error_analysis, f, indent=2)
    
    print(f"Error analysis saved to {results_path / 'error_analysis.json'}")
    
    return error_analysis


if __name__ == "__main__":
    comparison_df = compare_models()
    error_analysis = perform_error_analysis()
    
    print("\n" + "=" * 80)
    print("MODEL COMPARISON AND ERROR ANALYSIS COMPLETE")
    print("=" * 80)
