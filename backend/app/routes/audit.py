from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
import sys
from pathlib import Path

from app.database import get_db
from app.models import AuditLog
from app.config import settings
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

AUDIT_AVAILABLE = True
DataQualityAudit = None
preprocess_training_data = None
preprocess_test_data = None

def load_audit_modules():
    global AUDIT_AVAILABLE, DataQualityAudit, preprocess_training_data, preprocess_test_data

    if DataQualityAudit is not None:
        return

    try:
        ml_path = str(Path(__file__).parent.parent.parent.parent / "ml")
        if ml_path not in sys.path:
            sys.path.insert(0, ml_path)

        from src.data_quality_audit import DataQualityAudit as DQA
        from src.preprocessing import preprocess_training_data as ptd, preprocess_test_data as ptd2

        DataQualityAudit = DQA
        preprocess_training_data = ptd
        preprocess_test_data = ptd2
        print("✓ Audit modules loaded successfully")
    except Exception as e:
        AUDIT_AVAILABLE = False
        print(f"Warning: Audit modules not available: {e}")

router = APIRouter(prefix="/audit", tags=["audit"])

class AuditStatusResponse(BaseModel):
    audit_id: str
    status: str
    data_health_score: Optional[float]
    total_issues: int
    critical_issues: int

    class Config:
        from_attributes = True

class AuditReportResponse(BaseModel):
    audit_id: str
    status: str
    data_health_score: Optional[float]
    total_checks: int
    passed_checks: int
    failed_checks: int
    total_issues: int
    critical_issues: int
    warning_issues: int
    issues: Optional[List[Dict]]
    recommendations: Optional[List[str]]
    execution_time_seconds: Optional[float]

    class Config:
        from_attributes = True

def convert_types(obj):
    """Convert numpy types to Python types for JSON serialization"""
    import numpy as np
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, dict):
        return {(convert_types(k) if isinstance(k, (np.integer, np.floating)) else k): convert_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_types(v) for v in obj]
    return obj

def run_audit_background(db: Session, data_dir: str = None):
    audit = None
    try:
        load_audit_modules()

        if not AUDIT_AVAILABLE or DataQualityAudit is None:
            raise Exception("Audit module not available")

        audit = AuditLog(
            audit_id="temp",
            status="running",
            audit_type="full",
            created_at=datetime.utcnow(),
            started_at=datetime.utcnow()
        )
        db.add(audit)
        db.commit()
        db.refresh(audit)

        audit.audit_id = f"audit-{audit.id}"
        db.commit()

        data_path = data_dir or str(Path.home() / "Downloads" / "archive")
        train_df = preprocess_training_data(data_path)
        test_df, rul_df = preprocess_test_data(data_path)

        audit_engine = DataQualityAudit(verbose=False)
        report = audit_engine.audit(train_df, test_df)

        audit.status = "completed"
        audit.completed_at = datetime.utcnow()
        audit.data_health_score = float(report.data_health_score)
        audit.total_checks = int(report.total_checks)
        audit.passed_checks = int(report.passed_checks)
        audit.failed_checks = int(report.failed_checks)
        audit.total_issues = int(report.total_issues)
        audit.critical_issues = int(report.critical_issues)
        audit.warning_issues = int(report.warning_issues)
        audit.info_issues = int(report.info_issues)
        audit.report = convert_types(report.to_dict())
        audit.issues = convert_types(report.issues)
        audit.sensor_stats = convert_types(report.sensor_stats)
        audit.engine_stats = convert_types(report.engine_stats)
        audit.recommendations = report.recommendations

        delta = datetime.utcnow() - audit.started_at
        audit.execution_time_seconds = delta.total_seconds()

        db.commit()
        print(f"✓ Audit {audit.audit_id} completed and saved successfully")

    except Exception as e:
        if audit:
            try:
                db.rollback()
            except:
                pass
            audit.status = "failed"
            audit.error_message = str(e)
            audit.completed_at = datetime.utcnow()
            try:
                db.commit()
            except:
                print(f"Could not save error to DB: {e}")
        print(f"Error in audit: {e}")

@router.get("/health")
def get_audit_health(db: Session = Depends(get_db)):
    latest_audit = db.query(AuditLog).filter(
        AuditLog.status == "completed"
    ).order_by(AuditLog.completed_at.desc()).first()

    if not latest_audit:
        return {
            "status": "unknown",
            "message": "No completed audits",
            "data_health_score": None
        }

    return {
        "status": "healthy" if latest_audit.data_health_score >= 75 else "degraded",
        "message": f"Data health: {latest_audit.data_health_score:.1f}/100",
        "data_health_score": latest_audit.data_health_score,
        "latest_audit": latest_audit.to_dict()
    }

@router.post("/run-audit")
def trigger_audit(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        load_audit_modules()
        if not AUDIT_AVAILABLE:
            raise HTTPException(status_code=503, detail="Audit module unavailable")
    except:
        raise HTTPException(status_code=503, detail="Audit module unavailable")

    audit = AuditLog(
        audit_id="temp",
        status="pending",
        audit_type="full",
        created_at=datetime.utcnow()
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)

    audit.audit_id = f"audit-{audit.id}"
    db.commit()

    background_tasks.add_task(run_audit_background, db, None)

    return {
        "audit_id": audit.audit_id,
        "status": "pending",
        "message": "Audit started"
    }

@router.get("/report/{audit_id}", response_model=AuditReportResponse)
def get_audit_report(audit_id: str, db: Session = Depends(get_db)):
    audit = db.query(AuditLog).filter(AuditLog.audit_id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit

@router.get("/latest", response_model=AuditReportResponse)
def get_latest_audit(db: Session = Depends(get_db)):
    audit = db.query(AuditLog).filter(
        AuditLog.status == "completed"
    ).order_by(AuditLog.completed_at.desc()).first()
    if not audit:
        raise HTTPException(status_code=404, detail="No audits found")
    return audit

@router.get("/history")
def get_audit_history(limit: int = 10, db: Session = Depends(get_db)):
    audits = db.query(AuditLog).filter(
        AuditLog.status == "completed"
    ).order_by(AuditLog.completed_at.desc()).limit(limit).all()
    return [audit.to_dict() for audit in audits]

@router.get("/status/{audit_id}")
def get_audit_status(audit_id: str, db: Session = Depends(get_db)):
    audit = db.query(AuditLog).filter(AuditLog.audit_id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return {
        "audit_id": audit.audit_id,
        "status": audit.status,
        "data_health_score": audit.data_health_score,
        "total_issues": audit.total_issues,
        "critical_issues": audit.critical_issues,
        "execution_time_seconds": audit.execution_time_seconds
    }