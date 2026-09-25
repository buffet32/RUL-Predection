import sys
from pathlib import Path
import importlib.util

# Add ml/src to path for importing prediction logic
# The file is in backend/app/services/prediction_service.py
# We need to go up 3 levels to reach the project root, then down to ml/src
project_root = Path(__file__).resolve().parent.parent.parent.parent
ml_src_path = project_root / "ml" / "src"
if str(ml_src_path) not in sys.path:
    sys.path.append(str(ml_src_path))

import joblib
from app.config import settings


class PredictionService:
    """Service for RUL predictions using the trained ML model"""

    def __init__(self):
        """Initialize the prediction service by loading the model"""
        self.model = None
        self.scaler = None
        self.decision_layer = None
        self._load_model()

    def _load_model(self):
        """Load the trained model and preprocessing pipeline"""
        try:
            # Load model using config helper method
            model_path = settings.get_model_path()
            self.model = joblib.load(model_path)

            # Load scaler using config helper method
            scaler_path = settings.get_scaler_path()
            self.scaler = joblib.load(scaler_path)

            # Load decision layer using importlib for reliable module loading
            spec = importlib.util.spec_from_file_location(
                "maintenance_decision",
                ml_src_path / "maintenance_decision.py",
            )
            if spec is None or spec.loader is None:
                raise ImportError("Could not load maintenance_decision module")

            maintenance_decision_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(maintenance_decision_module)
            MaintenanceDecisionLayer = maintenance_decision_module.MaintenanceDecisionLayer

            config_path = settings.get_decision_config_path()
            self.decision_layer = MaintenanceDecisionLayer.load_config(config_path)

            print("[OK] ML model and decision layer loaded successfully")
        except Exception as e:
            print(f"⚠ Warning: ML models not available: {e}")
            print("  Continuing without ML model features (audit system will work)")
            # Don't raise - allow backend to start anyway
            self.model = None
            self.scaler = None
            self.decision_layer = None

    def predict(self, sensor_data: dict) -> dict:
        """
        Make RUL prediction from sensor data

        Args:
            sensor_data: Dictionary with sensor readings

        Returns:
            Dictionary with prediction results
        """
        if self.model is None or self.scaler is None or self.decision_layer is None:
            raise RuntimeError("Model not loaded")

        # Extract features in correct order
        feature_order = [
            "setting_1",
            "setting_2",
            "setting_3",
            "sensor_2",
            "sensor_3",
            "sensor_4",
            "sensor_6",
            "sensor_7",
            "sensor_8",
            "sensor_9",
            "sensor_11",
            "sensor_12",
            "sensor_13",
            "sensor_14",
            "sensor_15",
            "sensor_17",
            "sensor_20",
            "sensor_21",
        ]

        # Create feature array
        import numpy as np

        X = np.array([[sensor_data[feature] for feature in feature_order]])

        # Scale features
        X_scaled = self.scaler.transform(X)

        # Predict RUL
        predicted_rul = self.model.predict(X_scaled)[0]

        # Apply decision layer
        decision_result = self.decision_layer.process_prediction(predicted_rul)

        return decision_result

    def is_loaded(self) -> bool:
        """Check if the model is loaded"""
        return self.model is not None and self.scaler is not None and self.decision_layer is not None


# Global prediction service instance
# Now safely handles missing models
prediction_service = PredictionService()