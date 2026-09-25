#!/usr/bin/env python3
"""Seed sample sensor readings for aircraft engines"""

from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import SensorReading, Machine

def seed_sensor_readings():
    """Generate realistic sensor readings for all machines"""

    db: Session = SessionLocal()

    try:
        # Get all machines
        machines = db.query(Machine).all()

        if not machines:
            print("✗ No machines found. Create machines first!")
            return

        # Generate 50 sensor readings per machine
        readings_created = 0
        now = datetime.utcnow()

        for machine in machines:
            # Create readings for the last 30 days
            for i in range(50):
                reading = SensorReading(
                    machine_id=machine.id,
                    cycle=i + 1,
                    timestamp=now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23)),

                    # Operating settings
                    setting_1=random.uniform(20, 30),      # Altitude
                    setting_2=random.uniform(0.5, 0.9),     # Throttle
                    setting_3=random.uniform(0, 100),       # Load

                    # Sensor readings (normalized 0-100)
                    sensor_2=random.uniform(400, 500),      # Temperature
                    sensor_3=random.uniform(2000, 3000),    # Pressure
                    sensor_4=random.uniform(8000, 9000),    # RPM
                    sensor_6=random.uniform(300, 400),      # Vibration
                    sensor_7=random.uniform(0, 50),         # Oil level
                    sensor_8=random.uniform(50, 100),       # Fuel flow
                    sensor_9=random.uniform(10, 50),        # Temperature 2
                    sensor_11=random.uniform(200, 300),     # Pressure 2
                    sensor_12=random.uniform(100, 150),     # Humidity
                    sensor_13=random.uniform(2.5, 3.5),     # Bleed valve
                    sensor_14=random.uniform(25, 35),       # Bypass valve
                    sensor_15=random.uniform(0, 100),       # Stator temp
                    sensor_17=random.uniform(20, 40),       # Fan vibration
                    sensor_20=random.uniform(0.5, 1.5),     # Fuel ratio
                    sensor_21=random.uniform(30, 50),       # Combustor pressure
                )
                db.add(reading)
                readings_created += 1

        db.commit()
        print(f"✓ Successfully created {readings_created} sensor readings")
        print(f"  - {len(machines)} machines")
        print(f"  - {readings_created // len(machines)} readings per machine")

    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_sensor_readings()
