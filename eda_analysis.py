"""
Exploratory Data Analysis for NASA C-MAPSS FD001 Dataset
Predictive Maintenance for Industrial Equipment - Final Academic Project
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Define paths - use environment variable or project-relative path
DATA_DIR = Path(os.getenv('CMAPSS_DATA_DIR', Path(__file__).parent / "data" / "archive"))
OUTPUT_DIR = Path(__file__).parent / "visualizations"
TRAIN_PATH = DATA_DIR / "train_FD001.txt"
TEST_PATH = DATA_DIR / "test_FD001.txt"
RUL_PATH = DATA_DIR / "RUL_FD001.txt"

# Define column names
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

def load_data():
    """Load train, test, and RUL data"""
    print("=" * 80)
    print("LOADING DATA")
    print("=" * 80)
    
    # Load training data
    train_df = pd.read_csv(TRAIN_PATH, sep='\s+', header=None, names=COLUMN_NAMES, engine='python')
    print(f"Training data shape: {train_df.shape}")
    
    # Load test data
    test_df = pd.read_csv(TEST_PATH, sep='\s+', header=None, names=COLUMN_NAMES, engine='python')
    print(f"Test data shape: {test_df.shape}")
    
    # Load RUL data
    rul_df = pd.read_csv(RUL_PATH, sep=' ', header=None)
    rul_df = rul_df.dropna(axis=1, how='all')
    rul_df.columns = ['RUL']
    print(f"RUL data shape: {rul_df.shape}")
    
    return train_df, test_df, rul_df

def analyze_basic_structure(train_df, test_df, rul_df):
    """Analyze basic structure of the dataset"""
    print("\n" + "=" * 80)
    print("BASIC STRUCTURE ANALYSIS")
    print("=" * 80)
    
    # Number of engines
    train_engines = train_df['engine_id'].nunique()
    test_engines = test_df['engine_id'].nunique()
    print(f"\nNumber of engines in training set: {train_engines}")
    print(f"Number of engines in test set: {test_engines}")
    
    # Number of cycles per engine
    train_cycles = train_df.groupby('engine_id')['cycle'].max()
    test_cycles = test_df.groupby('engine_id')['cycle'].max()
    
    print(f"\nTraining set - Cycles per engine:")
    print(f"  Min: {train_cycles.min()}")
    print(f"  Max: {train_cycles.max()}")
    print(f"  Mean: {train_cycles.mean():.2f}")
    print(f"  Median: {train_cycles.median():.2f}")
    
    print(f"\nTest set - Cycles per engine:")
    print(f"  Min: {test_cycles.min()}")
    print(f"  Max: {test_cycles.max()}")
    print(f"  Mean: {test_cycles.mean():.2f}")
    print(f"  Median: {test_cycles.median():.2f}")
    
    # Total cycles
    print(f"\nTotal cycles in training set: {len(train_df)}")
    print(f"Total cycles in test set: {len(test_df)}")
    
    # RUL statistics
    print(f"\nRUL statistics for test set:")
    print(f"  Min: {rul_df['RUL'].min()}")
    print(f"  Max: {rul_df['RUL'].max()}")
    print(f"  Mean: {rul_df['RUL'].mean():.2f}")
    print(f"  Median: {rul_df['RUL'].median():.2f}")
    
    return train_engines, test_engines, train_cycles, test_cycles

def analyze_columns(train_df):
    """Analyze and explain all columns"""
    print("\n" + "=" * 80)
    print("COLUMN ANALYSIS")
    print("=" * 80)
    
    print("\nColumn descriptions:")
    print("1. engine_id: Unique identifier for each engine (1-100)")
    print("2. cycle: Time in cycles (operational time)")
    print("3. setting_1: Operational setting 1 (affects engine performance)")
    print("4. setting_2: Operational setting 2 (affects engine performance)")
    print("5. setting_3: Operational setting 3 (affects engine performance)")
    print("6-26. sensor_1 to sensor_21: Various sensor measurements")
    
    print("\nData types:")
    print(train_df.dtypes)
    
    print("\nBasic statistics:")
    print(train_df.describe())

def check_missing_values(train_df, test_df):
    """Check for missing values"""
    print("\n" + "=" * 80)
    print("MISSING VALUES ANALYSIS")
    print("=" * 80)
    
    print("\nTraining set - Missing values:")
    train_missing = train_df.isnull().sum()
    print(train_missing[train_missing > 0] if train_missing.sum() > 0 else "No missing values")
    
    print("\nTest set - Missing values:")
    test_missing = test_df.isnull().sum()
    print(test_missing[test_missing > 0] if test_missing.sum() > 0 else "No missing values")
    
    return train_missing.sum() == 0 and test_missing.sum() == 0

def analyze_constant_sensors(train_df, test_df):
    """Identify constant or nearly constant sensors"""
    print("\n" + "=" * 80)
    print("CONSTANT SENSOR ANALYSIS")
    print("=" * 80)
    
    sensor_cols = [col for col in train_df.columns if col.startswith('sensor_')]
    
    print("\nTraining set - Constant sensors:")
    constant_sensors_train = []
    for sensor in sensor_cols:
        std = train_df[sensor].std()
        if std < 1e-6:
            constant_sensors_train.append(sensor)
            print(f"  {sensor}: std = {std:.10f} (CONSTANT)")
    
    print("\nTest set - Constant sensors:")
    constant_sensors_test = []
    for sensor in sensor_cols:
        std = test_df[sensor].std()
        if std < 1e-6:
            constant_sensors_test.append(sensor)
            print(f"  {sensor}: std = {std:.10f} (CONSTANT)")
    
    # Check for nearly constant sensors (low variance)
    print("\nTraining set - Nearly constant sensors (std < 0.01):")
    nearly_constant_train = []
    for sensor in sensor_cols:
        std = train_df[sensor].std()
        if std < 0.01 and std >= 1e-6:
            nearly_constant_train.append(sensor)
            print(f"  {sensor}: std = {std:.6f}")
    
    print("\nTest set - Nearly constant sensors (std < 0.01):")
    nearly_constant_test = []
    for sensor in sensor_cols:
        std = test_df[sensor].std()
        if std < 0.01 and std >= 1e-6:
            nearly_constant_test.append(sensor)
            print(f"  {sensor}: std = {std:.6f}")
    
    return constant_sensors_train, constant_sensors_test, nearly_constant_train, nearly_constant_test

def analyze_sensor_distributions(train_df):
    """Analyze distribution of sensor variables"""
    print("\n" + "=" * 80)
    print("SENSOR DISTRIBUTION ANALYSIS")
    print("=" * 80)
    
    sensor_cols = [col for col in train_df.columns if col.startswith('sensor_')]
    
    print("\nSensor statistics (Training set):")
    for sensor in sensor_cols:
        mean = train_df[sensor].mean()
        std = train_df[sensor].std()
        min_val = train_df[sensor].min()
        max_val = train_df[sensor].max()
        skew = train_df[sensor].skew()
        print(f"  {sensor}: mean={mean:.2f}, std={std:.2f}, min={min_val:.2f}, max={max_val:.2f}, skew={skew:.2f}")

def calculate_rul_training(train_df):
    """Calculate RUL for training data"""
    print("\n" + "=" * 80)
    print("RUL CALCULATION FOR TRAINING DATA")
    print("=" * 80)
    
    print("\nExplanation:")
    print("- In the training set, each engine runs until failure")
    print("- RUL for each cycle = max_cycle_for_engine - current_cycle")
    print("- This represents remaining cycles before failure")
    
    # Calculate RUL for training data
    max_cycles = train_df.groupby('engine_id')['cycle'].max().reset_index()
    max_cycles.columns = ['engine_id', 'max_cycle']
    train_df = train_df.merge(max_cycles, on='engine_id')
    train_df['RUL'] = train_df['max_cycle'] - train_df['cycle']
    
    print("\nTraining RUL statistics:")
    print(f"  Min: {train_df['RUL'].min()}")
    print(f"  Max: {train_df['RUL'].max()}")
    print(f"  Mean: {train_df['RUL'].mean():.2f}")
    
    return train_df

def explain_rul_test(test_df, rul_df):
    """Explain how RUL should be used for test data"""
    print("\n" + "=" * 80)
    print("RUL USAGE FOR TEST DATA")
    print("=" * 80)
    
    print("\nExplanation:")
    print("- Test data ends BEFORE failure occurs")
    print("- RUL_FD001.txt provides the true remaining useful life for each test engine")
    print("- For each test engine: RUL = provided_RUL_value")
    print("- This is the ground truth for evaluation")
    print("- Model should predict RUL for the LAST cycle of each test engine")
    
    print("\nTest set RUL values (first 10 engines):")
    print(rul_df.head(10))

def identify_data_leakage():
    """Identify potential data leakage problems"""
    print("\n" + "=" * 80)
    print("DATA LEAKAGE ANALYSIS")
    print("=" * 80)
    
    print("\nPotential data leakage issues:")
    print("1. Engine ID: Using engine_id as a feature would leak information")
    print("   - Solution: Do NOT use engine_id as a feature for prediction")
    print("   - Use only for grouping during analysis")
    
    print("\n2. Cycle number: Direct use might leak temporal information")
    print("   - Solution: Use relative degradation features, not absolute cycle")
    print("   - Consider using cycle as a feature with caution")
    
    print("\n3. Future information in training:")
    print("   - When calculating RUL, ensure no future sensor data is used")
    print("   - Use only current and past sensor readings")
    
    print("\n4. Test set contamination:")
    print("   - Ensure test engines are not in training set")
    print("   - FD001 has separate engines (100 train, 100 test)")
    
    print("\n5. Sensor selection:")
    print("   - Constant sensors provide no information")
    print("   - Remove them to avoid noise and potential leakage")

def recommend_train_val_test_methodology():
    """Recommend appropriate train/validation/test methodology"""
    print("\n" + "=" * 80)
    print("TRAIN/VALIDATION/TEST METHODOLOGY RECOMMENDATIONS")
    print("=" * 80)
    
    print("\nFor time-series predictive maintenance:")
    print("\n1. Engine-based split (recommended):")
    print("   - Split by engines, not by cycles")
    print("   - Train: 70% of engines")
    print("   - Validation: 15% of engines")
    print("   - Test: 15% of engines")
    print("   - This prevents data leakage from same engine")
    
    print("\n2. Time-based split within engines:")
    print("   - For each engine: use early cycles for training, later for validation")
    print("   - Simulates real-world scenario (predict future from past)")
    
    print("\n3. Cross-validation strategy:")
    print("   - Use GroupKFold with engine_id as groups")
    print("   - Ensures same engine doesn't appear in both train and val")
    
    print("\n4. Final evaluation:")
    print("   - Use provided test set (FD001 test)")
    print("   - Compare predictions with RUL_FD001 ground truth")

def recommend_ml_models():
    """Recommend suitable ML models for RUL prediction"""
    print("\n" + "=" * 80)
    print("ML MODEL RECOMMENDATIONS")
    print("=" * 80)
    
    print("\n1. Baseline models:")
    print("   - Linear Regression: Simple baseline")
    print("   - Decision Tree: Interpretable, handles non-linearities")
    
    print("\n2. Ensemble methods:")
    print("   - Random Forest: Robust, handles noise well")
    print("   - Gradient Boosting (XGBoost, LightGBM): State-of-the-art for tabular data")
    print("   - Good for handling sensor correlations")
    
    print("\n3. Deep learning approaches:")
    print("   - LSTM/GRU: Captures temporal dependencies")
    print("   - 1D CNN: Efficient for time-series patterns")
    print("   - Transformer: For long-range dependencies")
    
    print("\n4. Specialized approaches:")
    print("   - CNN-LSTM hybrid: Combines spatial and temporal features")
    print("   - Attention mechanisms: Focus on important time steps")
    
    print("\nRecommendation for FD001:")
    print("   - Start with Random Forest or XGBoost (good baseline)")
    print("   - Progress to LSTM if temporal patterns are important")
    print("   - FD001 has single condition, simpler than FD002/004")

def recommend_evaluation_metrics():
    """Recommend suitable evaluation metrics"""
    print("\n" + "=" * 80)
    print("EVALUATION METRICS RECOMMENDATIONS")
    print("=" * 80)
    
    print("\n1. Regression metrics:")
    print("   - RMSE (Root Mean Squared Error): Penalizes large errors")
    print("   - MAE (Mean Absolute Error): Easy to interpret")
    print("   - R² (R-squared): Explains variance")
    
    print("\n2. Specialized metrics for predictive maintenance:")
    print("   - RMSE (commonly used in C-MAPSS challenge)")
    print("   - Score function: exp(-error/13) - 1 for error < 0")
    print("   - This asymmetric metric penalizes late predictions more")
    
    print("\n3. Business-oriented metrics:")
    print("   - Accuracy within threshold (e.g., ±20 cycles)")
    print("   - Precision/Recall for failure prediction")
    print("   - Cost-based metrics (maintenance cost optimization)")
    
    print("\nRecommendation:")
    print("   - Primary: RMSE (standard for C-MAPSS)")
    print("   - Secondary: MAE for interpretability")
    print("   - Additional: Accuracy within ±30 cycles")

def visualize_data(train_df, test_df):
    """Create visualizations for the data"""
    print("\n" + "=" * 80)
    print("CREATING VISUALIZATIONS")
    print("=" * 80)
    
    # Create output directory
    output_dir = Path("c:/Users/ULTRAPC/Desktop/PFA26/visualizations")
    output_dir.mkdir(exist_ok=True)
    
    # 1. Distribution of cycles per engine
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    train_cycles = train_df.groupby('engine_id')['cycle'].max()
    test_cycles = test_df.groupby('engine_id')['cycle'].max()
    
    axes[0].hist(train_cycles, bins=30, alpha=0.7, label='Train')
    axes[0].set_xlabel('Max Cycles')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Distribution of Max Cycles per Engine (Train)')
    axes[0].legend()
    
    axes[1].hist(test_cycles, bins=30, alpha=0.7, color='orange', label='Test')
    axes[1].set_xlabel('Max Cycles')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Distribution of Max Cycles per Engine (Test)')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'cycles_distribution.png', dpi=300)
    print("Saved: cycles_distribution.png")
    plt.close()
    
    # 2. Sensor correlation heatmap
    sensor_cols = [col for col in train_df.columns if col.startswith('sensor_')]
    sensor_data = train_df[sensor_cols].sample(min(10000, len(train_df)))
    
    plt.figure(figsize=(15, 12))
    correlation_matrix = sensor_data.corr()
    sns.heatmap(correlation_matrix, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('Sensor Correlation Matrix')
    plt.tight_layout()
    plt.savefig(output_dir / 'sensor_correlation.png', dpi=300)
    print("Saved: sensor_correlation.png")
    plt.close()
    
    # 3. Sample sensor trajectories for a few engines
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    
    sample_engines = [1, 2, 3, 4, 5, 6]
    for idx, engine_id in enumerate(sample_engines):
        engine_data = train_df[train_df['engine_id'] == engine_id]
        axes[idx].plot(engine_data['cycle'], engine_data['sensor_2'], label='Sensor 2')
        axes[idx].plot(engine_data['cycle'], engine_data['sensor_3'], label='Sensor 3')
        axes[idx].plot(engine_data['cycle'], engine_data['sensor_4'], label='Sensor 4')
        axes[idx].set_xlabel('Cycle')
        axes[idx].set_ylabel('Sensor Value')
        axes[idx].set_title(f'Engine {engine_id} - Sensor Trajectories')
        axes[idx].legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'sensor_trajectories.png', dpi=300)
    print("Saved: sensor_trajectories.png")
    plt.close()
    
    # 4. RUL distribution (if calculated)
    if 'RUL' in train_df.columns:
        plt.figure(figsize=(10, 6))
        plt.hist(train_df['RUL'], bins=50, alpha=0.7, edgecolor='black')
        plt.xlabel('RUL (cycles)')
        plt.ylabel('Frequency')
        plt.title('Distribution of RUL in Training Set')
        plt.tight_layout()
        plt.savefig(output_dir / 'rul_distribution.png', dpi=300)
        print("Saved: rul_distribution.png")
        plt.close()
    
    print(f"\nAll visualizations saved to: {output_dir}")

def main():
    """Main analysis pipeline"""
    print("\n" + "=" * 80)
    print("NASA C-MAPSS FD001 DATASET EXPLORATORY DATA ANALYSIS")
    print("=" * 80)
    
    # Load data
    train_df, test_df, rul_df = load_data()
    
    # Basic structure analysis
    analyze_basic_structure(train_df, test_df, rul_df)
    
    # Column analysis
    analyze_columns(train_df)
    
    # Missing values
    has_no_missing = check_missing_values(train_df, test_df)
    
    # Constant sensors
    const_train, const_test, near_const_train, near_const_test = analyze_constant_sensors(train_df, test_df)
    
    # Sensor distributions
    analyze_sensor_distributions(train_df)
    
    # RUL calculation
    train_df = calculate_rul_training(train_df)
    
    # RUL explanation
    explain_rul_test(test_df, rul_df)
    
    # Data leakage
    identify_data_leakage()
    
    # Methodology recommendations
    recommend_train_val_test_methodology()
    
    # ML model recommendations
    recommend_ml_models()
    
    # Evaluation metrics
    recommend_evaluation_metrics()
    
    # Visualizations
    visualize_data(train_df, test_df)
    
    # Summary
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"\nDataset: NASA C-MAPSS FD001")
    print(f"Training engines: {train_df['engine_id'].nunique()}")
    print(f"Test engines: {test_df['engine_id'].nunique()}")
    print(f"Total training cycles: {len(train_df)}")
    print(f"Total test cycles: {len(test_df)}")
    print(f"Constant sensors (train): {len(const_train)}")
    print(f"Constant sensors (test): {len(const_test)}")
    print(f"No missing values: {has_no_missing}")
    print(f"\nConditions: ONE (Sea Level)")
    print(f"Fault Modes: ONE (HPC Degradation)")
    print("\nEDA completed successfully!")

if __name__ == "__main__":
    main()
