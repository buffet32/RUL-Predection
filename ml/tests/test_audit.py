"""
Unit tests for Data Quality Audit System
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_quality_audit import DataQualityAudit, IssueSeverity, IssueCategory
from audit_utils import (
    SensorValidator, EngineValidator, DataLeakageDetector,
    HealthScoreCalculator, ReportFormatter
)


class TestSensorValidator:
    """Test sensor validation utilities"""

    def test_get_constant_sensors(self):
        constant = SensorValidator.get_constant_sensors()
        assert len(constant) == 6
        assert 'sensor_1' in constant

    def test_get_useful_sensors(self):
        useful = SensorValidator.get_useful_sensors()
        assert len(useful) == 15
        assert 'sensor_1' not in useful
        assert 'sensor_2' in useful

    def test_detect_outliers_iqr(self):
        data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 100])  # 100 is outlier
        outliers, pct = SensorValidator.detect_outliers_iqr(data)
        assert outliers[-1] == True  # Last value is outlier
        assert pct > 0

    def test_validate_range(self):
        data = pd.Series([10, 20, 30, 40, 50])
        below, above = SensorValidator.validate_range(data, 15, 45)
        assert below == 1  # 10 is below
        assert above == 1  # 50 is above

    def test_calculate_sensor_stats(self):
        df = pd.DataFrame({'sensor_2': [1, 2, 3, 4, 5]})
        stats = SensorValidator.calculate_sensor_stats(df, 'sensor_2')
        assert stats['mean'] == 3.0
        assert stats['count'] == 5


class TestEngineValidator:
    """Test engine validation utilities"""

    def test_check_sequential_cycles_valid(self):
        df = pd.DataFrame({
            'engine_id': [1, 1, 1, 1],
            'cycle': [1, 2, 3, 4]
        })
        is_seq, missing = EngineValidator.check_sequential_cycles(df)
        assert is_seq == True
        assert len(missing) == 0

    def test_check_sequential_cycles_missing(self):
        df = pd.DataFrame({
            'engine_id': [1, 1, 1],
            'cycle': [1, 2, 4]  # 3 is missing
        })
        is_seq, missing = EngineValidator.check_sequential_cycles(df)
        assert is_seq == False
        assert 3 in missing

    def test_check_monotonic_degradation_valid(self):
        df = pd.DataFrame({
            'engine_id': [1, 1, 1],
            'cycle': [1, 2, 3],
            'RUL': [100, 50, 0]  # Decreasing
        })
        is_mono, violations = EngineValidator.check_monotonic_degradation(df)
        assert is_mono == True
        assert violations == 0


class TestDataLeakageDetector:
    """Test leakage detection"""

    def test_detect_engine_overlap(self):
        train = pd.DataFrame({'engine_id': [1, 2, 3, 4, 5]})
        test = pd.DataFrame({'engine_id': [4, 5, 6, 7]})
        overlap, count = DataLeakageDetector.detect_engine_overlap(train, test)
        assert count == 2
        assert 4 in overlap
        assert 5 in overlap

    def test_no_engine_overlap(self):
        train = pd.DataFrame({'engine_id': [1, 2, 3]})
        test = pd.DataFrame({'engine_id': [4, 5, 6]})
        overlap, count = DataLeakageDetector.detect_engine_overlap(train, test)
        assert count == 0


class TestHealthScoreCalculator:
    """Test health score calculation"""

    def test_perfect_score(self):
        score = HealthScoreCalculator.calculate_score(10, 10, 0, 0, 0)
        assert score == 100.0

    def test_score_with_issues(self):
        score = HealthScoreCalculator.calculate_score(10, 8, 1, 1, 0)
        # base = 80%, penalty = 13, result = 67
        assert 60 < score < 70

    def test_health_status(self):
        assert HealthScoreCalculator.get_health_status(95) == "Excellent"
        assert HealthScoreCalculator.get_health_status(80) == "Good"
        assert HealthScoreCalculator.get_health_status(50) == "Poor"

    def test_health_color(self):
        color = HealthScoreCalculator.get_health_color(95)
        assert color == "#10b981"  # green


class TestDataQualityAudit:
    """Test main audit engine"""

    @pytest.fixture
    def sample_train_data(self):
        """Create sample training data"""
        np.random.seed(42)
        n_engines = 5
        cycles_per_engine = 100

        data = []
        for engine_id in range(1, n_engines + 1):
            for cycle in range(1, cycles_per_engine + 1):
                data.append({
                    'engine_id': engine_id,
                    'cycle': cycle,
                    'setting_1': 0.0,
                    'setting_2': 0.0,
                    'setting_3': 100.0,
                    'sensor_2': 642.0 + np.random.normal(0, 0.5),
                    'sensor_3': 1590.0 + np.random.normal(0, 5),
                    'sensor_4': 1408.0 + np.random.normal(0, 5),
                    'RUL': cycles_per_engine - cycle
                })

        df = pd.DataFrame(data)
        # Add required columns
        df['max_cycle'] = cycles_per_engine
        return df

    @pytest.fixture
    def sample_test_data(self):
        """Create sample test data"""
        np.random.seed(42)
        n_engines = 5
        cycles_per_engine = 80

        data = []
        for engine_id in range(n_engines + 1, n_engines + 6):  # Different engines
            for cycle in range(1, cycles_per_engine + 1):
                data.append({
                    'engine_id': engine_id,
                    'cycle': cycle,
                    'setting_1': 0.0,
                    'setting_2': 0.0,
                    'setting_3': 100.0,
                    'sensor_2': 642.0 + np.random.normal(0, 0.5),
                    'sensor_3': 1590.0 + np.random.normal(0, 5),
                    'sensor_4': 1408.0 + np.random.normal(0, 5),
                })

        df = pd.DataFrame(data)
        df['max_cycle'] = cycles_per_engine
        return df

    def test_audit_creation(self):
        audit = DataQualityAudit(verbose=False)
        assert audit is not None
        assert audit.verbose == False

    def test_check_missing_values_clean(self, sample_train_data):
        audit = DataQualityAudit(verbose=False)
        result = audit.check_missing_values(sample_train_data)
        assert result == True
        assert audit.checks_passed == 1

    def test_check_missing_values_dirty(self):
        df = pd.DataFrame({
            'engine_id': [1, 1, None, 1],
            'cycle': [1, 2, 3, 4]
        })
        audit = DataQualityAudit(verbose=False)
        result = audit.check_missing_values(df)
        assert result == False
        assert len(audit.issues) > 0

    def test_check_duplicates_clean(self, sample_train_data):
        audit = DataQualityAudit(verbose=False)
        result = audit.check_duplicates(sample_train_data)
        assert result == True

    def test_check_duplicates_dirty(self):
        df = pd.DataFrame({
            'engine_id': [1, 1, 1, 1],
            'cycle': [1, 2, 2, 3]  # Duplicate row
        })
        audit = DataQualityAudit(verbose=False)
        result = audit.check_duplicates(df)
        assert result == False

    def test_full_audit(self, sample_train_data, sample_test_data):
        audit = DataQualityAudit(verbose=False)
        report = audit.audit(sample_train_data, sample_test_data)

        assert report.audit_id is not None
        assert report.data_health_score >= 0
        assert report.data_health_score <= 100
        assert report.total_checks > 0
        assert report.total_issues >= 0

    def test_audit_report_structure(self, sample_train_data, sample_test_data):
        audit = DataQualityAudit(verbose=False)
        report = audit.audit(sample_train_data, sample_test_data)

        # Check report has all required fields
        assert hasattr(report, 'audit_id')
        assert hasattr(report, 'timestamp')
        assert hasattr(report, 'data_health_score')
        assert hasattr(report, 'total_checks')
        assert hasattr(report, 'issues')

    def test_report_conversion_to_dict(self, sample_train_data, sample_test_data):
        audit = DataQualityAudit(verbose=False)
        report = audit.audit(sample_train_data, sample_test_data)

        report_dict = report.to_dict()
        assert isinstance(report_dict, dict)
        assert 'audit_id' in report_dict
        assert 'issues' in report_dict

    def test_report_conversion_to_json(self, sample_train_data, sample_test_data):
        audit = DataQualityAudit(verbose=False)
        report = audit.audit(sample_train_data, sample_test_data)

        json_str = report.to_json()
        assert isinstance(json_str, str)
        assert 'audit_id' in json_str


class TestReportFormatter:
    """Test report formatting"""

    @pytest.fixture
    def sample_report(self):
        return {
            'audit_id': 'test-123',
            'timestamp': '2026-09-11T14:30:00',
            'data_health_score': 85.5,
            'total_checks': 10,
            'passed_checks': 9,
            'failed_checks': 1,
            'total_issues': 1,
            'critical_issues': 0,
            'warning_issues': 1,
            'info_issues': 0,
            'issues': [
                {
                    'category': 'anomaly',
                    'check_name': 'test_check',
                    'severity': 'warning',
                    'description': 'Test issue',
                    'affected_items': ['item1'],
                    'count': 5,
                    'recommendation': 'Fix this'
                }
            ],
            'recommendations': ['Recommendation 1']
        }

    def test_format_text(self, sample_report):
        text = ReportFormatter.format_text(sample_report)
        assert isinstance(text, str)
        assert 'DATA QUALITY AUDIT REPORT' in text
        assert '85.5' in text

    def test_format_json(self, sample_report):
        json_str = ReportFormatter.format_json(sample_report)
        assert isinstance(json_str, str)
        assert 'audit_id' in json_str

    def test_format_html(self, sample_report):
        html = ReportFormatter.format_html(sample_report)
        assert isinstance(html, str)
        assert '<html>' in html
        assert 'Data Quality Audit Report' in html


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
