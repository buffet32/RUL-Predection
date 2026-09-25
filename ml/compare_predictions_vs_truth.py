"""
Full evaluation of final model against official test set ground truth.
For academic defense presentation.
"""

import sys
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Add src directory to path
sys.path.append(str(Path(__file__).parent / 'src'))

def load_official_test_data(data_dir: str):
    """
    Load official C-MAPSS FD001 test data and ground truth RUL.
    """
    print("=" * 80)
    print("LOADING OFFICIAL TEST DATA")
    print("=" * 80)
    
    data_path = Path(data_dir)
    
    # Load test sensor data
    test_df = pd.read_csv(
        data_path / "test_FD001.txt",
        sep=' ',
        header=None,
        engine='python'
    )
    test_df = test_df.dropna(axis=1, how='all')
    
    # Assign column names
    column_names = ['engine_id', 'cycle', 'setting_1', 'setting_2', 'setting_3'] + [f'sensor_{i}' for i in range(1, 22)]
    test_df.columns = column_names
    
    # Remove constant sensors (same as training)
    constant_sensors = ['sensor_1', 'sensor_5', 'sensor_10', 'sensor_16', 'sensor_18', 'sensor_19']
    test_df = test_df.drop(columns=constant_sensors)
    
    print(f"Loaded test data: {test_df.shape}")
    
    # Load ground truth RUL
    rul_df = pd.read_csv(
        data_path / "RUL_FD001.txt",
        sep=' ',
        header=None,
        engine='python'
    )
    rul_df = rul_df.dropna(axis=1, how='all')
    rul_df.columns = ['RUL']
    rul_df['engine_id'] = range(1, 101)  # Engine IDs 1-100
    
    print(f"Loaded ground truth RUL: {rul_df.shape}")
    
    return test_df, rul_df

def extract_last_cycle_features(test_df: pd.DataFrame):
    """
    Extract the last cycle for each engine in the test set.
    This is the standard evaluation method for C-MAPSS.
    """
    print("\n" + "=" * 80)
    print("EXTRACTING LAST CYCLE FEATURES")
    print("=" * 80)
    
    # Find the last cycle for each engine
    last_cycles = test_df.groupby('engine_id').last().reset_index()
    
    print(f"Extracted last cycles for {len(last_cycles)} engines")
    
    return last_cycles

def prepare_features(test_df: pd.DataFrame):
    """
    Prepare the 18 features needed by the model.
    """
    print("\n" + "=" * 80)
    print("PREPARING FEATURES")
    print("=" * 80)
    
    # Features must match model training exactly
    feature_columns = [
        'setting_1', 'setting_2', 'setting_3',
        'sensor_2', 'sensor_3', 'sensor_4', 'sensor_6', 'sensor_7', 'sensor_8', 'sensor_9',
        'sensor_11', 'sensor_12', 'sensor_13', 'sensor_14', 'sensor_15', 'sensor_17', 'sensor_20', 'sensor_21'
    ]
    
    # Extract features and sort by engine_id
    features = test_df[feature_columns].copy()
    features['engine_id'] = test_df['engine_id']
    features = features.sort_values('engine_id')
    
    print(f"Prepared features: {features.shape}")
    print(f"Feature columns: {len(feature_columns)}")
    
    return features, feature_columns

def make_predictions(features: pd.DataFrame, feature_columns: list, model, scaler):
    """
    Scale features and make predictions using the saved model.
    """
    print("\n" + "=" * 80)
    print("MAKING PREDICTIONS")
    print("=" * 80)
    
    # Extract feature array (in correct order)
    X = features[feature_columns].values
    
    # Scale features using the fitted scaler
    X_scaled = scaler.transform(X)
    
    # Make predictions
    predictions = model.predict(X_scaled)
    
    print(f"Made {len(predictions)} predictions")
    print(f"Prediction range: {predictions.min():.2f} to {predictions.max():.2f}")
    
    return predictions

def evaluate_predictions(true_rul: np.ndarray, predicted_rul: np.ndarray):
    """
    Compute evaluation metrics and create comparison table.
    """
    print("\n" + "=" * 80)
    print("EVALUATING PREDICTIONS")
    print("=" * 80)
    
    # Compute metrics
    rmse = np.sqrt(mean_squared_error(true_rul, predicted_rul))
    mae = mean_absolute_error(true_rul, predicted_rul)
    r2 = r2_score(true_rul, predicted_rul)
    
    print(f"\nOfficial Test Metrics:")
    print(f"  RMSE: {rmse:.4f} cycles")
    print(f"  MAE: {mae:.4f} cycles")
    print(f"  R²: {r2:.4f}")
    
    # Create comparison table
    comparison_df = pd.DataFrame({
        'engine_id': range(1, 101),
        'true_rul': true_rul,
        'predicted_rul': predicted_rul,
        'error': predicted_rul - true_rul,
        'abs_error': np.abs(predicted_rul - true_rul)
    })
    
    print(f"\nComparison table: {comparison_df.shape}")
    
    return comparison_df, rmse, mae, r2

def create_scatter_plot(comparison_df: pd.DataFrame, save_path: Path):
    """
    Create scatter plot of predicted vs true RUL with diagonal line.
    """
    print("\n" + "=" * 80)
    print("CREATING SCATTER PLOT")
    print("=" * 80)
    
    plt.figure(figsize=(10, 8))
    
    # Scatter plot
    plt.scatter(comparison_df['true_rul'], comparison_df['predicted_rul'], 
                alpha=0.6, s=50, edgecolors='k', linewidth=0.5)
    
    # Diagonal line (perfect prediction)
    max_val = max(comparison_df['true_rul'].max(), comparison_df['predicted_rul'].max())
    plt.plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='Perfect Prediction')
    
    plt.xlabel('True RUL (cycles)', fontsize=12)
    plt.ylabel('Predicted RUL (cycles)', fontsize=12)
    plt.title('Predicted vs True RUL - Official Test Set', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    
    # Add metrics to plot
    rmse = np.sqrt(mean_squared_error(comparison_df['true_rul'], comparison_df['predicted_rul']))
    mae = mean_absolute_error(comparison_df['true_rul'], comparison_df['predicted_rul'])
    r2 = r2_score(comparison_df['true_rul'], comparison_df['predicted_rul'])
    
    plt.text(0.05, 0.95, f'RMSE: {rmse:.2f} cycles\nMAE: {mae:.2f} cycles\nR²: {r2:.3f}',
             transform=plt.gca().transAxes,
             fontsize=11,
             verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Scatter plot saved to: {save_path}")
    plt.close()

def save_comparison_table(comparison_df: pd.DataFrame, save_path: Path):
    """
    Save comparison table to CSV.
    """
    print("\n" + "=" * 80)
    print("SAVING COMPARISON TABLE")
    print("=" * 80)
    
    comparison_df.to_csv(save_path, index=False)
    print(f"Comparison table saved to: {save_path}")

def compare_with_documented(computed_rmse: float, computed_mae: float, 
                          documented_rmse: float = 31.73, documented_mae: float = 23.39):
    """
    Compare computed metrics with documented values.
    """
    print("\n" + "=" * 80)
    print("COMPARISON WITH DOCUMENTED VALUES")
    print("=" * 80)
    
    print(f"\nDocumented Metrics:")
    print(f"  RMSE: {documented_rmse:.2f} cycles")
    print(f"  MAE: {documented_mae:.2f} cycles")
    
    print(f"\nComputed Metrics:")
    print(f"  RMSE: {computed_rmse:.2f} cycles")
    print(f"  MAE: {computed_mae:.2f} cycles")
    
    rmse_diff = abs(computed_rmse - documented_rmse)
    mae_diff = abs(computed_mae - documented_mae)
    
    print(f"\nDifferences:")
    print(f"  RMSE difference: {rmse_diff:.2f} cycles ({rmse_diff/documented_rmse*100:.1f}%)")
    print(f"  MAE difference: {mae_diff:.2f} cycles ({mae_diff/documented_mae*100:.1f}%)")
    
    # Allow small tolerance for floating point precision
    tolerance = 0.1
    if rmse_diff < tolerance and mae_diff < tolerance:
        print("\n[OK] Metrics MATCH documented values (within tolerance)")
    else:
        print(f"\n[WARNING] Metrics differ from documented values by more than {tolerance} cycles")
        print("   This could be due to:")
        print("   - Different data preprocessing")
        print("   - Different engine selection")
        print("   - Different evaluation method")
        print("   - Rounding differences")

def main():
    """
    Main evaluation function.
    """
    print("=" * 80)
    print("OFFICIAL TEST SET EVALUATION")
    print("For Academic Defense Presentation")
    print("=" * 80)
    
    # Configuration
    data_dir = "C:/Users/ULTRAPC/Downloads/archive"
    models_dir = Path(__file__).parent.parent / "models"
    results_dir = Path(__file__).parent / "results"
    
    # Load model and scaler
    print("\nLoading model and scaler...")
    model = joblib.load(models_dir / "final_rul_model.joblib")
    scaler = joblib.load(models_dir / "preprocessing_pipeline.joblib")
    print(f"Model: {model}")
    print(f"Scaler loaded")
    
    # Load official test data
    test_df, rul_df = load_official_test_data(data_dir)
    
    # Extract last cycle features
    last_cycles = extract_last_cycle_features(test_df)
    
    # Prepare features
    features, feature_columns = prepare_features(last_cycles)
    
    # Make predictions
    predictions = make_predictions(features, feature_columns, model, scaler)
    
    # Get true RUL values (in engine_id order 1-100)
    true_rul = rul_df.sort_values('engine_id')['RUL'].values
    
    # Evaluate predictions
    comparison_df, rmse, mae, r2 = evaluate_predictions(true_rul, predictions)
    
    # Print first 20 rows of comparison table
    print("\n" + "=" * 80)
    print("COMPARISON TABLE (First 20 Rows)")
    print("=" * 80)
    print(comparison_df.head(20).to_string(index=False))
    
    # Print worst predictions
    print("\n" + "=" * 80)
    print("WORST PREDICTIONS (Top 10 by Absolute Error)")
    print("=" * 80)
    worst_predictions = comparison_df.nlargest(10, 'abs_error')
    print(worst_predictions.to_string(index=False))
    
    # Compare with documented values
    compare_with_documented(rmse, mae)
    
    # Create scatter plot
    plot_path = results_dir / "predictions_vs_truth.png"
    create_scatter_plot(comparison_df, plot_path)
    
    # Save comparison table
    csv_path = results_dir / "predictions_vs_truth.csv"
    save_comparison_table(comparison_df, csv_path)
    
    print("\n" + "=" * 80)
    print("EVALUATION COMPLETE")
    print("=" * 80)
    print(f"\nResults saved to:")
    print(f"  - Scatter plot: {plot_path}")
    print(f"  - Comparison table: {csv_path}")
    print(f"\nOfficial Test RMSE: {rmse:.4f} cycles")
    print(f"Official Test MAE: {mae:.4f} cycles")
    print(f"Official Test R²: {r2:.4f}")

if __name__ == "__main__":
    main()
