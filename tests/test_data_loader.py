"""Tests for data loading functionality"""

import pytest
from pathlib import Path
from src.ifrs17.data_loader import DataLoader


def test_load_sample_contracts():
    """Test loading sample contracts from CSV"""
    # Use the actual sample data file
    data_path = "data/sample_contracts.csv"

    # Check file exists
    assert Path(data_path).exists()

    # Load contracts
    contracts = DataLoader.load_contracts(data_path)

    # Should have loaded contracts
    assert len(contracts) > 0

    # Check first contract has required attributes
    first_contract = contracts[0]
    assert first_contract.contract_id is not None
    assert first_contract.inception_date is not None
    assert first_contract.measurement_model in ['BBA', 'PAA', 'GMM']
    assert first_contract.initial_premium > 0
    assert first_contract.coverage_period_years > 0
    assert first_contract.discount_rate > 0


def test_contract_data_types():
    """Test that loaded contract data has correct types"""
    contracts = DataLoader.load_contracts("data/sample_contracts.csv")

    for contract in contracts:
        assert isinstance(contract.contract_id, str)
        assert isinstance(contract.initial_premium, float)
        assert isinstance(contract.coverage_period_years, int)
        assert isinstance(contract.discount_rate, float)
