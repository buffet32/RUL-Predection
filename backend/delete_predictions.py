#!/usr/bin/env python3
"""Delete all predictions from database"""

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Prediction

def delete_predictions():
    db: Session = SessionLocal()
    try:
        count = db.query(Prediction).count()
        db.query(Prediction).delete()
        db.commit()
        print(f"[OK] Successfully deleted {count} predictions")
    except Exception as e:
        print(f"[ERROR] {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    delete_predictions()
