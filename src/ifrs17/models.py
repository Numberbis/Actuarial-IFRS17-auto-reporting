"""Data models for IFRS 17 insurance contracts"""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass
class InsuranceContract:
    """Represents an insurance contract under IFRS 17"""
    contract_id: str
    inception_date: date
    measurement_model: str  # 'BBA', 'PAA', or 'GMM'
    initial_premium: float
    coverage_period_years: int
    discount_rate: float
    risk_adjustment: float
    expected_claims: float
    acquisition_costs: float


@dataclass
class CoverageUnit:
    """Coverage units for CSM allocation"""
    period: str
    units: float


@dataclass
class CSMMovement:
    """Contractual Service Margin movements"""
    opening_balance: float
    interest_accretion: float
    changes_in_estimates: float
    release_for_service: float
    closing_balance: float


@dataclass
class IFRS17Result:
    """IFRS 17 calculation results"""
    contract_id: str
    reporting_date: date
    measurement_model: str
    csm: CSMMovement
    fulfilment_cash_flows: float
    risk_adjustment: float
    insurance_contract_liability: float
    coverage_units: List[CoverageUnit]
    insurance_revenue: float
    insurance_service_expense: float
