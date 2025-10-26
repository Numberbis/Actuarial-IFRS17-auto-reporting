"""Tests for IFRS 17 calculations"""

import pytest
from datetime import date
from src.ifrs17.models import InsuranceContract
from src.ifrs17.calculations import IFRS17Calculator


@pytest.fixture
def sample_contract():
    """Create a sample insurance contract for testing"""
    return InsuranceContract(
        contract_id="TEST-001",
        inception_date=date(2024, 1, 1),
        measurement_model="BBA",
        initial_premium=100000,
        coverage_period_years=5,
        discount_rate=0.05,
        risk_adjustment=5000,
        expected_claims=80000,
        acquisition_costs=3000
    )


@pytest.fixture
def calculator():
    """Create IFRS17 calculator"""
    return IFRS17Calculator(reporting_date=date(2024, 10, 26))


def test_coverage_units_calculation(calculator, sample_contract):
    """Test coverage units are calculated correctly"""
    coverage_units = calculator.calculate_coverage_units(sample_contract)

    # Should have coverage units for each month
    expected_months = sample_contract.coverage_period_years * 12
    assert len(coverage_units) == expected_months

    # Each unit should have a period and units value
    for unit in coverage_units:
        assert unit.period is not None
        assert unit.units > 0


def test_fulfilment_cash_flows(calculator, sample_contract):
    """Test FCF calculation"""
    fcf = calculator.calculate_fulfilment_cash_flows(sample_contract)

    # FCF should be a float
    assert isinstance(fcf, float)

    # FCF represents present value of liability
    # Should be positive when claims + costs exceed premiums
    assert fcf > 0


def test_csm_calculation(calculator, sample_contract):
    """Test CSM movement calculation"""
    coverage_units = calculator.calculate_coverage_units(sample_contract)
    csm = calculator.calculate_csm(sample_contract, coverage_units)

    # CSM components should be present
    assert csm.opening_balance >= 0
    assert csm.interest_accretion >= 0
    assert csm.release_for_service >= 0
    assert csm.closing_balance >= 0

    # Closing balance should equal opening + accretion + changes - release
    expected_closing = (
        csm.opening_balance +
        csm.interest_accretion +
        csm.changes_in_estimates -
        csm.release_for_service
    )
    assert abs(csm.closing_balance - expected_closing) < 0.01


def test_full_calculation(calculator, sample_contract):
    """Test complete IFRS 17 calculation"""
    result = calculator.calculate(sample_contract)

    # Check all required fields are present
    assert result.contract_id == sample_contract.contract_id
    assert result.reporting_date == calculator.reporting_date
    assert result.measurement_model == sample_contract.measurement_model

    # Check numeric results
    assert isinstance(result.insurance_contract_liability, float)
    assert isinstance(result.insurance_revenue, float)
    assert isinstance(result.insurance_service_expense, float)

    # Liability should be positive
    assert result.insurance_contract_liability >= 0


def test_insurance_revenue_calculation(calculator, sample_contract):
    """Test insurance revenue calculation"""
    coverage_units = calculator.calculate_coverage_units(sample_contract)
    csm = calculator.calculate_csm(sample_contract, coverage_units)

    revenue = calculator.calculate_insurance_revenue(csm, 500)

    # Revenue should be positive
    assert revenue > 0

    # Revenue should include CSM release
    assert revenue >= csm.release_for_service


def test_onerous_contract():
    """Test handling of onerous contracts (negative CSM)"""
    calculator = IFRS17Calculator(reporting_date=date(2024, 10, 26))

    # Create an onerous contract (claims exceed premiums)
    onerous_contract = InsuranceContract(
        contract_id="ONEROUS-001",
        inception_date=date(2024, 1, 1),
        measurement_model="BBA",
        initial_premium=50000,
        coverage_period_years=5,
        discount_rate=0.05,
        risk_adjustment=5000,
        expected_claims=80000,  # Higher than premium
        acquisition_costs=3000
    )

    result = calculator.calculate(onerous_contract)

    # For onerous contracts, CSM should be zero
    assert result.csm.opening_balance == 0
    assert result.csm.closing_balance == 0
