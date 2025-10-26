# IFRS 17 Automated Actuarial Reporting

![Tests](https://github.com/YOUR_USERNAME/Actuarial-IFRS17-auto-reporting/workflows/Tests/badge.svg)
![Generate Report](https://github.com/YOUR_USERNAME/Actuarial-IFRS17-auto-reporting/workflows/Generate%20IFRS%2017%20Report/badge.svg)

Automated system for generating IFRS 17 actuarial reports with CI/CD pipeline integration.

## Overview

This project provides a complete solution for automating IFRS 17 insurance contract measurements and reporting. It includes:

- **IFRS 17 Calculation Engine**: Implementation of the Building Block Approach (BBA)
- **Automated Report Generation**: Creates detailed markdown reports
- **CI/CD Pipeline**: GitHub Actions workflows for automated execution
- **Comprehensive Testing**: Unit tests with high code coverage
- **Flexible Data Input**: CSV-based contract data loading

## Features

### IFRS 17 Calculations

- **Contractual Service Margin (CSM)** calculation and movements
- **Fulfilment Cash Flows (FCF)** with discounting
- **Risk Adjustment** for non-financial risk
- **Coverage Units** allocation (straight-line approach)
- **Insurance Revenue** and expense recognition
- **Insurance Contract Liability** measurement

### Reporting

- Professional markdown reports with:
  - Executive summary with key metrics
  - Portfolio-level aggregations
  - Contract-level detail tables
  - CSM movement analysis
  - P&L impact statements
  - Methodology documentation

### Automation

- **Automatic Report Generation**: Triggered on code push, PR, or schedule
- **Monthly Scheduled Runs**: Configurable via GitHub Actions cron
- **Manual Triggers**: On-demand report generation with custom parameters
- **Artifact Storage**: Reports saved as downloadable artifacts
- **Auto-Commit**: Reports automatically committed to repository

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Git
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/Actuarial-IFRS17-auto-reporting.git
cd Actuarial-IFRS17-auto-reporting
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

### Running Locally

Generate a report using the sample data:

```bash
python -m ifrs17.main
```

With custom parameters:

```bash
python -m ifrs17.main \
  --input data/sample_contracts.csv \
  --output reports/my_report.md \
  --reporting-date 2024-12-31 \
  --company-name "My Insurance Company"
```

### Running Tests

```bash
pytest
```

With coverage report:

```bash
pytest --cov=src/ifrs17 --cov-report=html
```

## Project Structure

```
Actuarial-IFRS17-auto-reporting/
├── .github/
│   └── workflows/
│       ├── generate-report.yml    # Report generation pipeline
│       └── tests.yml               # Test pipeline
├── data/
│   └── sample_contracts.csv        # Sample contract data
├── reports/
│   └── ifrs17_report.md           # Generated reports (auto-created)
├── src/
│   └── ifrs17/
│       ├── __init__.py
│       ├── models.py               # Data models
│       ├── calculations.py         # IFRS 17 calculation engine
│       ├── data_loader.py          # CSV data loading
│       ├── report_generator.py     # Markdown report generator
│       └── main.py                 # CLI entry point
├── tests/
│   ├── test_calculations.py        # Calculation tests
│   ├── test_data_loader.py         # Data loading tests
│   └── test_report_generator.py    # Report generation tests
├── .gitignore
├── pytest.ini
├── requirements.txt
├── setup.py
└── README.md
```

## Data Format

### Input CSV Format

The system expects a CSV file with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| contract_id | string | Unique contract identifier |
| inception_date | date | Contract start date (YYYY-MM-DD) |
| measurement_model | string | BBA, PAA, or GMM |
| initial_premium | float | Premium received at inception |
| coverage_period_years | int | Coverage period in years |
| discount_rate | float | Annual discount rate (decimal) |
| risk_adjustment | float | Risk adjustment amount |
| expected_claims | float | Expected total claims |
| acquisition_costs | float | Initial acquisition costs |

Example:

```csv
contract_id,inception_date,measurement_model,initial_premium,coverage_period_years,discount_rate,risk_adjustment,expected_claims,acquisition_costs
CON-2024-001,2024-01-01,BBA,100000,5,0.05,5000,80000,3000
```

## CI/CD Pipeline

### Automatic Report Generation

The GitHub Actions workflow automatically generates reports:

**Triggers:**
- Push to `main` branch
- Pull requests to `main`
- Monthly schedule (1st of each month)
- Manual workflow dispatch

**Workflow Steps:**
1. Checkout code
2. Set up Python environment
3. Install dependencies
4. Generate IFRS 17 report
5. Upload report as artifact
6. Commit report to repository (if not a PR)

### Manual Workflow Dispatch

You can manually trigger report generation from the GitHub Actions tab:

1. Go to **Actions** → **Generate IFRS 17 Report**
2. Click **Run workflow**
3. Optionally specify:
   - Custom reporting date
   - Custom company name
4. Click **Run workflow**

### Test Pipeline

Runs automatically on push and PR:
- Tests on Python 3.9, 3.10, 3.11, and 3.12
- Generates code coverage reports
- Uploads coverage to Codecov (if configured)

## IFRS 17 Methodology

### Building Block Approach (BBA)

The system implements the general measurement model (BBA) with:

1. **Fulfilment Cash Flows (FCF)**
   - Present value of future cash flows
   - Discounted using contract-specific rates
   - Includes premiums, claims, and expenses

2. **Risk Adjustment (RA)**
   - Compensation for bearing non-financial risk
   - Released over coverage period
   - Included in insurance revenue

3. **Contractual Service Margin (CSM)**
   - Unearned profit from insurance contracts
   - Released over coverage period based on coverage units
   - Earns interest accretion at discount rate
   - Updated for changes in estimates

### Insurance Contract Liability

```
Liability = FCF + RA + CSM
```

### Insurance Revenue

```
Revenue = CSM Release + RA Release
```

## Customization

### Adding New Contracts

1. Update `data/sample_contracts.csv` with new contract data
2. Push to GitHub or run locally
3. Report automatically generated

### Custom Calculations

Extend `src/ifrs17/calculations.py` to add:
- Different measurement models (PAA, GMM)
- Custom coverage unit patterns
- Additional movements and adjustments

### Report Customization

Modify `src/ifrs17/report_generator.py` to:
- Change report format and sections
- Add charts and visualizations
- Include additional metrics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Testing

The project includes comprehensive unit tests:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/ifrs17

# Run specific test file
pytest tests/test_calculations.py

# Run with verbose output
pytest -v
```

## License

This project is provided as-is for educational and commercial use.

## Acknowledgments

- Implements IFRS 17 standard as published by IASB
- Uses Building Block Approach (BBA) for general measurement

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Generated by:** IFRS 17 Automated Reporting System
**Last Updated:** 2024