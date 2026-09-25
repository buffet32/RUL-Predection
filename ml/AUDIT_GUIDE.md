# Data Quality Audit System - User Guide

## Overview

The Data Quality Audit System is a comprehensive tool for validating sensor data quality in the NASA C-MAPSS FD001 dataset. It performs 33+ automated checks across three categories and generates detailed reports.

## Quick Start

### 1. Run Audit from CLI

```bash
cd ml/
python audit_runner.py \
  --data-dir ../../Downloads/archive \
  --output results/audit_report \
  --format all \
  --export-stats
```

### 2. Run Audit from Python

```python
from src.data_quality_audit import DataQualityAudit
from src.preprocessing import preprocess_training_data, preprocess_test_data

# Load data
train_df = preprocess_training_data("../../Downloads/archive")
test_df, rul_df = preprocess_test_data("../../Downloads/archive")

# Run audit
audit = DataQualityAudit(verbose=True)
report = audit.audit(train_df, test_df)

# View results
print(f"Health Score: {report.data_health_score:.1f}/100")
print(f"Total Issues: {report.total_issues}")
print(report.to_json())
```

## Features

### 1. Anomaly Detection (7 checks)
- **Missing Values**: Identifies null/NaN values
- **Duplicates**: Finds exact row duplicates
- **Constant Sensors**: Verifies known constant sensors remain constant
- **Zero Variance**: Detects unexpected constant sensors
- **Outliers**: Uses IQR method to find statistical anomalies
- **Rate of Change**: Detects sudden sensor jumps
- **Sensor Ranges**: Validates values within expected bounds

### 2. Data Leakage Detection (3 checks)
- **Engine Overlap**: Detects same engines in train/test
- **Temporal Leakage**: Checks for cycle range overlaps
- **Feature Leakage**: Identifies features with high target correlation

### 3. Consistency Validation (4 checks)
- **Sequential Cycles**: Verifies no missing cycles per engine
- **Settings Ranges**: Validates operational settings
- **RUL Calculation**: Verifies RUL = max_cycle - current_cycle
- **Degradation Consistency**: Ensures monotonic RUL decrease

## Health Score

The health score (0-100) is calculated as:

```
base_score = (passed_checks / total_checks) × 100
penalties = (critical × 10) + (warnings × 3) + (info × 0.5)
health_score = max(0, min(100, base_score - penalties))
```

### Score Interpretation
- **90-100**: Excellent - Data is production-ready
- **75-89**: Good - Minor issues, generally usable
- **60-74**: Fair - Several issues should be addressed
- **45-59**: Poor - Significant quality problems
- **0-44**: Critical - Major issues must be resolved

## CLI Usage

### Basic Audit
```bash
python audit_runner.py --data-dir path/to/data
```

### Save Multiple Formats
```bash
python audit_runner.py \
  --data-dir path/to/data \
  --format all
# Outputs: audit_report.txt, .json, .html
```

### Export Statistics
```bash
python audit_runner.py \
  --data-dir path/to/data \
  --export-stats
# Outputs: audit_report_sensor_stats.csv, _issues.csv
```

### Quiet Mode
```bash
python audit_runner.py --quiet --data-dir path/to/data
```

## Python API

### DataQualityAudit Class

```python
from src.data_quality_audit import DataQualityAudit

# Create audit instance
audit = DataQualityAudit(verbose=True)

# Run audit
report = audit.audit(train_df, test_df)

# Access results
print(report.data_health_score)
print(report.total_issues)
print(report.critical_issues)
print(report.issues)
print(report.recommendations)
```

### DataQualityReport Object

```python
report = audit.audit(train_df, test_df)

# Attributes
report.audit_id              # Unique audit ID
report.timestamp             # When audit ran
report.data_health_score     # Overall score (0-100)
report.total_checks          # Number of checks performed
report.passed_checks         # Checks that passed
report.failed_checks         # Checks that failed
report.total_issues          # Number of issues found
report.critical_issues       # Critical severity issues
report.warning_issues        # Warning severity issues
report.info_issues           # Info severity issues
report.issues                # List of issue details
report.sensor_stats          # Per-sensor statistics
report.engine_stats          # Per-engine statistics
report.recommendations       # List of recommendations

# Methods
report.to_dict()             # Convert to dictionary
report.to_json()             # Convert to JSON string
```

### Utility Classes

#### SensorValidator
```python
from src.audit_utils import SensorValidator

# Get constant sensors
constant = SensorValidator.get_constant_sensors()
# ['sensor_1', 'sensor_5', 'sensor_10', ...]

# Get useful sensors
useful = SensorValidator.get_useful_sensors()
# ['sensor_2', 'sensor_3', 'sensor_4', ...]

# Detect outliers (IQR method)
outliers, pct = SensorValidator.detect_outliers_iqr(series)

# Validate sensor range
below, above = SensorValidator.validate_range(series, min_val, max_val)

# Get sensor statistics
stats = SensorValidator.calculate_sensor_stats(df, 'sensor_2')
```

#### DataLeakageDetector
```python
from src.audit_utils import DataLeakageDetector

# Check for engine overlap
overlap, count = DataLeakageDetector.detect_engine_overlap(train_df, test_df)
if count > 0:
    print(f"ERROR: {count} engines appear in both train and test!")

# Detect feature leakage
leaking_features = DataLeakageDetector.detect_feature_leakage(
    df, target_col='RUL', threshold=0.3
)
```

#### HealthScoreCalculator
```python
from src.audit_utils import HealthScoreCalculator

# Calculate health score
score = HealthScoreCalculator.calculate_score(
    total_checks=10,
    passed_checks=9,
    critical_issues=0,
    warning_issues=1,
    info_issues=0
)

# Get status
status = HealthScoreCalculator.get_health_status(score)  # "Good"

# Get color for visualization
color = HealthScoreCalculator.get_health_color(score)  # "#3b82f6"
```

#### ReportFormatter
```python
from src.audit_utils import ReportFormatter

report_dict = report.to_dict()

# Format as text
text = ReportFormatter.format_text(report_dict)
with open('report.txt', 'w') as f:
    f.write(text)

# Format as JSON
json_str = ReportFormatter.format_json(report_dict)

# Format as HTML
html = ReportFormatter.format_html(report_dict)
with open('report.html', 'w') as f:
    f.write(html)
```

## Integration with ML Pipeline

### Before Training

```python
from src.data_quality_audit import DataQualityAudit
from src.preprocessing import preprocess_training_data, preprocess_test_data

# Preprocess
train_df = preprocess_training_data()
test_df, rul_df = preprocess_test_data()

# Audit
audit = DataQualityAudit()
report = audit.audit(train_df, test_df)

# Check health before training
if report.data_health_score < 60:
    print("WARNING: Data quality is poor. Review issues before training.")
    for issue in report.issues:
        if issue['severity'] == 'critical':
            print(f"  CRITICAL: {issue['description']}")

elif report.critical_issues > 0:
    print("WARNING: Critical issues detected. Review recommendations.")
    for rec in report.recommendations:
        print(f"  {rec}")

else:
    print("✓ Data quality is good. Proceeding with training...")
    # Continue with model training
```

### Generate School Report

```python
from src.audit_utils import ReportFormatter, AuditDataExporter
from pathlib import Path

report = audit.audit(train_df, test_df)
report_dict = report.to_dict()

# Create reports directory
reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)

# Generate all formats
text = ReportFormatter.format_text(report_dict)
with open(reports_dir / "data_quality_report.txt", 'w') as f:
    f.write(text)

html = ReportFormatter.format_html(report_dict)
with open(reports_dir / "data_quality_report.html", 'w') as f:
    f.write(html)

# Export statistics
AuditDataExporter.export_sensor_stats_to_csv(
    report.sensor_stats,
    str(reports_dir / "sensor_statistics.csv")
)

AuditDataExporter.export_to_csv(
    report_dict,
    str(reports_dir / "issues.csv")
)

print(f"✓ Reports saved to {reports_dir}/")
```

## Issue Categories and Severity

### Issue Severity Levels

1. **CRITICAL** (🔴)
   - Model-breaking issues
   - MUST be fixed before training
   - Examples: Engine overlap, missing values, calculation errors
   - Penalty: -10 points per issue

2. **WARNING** (🟡)
   - Performance degradation risk
   - SHOULD be investigated
   - Examples: Outliers, range violations, non-sequential cycles
   - Penalty: -3 points per issue

3. **INFO** (ℹ️)
   - Informational only
   - May not need immediate action
   - Examples: Rate of change spikes, degradation patterns
   - Penalty: -0.5 points per issue

### Issue Categories

- **Anomaly**: Statistical irregularities in sensor data
- **Leakage**: Risk of information leakage between train/test
- **Consistency**: Violations of expected data patterns

## Examples

### Example 1: Quick Health Check

```python
from src.data_quality_audit import run_audit_on_files

report = run_audit_on_files(data_dir="../../Downloads/archive")
print(f"Health Score: {report.data_health_score:.1f}")
print(f"Status: {'✓ PASS' if report.critical_issues == 0 else '✗ FAIL'}")
```

### Example 2: Detailed Issue Investigation

```python
audit = DataQualityAudit()
report = audit.audit(train_df, test_df)

# Filter by severity
critical_issues = [i for i in report.issues if i['severity'] == 'critical']
print(f"Critical Issues: {len(critical_issues)}")

for issue in critical_issues:
    print(f"\n{issue['check_name']}")
    print(f"  Description: {issue['description']}")
    print(f"  Affected: {issue['affected_items']}")
    print(f"  Action: {issue['recommendation']}")
```

### Example 3: Sensor Quality Analysis

```python
report = audit.audit(train_df, test_df)

# Analyze sensor statistics
print("Sensor Quality Analysis")
print("-" * 60)
print(f"{'Sensor':<12} {'Mean':>10} {'Std':>10} {'Min':>10} {'Max':>10}")
print("-" * 60)

for sensor, stats in report.sensor_stats.items():
    print(f"{sensor:<12} {stats['mean']:>10.2f} {stats['std']:>10.2f} "
          f"{stats['min']:>10.2f} {stats['max']:>10.2f}")
```

### Example 4: Engine-Level Health

```python
report = audit.audit(train_df, test_df)

# Analyze engine statistics
print("Engine Statistics")
print("-" * 80)
print(f"{'Engine':<8} {'Cycles':<8} {'Sequential':<12} {'Monotonic':<12} {'RUL':<8}")
print("-" * 80)

for engine_id, stats in sorted(report.engine_stats.items()):
    seq = "✓" if stats['sequential'] else "✗"
    mono = "✓" if stats['monotonic'] else "✗"
    print(f"{engine_id:<8} {stats['num_cycles']:<8} {seq:<12} {mono:<12} "
          f"{stats['final_rul']:<8}")
```

## Troubleshooting

### Issue: "Data not found"
```
Solution: Verify data directory path:
python audit_runner.py --data-dir /full/path/to/data
```

### Issue: "Out of memory"
```
Solution: Reduce dataset or use a subset for initial testing
```

### Issue: "Import error"
```
Solution: Ensure you're running from correct directory:
cd ml/
python audit_runner.py --data-dir path/to/data
```

## Output Files

When running audit, the following files are generated:

- **audit_report.txt** - Human-readable text report
- **audit_report.json** - Machine-readable JSON report
- **audit_report.html** - Interactive HTML visualization
- **audit_report_sensor_stats.csv** - Sensor statistics
- **audit_report_issues.csv** - Detailed issues

## Next Steps

After Phase 1 (Core Audit Engine), the system will include:

- **Phase 2**: Backend API integration with persistence
- **Phase 3**: React dashboard with real-time monitoring
- **Phase 4**: Advanced features (PDF export, automated alerts, trends)

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review test cases in `tests/test_audit.py`
3. Run with `--verbose` for detailed output
4. Check log files for error details

---

**Version**: 1.0  
**Last Updated**: 2026-09-11  
**Status**: Phase 1 Complete (Core Audit Engine)
