"""
Utility functions for ML pipeline
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns


def set_random_seed(seed: int = 42) -> None:
    """
    Set random seed for reproducibility
    
    Args:
        seed: Random seed value
    """
    np.random.seed(seed)
    print(f"Random seed set to {seed}")


def split_engines_by_id(
    engine_ids: List[int],
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42
) -> Dict[str, List[int]]:
    """
    Split engines into train/validation/test sets at engine level
    
    Args:
        engine_ids: List of engine IDs
        train_ratio: Proportion of engines for training
        val_ratio: Proportion of engines for validation
        test_ratio: Proportion of engines for testing
        seed: Random seed for reproducibility
        
    Returns:
        Dictionary with 'train', 'val', 'test' keys containing engine IDs
    """
    np.random.seed(seed)
    
    n_engines = len(engine_ids)
    n_train = int(n_engines * train_ratio)
    n_val = int(n_engines * val_ratio)
    
    # Shuffle engine IDs
    shuffled_ids = np.random.permutation(engine_ids)
    
    train_ids = shuffled_ids[:n_train].tolist()
    val_ids = shuffled_ids[n_train:n_train + n_val].tolist()
    test_ids = shuffled_ids[n_train + n_val:].tolist()
    
    print(f"\nEngine Split:")
    print(f"  Train: {len(train_ids)} engines ({len(train_ids)/n_engines:.1%})")
    print(f"  Val: {len(val_ids)} engines ({len(val_ids)/n_engines:.1%})")
    print(f"  Test: {len(test_ids)} engines ({len(test_ids)/n_engines:.1%})")
    
    print(f"\nTrain engine IDs: {sorted(train_ids)}")
    print(f"Val engine IDs: {sorted(val_ids)}")
    print(f"Test engine IDs: {sorted(test_ids)}")
    
    return {
        'train': train_ids,
        'val': val_ids,
        'test': test_ids
    }


def split_data_by_engines(
    df: pd.DataFrame,
    engine_split: Dict[str, List[int]]
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split dataframe by engine IDs
    
    Args:
        df: Input dataframe with engine_id column
        engine_split: Dictionary with train/val/test engine IDs
        
    Returns:
        train_df, val_df, test_df
    """
    train_df = df[df['engine_id'].isin(engine_split['train'])].copy()
    val_df = df[df['engine_id'].isin(engine_split['val'])].copy()
    test_df = df[df['engine_id'].isin(engine_split['test'])].copy()
    
    print(f"\nData Split:")
    print(f"  Train: {len(train_df)} rows")
    print(f"  Val: {len(val_df)} rows")
    print(f"  Test: {len(test_df)} rows")
    
    return train_df, val_df, test_df


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculate evaluation metrics
    
    Args:
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        Dictionary with RMSE, MAE, and R²
    """
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    return {
        'RMSE': rmse,
        'MAE': mae,
        'R2': r2
    }


def save_results(results: Dict, filepath: str) -> None:
    """
    Save results to JSON file
    
    Args:
        results: Dictionary of results
        filepath: Path to save results
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {filepath}")


def load_results(filepath: str) -> Dict:
    """
    Load results from JSON file
    
    Args:
        filepath: Path to results file
        
    Returns:
        Dictionary of results
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def plot_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    title: str = "Actual vs Predicted RUL",
    save_path: str = None
) -> None:
    """
    Plot actual vs predicted values
    
    Args:
        y_true: True values
        y_pred: Predicted values
        title: Plot title
        save_path: Path to save plot
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(y_true, y_pred, alpha=0.5, s=20)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
    plt.xlabel('Actual RUL')
    plt.ylabel('Predicted RUL')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_residuals(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    title: str = "Residual Plot",
    save_path: str = None
) -> None:
    """
    Plot residuals (prediction errors)
    
    Args:
        y_true: True values
        y_pred: Predicted values
        title: Plot title
        save_path: Path to save plot
    """
    residuals = y_true - y_pred
    
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuals, alpha=0.5, s=20)
    plt.axhline(y=0, color='r', linestyle='--', lw=2)
    plt.xlabel('Predicted RUL')
    plt.ylabel('Residual (Actual - Predicted)')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_feature_importance(
    feature_names: List[str],
    importance: np.ndarray,
    title: str = "Feature Importance",
    top_n: int = 20,
    save_path: str = None
) -> None:
    """
    Plot feature importance
    
    Args:
        feature_names: List of feature names
        importance: Feature importance values
        title: Plot title
        top_n: Number of top features to show
        save_path: Path to save plot
    """
    # Sort by importance
    indices = np.argsort(importance)[::-1][:top_n]
    
    plt.figure(figsize=(10, 8))
    plt.barh(range(len(indices)), importance[indices])
    plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
    plt.xlabel('Importance')
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_error_distribution(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    title: str = "Error Distribution",
    save_path: str = None
) -> None:
    """
    Plot distribution of prediction errors
    
    Args:
        y_true: True values
        y_pred: Predicted values
        title: Plot title
        save_path: Path to save plot
    """
    errors = y_true - y_pred
    
    plt.figure(figsize=(10, 6))
    plt.hist(errors, bins=50, edgecolor='black', alpha=0.7)
    plt.axvline(x=0, color='r', linestyle='--', lw=2)
    plt.axvline(x=np.mean(errors), color='g', linestyle='--', lw=2, label=f'Mean: {np.mean(errors):.2f}')
    plt.xlabel('Error (Actual - Predicted)')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_rul_vs_error(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    title: str = "RUL vs Prediction Error",
    save_path: str = None
) -> None:
    """
    Plot RUL vs prediction error to analyze error patterns
    
    Args:
        y_true: True values
        y_pred: Predicted values
        title: Plot title
        save_path: Path to save plot
    """
    errors = y_true - y_pred
    
    plt.figure(figsize=(10, 6))
    plt.scatter(y_true, errors, alpha=0.5, s=20)
    plt.axhline(y=0, color='r', linestyle='--', lw=2)
    plt.xlabel('Actual RUL')
    plt.ylabel('Error (Actual - Predicted)')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()


if __name__ == "__main__":
    # Test utility functions
    print("Testing utility functions...")
    
    # Test engine split
    engine_ids = list(range(1, 101))
    split = split_engines_by_id(engine_ids, seed=42)
    
    print("\nUtility functions test complete")
