"""
Maintenance Decision Layer
Includes safety margin, health score, and maintenance status
"""

import numpy as np
import json
from pathlib import Path


class MaintenanceDecisionLayer:
    """
    Maintenance decision layer for RUL predictions
    """
    
    def __init__(self, safety_margin_cycles=50):
        """
        Initialize decision layer
        
        Args:
            safety_margin_cycles: Conservative margin to subtract from predictions
        """
        self.safety_margin_cycles = safety_margin_cycles
        
        # Maintenance thresholds (in cycles)
        self.thresholds = {
            'critical': 20,      # RUL <= 20: CRITICAL
            'maintenance': 50,   # 20 < RUL <= 50: MAINTENANCE_RECOMMENDED
            'monitor': 100       # 50 < RUL <= 100: MONITOR
        }
        # RUL > 100: NORMAL
    
    def apply_safety_margin(self, predicted_rul):
        """
        Apply conservative safety margin to prediction
        
        Args:
            predicted_rul: Predicted RUL
            
        Returns:
            Effective RUL after safety margin
        """
        effective_rul = max(0, predicted_rul - self.safety_margin_cycles)
        return effective_rul
    
    def calculate_health_score(self, rul):
        """
        Calculate normalized health score (0-100)
        Higher RUL → higher health score
        
        Args:
            rul: Remaining useful life in cycles
            
        Returns:
            Health score from 0 to 100
        """
        # Use sigmoid-like transformation for smooth mapping
        # Map RUL to 0-100 scale
        max_rul = 200  # Cap at 200 cycles for normalization
        
        if rul >= max_rul:
            return 100.0
        elif rul <= 0:
            return 0.0
        else:
            # Linear scaling
            score = (rul / max_rul) * 100
            return min(100.0, max(0.0, score))
    
    def get_maintenance_status(self, rul):
        """
        Determine maintenance status based on RUL
        
        Args:
            rul: Remaining useful life in cycles
            
        Returns:
            Maintenance status string
        """
        if rul <= self.thresholds['critical']:
            return 'CRITICAL'
        elif rul <= self.thresholds['maintenance']:
            return 'MAINTENANCE_RECOMMENDED'
        elif rul <= self.thresholds['monitor']:
            return 'MONITOR'
        else:
            return 'NORMAL'
    
    def process_prediction(self, predicted_rul):
        """
        Process a single RUL prediction through the decision layer
        
        Args:
            predicted_rul: Predicted RUL from model
            
        Returns:
            Dictionary with decision outputs
        """
        # Apply safety margin
        effective_rul = self.apply_safety_margin(predicted_rul)
        
        # Calculate health score
        health_score = self.calculate_health_score(effective_rul)
        
        # Determine maintenance status
        maintenance_status = self.get_maintenance_status(effective_rul)
        
        return {
            'predicted_rul': float(predicted_rul),
            'effective_rul': float(effective_rul),
            'safety_margin_applied': self.safety_margin_cycles,
            'health_score': float(health_score),
            'maintenance_status': maintenance_status
        }
    
    def save_config(self, filepath):
        """
        Save decision layer configuration
        
        Args:
            filepath: Path to save configuration
        """
        config = {
            'safety_margin_cycles': self.safety_margin_cycles,
            'thresholds': self.thresholds,
            'health_score_max_rul': 200
        }
        
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
    
    @classmethod
    def load_config(cls, filepath):
        """
        Load decision layer configuration
        
        Args:
            filepath: Path to configuration file
            
        Returns:
            MaintenanceDecisionLayer instance
        """
        with open(filepath, 'r') as f:
            config = json.load(f)
        
        decision_layer = cls(safety_margin_cycles=config['safety_margin_cycles'])
        decision_layer.thresholds = config['thresholds']
        
        return decision_layer


def create_decision_layer_from_validation():
    """
    Create decision layer with safety margin derived from validation data
    """
    print("=" * 80)
    print("CREATING MAINTENANCE DECISION LAYER")
    print("=" * 80)
    
    # Load bias analysis
    results_path = Path(__file__).parent.parent / "results"
    with open(results_path / "bias_analysis.json", 'r') as f:
        bias_results = json.load(f)
    
    print("\nValidation Bias Analysis:")
    print(f"  Mean error: {bias_results['mean_error']:.2f} cycles")
    print(f"  Overestimation rate: {bias_results['overestimation_rate']:.2%}")
    print(f"  Safety margins (positive errors):")
    print(f"    50th percentile: {bias_results['safety_margins']['p50']:.2f}")
    print(f"    75th percentile: {bias_results['safety_margins']['p75']:.2f}")
    print(f"    90th percentile: {bias_results['safety_margins']['p90']:.2f}")
    
    # Select safety margin (75th percentile for conservative approach)
    selected_margin = int(bias_results['safety_margins']['p75'])
    print(f"\nSelected safety margin: {selected_margin} cycles")
    print("  Rationale: 75th percentile of positive errors covers most overestimation cases")
    print("  Trade-off: More conservative (earlier maintenance) but safer")
    
    # Create decision layer
    decision_layer = MaintenanceDecisionLayer(safety_margin_cycles=selected_margin)
    
    # Save configuration
    config_path = results_path / "decision_layer_config.json"
    decision_layer.save_config(config_path)
    print(f"\nDecision layer configuration saved to {config_path}")
    
    # Test with example predictions
    print("\n" + "=" * 80)
    print("EXAMPLE PREDICTIONS")
    print("=" * 80)
    
    example_ruls = [10, 30, 60, 120, 200]
    for rul in example_ruls:
        result = decision_layer.process_prediction(rul)
        print(f"\nPredicted RUL: {rul}")
        print(f"  Effective RUL: {result['effective_rul']:.1f}")
        print(f"  Health Score: {result['health_score']:.1f}/100")
        print(f"  Status: {result['maintenance_status']}")
    
    print("\n" + "=" * 80)
    print("DECISION LAYER CREATED")
    print("=" * 80)
    
    return decision_layer


if __name__ == "__main__":
    decision_layer = create_decision_layer_from_validation()
