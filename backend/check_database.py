#!/usr/bin/env python3
"""Check database data summary"""

from sqlalchemy import func
from app.database import SessionLocal
from app.models import Machine, SensorReading, Prediction, AuditLog

def check_database():
    db = SessionLocal()
    try:
        # Count records in each table
        machines_count = db.query(func.count(Machine.id)).scalar()
        sensor_readings_count = db.query(func.count(SensorReading.id)).scalar()
        predictions_count = db.query(func.count(Prediction.id)).scalar()
        audit_logs_count = db.query(func.count(AuditLog.id)).scalar()

        print("=" * 60)
        print("DATABASE DATA SUMMARY")
        print("=" * 60)
        print(f"Machines:        {machines_count} records")
        print(f"Sensor Readings: {sensor_readings_count} records")
        print(f"Predictions:     {predictions_count} records")
        print(f"Audit Logs:      {audit_logs_count} records")
        print("=" * 60)

        # Show sample machines
        if machines_count > 0:
            print("\nSample Machines:")
            machines = db.query(Machine).limit(5).all()
            for m in machines:
                print(f"  - ID {m.id}: {m.name} ({m.model})")

        # Show sample predictions
        if predictions_count > 0:
            print(f"\nSample Predictions (latest 5):")
            predictions = db.query(Prediction).order_by(Prediction.timestamp.desc()).limit(5).all()
            for p in predictions:
                print(f"  - Machine {p.machine_id}: RUL={p.predicted_rul:.1f}, Health={p.health_score:.1f}, Status={p.maintenance_status}")
        else:
            print("\n❌ No predictions found")

        # Show sample sensor readings
        if sensor_readings_count > 0:
            print(f"\nSample Sensor Readings (latest 3):")
            readings = db.query(SensorReading).order_by(SensorReading.timestamp.desc()).limit(3).all()
            for r in readings:
                print(f"  - Machine {r.machine_id}, Cycle {r.cycle}: Temp={r.sensor_2:.1f}, RPM={r.sensor_4:.1f}")
        else:
            print("\n❌ No sensor readings found")

    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_database()
