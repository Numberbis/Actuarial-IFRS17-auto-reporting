"""Main script for generating IFRS 17 reports"""

import argparse
from datetime import datetime
from pathlib import Path
from .data_loader import DataLoader
from .calculations import IFRS17Calculator
from .report_generator import MarkdownReportGenerator


def main():
    """Main entry point for report generation"""

    parser = argparse.ArgumentParser(description='Generate IFRS 17 actuarial report')
    parser.add_argument(
        '--input',
        type=str,
        default='data/sample_contracts.csv',
        help='Path to input CSV file with contract data'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='reports/ifrs17_report.md',
        help='Path to output markdown report file'
    )
    parser.add_argument(
        '--reporting-date',
        type=str,
        default=datetime.now().strftime('%Y-%m-%d'),
        help='Reporting date in YYYY-MM-DD format'
    )
    parser.add_argument(
        '--company-name',
        type=str,
        default='Insurance Company',
        help='Company name for the report'
    )

    args = parser.parse_args()

    # Parse reporting date
    reporting_date = datetime.strptime(args.reporting_date, '%Y-%m-%d').date()

    print(f"IFRS 17 Report Generation")
    print(f"========================")
    print(f"Input file: {args.input}")
    print(f"Output file: {args.output}")
    print(f"Reporting date: {reporting_date}")
    print(f"Company: {args.company_name}")
    print()

    # Load contracts
    print("Loading contracts...")
    contracts = DataLoader.load_contracts(args.input)
    print(f"Loaded {len(contracts)} contracts")

    # Calculate IFRS 17 measurements
    print("Calculating IFRS 17 measurements...")
    calculator = IFRS17Calculator(reporting_date)
    results = []

    for contract in contracts:
        result = calculator.calculate(contract)
        results.append(result)
        print(f"  - {contract.contract_id}: Liability ${result.insurance_contract_liability:,.2f}")

    # Generate report
    print()
    print("Generating markdown report...")
    report_generator = MarkdownReportGenerator(reporting_date, args.company_name)

    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report_generator.generate(results, args.output)

    print(f"Report generated successfully: {args.output}")
    print()

    # Print summary
    total_liability = sum(r.insurance_contract_liability for r in results)
    total_revenue = sum(r.insurance_revenue for r in results)
    print("Summary:")
    print(f"  Total Liability: ${total_liability:,.2f}")
    print(f"  Total Revenue: ${total_revenue:,.2f}")


if __name__ == '__main__':
    main()
