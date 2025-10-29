"""Tests for markdown report generation"""

import pytest
import tempfile
from pathlib import Path
from datetime import date
from src.ifrs17.models import IFRS17Result, CSMMovement, CoverageUnit
from src.ifrs17.report_generator import MarkdownReportGenerator


@pytest.fixture
def sample_result():
    """Create sample IFRS 17 result for testing"""
    csm = CSMMovement(
        opening_balance=10000,
        interest_accretion=500,
        changes_in_estimates=0,
        release_for_service=1000,
        closing_balance=9500
    )

    coverage_units = [
        CoverageUnit(period="2024-01", units=1.0),
        CoverageUnit(period="2024-02", units=1.0),
    ]

    return IFRS17Result(
        contract_id="TEST-001",
        reporting_date=date(2024, 10, 26),
        measurement_model="BBA",
        csm=csm,
        fulfilment_cash_flows=-5000,
        risk_adjustment=3000,
        insurance_contract_liability=7500,
        coverage_units=coverage_units,
        insurance_revenue=1500,
        insurance_service_expense=1000
    )


def test_report_generation(sample_result):
    """Test basic report generation"""
    generator = MarkdownReportGenerator(
        reporting_date=date(2024, 10, 26),
        company_name="Test Insurance Co"
    )

    # Create temporary file for output
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        output_path = f.name

    try:
        # Generate report
        generator.generate([sample_result], output_path)

        # Check file was created
        assert Path(output_path).exists()

        # Read and verify content
        with open(output_path, 'r') as f:
            content = f.read()

        # Check for key sections
        assert "IFRS 17 Actuarial Report" in content
        assert "Test Insurance Co" in content
        assert "Executive Summary" in content
        assert "Contract-Level Details" in content
        assert "TEST-001" in content
        assert "Methodology" in content

        # Check for numeric values
        assert "7,500.00" in content  # Liability
        assert "1,500.00" in content  # Revenue

    finally:
        # Clean up
        Path(output_path).unlink()


def test_report_totals(sample_result):
    """Test that report correctly calculates totals"""
    # Create multiple results
    results = [sample_result, sample_result]

    generator = MarkdownReportGenerator(
        reporting_date=date(2024, 10, 26),
        company_name="Test Insurance Co"
    )

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        output_path = f.name

    try:
        generator.generate(results, output_path)

        with open(output_path, 'r') as f:
            content = f.read()

        # Total liability should be 2x individual
        assert "15,000.00" in content  # 7500 * 2

    finally:
        Path(output_path).unlink()
