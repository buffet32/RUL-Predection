from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Machine, Prediction
from typing import List

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


@router.get("/status/{machine_id}")
async def get_maintenance_status(machine_id: int, db: Session = Depends(get_db)):
    """
    Get the current maintenance status for a machine based on the latest prediction
    """
    # Verify machine exists
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    # Get latest prediction for this machine
    latest_prediction = db.query(Prediction).filter(
        Prediction.machine_id == machine_id
    ).order_by(Prediction.timestamp.desc()).first()
    
    if not latest_prediction:
        return {
            "machine_id": machine_id,
            "status": "NO_DATA",
            "message": "No predictions available for this machine"
        }
    
    return {
        "machine_id": machine_id,
        "status": latest_prediction.maintenance_status,
        "predicted_rul": latest_prediction.predicted_rul,
        "effective_rul": latest_prediction.effective_rul,
        "health_score": latest_prediction.health_score,
        "last_prediction_timestamp": latest_prediction.timestamp
    }


@router.get("/summary")
async def get_maintenance_summary(db: Session = Depends(get_db)):
    """
    Get a summary of maintenance status across all machines
    """
    # Get latest prediction for each machine
    subquery = db.query(
        Prediction.machine_id,
        func.max(Prediction.timestamp).label('max_timestamp')
    ).group_by(Prediction.machine_id).subquery()
    
    latest_predictions = db.query(Prediction).join(
        subquery,
        (Prediction.machine_id == subquery.c.machine_id) &
        (Prediction.timestamp == subquery.c.max_timestamp)
    ).all()
    
    # Count by status
    status_counts = {
        'NORMAL': 0,
        'MONITOR': 0,
        'MAINTENANCE_RECOMMENDED': 0,
        'CRITICAL': 0,
        'NO_DATA': 0
    }
    
    for prediction in latest_predictions:
        status = prediction.maintenance_status
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts['NO_DATA'] += 1
    
    summary = {
        "normal_count": status_counts['NORMAL'],
        "monitor_count": status_counts['MONITOR'],
        "maintenance_count": status_counts['MAINTENANCE_RECOMMENDED'],
        "critical_count": status_counts['CRITICAL'],
        "total_machines": len(set(p.machine_id for p in latest_predictions)),
        "status_breakdown": status_counts
    }
    
    return summary
