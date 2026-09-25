#!/usr/bin/env python3
"""Add model column to machines table"""

from sqlalchemy import text
from app.database import engine

def add_model_column():
    with engine.connect() as conn:
        try:
            # Check if column already exists
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name='machines' AND column_name='model'
            """))

            if result.fetchone():
                print("✓ Column 'model' already exists")
                return

            # Add the column
            conn.execute(text("ALTER TABLE machines ADD COLUMN model VARCHAR;"))
            conn.commit()
            print("✓ Successfully added 'model' column to machines table")

        except Exception as e:
            print(f"✗ Error: {e}")
            conn.rollback()

if __name__ == "__main__":
    add_model_column()
