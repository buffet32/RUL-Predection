"""
Prediction Interface for RUL Prediction
"""

import sys
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from maintenance_decision import MaintenanceDecisionLayer


class RULPredictor:
    """
    RUL Prediction interface for deployment
    """
    
    def __init__(self, model_path=None, scaler_path=None, config_path=None):
        """
        Initialize predictor with saved artifacts
        
        Args:
            model_path: Path to saved model
            scaler_path: Path to saved scaler
            config_path: Path to decision layer config
        """
        # Default paths
        if model_path is None:
            model_path = Path(__file__).parent.parent.parent / "models" / "final_rul_model.joblib"
        if scaler_path is None:
            scaler_path = Path(__file__).parent.parent.parent / "models" / "preprocessing_pipeline.joblib"
        if config_path is None:
            config_path = Path(__file__).parent.parent / "results" / "decision_layer_config.json"
        
        # Load artifacts
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.decision_layer = MaintenanceDecisionLayer.load_config(config_path)
        
        # Feature columns (must match training)
        self.feature_columns = [
            'setting_1', 'setting_2', 'setting_3',
            'sensor_2', 'sensor_3', 'sensor_4', 'sensor_6', 'sensor_7', 'sensor_8', 'sensor_9',
            'sensor_11', 'sensor_12', 'sensor_13', 'sensor_14', 'sensor_15', 'sensor_17', 'sensor_20', 'sensor_21'
        ]
    
    def predict_rul(self, sensor_data):
        """
        Predict RUL from sensor data

        Args:
            sensor_data: Dictionary or DataFrame with sensor readings
                        Must contain: setting_1, setting_2, setting_3, and 15 sensor values

        Returns:
            Dictionary with prediction results

        Raises:
            ValueError: If input validation fails
        """
        # Convert to DataFrame if dict
        if isinstance(sensor_data, dict):
            sensor_data = pd.DataFrame([sensor_data])

        # Validate input
        self._validate_input(sensor_data)

        # Extract features
        X = sensor_data[self.feature_columns].values

        # Scale features
        X_scaled = self.scaler.transform(X)

        # Predict RUL
        predicted_rul = self.model.predict(X_scaled)[0]

        # Apply decision layer
        decision_result = self.decision_layer.process_prediction(predicted_rul)

        return decision_result

    def _validate_input(self, sensor_data):
        """
        Validate sensor data before prediction

        Args:
            sensor_data: DataFrame with sensor readings

        Raises:
            ValueError: If validation fails
        """
        # Check for missing features
        missing_features = set(self.feature_columns) - set(sensor_data.columns)
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")

        # Check for NaN or Inf values
        if sensor_data[self.feature_columns].isnull().any().any():
            raise ValueError("Input contains NaN values")

        if np.isinf(sensor_data[self.feature_columns].values).any():
            raise ValueError("Input contains infinite values")

        # Define reasonable ranges for sensor validation
        # Based on NASA C-MAPSS dataset statistics
        sensor_ranges = {
            'setting_1': (-0.1, 0.1),
            'setting_2': (-0.01, 0.01),
            'setting_3': (80, 120),
            'sensor_2': (500, 550),
            'sensor_3': (600, 700),
            'sensor_4': (1400, 1700),
            'sensor_6': (10, 25),
            'sensor_7': (15, 30),
            'sensor_8': (500, 600),
            'sensor_9': (2000, 2500),
            'sensor_11': (40, 55),
            'sensor_12': (500, 550),
            'sensor_13': (2000, 2500),
            'sensor_14': (7500, 9000),
            'sensor_15': (5, 15),
            'sensor_17': (350, 450),
            'sensor_20': (30, 45),
            'sensor_21': (20, 30)
        }

        # Validate ranges
        for feature in self.feature_columns:
            if feature in sensor_ranges:
                min_val, max_val = sensor_ranges[feature]
                values = sensor_data[feature].values
                if np.any(values < min_val) or np.any(values > max_val):
                    raise ValueError(
                        f"{feature} value out of expected range [{min_val}, {max_val}]. "
                        f"Got: {values[0]:.2f}"
                    )
    
    def predict_batch(self, sensor_data_list):
        """
        Predict RUL for multiple sensor readings
        
        Args:
            sensor_data_list: List of dictionaries or DataFrame with multiple rows
        
        Returns:
            List of prediction results
        """
        results = []
        
        # Convert to DataFrame if list of dicts
        if isinstance(sensor_data_list, list) and isinstance(sensor_data_list[0], dict):
            sensor_data_list = pd.DataFrame(sensor_data_list)
        
        # Extract features
        X = sensor_data_list[self.feature_columns].values
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Predict RUL
        predicted_ruls = self.model.predict(X_scaled)
        
        # Apply decision layer to each prediction
        for rul in predicted_ruls:
            decision_result = self.decision_layer.process_prediction(rul)
            results.append(decision_result)
        
        return results


def predict_rul(sensor_data):
    """
    Simple prediction function for FastAPI integration
    
    Args:
        sensor_data: Dictionary with sensor readings
    
    Returns:
        Dictionary with prediction results
    """
    predictor = RULPredictor()
    return predictor.predict_rul(sensor_data)


if __name__ == "__main__":
    # Test prediction interface
    print("=" * 80)
    print("TESTING PREDICTION INTERFACE")
    print("=" * 80)
    
    # Create sample sensor data
    sample_data = {
        'setting_1': 0.0,
        'setting_2': 0.0,
        'setting_3': 100.0,
        'sensor_2': 518.67,
        'sensor_3': 641.82,
        'sensor_4': 1589.24,
        'sensor_6': 14.62,
        'sensor_7': 21.61,
        'sensor_8': 550.69,
        'sensor_9': 2388.06,
        'sensor_11': 47.54,
        'sensor_12': 521.61,
        'sensor_13': 2388.02,
        'sensor_14': 8142.44,
        'sensor_15': 8.31,
        'sensor_17': 391.00,
        'sensor_20': 39.14,
        'sensor_21': 23.29
    }
    
    print("\nSample sensor data:")
    for key, value in sample_data.items():
        print(f"  {key}: {value}")
    
    # Make prediction
    result = predict_rul(sample_data)
    
    print("\nPrediction Result:")
    print(f"  Predicted RUL: {result['predicted_rul']:.2f} cycles")
    print(f"  Effective RUL: {result['effective_rul']:.2f} cycles")
    print(f"  Safety Margin Applied: {result['safety_margin_applied']} cycles")
    print(f"  Health Score: {result['health_score']:.1f}/100")
    print(f"  Maintenance Status: {result['maintenance_status']}")
    
    print("\n" + "=" * 80)
    print("PREDICTION INTERFACE TEST COMPLETE")
    print("=" * 80)
