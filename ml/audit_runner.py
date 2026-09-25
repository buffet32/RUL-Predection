"""
Data Quality Audit Runner
CLI tool to execute audits on the NASA C-MAPSS dataset
"""

import argparse
import sys
from pathlib import Path
import json
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from data_quality_audit import DataQualityAudit, run_audit_on_files
from audit_utils import ReportFormatter, AuditDataExporter, HealthScoreCalculator
from preprocessing import preprocess_training_data, preprocess_test_data


def main():
    parser = argparse.ArgumentParser(
        description="Data Quality Audit Tool for NASA C-MAPSS FD001 Dataset"
    )

    parser.add_argument(
        '--data-dir',
        type=str,
        default=None,
        help='Path to data directory containing train/test/RUL files'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='audit_report',
        help='Output file prefix for reports (default: audit_report)'
    )

    parser.add_argument(
        '--format',
        type=str,
        choices=['text', 'json', 'html', 'all'],
        default='text',
        help='Report format (default: text)'
    )

    parser.add_argument(
        '--export-stats',
        action='store_true',
        help='Export sensor and engine statistics to CSV'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        default=True,
        help='Verbose output during audit'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )

    args = parser.parse_args()

    if args.quiet:
        args.verbose = False

    # Run audit
    print("=" * 80)
    print("DATA QUALITY AUDIT TOOL")
    print("=" * 80)
    print(f"Start Time: {datetime.now().isoformat()}")
    print()

    try:
        # Load and preprocess data
        print("Loading and preprocessing data...")
        train_df = preprocess_training_data(args.data_dir or "../../Downloads/archive")
        test_df, rul_df = preprocess_test_data(args.data_dir or "../../Downloads/archive")

        print(f"Training data shape: {train_df.shape}")
        print(f"Test data shape: {test_df.shape}")
        print()

        # Run audit
        print("Running audit...")
        audit = DataQualityAudit(verbose=args.verbose)
        report = audit.audit(train_df, test_df)

        report_dict = report.to_dict()

        # Display summary
        print()
        print("=" * 80)
        print("AUDIT RESULTS")
        print("=" * 80)
        print(f"Health Score: {report.data_health_score:.1f}/100 ({HealthScoreCalculator.get_health_status(report.data_health_score)})")
        print(f"Total Issues: {report.total_issues}")
        print(f"  - Critical: {report.critical_issues}")
        print(f"  - Warnings: {report.warning_issues}")
        print(f"  - Info: {report.info_issues}")
        print(f"Checks Passed: {report.passed_checks}/{report.total_checks}")
        print()

        if report.recommendations:
            print("Recommendations:")
            for rec in report.recommendations:
                print(f"  • {rec}")
            print()

        # Save reports
        print("Saving reports...")
        output_dir = Path(args.output).parent
        output_prefix = Path(args.output).name

        if output_dir != Path('.'):
            output_dir.mkdir(parents=True, exist_ok=True)

        formats = ['text', 'json', 'html'] if args.format == 'all' else [args.format]

        for fmt in formats:
            if fmt == 'text':
                output_file = output_dir / f"{output_prefix}.txt"
                text_report = ReportFormatter.format_text(report_dict)
                with open(output_file, 'w') as f:
                    f.write(text_report)
                print(f"  ✓ Text report: {output_file}")

            elif fmt == 'json':
                output_file = output_dir / f"{output_prefix}.json"
                json_report = ReportFormatter.format_json(report_dict)
                with open(output_file, 'w') as f:
                    f.write(json_report)
                print(f"  ✓ JSON report: {output_file}")

            elif fmt == 'html':
                output_file = output_dir / f"{output_prefix}.html"
                html_report = ReportFormatter.format_html(report_dict)
                with open(output_file, 'w') as f:
                    f.write(html_report)
                print(f"  ✓ HTML report: {output_file}")

        # Export statistics if requested
        if args.export_stats:
            print()
            print("Exporting statistics...")

            sensor_csv = output_dir / f"{output_prefix}_sensor_stats.csv"
            if report.sensor_stats:
                AuditDataExporter.export_sensor_stats_to_csv(report.sensor_stats, str(sensor_csv))
                print(f"  ✓ Sensor statistics: {sensor_csv}")

            issues_csv = output_dir / f"{output_prefix}_issues.csv"
            AuditDataExporter.export_to_csv(report_dict, str(issues_csv))
            print(f"  ✓ Issues: {issues_csv}")

        print()
        print("=" * 80)
        print(f"Audit completed at {datetime.now().isoformat()}")
        print("=" * 80)

        return 0

    except Exception as e:
        print(f"\n❌ Error during audit: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
