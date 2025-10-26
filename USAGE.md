# Usage Guide

## Quick Start Examples

### 1. Generate Report with Default Settings

```bash
python -m ifrs17.main
```

This will:
- Use `data/sample_contracts.csv` as input
- Generate report at `reports/ifrs17_report.md`
- Use today's date as reporting date
- Use "Insurance Company" as company name

### 2. Custom Reporting Date

```bash
python -m ifrs17.main --reporting-date 2024-12-31
```

### 3. Custom Company Name

```bash
python -m ifrs17.main --company-name "ABC Insurance Ltd"
```

### 4. Custom Input File

```bash
python -m ifrs17.main --input data/my_contracts.csv
```

### 5. Full Customization

```bash
python -m ifrs17.main \
  --input data/Q4_2024_contracts.csv \
  --output reports/Q4_2024_report.md \
  --reporting-date 2024-12-31 \
  --company-name "ABC Insurance Ltd"
```

## GitHub Actions

### Manual Trigger

1. Navigate to **Actions** tab in your repository
2. Select **Generate IFRS 17 Report** workflow
3. Click **Run workflow** button
4. (Optional) Enter custom parameters:
   - **reporting_date**: YYYY-MM-DD format
   - **company_name**: Your company name
5. Click **Run workflow**

The report will be:
- Generated and committed to the `reports/` directory
- Available as a downloadable artifact

### Scheduled Reports

The system automatically generates reports:
- **Monthly**: On the 1st of each month at midnight UTC
- Edit `.github/workflows/generate-report.yml` to change schedule

### View Generated Reports

After workflow runs:
1. Go to **Actions** tab
2. Click on the completed workflow run
3. Scroll to **Artifacts** section
4. Download `ifrs17-report` artifact

Or view directly in repository:
- Navigate to `reports/ifrs17_report.md`

## Working with Contract Data

### Prepare Your Data

Create a CSV file with these columns:

```csv
contract_id,inception_date,measurement_model,initial_premium,coverage_period_years,discount_rate,risk_adjustment,expected_claims,acquisition_costs
CON-001,2024-01-01,BBA,100000,5,0.05,5000,80000,3000
CON-002,2024-02-15,BBA,250000,10,0.045,12000,200000,7500
```

### Column Descriptions

- **contract_id**: Unique identifier for each contract
- **inception_date**: When coverage begins (YYYY-MM-DD)
- **measurement_model**: Always "BBA" (Building Block Approach)
- **initial_premium**: Premium amount in dollars
- **coverage_period_years**: Length of coverage in years
- **discount_rate**: Annual discount rate as decimal (5% = 0.05)
- **risk_adjustment**: Dollar amount for risk compensation
- **expected_claims**: Total expected claims over contract life
- **acquisition_costs**: Initial costs to acquire the contract

### Load and Process

```bash
python -m ifrs17.main --input data/my_contracts.csv
```

## Development Workflow

### Install in Development Mode

```bash
pip install -e .
```

### Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src/ifrs17 --cov-report=html

# Specific test
pytest tests/test_calculations.py -v

# Single test function
pytest tests/test_calculations.py::test_csm_calculation -v
```

### Modify Calculations

Edit `src/ifrs17/calculations.py` to customize:

```python
# Example: Add custom coverage unit pattern
def calculate_coverage_units(self, contract):
    # Your custom logic here
    pass
```

### Customize Reports

Edit `src/ifrs17/report_generator.py`:

```python
# Example: Add new section to report
def _build_report(self, results, ...):
    md.append("## My Custom Section\n")
    md.append("Custom content here\n")
```

## Troubleshooting

### Missing Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### Import Errors

Make sure you're in the project root directory:
```bash
cd Actuarial-IFRS17-auto-reporting
python -m ifrs17.main
```

### Data Format Errors

Verify your CSV has:
- Correct column names (case-sensitive)
- Date format: YYYY-MM-DD
- Numeric values without currency symbols
- No missing values

### Test Failures

Update test data paths if needed:
```bash
# From project root
pytest tests/ -v
```

## Integration Examples

### Python Script Integration

```python
from datetime import date
from ifrs17.data_loader import DataLoader
from ifrs17.calculations import IFRS17Calculator
from ifrs17.report_generator import MarkdownReportGenerator

# Load contracts
contracts = DataLoader.load_contracts('data/contracts.csv')

# Calculate
calculator = IFRS17Calculator(reporting_date=date(2024, 12, 31))
results = [calculator.calculate(c) for c in contracts]

# Generate report
generator = MarkdownReportGenerator(
    reporting_date=date(2024, 12, 31),
    company_name="My Company"
)
generator.generate(results, 'output/report.md')
```

### Automated Pipeline

Add to your existing CI/CD:

```yaml
- name: Generate IFRS 17 Report
  run: |
    pip install -r requirements.txt
    pip install -e .
    python -m ifrs17.main --reporting-date $(date +%Y-%m-%d)
```

## Best Practices

1. **Version Control**: Always commit contract data changes with clear messages
2. **Testing**: Run tests before pushing changes
3. **Date Consistency**: Use consistent reporting dates across analysis
4. **Backup**: Keep historical reports for audit trail
5. **Documentation**: Document any custom calculations or assumptions

## Support

For questions or issues:
1. Check this usage guide
2. Review the main README.md
3. Check existing GitHub issues
4. Open a new issue with details
