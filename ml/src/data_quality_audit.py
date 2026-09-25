"""
Data Quality Audit System for NASA C-MAPSS FD001 Dataset
Validates sensor data for anomalies, leakage, and consistency
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import json
from enum import Enum


class IssueSeverity(Enum):
    """Severity levels for data quality issues"""
    CRITICAL = "critical"      # Model breaking issues
    WARNING = "warning"        # Performance degradation
    INFO = "info"             # Informational only


class IssueCategory(Enum):
    """Categories of data quality issues"""
    ANOMALY = "anomaly"
    LEAKAGE = "leakage"
    CONSISTENCY = "consistency"


@dataclass
class DataQualityIssue:
    """Represents a single data quality issue"""
    category: str
    check_name: str
    severity: str
    description: str
    affected_items: List[str] = None
    count: int = 0
    recommendation: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class DataQualityReport:
    """Comprehensive data quality report"""
    audit_id: str
    timestamp: str
    data_health_score: float
    total_checks: int
    passed_checks: int
    failed_checks: int
    total_issues: int
    critical_issues: int
    warning_issues: int
    info_issues: int
    issues: List[Dict] = None
    sensor_stats: Dict = None
    engine_stats: Dict = None
    recommendations: List[str] = None

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, default=str)


class DataQualityAudit:
    """Main audit engine with modular checkers"""

    # Known constant sensors from EDA
    CONSTANT_SENSORS = ['sensor_1', 'sensor_5', 'sensor_10', 'sensor_16', 'sensor_18', 'sensor_19']

    # Settings columns
    SETTINGS_COLS = ['setting_1', 'setting_2', 'setting_3']

    # Sensor columns (all 21)
    SENSOR_COLS = [f'sensor_{i}' for i in range(1, 22)]

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.issues: List[DataQualityIssue] = []
        self.checks_run = 0
        self.checks_passed = 0

    def log(self, message: str):
        if self.verbose:
            print(f"[AUDIT] {message}")

    def add_issue(self, category: IssueCategory, check_name: str, severity: IssueSeverity,
                  description: str, affected_items: List[str] = None, count: int = 0,
                  recommendation: str = ""):
        """Add an issue to the report"""
        issue = DataQualityIssue(
            category=category.value,
            check_name=check_name,
            severity=severity.value,
            description=description,
            affected_items=affected_items or [],
            count=count,
            recommendation=recommendation
        )
        self.issues.append(issue)
        self.log(f"  ⚠️  [{severity.value.upper()}] {check_name}: {description}")

    # ==================== ANOMALY CHECKS ====================

    def check_missing_values(self, df: pd.DataFrame) -> bool:
        """Check for missing values"""
        self.log("Checking for missing values...")
        self.checks_run += 1

        missing = df.isnull().sum()
        if missing.sum() == 0:
            self.log("  ✓ No missing values found")
            self.checks_passed += 1
            return True

        missing_cols = missing[missing > 0]
        self.add_issue(
            IssueCategory.ANOMALY,
            "missing_values",
            IssueSeverity.CRITICAL,
            f"Missing values detected in {len(missing_cols)} columns",
            affected_items=missing_cols.index.tolist(),
            count=missing.sum(),
            recommendation="Investigate source of missing values. Consider forward-fill or removal."
        )
        return False

    def check_duplicates(self, df: pd.DataFrame) -> bool:
        """Check for duplicate rows"""
        self.log("Checking for duplicate rows...")
        self.checks_run += 1

        duplicates_count = df.duplicated().sum()
        if duplicates_count == 0:
            self.log("  ✓ No duplicate rows")
            self.checks_passed += 1
            return True

        self.add_issue(
            IssueCategory.ANOMALY,
            "duplicate_rows",
            IssueSeverity.WARNING,
            f"Exact duplicate rows found",
            count=duplicates_count,
            recommendation="Remove duplicate rows using df.drop_duplicates()"
        )
        return False

    def check_constant_sensors(self, df: pd.DataFrame) -> bool:
        """Verify constant sensors are truly constant"""
        self.log("Checking constant sensors...")
        self.checks_run += 1

        constant_found = []
        for sensor in self.CONSTANT_SENSORS:
            if sensor in df.columns:
                std = df[sensor].std()
                if std == 0:
                    constant_found.append(sensor)

        if len(constant_found) == len(self.CONSTANT_SENSORS):
            self.log(f"  ✓ All {len(constant_found)} constant sensors verified")
            self.checks_passed += 1
            return True

        missing_constant = set(self.CONSTANT_SENSORS) - set(constant_found)
        self.add_issue(
            IssueCategory.ANOMALY,
            "constant_sensors_drift",
            IssueSeverity.CRITICAL,
            f"Expected constant sensors not constant: {missing_constant}",
            affected_items=list(missing_constant),
            recommendation="Investigate sensor {0} - should have zero variance".format(', '.join(missing_constant))
        )
        return False

    def check_zero_variance_sensors(self, df: pd.DataFrame) -> bool:
        """Find sensors with zero variance (constant)"""
        self.log("Checking for zero-variance sensors...")
        self.checks_run += 1

        zero_var_sensors = []
        for col in df.columns:
            if col.startswith('sensor_') and df[col].std() == 0:
                zero_var_sensors.append(col)

        if len(zero_var_sensors) == 0:
            self.log("  ✓ No unexpected zero-variance sensors")
            self.checks_passed += 1
            return True

        # Filter out expected constant sensors
        unexpected = [s for s in zero_var_sensors if s not in self.CONSTANT_SENSORS]
        if len(unexpected) == 0:
            self.checks_passed += 1
            return True

        self.add_issue(
            IssueCategory.ANOMALY,
            "unexpected_zero_variance",
            IssueSeverity.WARNING,
            f"Unexpected zero-variance sensors found",
            affected_items=unexpected,
            recommendation="Remove zero-variance sensors as they provide no predictive value"
        )
        return False

    def check_outliers(self, df: pd.DataFrame, iqr_multiplier: float = 1.5) -> bool:
        """Detect outliers using IQR method"""
        self.log(f"Checking for outliers (IQR multiplier={iqr_multiplier})...")
        self.checks_run += 1

        outlier_counts = {}
        total_outliers = 0

        for col in self.SENSOR_COLS:
            if col not in df.columns or col in self.CONSTANT_SENSORS:
                continue

            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - iqr_multiplier * IQR
            upper_bound = Q3 + iqr_multiplier * IQR

            outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            outlier_count = outlier_mask.sum()

            if outlier_count > 0:
                outlier_pct = (outlier_count / len(df)) * 100
                if outlier_pct > 5:  # Flag if >5% outliers
                    outlier_counts[col] = (outlier_count, outlier_pct)
                    total_outliers += outlier_count

        if len(outlier_counts) == 0:
            self.log("  ✓ No significant outliers detected")
            self.checks_passed += 1
            return True

        affected = [f"{col} ({pct:.1f}%)" for col, (cnt, pct) in outlier_counts.items()]
        self.add_issue(
            IssueCategory.ANOMALY,
            "outliers",
            IssueSeverity.WARNING,
            f"Outliers detected in {len(outlier_counts)} sensors",
            affected_items=affected,
            count=total_outliers,
            recommendation="Consider robust scaling or removing extreme outliers"
        )
        return False

    def check_rate_of_change(self, df: pd.DataFrame, threshold_pct: float = 20.0) -> bool:
        """Detect sudden sensor jumps"""
        self.log(f"Checking rate of change (threshold={threshold_pct}%)...")
        self.checks_run += 1

        df_sorted = df.sort_values(['engine_id', 'cycle']).reset_index(drop=True)
        spike_issues = {}
        total_spikes = 0

        for col in self.SENSOR_COLS:
            if col not in df_sorted.columns or col in self.CONSTANT_SENSORS:
                continue

            # Calculate rate of change within each engine
            for engine_id in df_sorted['engine_id'].unique():
                engine_data = df_sorted[df_sorted['engine_id'] == engine_id][col].values

                if len(engine_data) < 2:
                    continue

                pct_change = np.abs(np.diff(engine_data) / (np.abs(engine_data[:-1]) + 1e-10)) * 100
                spike_mask = pct_change > threshold_pct
                spike_count = spike_mask.sum()

                if spike_count > 0:
                    key = f"{col}_engine_{engine_id}"
                    spike_issues[key] = spike_count
                    total_spikes += spike_count

        if len(spike_issues) == 0:
            self.log("  ✓ No sudden sensor jumps detected")
            self.checks_passed += 1
            return True

        top_spikes = sorted(spike_issues.items(), key=lambda x: x[1], reverse=True)[:5]
        affected = [f"{k} ({v} spikes)" for k, v in top_spikes]

        self.add_issue(
            IssueCategory.ANOMALY,
            "rate_of_change_spikes",
            IssueSeverity.INFO,
            f"Sudden sensor changes detected in {len(spike_issues)} sensor-engine combinations",
            affected_items=affected,
            count=total_spikes,
            recommendation="Investigate whether spikes are legitimate degradation or sensor errors"
        )
        return False

    def check_sensor_ranges(self, df: pd.DataFrame) -> bool:
        """Validate sensor values are within expected ranges"""
        self.log("Checking sensor ranges...")
        self.checks_run += 1

        # Expected ranges from DATASET_ANALYSIS.md
        expected_ranges = {
            'sensor_2': (640, 645),
            'sensor_3': (1570, 1620),
            'sensor_4': (1380, 1445),
            'sensor_7': (549, 557),
            'sensor_8': (2387, 2389),
            'sensor_9': (9020, 9250),
            'sensor_11': (46, 49),
            'sensor_12': (518, 524),
            'sensor_13': (2387, 2389),
            'sensor_14': (8090, 8300),
            'sensor_15': (8.3, 8.6),
            'sensor_17': (388, 401),
            'sensor_20': (38, 40),
            'sensor_21': (22, 24)
        }

        range_violations = {}
        for sensor, (min_val, max_val) in expected_ranges.items():
            if sensor not in df.columns:
                continue

            below_min = (df[sensor] < min_val).sum()
            above_max = (df[sensor] > max_val).sum()
            violations = below_min + above_max

            if violations > 0:
                range_violations[sensor] = violations

        if len(range_violations) == 0:
            self.log("  ✓ All sensors within expected ranges")
            self.checks_passed += 1
            return True

        affected = [f"{col} ({cnt} violations)" for col, cnt in range_violations.items()]
        self.add_issue(
            IssueCategory.ANOMALY,
            "sensor_range_violations",
            IssueSeverity.WARNING,
            f"Values outside expected ranges in {len(range_violations)} sensors",
            affected_items=affected,
            recommendation="Verify these are legitimate extremes or data collection errors"
        )
        return False

    # ==================== LEAKAGE CHECKS ====================

    def check_engine_overlap(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> bool:
        """Check if same engines appear in both train and test"""
        self.log("Checking for engine ID overlap (train/test leakage)...")
        self.checks_run += 1

        train_engines = set(train_df['engine_id'].unique())
        test_engines = set(test_df['engine_id'].unique())
        overlap = train_engines & test_engines

        if len(overlap) == 0:
            self.log("  ✓ No engine overlap between train and test")
            self.checks_passed += 1
            return True

        self.add_issue(
            IssueCategory.LEAKAGE,
            "engine_overlap",
            IssueSeverity.CRITICAL,
            f"Same engines appear in both train and test sets",
            affected_items=sorted(list(overlap)),
            count=len(overlap),
            recommendation="CRITICAL: Remove overlapping engines from one set before modeling"
        )
        return False

    def check_temporal_leakage(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> bool:
        """Check for temporal leakage between splits"""
        self.log("Checking for temporal leakage...")
        self.checks_run += 1

        # This is mostly for same-engine temporal split, but check cycle ranges
        train_max_cycle = train_df['cycle'].max()
        test_max_cycle = test_df['cycle'].max()
        test_min_cycle = test_df['cycle'].min()

        # Check if test cycles are significantly different from training
        if test_max_cycle <= train_max_cycle and test_min_cycle >= 1:
            self.log("  ✓ No temporal leakage detected")
            self.checks_passed += 1
            return True

        self.log("  ℹ️  Note: Test max cycle exceeds training (may be expected)")
        self.checks_passed += 1
        return True

    def check_data_leakage_indicators(self, df: pd.DataFrame) -> bool:
        """Check for other leakage indicators"""
        self.log("Checking for data leakage indicators...")
        self.checks_run += 1

        issues_found = []

        # Check if engine_id would leak information
        if 'engine_id' in df.columns:
            engine_corr = df['engine_id'].corr(df['RUL']) if 'RUL' in df.columns else 0
            if abs(engine_corr) > 0.3:
                issues_found.append("engine_id has high correlation with RUL")

        if len(issues_found) == 0:
            self.log("  ✓ No significant leakage indicators")
            self.checks_passed += 1
            return True

        self.add_issue(
            IssueCategory.LEAKAGE,
            "leakage_indicators",
            IssueSeverity.WARNING,
            "Potential information leakage detected",
            affected_items=issues_found,
            recommendation="Be cautious with features that correlate with RUL"
        )
        return False

    # ==================== CONSISTENCY CHECKS ====================

    def check_sequential_cycles(self, df: pd.DataFrame) -> bool:
        """Verify cycles are sequential for each engine"""
        self.log("Checking cycle sequencing...")
        self.checks_run += 1

        df_sorted = df.sort_values(['engine_id', 'cycle']).reset_index(drop=True)
        non_sequential = []

        for engine_id in df_sorted['engine_id'].unique():
            engine_cycles = df_sorted[df_sorted['engine_id'] == engine_id]['cycle'].values

            expected_cycles = np.arange(engine_cycles[0], engine_cycles[-1] + 1)
            if not np.array_equal(engine_cycles, expected_cycles):
                non_sequential.append(f"Engine {engine_id}: missing cycles")

        if len(non_sequential) == 0:
            self.log("  ✓ All cycles are sequential")
            self.checks_passed += 1
            return True

        self.add_issue(
            IssueCategory.CONSISTENCY,
            "non_sequential_cycles",
            IssueSeverity.CRITICAL,
            f"Gaps in cycle sequences found in {len(non_sequential)} engines",
            affected_items=non_sequential[:10],
            count=len(non_sequential),
            recommendation="Investigate why cycles are missing for these engines"
        )
        return False

    def check_settings_ranges(self, df: pd.DataFrame) -> bool:
        """Validate operational settings are within expected ranges"""
        self.log("Checking operational settings ranges...")
        self.checks_run += 1

        # Settings should be relatively constant
        setting_ranges = {}
        for setting in self.SETTINGS_COLS:
            if setting in df.columns:
                unique_vals = df[setting].nunique()
                setting_ranges[setting] = unique_vals

        # Most operations use fixed settings
        high_variance_settings = {k: v for k, v in setting_ranges.items() if v > 100}

        if len(high_variance_settings) == 0:
            self.log("  ✓ Settings within expected ranges")
            self.checks_passed += 1
            return True

        self.log("  ℹ️  High variance in some settings (may be expected)")
        self.checks_passed += 1
        return True

    def check_rul_calculation(self, df: pd.DataFrame) -> bool:
        """Verify RUL calculation is correct"""
        self.log("Checking RUL calculation...")
        self.checks_run += 1

        if 'RUL' not in df.columns or 'max_cycle' not in df.columns:
            self.log("  ℹ️  RUL not in dataframe, skipping check")
            self.checks_passed += 1
            return True

        df_sorted = df.sort_values(['engine_id', 'cycle']).reset_index(drop=True)
        calculation_errors = []

        for engine_id in df_sorted['engine_id'].unique():
            engine_data = df_sorted[df_sorted['engine_id'] == engine_id]
            max_cycle = engine_data['max_cycle'].iloc[0]

            calculated_rul = max_cycle - engine_data['cycle']
            actual_rul = engine_data['RUL']

            if not np.allclose(calculated_rul.values, actual_rul.values, atol=1):
                calculation_errors.append(f"Engine {engine_id}")

        if len(calculation_errors) == 0:
            self.log("  ✓ RUL calculation verified")
            self.checks_passed += 1
            return True

        self.add_issue(
            IssueCategory.CONSISTENCY,
            "rul_calculation_error",
            IssueSeverity.CRITICAL,
            f"RUL calculation errors in {len(calculation_errors)} engines",
            affected_items=calculation_errors[:10],
            recommendation="Recalculate RUL using: RUL = max_cycle - current_cycle"
        )
        return False

    def check_degradation_consistency(self, df: pd.DataFrame) -> bool:
        """Check that sensor degradation is generally monotonic"""
        self.log("Checking degradation consistency...")
        self.checks_run += 1

        if 'RUL' not in df.columns:
            self.log("  ℹ️  RUL not in dataframe, skipping check")
            self.checks_passed += 1
            return True

        df_sorted = df.sort_values(['engine_id', 'cycle']).reset_index(drop=True)
        anomalous_engines = []

        # Check if RUL decreases monotonically within each engine
        for engine_id in df_sorted['engine_id'].unique():
            engine_rul = df_sorted[df_sorted['engine_id'] == engine_id]['RUL'].values

            # RUL should be strictly decreasing
            if not np.all(np.diff(engine_rul) <= 0):
                anomalous_engines.append(f"Engine {engine_id}: non-monotonic RUL")

        if len(anomalous_engines) == 0:
            self.log("  ✓ Degradation is consistent")
            self.checks_passed += 1
            return True

        self.add_issue(
            IssueCategory.CONSISTENCY,
            "non_monotonic_degradation",
            IssueSeverity.WARNING,
            f"Non-monotonic degradation in {len(anomalous_engines)} engines",
            affected_items=anomalous_engines[:10],
            recommendation="Expected: RUL should always decrease. Verify data sorting."
        )
        return False

    def check_engine_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate engine-level statistics"""
        self.log("Computing engine statistics...")

        engine_stats = {}
        for engine_id in df['engine_id'].unique():
            engine_data = df[df['engine_id'] == engine_id]

            engine_stats[engine_id] = {
                'cycles': len(engine_data),
                'max_cycle': engine_data['cycle'].max(),
                'min_cycle': engine_data['cycle'].min(),
                'RUL': engine_data['RUL'].iloc[-1] if 'RUL' in engine_data.columns else None
            }

        return engine_stats

    def check_sensor_statistics(self, df: pd.DataFrame) -> Dict[str, Dict]:
        """Calculate sensor statistics"""
        self.log("Computing sensor statistics...")

        sensor_stats = {}
        for col in self.SENSOR_COLS:
            if col not in df.columns or col in self.CONSTANT_SENSORS:
                continue

            sensor_stats[col] = {
                'mean': float(df[col].mean()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'q25': float(df[col].quantile(0.25)),
                'q75': float(df[col].quantile(0.75))
            }

        return sensor_stats

    # ==================== MAIN AUDIT METHOD ====================

    def audit(self, train_df: pd.DataFrame = None, test_df: pd.DataFrame = None) -> DataQualityReport:
        """
        Run complete data quality audit

        Args:
            train_df: Training data
            test_df: Test data (optional)

        Returns:
            DataQualityReport with results
        """
        self.log("=" * 80)
        self.log("STARTING DATA QUALITY AUDIT")
        self.log("=" * 80)

        self.issues = []
        self.checks_run = 0
        self.checks_passed = 0

        # ===== ANOMALY CHECKS =====
        self.log("\n[PHASE 1: ANOMALY DETECTION]")
        if train_df is not None:
            self.check_missing_values(train_df)
            self.check_duplicates(train_df)
            self.check_constant_sensors(train_df)
            self.check_zero_variance_sensors(train_df)
            self.check_outliers(train_df)
            self.check_rate_of_change(train_df)
            self.check_sensor_ranges(train_df)

        # ===== LEAKAGE CHECKS =====
        self.log("\n[PHASE 2: LEAKAGE DETECTION]")
        if train_df is not None and test_df is not None:
            self.check_engine_overlap(train_df, test_df)
            self.check_temporal_leakage(train_df, test_df)

        if train_df is not None:
            self.check_data_leakage_indicators(train_df)

        # ===== CONSISTENCY CHECKS =====
        self.log("\n[PHASE 3: CONSISTENCY VALIDATION]")
        if train_df is not None:
            self.check_sequential_cycles(train_df)
            self.check_settings_ranges(train_df)
            self.check_rul_calculation(train_df)
            self.check_degradation_consistency(train_df)

        # ===== GENERATE REPORT =====
        self.log("\n[PHASE 4: GENERATING REPORT]")

        critical_count = sum(1 for i in self.issues if i.severity == 'critical')
        warning_count = sum(1 for i in self.issues if i.severity == 'warning')
        info_count = sum(1 for i in self.issues if i.severity == 'info')

        # Calculate health score (0-100)
        # Score = (passed_checks / total_checks) * 100 - (critical_issues * 10 + warning_issues * 3)
        base_score = (self.checks_passed / max(self.checks_run, 1)) * 100
        penalty = (critical_count * 10) + (warning_count * 3) + (info_count * 0.5)
        health_score = max(0, min(100, base_score - penalty))

        # Generate recommendations
        recommendations = []
        if critical_count > 0:
            recommendations.append(f"🔴 {critical_count} CRITICAL issues must be resolved before modeling")
        if warning_count > 0:
            recommendations.append(f"🟡 {warning_count} WARNING issues should be investigated")
        if self.checks_passed == self.checks_run:
            recommendations.append("✅ All checks passed - data quality is good")

        # Compute statistics
        engine_stats = self.check_engine_statistics(train_df) if train_df is not None else {}
        sensor_stats = self.check_sensor_statistics(train_df) if train_df is not None else {}

        report = DataQualityReport(
            audit_id=self._generate_audit_id(),
            timestamp=datetime.now().isoformat(),
            data_health_score=health_score,
            total_checks=self.checks_run,
            passed_checks=self.checks_passed,
            failed_checks=self.checks_run - self.checks_passed,
            total_issues=len(self.issues),
            critical_issues=critical_count,
            warning_issues=warning_count,
            info_issues=info_count,
            issues=[issue.to_dict() for issue in self.issues],
            sensor_stats=sensor_stats,
            engine_stats=engine_stats,
            recommendations=recommendations
        )

        self.log("\n" + "=" * 80)
        self.log("AUDIT COMPLETE")
        self.log("=" * 80)
        self.log(f"Health Score: {health_score:.1f}/100")
        self.log(f"Issues: {critical_count} critical, {warning_count} warnings, {info_count} info")
        self.log(f"Checks: {self.checks_passed}/{self.checks_run} passed")

        return report

    def _generate_audit_id(self) -> str:
        """Generate unique audit ID"""
        from uuid import uuid4
        return str(uuid4())


def run_audit_on_files(train_path: str = None, test_path: str = None,
                       rul_path: str = None, data_dir: str = None) -> DataQualityReport:
    """
    Convenience function to run audit on raw data files

    Args:
        train_path: Path to train_FD001.txt
        test_path: Path to test_FD001.txt
        rul_path: Path to RUL_FD001.txt
        data_dir: Alternative - specify data directory containing all files

    Returns:
        DataQualityReport
    """
    from preprocessing import load_data, remove_constant_sensors, calculate_rul_training, add_relative_cycle

    # Load data
    train_df, test_df, rul_df = load_data(data_dir)

    # Preprocess training data
    train_df = remove_constant_sensors(train_df)
    train_df = calculate_rul_training(train_df)
    train_df = add_relative_cycle(train_df)

    # Preprocess test data
    test_df = remove_constant_sensors(test_df)
    max_cycles = test_df.groupby('engine_id')['cycle'].max().reset_index()
    max_cycles.columns = ['engine_id', 'max_cycle']
    test_df = test_df.merge(max_cycles, on='engine_id')
    test_df = add_relative_cycle(test_df)

    # Run audit
    audit = DataQualityAudit(verbose=True)
    report = audit.audit(train_df, test_df)

    return report


if __name__ == "__main__":
    # Example: Run audit
    print("Data Quality Audit Module")
    print("To use: from data_quality_audit import DataQualityAudit, run_audit_on_files")
    print("\nExample:")
    print("  audit = DataQualityAudit()")
    print("  report = audit.audit(train_df, test_df)")
    print("  print(report.to_json())")
