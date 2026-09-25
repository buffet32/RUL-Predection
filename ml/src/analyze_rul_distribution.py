"""
Analyze RUL distribution in official test set vs validation set
"""

import pandas as pd
import numpy as np
from pathlib import Path
import os

def analyze_rul_distribution():
    """
    Compare RUL distribution between official test set and validation set
    """
    print("=" * 80)
    print("RUL DISTRIBUTION ANALYSIS")
    print("=" * 80)

    # Load data - use environment variable or project-relative path
    data_dir = Path(os.getenv('CMAPSS_DATA_DIR', Path(__file__).parent.parent.parent / "data" / "archive"))
    
    # Load training data
    train_df = pd.read_csv(
        data_dir / "train_FD001.txt",
        sep=' ',
        header=None,
        engine='python'
    )
    train_df = train_df.dropna(axis=1, how='all')
    column_names = ['engine_id', 'cycle', 'setting_1', 'setting_2', 'setting_3'] + [f'sensor_{i}' for i in range(1, 22)]
    train_df.columns = column_names
    
    # Remove constant sensors
    constant_sensors = ['sensor_1', 'sensor_5', 'sensor_10', 'sensor_16', 'sensor_18', 'sensor_19']
    train_df = train_df.drop(columns=constant_sensors)
    
    # Calculate RUL
    max_cycles = train_df.groupby('engine_id')['cycle'].max().reset_index()
    max_cycles.columns = ['engine_id', 'max_cycle']
    train_df = train_df.merge(max_cycles, on='engine_id')
    train_df['RUL'] = train_df['max_cycle'] - train_df['cycle']
    train_df = train_df.drop(columns=['max_cycle'])
    
    # Get engine split
    engine_ids = sorted(train_df['engine_id'].unique())
    np.random.seed(42)
    np.random.shuffle(engine_ids)
    
    n_engines = len(engine_ids)
    n_train = int(0.7 * n_engines)
    n_val = int(0.15 * n_engines)
    
    train_engines = set(engine_ids[:n_train])
    val_engines = set(engine_ids[n_train:n_train + n_val])
    test_engines = set(engine_ids[n_train + n_val:])
    
    # Split data
    val_data = train_df[train_df['engine_id'].isin(val_engines)]
    
    # Load official test RUL
    official_rul = pd.read_csv(
        data_dir / "RUL_FD001.txt",
        sep=' ',
        header=None,
        engine='python'
    )
    official_rul = official_rul.dropna(axis=1, how='all')
    official_rul.columns = ['RUL']
    official_rul['engine_id'] = range(1, 101)  # Engine IDs 1-100
    
    print("\n" + "=" * 80)
    print("VALIDATION SET RUL DISTRIBUTION")
    print("=" * 80)
    
    val_rul = val_data['RUL'].values
    print(f"Count: {len(val_rul)}")
    print(f"Mean: {np.mean(val_rul):.2f}")
    print(f"Std: {np.std(val_rul):.2f}")
    print(f"Min: {np.min(val_rul)}")
    print(f"Max: {np.max(val_rul)}")
    print(f"Median: {np.median(val_rul):.2f}")
    print(f"25th percentile: {np.percentile(val_rul, 25):.2f}")
    print(f"75th percentile: {np.percentile(val_rul, 75):.2f}")
    
    # Check for capping
    print(f"\nRUL range: {np.min(val_rul)} to {np.max(val_rul)}")
    print(f"Unique values: {len(np.unique(val_rul))}")
    
    print("\n" + "=" * 80)
    print("OFFICIAL TEST SET RUL DISTRIBUTION")
    print("=" * 80)
    
    test_rul = official_rul['RUL'].values
    print(f"Count: {len(test_rul)}")
    print(f"Mean: {np.mean(test_rul):.2f}")
    print(f"Std: {np.std(test_rul):.2f}")
    print(f"Min: {np.min(test_rul)}")
    print(f"Max: {np.max(test_rul)}")
    print(f"Median: {np.median(test_rul):.2f}")
    print(f"25th percentile: {np.percentile(test_rul, 25):.2f}")
    print(f"75th percentile: {np.percentile(test_rul, 75):.2f}")
    
    # Check for capping
    print(f"\nRUL range: {np.min(test_rul)} to {np.max(test_rul)}")
    print(f"Unique values: {len(np.unique(test_rul))}")
    
    # Check if values are capped
    max_val = np.max(test_rul)
    near_max_count = np.sum(test_rul >= max_val - 1)
    print(f"\nCapping analysis:")
    print(f"Max value: {max_val}")
    print(f"Values within 1 of max: {near_max_count}")
    print(f"Percentage near max: {near_max_count / len(test_rul) * 100:.1f}%")
    
    if near_max_count > len(test_rul) * 0.1:  # More than 10% near max
        print(f"--> Appears to be CAPPED at {max_val} cycles")
    
    print("\n" + "=" * 80)
    print("COMPARISON")
    print("=" * 80)
    
    print(f"\nValidation Set:")
    print(f"  Mean RUL: {np.mean(val_rul):.2f}")
    print(f"  Std RUL: {np.std(val_rul):.2f}")
    print(f"  Range: {np.min(val_rul)} to {np.max(val_rul)}")
    
    print(f"\nOfficial Test Set:")
    print(f"  Mean RUL: {np.mean(test_rul):.2f}")
    print(f"  Std RUL: {np.std(test_rul):.2f}")
    print(f"  Range: {np.min(test_rul)} to {np.max(test_rul)}")
    
    print(f"\nVariance ratio (test/val): {np.var(test_rul) / np.var(val_rul):.2f}")
    print(f"Std ratio (test/val): {np.std(test_rul) / np.std(val_rul):.2f}")
    
    print("\n" + "=" * 80)
    print("EXPLANATION FOR RMSE/R2 DISCREPANCY")
    print("=" * 80)
    
    print("\nLower variance in test set explains both:")
    print("1. Lower RMSE (smaller variance = smaller potential errors)")
    print("2. Lower R2 (model explains less of already-limited variance)")
    
    print("\nR2 formula: R2 = 1 - (SS_res / SS_tot)")
    print("When SS_tot (total variance) is smaller, the same SS_res")
    print("leads to a lower R2, even if absolute error (RMSE) is better.")
    
    # Save results
    results = {
        'validation_rul': {
            'count': int(len(val_rul)),
            'mean': float(np.mean(val_rul)),
            'std': float(np.std(val_rul)),
            'min': float(np.min(val_rul)),
            'max': float(np.max(val_rul)),
            'median': float(np.median(val_rul)),
            'p25': float(np.percentile(val_rul, 25)),
            'p75': float(np.percentile(val_rul, 75)),
            'is_capped': False
        },
        'official_test_rul': {
            'count': int(len(test_rul)),
            'mean': float(np.mean(test_rul)),
            'std': float(np.std(test_rul)),
            'min': float(np.min(test_rul)),
            'max': float(np.max(test_rul)),
            'median': float(np.median(test_rul)),
            'p25': float(np.percentile(test_rul, 25)),
            'p75': float(np.percentile(test_rul, 75)),
            'is_capped': bool(near_max_count > len(test_rul) * 0.1),
            'cap_value': int(max_val) if near_max_count > len(test_rul) * 0.1 else None
        },
        'variance_ratio': float(np.var(test_rul) / np.var(val_rul)),
        'std_ratio': float(np.std(test_rul) / np.std(val_rul))
    }
    
    import json
    results_dir = Path(__file__).parent.parent / "results"
    with open(results_dir / "rul_distribution_analysis.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nRUL distribution analysis saved to {results_dir / 'rul_distribution_analysis.json'}")
    
    return results

if __name__ == "__main__":
    results = analyze_rul_distribution()
