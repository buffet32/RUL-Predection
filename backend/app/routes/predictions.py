from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Machine, SensorReading, Prediction
from app.schemas import PredictionRequest, PredictionResponse
from app.services.prediction_service import prediction_service

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.post("/", response_model=PredictionResponse, status_code=201)
async def create_prediction(request: PredictionRequest, db: Session = Depends(get_db)):
    """
    Create a RUL prediction for a machine based on sensor data
    """
    # Verify machine exists
    machine = db.query(Machine).filter(Machine.id == request.machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    # Make prediction using ML model
    sensor_data = request.model_dump()
    prediction_result = prediction_service.predict(sensor_data)
    
    # Store sensor reading
    sensor_reading = SensorReading(**sensor_data)
    db.add(sensor_reading)
    db.commit()
    db.refresh(sensor_reading)
    
    # Store prediction
    db_prediction = Prediction(
        machine_id=request.machine_id,
        sensor_reading_id=sensor_reading.id,
        predicted_rul=prediction_result['predicted_rul'],
        effective_rul=prediction_result['effective_rul'],
        health_score=prediction_result['health_score'],
        maintenance_status=prediction_result['maintenance_status'],
        safety_margin_applied=prediction_result['safety_margin_applied']
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    return db_prediction


@router.get("/", response_model=list[PredictionResponse])
async def get_predictions(
    machine_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get prediction history with optional machine filter and pagination
    """
    query = db.query(Prediction)
    
    if machine_id:
        query = query.filter(Prediction.machine_id == machine_id)
    
    predictions = query.order_by(Prediction.timestamp.desc()).offset(skip).limit(limit).all()
    return predictions


@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    """
    Get a specific prediction by ID
    """
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction
