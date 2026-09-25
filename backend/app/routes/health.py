from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas import HealthCheckResponse
from app.services.prediction_service import prediction_service
from app.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint to verify API and database status
    """
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
        database_connected = True
    except Exception:
        database_connected = False

    return HealthCheckResponse(
        status="healthy" if database_connected and prediction_service.is_loaded() else "unhealthy",
        app_name=settings.APP_NAME,
        app_version=settings.APP_VERSION,
        database_connected=database_connected,
        model_loaded=prediction_service.is_loaded()
    )
