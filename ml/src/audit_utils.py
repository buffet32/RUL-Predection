"""
Utility functions for Data Quality Audit System
Reusable helpers for checks, calculations, and reporting
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from datetime import datetime
import json


class AuditThresholds:
    """Configurable thresholds for audit checks"""

    # Outlier detection
    IQR_MULTIPLIER = 1.5
    OUTLIER_PERCENTAGE_THRESHOLD = 5.0  # Flag if >5% outliers in sensor

    # Rate of change
    RATE_OF_CHANGE_THRESHOLD = 20.0  # Percentage

    # Sensor ranges (from DATASET_ANALYSIS.md)
    EXPECTED_SENSOR_RANGES = {
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

    # Health score penalties
    CRITICAL_PENALTY = 10.0
    WARNING_PENALTY = 3.0
    INFO_PENALTY = 0.5

    # Leakage indicators
    CORRELATION_THRESHOLD = 0.3


class SensorValidator:
    """Validates sensor data"""

    @staticmethod
    def get_constant_sensors() -> List[str]:
        """Get list of known constant sensors"""
        return ['sensor_1', 'sensor_5', 'sensor_10', 'sensor_16', 'sensor_18', 'sensor_19']

    @staticmethod
    def get_useful_sensors() -> List[str]:
        """Get list of useful (non-constant) sensors"""
        all_sensors = [f'sensor_{i}' for i in range(1, 22)]
        constant = SensorValidator.get_constant_sensors()
        return [s for s in all_sensors if s not in constant]

    @staticmethod
    def detect_outliers_iqr(series: pd.Series, multiplier: float = 1.5) -> Tuple[np.ndarray, float]:
        """
        Detect outliers using IQR method

        Returns:
            Tuple of (boolean mask for outliers, percentage of outliers)
        """
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR

        outlier_mask = (series < lower_bound) | (series > upper_bound)
        outlier_pct = (outlier_mask.sum() / len(series)) * 100

        return outlier_mask.values, outlier_pct

    @staticmethod
    def detect_outliers_zscore(series: pd.Series, threshold: float = 3.0) -> Tuple[np.ndarray, float]:
        """
        Detect outliers using Z-score method

        Returns:
            Tuple of (boolean mask for outliers, percentage of outliers)
        """
        z_scores = np.abs((series - series.mean()) / series.std())
        outlier_mask = z_scores > threshold
        outlier_pct = (outlier_mask.sum() / len(series)) * 100

        return outlier_mask.values, outlier_pct

    @staticmethod
    def validate_range(series: pd.Series, min_val: float, max_val: float) -> Tuple[int, int]:
        """
        Check values outside range

        Returns:
            Tuple of (count below min, count above max)
        """
        below_min = (series < min_val).sum()
        above_max = (series > max_val).sum()
        return below_min, above_max

    @staticmethod
    def calculate_sensor_stats(df: pd.DataFrame, sensor_col: str) -> Dict[str, float]:
        """Calculate comprehensive statistics for a sensor"""
        series = df[sensor_col]
        return {
            'mean': float(series.mean()),
            'median': float(series.median()),
            'std': float(series.std()),
            'min': float(series.min()),
            'max': float(series.max()),
            'q25': float(series.quantile(0.25)),
            'q75': float(series.quantile(0.75)),
            'skew': float(series.skew()),
            'kurtosis': float(series.kurtosis()),
            'count': int(series.count()),
            'null_count': int(series.isnull().sum())
        }


class EngineValidator:
    """Validates engine-level data"""

    @staticmethod
    def check_sequential_cycles(engine_df: pd.DataFrame) -> Tuple[bool, List[int]]:
        """
        Check if cycles are sequential

        Returns:
            Tuple of (is_sequential, missing_cycles)
        """
        cycles = sorted(engine_df['cycle'].values)
        expected = np.arange(cycles[0], cycles[-1] + 1)
        missing = np.setdiff1d(expected, cycles).tolist()

        return len(missing) == 0, missing

    @staticmethod
    def check_monotonic_degradation(engine_df: pd.DataFrame) -> Tuple[bool, int]:
        """
        Check if RUL decreases monotonically

        Returns:
            Tuple of (is_monotonic, violation_count)
        """
        if 'RUL' not in engine_df.columns:
            return True, 0

        rul_values = engine_df.sort_values('cycle')['RUL'].values
        violations = (np.diff(rul_values) > 0).sum()

        return violations == 0, int(violations)

    @staticmethod
    def get_engine_stats(engine_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate comprehensive engine statistics"""
        return {
            'engine_id': int(engine_df['engine_id'].iloc[0]),
            'num_cycles': len(engine_df),
            'min_cycle': int(engine_df['cycle'].min()),
            'max_cycle': int(engine_df['cycle'].max()),
            'total_rul': float(engine_df['RUL'].iloc[0]) if 'RUL' in engine_df.columns else None,
            'final_rul': float(engine_df['RUL'].iloc[-1]) if 'RUL' in engine_df.columns else None,
            'sequential': EngineValidator.check_sequential_cycles(engine_df)[0],
            'monotonic': EngineValidator.check_monotonic_degradation(engine_df)[0]
        }


class DataLeakageDetector:
    """Detects various forms of data leakage"""

    @staticmethod
    def detect_engine_overlap(train_df: pd.DataFrame, test_df: pd.DataFrame) -> Tuple[set, int]:
        """
        Detect if same engines appear in train and test

        Returns:
            Tuple of (overlapping_engine_ids, count)
        """
        train_engines = set(train_df['engine_id'].unique())
        test_engines = set(test_df['engine_id'].unique())
        overlap = train_engines & test_engines
        return overlap, len(overlap)

    @staticmethod
    def detect_temporal_overlap(train_df: pd.DataFrame, test_df: pd.DataFrame) -> Tuple[bool, Dict]:
        """
        Check for temporal overlap in same engines

        Returns:
            Tuple of (has_overlap, details)
        """
        train_engines = set(train_df['engine_id'].unique())
        test_engines = set(test_df['engine_id'].unique())
        shared = train_engines & test_engines

        details = {
            'shared_engines': len(shared),
            'train_cycle_range': (int(train_df['cycle'].min()), int(train_df['cycle'].max())),
            'test_cycle_range': (int(test_df['cycle'].min()), int(test_df['cycle'].max()))
        }

        return len(shared) > 0, details

    @staticmethod
    def detect_feature_leakage(df: pd.DataFrame, target_col: str = 'RUL',
                               threshold: float = 0.3) -> List[Tuple[str, float]]:
        """
        Detect features with high correlation to target (potential leakage)

        Returns:
            List of (feature_name, correlation) tuples
        """
        if target_col not in df.columns:
            return []

        leaking_features = []
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            if col == target_col:
                continue

            corr = abs(df[col].corr(df[target_col]))
            if corr > threshold:
                leaking_features.append((col, float(corr)))

        return sorted(leaking_features, key=lambda x: x[1], reverse=True)


class HealthScoreCalculator:
    """Calculates overall data quality health score"""

    @staticmethod
    def calculate_score(total_checks: int, passed_checks: int,
                        critical_issues: int, warning_issues: int,
                        info_issues: int) -> float:
        """
        Calculate data health score (0-100)

        Formula:
            base_score = (passed_checks / total_checks) * 100
            penalties = critical * 10 + warning * 3 + info * 0.5
            score = max(0, min(100, base_score - penalties))
        """
        if total_checks == 0:
            return 100.0

        base_score = (passed_checks / total_checks) * 100
        penalty = (critical_issues * AuditThresholds.CRITICAL_PENALTY +
                   warning_issues * AuditThresholds.WARNING_PENALTY +
                   info_issues * AuditThresholds.INFO_PENALTY)

        score = max(0.0, min(100.0, base_score - penalty))
        return float(score)

    @staticmethod
    def get_health_status(score: float) -> str:
        """Get human-readable health status"""
        if score >= 90:
            return "Excellent"
        elif score >= 75:
            return "Good"
        elif score >= 60:
            return "Fair"
        elif score >= 45:
            return "Poor"
        else:
            return "Critical"

    @staticmethod
    def get_health_color(score: float) -> str:
        """Get color for visualization"""
        if score >= 90:
            return "#10b981"  # green
        elif score >= 75:
            return "#3b82f6"  # blue
        elif score >= 60:
            return "#f59e0b"  # amber
        elif score >= 45:
            return "#ef4444"  # red
        else:
            return "#7f1d1d"  # dark red


class ReportFormatter:
    """Formats audit reports for different outputs"""

    @staticmethod
    def format_text(report: Dict) -> str:
        """Format report as plain text"""
        lines = [
            "=" * 80,
            "DATA QUALITY AUDIT REPORT",
            "=" * 80,
            "",
            f"Audit ID: {report['audit_id']}",
            f"Timestamp: {report['timestamp']}",
            "",
            "SUMMARY",
            "-" * 40,
            f"Health Score: {report['data_health_score']:.1f}/100",
            f"Total Checks: {report['total_checks']}",
            f"Passed Checks: {report['passed_checks']}",
            f"Failed Checks: {report['failed_checks']}",
            "",
            "ISSUES",
            "-" * 40,
            f"Total Issues: {report['total_issues']}",
            f"  Critical: {report['critical_issues']}",
            f"  Warnings: {report['warning_issues']}",
            f"  Info: {report['info_issues']}",
            "",
        ]

        if report.get('recommendations'):
            lines.extend([
                "RECOMMENDATIONS",
                "-" * 40,
            ])
            for rec in report['recommendations']:
                lines.append(f"• {rec}")
            lines.append("")

        if report.get('issues'):
            lines.extend([
                "DETAILED ISSUES",
                "-" * 40,
            ])
            for issue in report['issues']:
                lines.append(f"\n[{issue['severity'].upper()}] {issue['check_name']}")
                lines.append(f"  Category: {issue['category']}")
                lines.append(f"  Description: {issue['description']}")
                if issue['affected_items']:
                    lines.append(f"  Affected: {', '.join(issue['affected_items'][:5])}")
                if issue['recommendation']:
                    lines.append(f"  Action: {issue['recommendation']}")

        return "\n".join(lines)

    @staticmethod
    def format_json(report: Dict) -> str:
        """Format report as JSON"""
        return json.dumps(report, indent=2, default=str)

    @staticmethod
    def format_html(report: Dict) -> str:
        """Format report as HTML (basic)"""
        health_color = HealthScoreCalculator.get_health_color(report['data_health_score'])
        health_status = HealthScoreCalculator.get_health_status(report['data_health_score'])

        html = f"""
        <html>
        <head>
            <title>Data Quality Audit Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; }}
                .health-score {{
                    font-size: 36px;
                    color: {health_color};
                    font-weight: bold;
                }}
                .summary {{ margin: 20px 0; }}
                .summary-item {{ margin: 10px 0; }}
                .issue {{
                    margin: 10px 0;
                    padding: 10px;
                    border-left: 4px solid {health_color};
                    background-color: #f9f9f9;
                }}
                .critical {{ border-left-color: #ef4444; }}
                .warning {{ border-left-color: #f59e0b; }}
                .info {{ border-left-color: #3b82f6; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Data Quality Audit Report</h1>
                <p>Audit ID: {report['audit_id']}</p>
                <p>Timestamp: {report['timestamp']}</p>
            </div>

            <h2>Health Score: <span class="health-score">{report['data_health_score']:.1f}/100</span> ({health_status})</h2>

            <div class="summary">
                <h3>Summary</h3>
                <div class="summary-item">Total Checks: {report['total_checks']}</div>
                <div class="summary-item">Passed Checks: {report['passed_checks']}</div>
                <div class="summary-item">Failed Checks: {report['failed_checks']}</div>
                <div class="summary-item">Total Issues: {report['total_issues']}</div>
                <div class="summary-item" style="color: #ef4444;">Critical Issues: {report['critical_issues']}</div>
                <div class="summary-item" style="color: #f59e0b;">Warning Issues: {report['warning_issues']}</div>
            </div>

            <h3>Issues</h3>
        """

        for issue in report.get('issues', []):
            severity_class = issue['severity'].lower()
            html += f"""
            <div class="issue {severity_class}">
                <strong>[{issue['severity'].upper()}]</strong> {issue['check_name']}<br/>
                {issue['description']}<br/>
                {f"<em>Action: {issue['recommendation']}</em>" if issue['recommendation'] else ""}
            </div>
            """

        html += """
        </body>
        </html>
        """
        return html


class AuditDataExporter:
    """Exports audit data to various formats"""

    @staticmethod
    def export_to_csv(report: Dict, filepath: str):
        """Export issues to CSV"""
        import csv

        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['category', 'check_name', 'severity', 'description', 'count'])
            writer.writeheader()

            for issue in report.get('issues', []):
                writer.writerow({
                    'category': issue['category'],
                    'check_name': issue['check_name'],
                    'severity': issue['severity'],
                    'description': issue['description'],
                    'count': issue['count']
                })

    @staticmethod
    def export_to_json(report: Dict, filepath: str):
        """Export report to JSON"""
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)

    @staticmethod
    def export_sensor_stats_to_csv(sensor_stats: Dict, filepath: str):
        """Export sensor statistics to CSV"""
        import csv

        if not sensor_stats:
            return

        with open(filepath, 'w', newline='') as f:
            fieldnames = list(sensor_stats.values())[0].keys() if sensor_stats else []
            writer = csv.DictWriter(f, fieldnames=['sensor'] + list(fieldnames))
            writer.writeheader()

            for sensor, stats in sensor_stats.items():
                row = {'sensor': sensor}
                row.update(stats)
                writer.writerow(row)


if __name__ == "__main__":
    print("Audit Utilities Module")
    print("Provides helper functions for data quality audit")
    print("\nClasses:")
    print("  - AuditThresholds: Configurable thresholds")
    print("  - SensorValidator: Sensor validation methods")
    print("  - EngineValidator: Engine-level validation")
    print("  - DataLeakageDetector: Leakage detection")
    print("  - HealthScoreCalculator: Score calculation")
    print("  - ReportFormatter: Report formatting")
    print("  - AuditDataExporter: Data export")
