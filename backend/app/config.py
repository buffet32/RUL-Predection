from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "Predictive Maintenance API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/predictive_maintenance"
    
    # ML Model Paths (relative to project root)
    MODEL_PATH: str = "models/final_rul_model.joblib"
    SCALER_PATH: str = "models/preprocessing_pipeline.joblib"
    DECISION_CONFIG_PATH: str = "ml/results/decision_layer_config.json"
    
    # API
    API_PREFIX: str = "/api/v1"
    
    # LLM Integration
    ANTHROPIC_API_KEY: Optional[str] = None
    
    def get_project_root(self) -> Path:
        """Get the project root directory"""
        return Path(__file__).parent.parent.parent
    
    def get_model_path(self) -> Path:
        """Get absolute path to model file"""
        return self.get_project_root() / self.MODEL_PATH
    
    def get_scaler_path(self) -> Path:
        """Get absolute path to scaler file"""
        return self.get_project_root() / self.SCALER_PATH
    
    def get_decision_config_path(self) -> Path:
        """Get absolute path to decision config file"""
        return self.get_project_root() / self.DECISION_CONFIG_PATH
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
