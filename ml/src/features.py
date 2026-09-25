"""
Feature Engineering for NASA C-MAPSS FD001 Dataset
Creates time-series features from sensor data
"""

import pandas as pd
import numpy as np
from typing import List


def add_rolling_features(
    df: pd.DataFrame,
    sensor_cols: List[str],
    windows: List[int] = [5, 10, 20]
) -> pd.DataFrame:
    """
    Add rolling window features for sensors
    
    Args:
        df: Input dataframe with engine_id, cycle, and sensor columns
        sensor_cols: List of sensor column names
        windows: List of window sizes for rolling calculations
        
    Returns:
        Dataframe with rolling features added
    """
    df = df.copy()
    df = df.sort_values(['engine_id', 'cycle'])
    
    print(f"Adding rolling features for windows: {windows}")
    
    for window in windows:
        for sensor in sensor_cols:
            # Rolling mean
            df[f'{sensor}_rolling_mean_{window}'] = df.groupby('engine_id')[sensor].transform(
                lambda x: x.rolling(window=window, min_periods=1).mean()
            )
            
            # Rolling std
            df[f'{sensor}_rolling_std_{window}'] = df.groupby('engine_id')[sensor].transform(
                lambda x: x.rolling(window=window, min_periods=1).std()
            )
            
            # Rolling min
            df[f'{sensor}_rolling_min_{window}'] = df.groupby('engine_id')[sensor].transform(
                lambda x: x.rolling(window=window, min_periods=1).min()
            )
            
            # Rolling max
            df[f'{sensor}_rolling_max_{window}'] = df.groupby('engine_id')[sensor].transform(
                lambda x: x.rolling(window=window, min_periods=1).max()
            )
    
    print(f"Added rolling features. New shape: {df.shape}")
    return df


def add_lag_features(
    df: pd.DataFrame,
    sensor_cols: List[str],
    lags: List[int] = [1, 2, 5]
) -> pd.DataFrame:
    """
    Add lag features for sensors
    
    Args:
        df: Input dataframe with engine_id, cycle, and sensor columns
        sensor_cols: List of sensor column names
        lags: List of lag values
        
    Returns:
        Dataframe with lag features added
    """
    df = df.copy()
    df = df.sort_values(['engine_id', 'cycle'])
    
    print(f"Adding lag features for lags: {lags}")
    
    for lag in lags:
        for sensor in sensor_cols:
            # Apply ffill/bfill within each engine group to prevent cross-engine contamination
            df[f'{sensor}_lag_{lag}'] = (
                df.groupby('engine_id')[sensor]
                .transform(lambda x: x.shift(lag).ffill().bfill())
            )
    
    print(f"Added lag features. New shape: {df.shape}")
    return df


def add_difference_features(
    df: pd.DataFrame,
    sensor_cols: List[str]
) -> pd.DataFrame:
    """
    Add first difference features (rate of change)
    
    Args:
        df: Input dataframe with engine_id, cycle, and sensor columns
        sensor_cols: List of sensor column names
        
    Returns:
        Dataframe with difference features added
    """
    df = df.copy()
    df = df.sort_values(['engine_id', 'cycle'])
    
    print("Adding difference features")
    
    for sensor in sensor_cols:
        # First difference (within each engine group)
        df[f'{sensor}_diff'] = df.groupby('engine_id')[sensor].transform('diff')

        # Rate of change (difference / current value)
        df[f'{sensor}_rate_of_change'] = df[f'{sensor}_diff'] / (df[sensor] + 1e-8)

        # Fill NaN values within each engine group to prevent cross-engine contamination
        df[f'{sensor}_diff'] = (
            df.groupby('engine_id')[f'{sensor}_diff']
            .transform(lambda x: x.ffill().bfill())
        )
        df[f'{sensor}_rate_of_change'] = (
            df.groupby('engine_id')[f'{sensor}_rate_of_change']
            .transform(lambda x: x.ffill().bfill())
        )
    
    print(f"Added difference features. New shape: {df.shape}")
    return df


def add_degradation_features(
    df: pd.DataFrame,
    sensor_cols: List[str]
) -> pd.DataFrame:
    """
    Add degradation features (deviation from baseline)
    
    Args:
        df: Input dataframe with engine_id, cycle, and sensor columns
        sensor_cols: List of sensor column names
        
    Returns:
        Dataframe with degradation features added
    """
    df = df.copy()
    df = df.sort_values(['engine_id', 'cycle'])
    
    print("Adding degradation features")
    
    for sensor in sensor_cols:
        # Calculate baseline (mean of first 5 cycles for each engine)
        baseline = df.groupby('engine_id')[sensor].transform(
            lambda x: x.head(5).mean()
        )
        
        # Deviation from baseline
        df[f'{sensor}_deviation_from_baseline'] = df[sensor] - baseline
        
        # Cumulative deviation
        df[f'{sensor}_cumulative_deviation'] = df.groupby('engine_id')[
            f'{sensor}_deviation_from_baseline'
        ].cumsum()
    
    print(f"Added degradation features. New shape: {df.shape}")
    return df


def add_all_time_series_features(
    df: pd.DataFrame,
    sensor_cols: List[str],
    windows: List[int] = [5, 10, 20],
    lags: List[int] = [1, 2, 5]
) -> pd.DataFrame:
    """
    Add all time-series features
    
    Args:
        df: Input dataframe
        sensor_cols: List of sensor column names
        windows: Rolling window sizes
        lags: Lag values
        
    Returns:
        Dataframe with all time-series features added
    """
    print("=" * 80)
    print("FEATURE ENGINEERING")
    print("=" * 80)
    
    # Add rolling features
    df = add_rolling_features(df, sensor_cols, windows)
    
    # Add lag features
    df = add_lag_features(df, sensor_cols, lags)
    
    # Add difference features
    df = add_difference_features(df, sensor_cols)
    
    # Add degradation features
    df = add_degradation_features(df, sensor_cols)
    
    print(f"\nFinal feature-engineered shape: {df.shape}")
    print(f"Total features: {df.shape[1]}")
    
    return df


def get_feature_documentation() -> str:
    """
    Get documentation of all engineered features
    
    Returns:
        String describing all features
    """
    doc = """
    ENGINEERED FEATURES DOCUMENTATION
    =================================
    
    BASE FEATURES:
    - engine_id: Unique engine identifier (NOT used for modeling)
    - cycle: Current operational cycle
    - max_cycle: Maximum cycle for the engine (failure point)
    - RUL: Remaining Useful Life (target variable)
    - relative_cycle: cycle / max_cycle (normalized position in engine life)
    - setting_1, setting_2, setting_3: Operational settings
    - sensor_2, sensor_3, sensor_4, sensor_6, sensor_7, sensor_8, sensor_9, sensor_11, 
      sensor_12, sensor_13, sensor_14, sensor_15, sensor_17, sensor_20, sensor_21: 
      Non-constant sensor measurements
    
    ROLLING WINDOW FEATURES (for each sensor and window size):
    - {sensor}_rolling_mean_{window}: Mean of sensor over last N cycles
    - {sensor}_rolling_std_{window}: Standard deviation over last N cycles
    - {sensor}_rolling_min_{window}: Minimum over last N cycles
    - {sensor}_rolling_max_{window}: Maximum over last N cycles
    
    LAG FEATURES (for each sensor and lag value):
    - {sensor}_lag_{N}: Sensor value N cycles ago
    
    DIFFERENCE FEATURES (for each sensor):
    - {sensor}_diff: First difference (current - previous)
    - {sensor}_rate_of_change: Rate of change (diff / current)
    
    DEGRADATION FEATURES (for each sensor):
    - {sensor}_deviation_from_baseline: Deviation from early-life baseline
    - {sensor}_cumulative_deviation: Cumulative sum of deviations
    
    WINDOW SIZES USED: 5, 10, 20 cycles
    LAG VALUES USED: 1, 2, 5 cycles
    
    IMPORTANT: All features use only current and past information.
    No future observations are used (prevents data leakage).
    """
    return doc


if __name__ == "__main__":
    # Test feature engineering
    print("Testing feature engineering...")
    
    # Create sample data
    sample_data = pd.DataFrame({
        'engine_id': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
        'cycle': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
        'sensor_2': [100, 101, 102, 103, 104, 100, 101, 102, 103, 104],
        'sensor_3': [200, 201, 202, 203, 204, 200, 201, 202, 203, 204]
    })
    
    sensor_cols = ['sensor_2', 'sensor_3']
    
    # Test rolling features
    result = add_rolling_features(sample_data, sensor_cols, windows=[3])
    print("\nRolling features test:")
    print(result.head())
    
    # Test lag features
    result = add_lag_features(sample_data, sensor_cols, lags=[1, 2])
    print("\nLag features test:")
    print(result.head())
    
    print("\nFeature engineering test complete")
