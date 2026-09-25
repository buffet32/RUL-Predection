from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Machine Schemas
class MachineBase(BaseModel):
    name: str = Field(..., description="Machine identifier")
    model: Optional[str] = Field(None, description="Machine model")
    description: Optional[str] = Field(None, description="Machine description")
    location: Optional[str] = Field(None, description="Machine location")


class MachineCreate(MachineBase):
    pass


class MachineUpdate(BaseModel):
    model: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None


class MachineResponse(MachineBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Sensor Reading Schemas
class SensorReadingBase(BaseModel):
    machine_id: int = Field(..., description="Machine ID")
    cycle: int = Field(..., description="Current cycle")
    setting_1: float
    setting_2: float
    setting_3: float
    sensor_2: float
    sensor_3: float
    sensor_4: float
    sensor_6: float
    sensor_7: float
    sensor_8: float
    sensor_9: float
    sensor_11: float
    sensor_12: float
    sensor_13: float
    sensor_14: float
    sensor_15: float
    sensor_17: float
    sensor_20: float
    sensor_21: float


class SensorReadingCreate(SensorReadingBase):
    pass


class SensorReadingResponse(SensorReadingBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


# Prediction Schemas
class PredictionRequest(BaseModel):
    machine_id: int = Field(..., description="Machine ID")
    cycle: int = Field(..., description="Current cycle")
    setting_1: float
    setting_2: float
    setting_3: float
    sensor_2: float
    sensor_3: float
    sensor_4: float
    sensor_6: float
    sensor_7: float
    sensor_8: float
    sensor_9: float
    sensor_11: float
    sensor_12: float
    sensor_13: float
    sensor_14: float
    sensor_15: float
    sensor_17: float
    sensor_20: float
    sensor_21: float


class PredictionResponse(BaseModel):
    id: int
    machine_id: int
    timestamp: datetime
    predicted_rul: float
    effective_rul: float
    health_score: float
    maintenance_status: str
    safety_margin_applied: float
    
    class Config:
        from_attributes = True


# Health Check Schema
class HealthCheckResponse(BaseModel):
    status: str
    app_name: str
    app_version: str
    database_connected: bool
    model_loaded: bool
