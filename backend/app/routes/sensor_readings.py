from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SensorReading
from app.schemas import SensorReadingCreate, SensorReadingResponse

router = APIRouter(prefix="/sensor-readings", tags=["sensor-readings"])


@router.post("/", response_model=SensorReadingResponse, status_code=201)
async def create_sensor_reading(reading: SensorReadingCreate, db: Session = Depends(get_db)):
    """
    Store a sensor reading for a machine
    """
    # Verify machine exists
    from app.models import Machine
    machine = db.query(Machine).filter(Machine.id == reading.machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    db_reading = SensorReading(**reading.model_dump())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    
    return db_reading


@router.get("/", response_model=List[SensorReadingResponse])
async def get_sensor_readings(
    machine_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get sensor readings with optional machine filter and pagination
    """
    query = db.query(SensorReading)
    
    if machine_id:
        query = query.filter(SensorReading.machine_id == machine_id)
    
    readings = query.order_by(SensorReading.timestamp.desc()).offset(skip).limit(limit).all()
    return readings


@router.get("/{reading_id}", response_model=SensorReadingResponse)
async def get_sensor_reading(reading_id: int, db: Session = Depends(get_db)):
    """
    Get a specific sensor reading by ID
    """
    reading = db.query(SensorReading).filter(SensorReading.id == reading_id).first()
    if not reading:
        raise HTTPException(status_code=404, detail="Sensor reading not found")
    return reading
