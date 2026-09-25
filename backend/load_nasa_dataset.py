#!/usr/bin/env python3
"""Load NASA C-MAPSS dataset into database and generate predictions"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Machine, SensorReading, Prediction

DATASET_PATH = Path("C:/Users/ULTRAPC/Downloads/archive")

def load_dataset():
    """Load NASA C-MAPSS train data"""
    db: Session = SessionLocal()

    try:
        # Load training data
        train_file = DATASET_PATH / "train_FD001.txt"
        rul_file = DATASET_PATH / "RUL_FD001.txt"

        if not train_file.exists():
            print(f"[ERROR] Dataset not found at {train_file}")
            return

        print(f"Loading dataset from {train_file}...")

        # Read training data - use more robust parsing
        train_data = pd.read_csv(
            train_file,
            sep=r"\s+",  # Use regex to handle multiple spaces
            header=None,
            engine="python"
        )

        print(f"  Loaded {train_data.shape[0]} rows, {train_data.shape[1]} columns")

        # Read RUL data
        rul_data = pd.read_csv(
            rul_file,
            sep=r"\s+",
            header=None,
            engine="python"
        )

        # Column names for NASA C-MAPSS dataset
        columns = ["engine_id", "cycle", "setting_1", "setting_2", "setting_3",
                   "sensor_2", "sensor_3", "sensor_4", "sensor_5", "sensor_6",
                   "sensor_7", "sensor_8", "sensor_9", "sensor_10", "sensor_11",
                   "sensor_12", "sensor_13", "sensor_14", "sensor_15", "sensor_16",
                   "sensor_17", "sensor_18", "sensor_19", "sensor_20", "sensor_21"]

        # Match the actual number of columns
        if train_data.shape[1] > len(columns):
            columns = columns + [f"extra_{i}" for i in range(train_data.shape[1] - len(columns))]
        elif train_data.shape[1] < len(columns):
            columns = columns[:train_data.shape[1]]

        train_data.columns = columns
        rul_data.columns = ["rul"]

        print(f"[OK] Loaded {len(train_data)} sensor readings from {len(train_data['engine_id'].unique())} engines")

        # Create machines and load sensor data
        engines = train_data["engine_id"].unique()
        now = datetime.utcnow()

        for engine_id in engines:
            # Create machine
            machine_name = f"Turbofan Engine #{engine_id}"

            # Check if machine exists
            existing = db.query(Machine).filter(Machine.name == machine_name).first()
            if not existing:
                machine = Machine(
                    name=machine_name,
                    model="CFM56-7B",
                    description=f"Engine from NASA C-MAPSS FD001 dataset",
                    location="Test Fleet"
                )
                db.add(machine)
                db.commit()
                db.refresh(machine)
                machine_id = machine.id
            else:
                machine_id = existing.id

            # Load sensor readings for this engine
            engine_data = train_data[train_data["engine_id"] == engine_id]
            rul_value = rul_data.iloc[engine_id - 1, 0]
            max_cycles = int(engine_data["cycle"].max())

            for _, row in engine_data.iterrows():
                cycle = int(row["cycle"])
                # Calculate RUL for this cycle
                cycles_remaining = int(max_cycles - cycle)

                reading = SensorReading(
                    machine_id=machine_id,
                    cycle=cycle,
                    timestamp=now - timedelta(days=cycles_remaining, hours=0),
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

                # Create prediction for final cycles
                if cycle > max_cycles - 10:  # Last 10 cycles
                    # Estimate health based on remaining cycles
                    health_score = (cycles_remaining / 10) * 100  # Scale to last 10 cycles
                    health_score = max(20, min(100, health_score))  # Clamp between 20-100

                    if cycles_remaining > 7:
                        maintenance_status = "HEALTHY"
                        predicted_rul = float(cycles_remaining * 1.2)
                    elif cycles_remaining > 3:
                        maintenance_status = "CAUTION"
                        predicted_rul = float(cycles_remaining * 1.0)
                    else:
                        maintenance_status = "ALERT"
                        predicted_rul = float(cycles_remaining * 0.8)

                    prediction = Prediction(
                        machine_id=machine_id,
                        sensor_reading_id=None,
                        timestamp=now - timedelta(days=cycles_remaining),
                        predicted_rul=round(predicted_rul, 2),
                        effective_rul=round(predicted_rul * 0.85, 2),
                        health_score=round(health_score, 2),
                        maintenance_status=maintenance_status,
                        safety_margin_applied=15.0,
                    )
                    db.add(prediction)

            db.commit()
            print(f"  [OK] Engine {engine_id}: {len(engine_data)} sensor readings, {max_cycles} cycles")

        print(f"\n[OK] Successfully loaded NASA C-MAPSS dataset!")

    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_dataset()
