#!/usr/bin/env python3
"""Seed sample predictions for aircraft engines"""

import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Machine, Prediction

def seed_predictions():
    """Generate realistic RUL predictions for all machines"""

    db: Session = SessionLocal()

    try:
        # Get all machines
        machines = db.query(Machine).all()

        if not machines:
            print("✗ No machines found. Create machines first!")
            return

        # Generate 20 predictions per machine
        predictions_created = 0
        now = datetime.utcnow()

        for machine in machines:
            # Create predictions for the last 30 days
            for i in range(20):
                # Realistic RUL values for aircraft engines (100-5000 hours)
                predicted_rul = random.uniform(100, 3000)

                # Apply safety margin (10-20%)
                safety_margin = random.uniform(0.1, 0.2)
                effective_rul = predicted_rul * (1 - safety_margin)

                # Health score based on RUL
                if predicted_rul > 2000:
                    health_score = random.uniform(85, 100)
                    maintenance_status = "HEALTHY"
                elif predicted_rul > 1000:
                    health_score = random.uniform(70, 85)
                    maintenance_status = "CAUTION"
                else:
                    health_score = random.uniform(40, 70)
                    maintenance_status = "ALERT"

                prediction = Prediction(
                    machine_id=machine.id,
                    sensor_reading_id=None,  # No sensor reading linked
                    timestamp=now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23)),
                    predicted_rul=round(predicted_rul, 2),
                    effective_rul=round(effective_rul, 2),
                    health_score=round(health_score, 2),
                    maintenance_status=maintenance_status,
                    safety_margin_applied=round(safety_margin * 100, 2),
                )
                db.add(prediction)
                predictions_created += 1

        db.commit()
        print(f"✓ Successfully created {predictions_created} predictions")
        print(f"  - {len(machines)} machines")
        print(f"  - {predictions_created // len(machines)} predictions per machine")
        print(f"\nStatus breakdown:")
        print(f"  - HEALTHY: RUL > 2000 hours")
        print(f"  - CAUTION: RUL 1000-2000 hours")
        print(f"  - ALERT: RUL < 1000 hours")

    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_predictions()
