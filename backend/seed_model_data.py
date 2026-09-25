#!/usr/bin/env python3
"""Seed model data for existing machines"""

from sqlalchemy import text
from app.database import engine

def seed_model_data():
    """Assign realistic aircraft engine models to machines"""

    engine_models = [
        'CFM56-5B4',      # Boeing 737
        'CFM56-5C',       # Boeing 737
        'GE90-115B',      # Boeing 777
        'PW4062',         # Boeing 747/767
        'PW4090',         # Boeing 777
        'RB211-535',      # Boeing 757
        'V2500-A5',       # Airbus A320
        'CFM56-7B',       # Boeing 737 NG
        'Trent 1000',     # Boeing 787
        'Trent 7000',     # Airbus A350
        'GE9X-115B',      # Boeing 777X
        'CFM RISE',       # Next-gen engine
    ]

    with engine.connect() as conn:
        try:
            # Get all machines with NULL model
            result = conn.execute(text("SELECT id FROM machines WHERE model IS NULL ORDER BY id"))
            machine_ids = [row[0] for row in result]

            if not machine_ids:
                print("✓ All machines already have model data")
                return

            # Assign engine models in rotation
            for idx, machine_id in enumerate(machine_ids):
                model = engine_models[idx % len(engine_models)]
                conn.execute(text(f"""
                    UPDATE machines
                    SET model = '{model}'
                    WHERE id = {machine_id}
                """))

            conn.commit()
            print(f"✓ Successfully assigned aircraft engine models to {len(machine_ids)} machines")

        except Exception as e:
            print(f"✗ Error: {e}")
            conn.rollback()

if __name__ == "__main__":
    seed_model_data()
