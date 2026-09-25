"""
Preprocessing Pipeline for NASA C-MAPSS FD001 Dataset
Handles data loading, cleaning, and RUL generation
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict


# Column names for the dataset
COLUMN_NAMES = [
    'engine_id',           # 1) unit number
    'cycle',               # 2) time, in cycles
    'setting_1',           # 3) operational setting 1
    'setting_2',           # 4) operational setting 2
    'setting_3',           # 5) operational setting 3
    'sensor_1',            # 6) sensor measurement 1
    'sensor_2',            # 7) sensor measurement 2
    'sensor_3',            # 8) sensor measurement 3
    'sensor_4',            # 9) sensor measurement 4
    'sensor_5',            # 10) sensor measurement 5
    'sensor_6',            # 11) sensor measurement 6
    'sensor_7',            # 12) sensor measurement 7
    'sensor_8',            # 13) sensor measurement 8
    'sensor_9',            # 14) sensor measurement 9
    'sensor_10',           # 15) sensor measurement 10
    'sensor_11',           # 16) sensor measurement 11
    'sensor_12',           # 17) sensor measurement 12
    'sensor_13',           # 18) sensor measurement 13
    'sensor_14',           # 19) sensor measurement 14
    'sensor_15',           # 20) sensor measurement 15
    'sensor_16',           # 21) sensor measurement 16
    'sensor_17',           # 22) sensor measurement 17
    'sensor_18',           # 23) sensor measurement 18
    'sensor_19',           # 24) sensor measurement 19
    'sensor_20',           # 25) sensor measurement 20
    'sensor_21'            # 26) sensor measurement 21
]

# Constant sensors identified from EDA - must be removed
CONSTANT_SENSORS = ['sensor_1', 'sensor_5', 'sensor_10', 'sensor_16', 'sensor_18', 'sensor_19']

# Remaining useful sensors after removing constant ones
USEFUL_SENSORS = [col for col in COLUMN_NAMES if col.startswith('sensor_') and col not in CONSTANT_SENSORS]


def load_data(data_dir: str = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load train, test, and RUL data from the NASA C-MAPSS dataset

    Args:
        data_dir: Path to the directory containing the dataset files

    Returns:
        train_df: Training data with column names
        test_df: Test data with column names
        rul_df: RUL data for test set
    """
    # Use project-relative path if not specified
    if data_dir is None:
        import os
        data_dir = os.getenv('CMAPSS_DATA_DIR', str(Path(__file__).parent.parent.parent / "data" / "archive"))

    data_path = Path(data_dir)
    
    # Load training data
    train_df = pd.read_csv(
        data_path / "train_FD001.txt",
        sep=r'\s+',
        header=None,
        names=COLUMN_NAMES,
        engine='python'
    )
    
    # Load test data
    test_df = pd.read_csv(
        data_path / "test_FD001.txt",
        sep=r'\s+',
        header=None,
        names=COLUMN_NAMES,
        engine='python'
    )
    
    # Load RUL data
    rul_df = pd.read_csv(
        data_path / "RUL_FD001.txt",
        sep=' ',
        header=None
    )
    rul_df = rul_df.dropna(axis=1, how='all')
    rul_df.columns = ['RUL']
    
    print(f"Loaded training data: {train_df.shape}")
    print(f"Loaded test data: {test_df.shape}")
    print(f"Loaded RUL data: {rul_df.shape}")
    
    return train_df, test_df, rul_df


def remove_constant_sensors(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove constant sensors that provide no information
    
    Args:
        df: Input dataframe
        
    Returns:
        Dataframe with constant sensors removed
    """
    columns_to_drop = [col for col in CONSTANT_SENSORS if col in df.columns]
    df_cleaned = df.drop(columns=columns_to_drop)
    
    print(f"Removed {len(columns_to_drop)} constant sensors: {columns_to_drop}")
    print(f"Remaining columns: {df_cleaned.shape[1]}")
    
    return df_cleaned


def calculate_rul_training(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate RUL for training data
    RUL = max_cycle_for_engine - current_cycle
    
    Args:
        df: Training dataframe with engine_id and cycle columns
        
    Returns:
        Dataframe with RUL column added
    """
    # Calculate max cycle for each engine
    max_cycles = df.groupby('engine_id')['cycle'].max().reset_index()
    max_cycles.columns = ['engine_id', 'max_cycle']
    
    # Merge back to original dataframe
    df = df.merge(max_cycles, on='engine_id')
    
    # Calculate RUL
    df['RUL'] = df['max_cycle'] - df['cycle']

    # Apply RUL capping at 125 cycles (NASA C-MAPSS standard)
    df['RUL'] = df['RUL'].clip(upper=125)

    print("RUL calculated for training data")
    print(f"Applied RUL capping at 125 cycles (NASA C-MAPSS standard)")
    print(f"RUL statistics: min={df['RUL'].min()}, max={df['RUL'].max()}, mean={df['RUL'].mean():.2f}")
    
    return df


def add_relative_cycle(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add normalized/relative cycle feature
    relative_cycle = cycle / max_cycle
    
    Args:
        df: Dataframe with engine_id and cycle columns
        
    Returns:
        Dataframe with relative_cycle column added
    """
    if 'max_cycle' not in df.columns:
        max_cycles = df.groupby('engine_id')['cycle'].max().reset_index()
        max_cycles.columns = ['engine_id', 'max_cycle']
        df = df.merge(max_cycles, on='engine_id')
    
    df['relative_cycle'] = df['cycle'] / df['max_cycle']
    
    print("Added relative_cycle feature")
    
    return df


def sort_and_validate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sort observations by engine_id and cycle
    Perform sanity checks
    
    Args:
        df: Input dataframe
        
    Returns:
        Sorted and validated dataframe
    """
    # Sort by engine_id and cycle
    df = df.sort_values(['engine_id', 'cycle']).reset_index(drop=True)
    
    # Sanity checks
    print("\n--- Sanity Checks ---")

    # Check for missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(f"WARNING: Missing values found:\n{missing[missing > 0]}")
    else:
        print("[OK] No missing values")

    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"WARNING: {duplicates} duplicate rows found")
    else:
        print("[OK] No duplicate rows")

    # Check engine_id range
    n_engines = df['engine_id'].nunique()
    print(f"[OK] Number of engines: {n_engines}")
    
    # Check cycle progression
    for engine_id in df['engine_id'].unique()[:5]:  # Check first 5 engines
        engine_data = df[df['engine_id'] == engine_id]
        cycles = engine_data['cycle'].values
        if not np.all(np.diff(cycles) == 1):
            print(f"WARNING: Engine {engine_id} has non-sequential cycles")
        else:
            print(f"[OK] Engine {engine_id}: cycles are sequential")
    
    return df


def preprocess_training_data(data_dir: str = "../../Downloads/archive") -> pd.DataFrame:
    """
    Complete preprocessing pipeline for training data
    
    Args:
        data_dir: Path to the directory containing the dataset files
        
    Returns:
        Preprocessed training dataframe
    """
    print("=" * 80)
    print("PREPROCESSING TRAINING DATA")
    print("=" * 80)
    
    # Load data
    train_df, _, _ = load_data(data_dir)
    
    # Remove constant sensors
    train_df = remove_constant_sensors(train_df)
    
    # Calculate RUL
    train_df = calculate_rul_training(train_df)
    
    # Add relative cycle
    train_df = add_relative_cycle(train_df)
    
    # Sort and validate
    train_df = sort_and_validate(train_df)
    
    print(f"\nFinal training data shape: {train_df.shape}")
    print(f"Columns: {list(train_df.columns)}")
    
    return train_df


def preprocess_test_data(data_dir: str = "../../Downloads/archive") -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Complete preprocessing pipeline for test data
    
    Args:
        data_dir: Path to the directory containing the dataset files
        
    Returns:
        Preprocessed test dataframe and RUL dataframe
    """
    print("\n" + "=" * 80)
    print("PREPROCESSING TEST DATA")
    print("=" * 80)
    
    # Load data
    _, test_df, rul_df = load_data(data_dir)
    
    # Remove constant sensors
    test_df = remove_constant_sensors(test_df)
    
    # Add relative cycle (for consistency)
    max_cycles = test_df.groupby('engine_id')['cycle'].max().reset_index()
    max_cycles.columns = ['engine_id', 'max_cycle']
    test_df = test_df.merge(max_cycles, on='engine_id')
    test_df = add_relative_cycle(test_df)
    
    # Sort and validate
    test_df = sort_and_validate(test_df)
    
    print(f"\nFinal test data shape: {test_df.shape}")
    print(f"RUL data shape: {rul_df.shape}")
    
    return test_df, rul_df


def verify_rul_calculation(df: pd.DataFrame, n_engines: int = 3) -> None:
    """
    Manually verify RUL calculation for sample engines
    
    Args:
        df: Training dataframe with RUL column
        n_engines: Number of engines to verify
    """
    print("\n" + "=" * 80)
    print("RUL CALCULATION VERIFICATION")
    print("=" * 80)
    
    for i, engine_id in enumerate(sorted(df['engine_id'].unique())[:n_engines]):
        engine_data = df[df['engine_id'] == engine_id].sort_values('cycle')
        
        print(f"\n--- Engine {engine_id} ---")
        print(f"Max cycle: {engine_data['max_cycle'].iloc[0]}")
        print(f"Total cycles: {len(engine_data)}")
        print("\nFirst 5 cycles:")
        print(engine_data[['cycle', 'RUL']].head())
        print("\nLast 5 cycles:")
        print(engine_data[['cycle', 'RUL']].tail())
        
        # Verify RUL calculation
        max_cycle = engine_data['max_cycle'].iloc[0]
        calculated_rul = max_cycle - engine_data['cycle'].values
        if np.allclose(calculated_rul, engine_data['RUL'].values):
            print("[OK] RUL calculation verified")
        else:
            print("✗ RUL calculation ERROR")


def get_feature_columns(df: pd.DataFrame, include_engine_id: bool = False) -> list:
    """
    Get feature columns for modeling
    
    Args:
        df: Dataframe
        include_engine_id: Whether to include engine_id (should be False for modeling)
        
    Returns:
        List of feature column names
    """
    # Exclude non-feature columns
    exclude_cols = ['engine_id', 'cycle', 'max_cycle', 'RUL']
    
    if include_engine_id:
        exclude_cols.remove('engine_id')
    
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    return feature_cols


if __name__ == "__main__":
    # Test preprocessing pipeline
    print("Testing preprocessing pipeline...")
    
    # Preprocess training data
    train_df = preprocess_training_data()
    
    # Verify RUL calculation
    verify_rul_calculation(train_df, n_engines=3)
    
    # Preprocess test data
    test_df, rul_df = preprocess_test_data()
    
    print("\n" + "=" * 80)
    print("PREPROCESSING COMPLETE")
    print("=" * 80)
