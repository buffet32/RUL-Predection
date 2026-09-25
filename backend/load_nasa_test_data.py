#!/usr/bin/env python3
"""Load NASA C-MAPSS test data with degraded engines"""

import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Machine, SensorReading, Prediction
from app.services.prediction_service import prediction_service

DATASET_PATH = Path("C:/Users/ULTRAPC/Downloads/archive")

def load_test_data():
    """Load NASA test data with engines at different degradation stages"""
    db: Session = SessionLocal()

    try:
        # Load test data
        test_file = DATASET_PATH / "test_FD001.txt"
        rul_file = DATASET_PATH / "RUL_FD001.txt"

        if not test_file.exists():
            print(f"[ERROR] Test dataset not found at {test_file}")
            return

        print(f"Loading test dataset from {test_file}...")

        # Read test data
        test_data = pd.read_csv(
            test_file,
            sep=r"\s+",
            header=None,
            engine="python"
        )

        # Read RUL data
        rul_data = pd.read_csv(
            rul_file,
            sep=r"\s+",
            header=None,
            engine="python"
        )

        # Column names
        columns = ["engine_id", "cycle", "setting_1", "setting_2", "setting_3",
                   "sensor_2", "sensor_3", "sensor_4", "sensor_5", "sensor_6",
                   "sensor_7", "sensor_8", "sensor_9", "sensor_10", "sensor_11",
                   "sensor_12", "sensor_13", "sensor_14", "sensor_15", "sensor_16",
                   "sensor_17", "sensor_18", "sensor_19", "sensor_20", "sensor_21"]

        if test_data.shape[1] > len(columns):
            columns = columns + [f"extra_{i}" for i in range(test_data.shape[1] - len(columns))]
        elif test_data.shape[1] < len(columns):
            columns = columns[:test_data.shape[1]]

        test_data.columns = columns
        rul_data.columns = ["rul"]

        print(f"[OK] Loaded {len(test_data)} test readings from {len(test_data['engine_id'].unique())} engines")

        # Create test machines and load sensor data
        engines = sorted(test_data["engine_id"].unique())
        now = datetime.utcnow()
        predictions_created = 0

        for idx, engine_id in enumerate(engines):
            # Create test machine (starting from ID 1000 to avoid conflicts)
            machine_name = f"Test Engine #{engine_id}"

            # Check if machine exists
            existing = db.query(Machine).filter(Machine.name == machine_name).first()
            if not existing:
                machine = Machine(
                    name=machine_name,
                    model="CFM56-7B",
                    description=f"Test engine from NASA C-MAPSS FD001",
                    location="Test Fleet"
                )
                db.add(machine)
                db.commit()
                db.refresh(machine)
                machine_id = machine.id
            else:
                machine_id = existing.id

            # Load sensor readings
            engine_data = test_data[test_data["engine_id"] == engine_id]
            rul_value = rul_data.iloc[engine_id - 1, 0]
            max_cycles = int(engine_data["cycle"].max())

            # Load readings
            for _, row in engine_data.iterrows():
                cycle = int(row["cycle"])
                cycles_remaining = int(max_cycles - cycle + int(rul_value))

                reading = SensorReading(
                    machine_id=machine_id,
                    cycle=cycle,
                    timestamp=now - timedelta(days=max_cycles - cycle),
                    setting_1=float(row["setting_1"]),
                    setting_2=float(row["setting_2"]),
                    setting_3=float(row["setting_3"]),
                    sensor_2=float(row["sensor_2"]),
                    sensor_3=float(row["sensor_3"]),
                    sensor_4=float(row["sensor_4"]),
                    sensor_6=float(row["sensor_6"]),
                    sensor_7=float(row["sensor_7"]),
                    sensor_8=float(row["sensor_8"]),
                    sensor_9=float(row["sensor_9"]),
                    sensor_11=float(row["sensor_11"]),
                    sensor_12=float(row["sensor_12"]),
                    sensor_13=float(row["sensor_13"]),
                    sensor_14=float(row["sensor_14"]),
                    sensor_15=float(row["sensor_15"]),
                    sensor_17=float(row["sensor_17"]),
                    sensor_20=float(row["sensor_20"]),
                    sensor_21=float(row["sensor_21"]),
                )
                db.add(reading)

            db.commit()

            # Generate prediction for last cycle
            last_reading = engine_data.iloc[-1]
            sensor_data = {
                "setting_1": float(last_reading["setting_1"]),
                "setting_2": float(last_reading["setting_2"]),
                "setting_3": float(last_reading["setting_3"]),
                "sensor_2": float(last_reading["sensor_2"]),
                "sensor_3": float(last_reading["sensor_3"]),
                "sensor_4": float(last_reading["sensor_4"]),
                "sensor_6": float(last_reading["sensor_6"]),
                "sensor_7": float(last_reading["sensor_7"]),
                "sensor_8": float(last_reading["sensor_8"]),
                "sensor_9": float(last_reading["sensor_9"]),
                "sensor_11": float(last_reading["sensor_11"]),
                "sensor_12": float(last_reading["sensor_12"]),
                "sensor_13": float(last_reading["sensor_13"]),
                "sensor_14": float(last_reading["sensor_14"]),
                "sensor_15": float(last_reading["sensor_15"]),
                "sensor_17": float(last_reading["sensor_17"]),
                "sensor_20": float(last_reading["sensor_20"]),
                "sensor_21": float(last_reading["sensor_21"]),
            }

            try:
                result = prediction_service.predict(sensor_data)
                prediction = Prediction(
                    machine_id=machine_id,
                    timestamp=now,
                    predicted_rul=result['predicted_rul'],
                    effective_rul=result['effective_rul'],
                    health_score=result['health_score'],
                    maintenance_status=result['maintenance_status'],
                    safety_margin_applied=result.get('safety_margin_applied', 15.0),
                )
                db.add(prediction)
                db.commit()
                predictions_created += 1

                print(f"Engine {engine_id:3d}: RUL={result['predicted_rul']:6.1f}, Health={result['health_score']:6.1f}%, Status={result['maintenance_status']}")
            except Exception as e:
                print(f"Engine {engine_id}: Error - {e}")

        print(f"\n[OK] Loaded {len(engine_data)} test engines with {predictions_created} predictions!")

    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_test_data()
