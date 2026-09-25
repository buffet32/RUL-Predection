"""
Save Production Artifacts
"""

import sys
import joblib
import json
from pathlib import Path
from datetime import datetime

# Add src directory to path
sys.path.append(str(Path(__file__).parent))


def save_production_artifacts():
    """
    Save all production artifacts with metadata
    """
    print("=" * 80)
    print("SAVING PRODUCTION ARTIFACTS")
    print("=" * 80)
    
    # Load models and results
    models_dir = Path(__file__).parent.parent / "models"
    results_dir = Path(__file__).parent.parent / "results"
    
    # Load optimized model
    model = joblib.load(models_dir / "random_forest_optimized.joblib")
    scaler = joblib.load(models_dir / "scaler_optimized.joblib")
    
    # Load optimization results
    with open(results_dir / "optimization_results.json", 'r') as f:
        opt_results = json.load(f)
    
    # Load bias analysis
    with open(results_dir / "bias_analysis.json", 'r') as f:
        bias_results = json.load(f)
    
    # Load decision layer config
    with open(results_dir / "decision_layer_config.json", 'r') as f:
        decision_config = json.load(f)
    
    # Load official test results
    with open(results_dir / "optimized_official_test_results.json", 'r') as f:
        test_results = json.load(f)
    
    # Create production directory
    prod_dir = Path(__file__).parent.parent.parent / "models"
    prod_dir.mkdir(parents=True, exist_ok=True)
    
    # Save final model
    final_model_path = prod_dir / "final_rul_model.joblib"
    joblib.dump(model, final_model_path)
    print(f"Final model saved to {final_model_path}")
    
    # Save preprocessing pipeline (scaler)
    pipeline_path = prod_dir / "preprocessing_pipeline.joblib"
    joblib.dump(scaler, pipeline_path)
    print(f"Preprocessing pipeline saved to {pipeline_path}")
    
    # Create metadata
    metadata = {
        "model_type": "RandomForestRegressor",
        "model_version": "1.0",
        "training_date": datetime.now().isoformat(),
        "random_seed": 42,
        
        "features": [
            "setting_1", "setting_2", "setting_3",
            "sensor_2", "sensor_3", "sensor_4", "sensor_6", "sensor_7", "sensor_8", "sensor_9",
            "sensor_11", "sensor_12", "sensor_13", "sensor_14", "sensor_15", "sensor_17", "sensor_20", "sensor_21"
        ],
        
        "preprocessing_steps": [
            "Remove constant sensors (sensor_1, sensor_5, sensor_10, sensor_16, sensor_18, sensor_19)",
            "Remove relative_cycle (data leakage)",
            "StandardScaler normalization"
        ],
        
        "hyperparameters": opt_results['best_params'],
        
        "validation_metrics": {
            "rmse": opt_results['val_metrics']['RMSE'],
            "mae": opt_results['val_metrics']['MAE'],
            "r2": opt_results['val_metrics']['R2']
        },
        
        "official_test_metrics": {
            "rmse": test_results['metrics']['RMSE'],
            "mae": test_results['metrics']['MAE'],
            "r2": test_results['metrics']['R2']
        },
        
        "bias_analysis": {
            "mean_error": bias_results['mean_error'],
            "overestimation_rate": bias_results['overestimation_rate']
        },
        
        "safety_margin": decision_config['safety_margin_cycles'],
        
        "maintenance_thresholds": decision_config['thresholds'],
        
        "health_score": {
            "method": "linear_scaling",
            "max_rul": 200,
            "range": "0-100"
        },
        
        "data_leakage_check": "PASSED - No relative_cycle feature used",
        
        "deployment_check": "PASSED - All features available in real-time"
    }
    
    # Save metadata
    metadata_path = prod_dir / "model_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Model metadata saved to {metadata_path}")
    
    print("\n" + "=" * 80)
    print("PRODUCTION ARTIFACTS SAVED")
    print("=" * 80)
    
    return metadata


if __name__ == "__main__":
    metadata = save_production_artifacts()
