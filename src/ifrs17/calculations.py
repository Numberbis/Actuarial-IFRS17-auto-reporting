"""IFRS 17 calculation engine"""

import numpy as np
from datetime import date, timedelta
from typing import List
from .models import InsuranceContract, CoverageUnit, CSMMovement, IFRS17Result


class IFRS17Calculator:
    """Calculator for IFRS 17 measurements"""

    def __init__(self, reporting_date: date):
        self.reporting_date = reporting_date

    def calculate_coverage_units(self, contract: InsuranceContract) -> List[CoverageUnit]:
        """
        Calculate coverage units for the contract.
        Simplified straight-line approach.
        """
        coverage_units = []
        total_periods = contract.coverage_period_years * 12  # Monthly
        units_per_period = 1.0  # Simplified

        for i in range(total_periods):
            period_date = contract.inception_date + timedelta(days=30*i)
            period_str = period_date.strftime("%Y-%m")
            coverage_units.append(CoverageUnit(period=period_str, units=units_per_period))

        return coverage_units

    def calculate_fulfilment_cash_flows(self, contract: InsuranceContract) -> float:
        """
        Calculate present value of expected cash flows.
        Simplified calculation: PV of claims minus PV of premiums.
        """
        n = contract.coverage_period_years
        r = contract.discount_rate

        # Present value of expected claims
        pv_claims = contract.expected_claims * self._annuity_factor(r, n)

        # Present value of premiums (received upfront)
        pv_premiums = contract.initial_premium

        # Net fulfilment cash flows
        fcf = pv_claims - pv_premiums + contract.acquisition_costs

        return fcf

    def calculate_csm(self, contract: InsuranceContract, coverage_units: List[CoverageUnit]) -> CSMMovement:
        """
        Calculate Contractual Service Margin (CSM) movements.
        Simplified BBA approach.
        """
        # Initial CSM = -(FCF + RA) if profitable
        fcf = self.calculate_fulfilment_cash_flows(contract)
        initial_csm = max(0, -(fcf + contract.risk_adjustment))

        # Calculate time since inception
        days_since_inception = (self.reporting_date - contract.inception_date).days
        months_since_inception = days_since_inception // 30

        # Interest accretion
        monthly_rate = contract.discount_rate / 12
        interest_accretion = initial_csm * monthly_rate * months_since_inception

        # Release based on coverage units consumed
        total_units = sum(cu.units for cu in coverage_units)
        consumed_units = sum(cu.units for i, cu in enumerate(coverage_units) if i < months_since_inception)

        if total_units > 0:
            release_ratio = consumed_units / total_units
        else:
            release_ratio = 0

        release_for_service = initial_csm * release_ratio

        # Simplified: no changes in estimates
        changes_in_estimates = 0.0

        closing_balance = initial_csm + interest_accretion + changes_in_estimates - release_for_service

        return CSMMovement(
            opening_balance=initial_csm,
            interest_accretion=interest_accretion,
            changes_in_estimates=changes_in_estimates,
            release_for_service=release_for_service,
            closing_balance=closing_balance
        )

    def calculate_insurance_revenue(self, csm_movement: CSMMovement, risk_adjustment_release: float) -> float:
        """Calculate insurance revenue for the period"""
        return csm_movement.release_for_service + risk_adjustment_release

    def calculate(self, contract: InsuranceContract) -> IFRS17Result:
        """
        Perform complete IFRS 17 calculation for a contract.
        """
        # Calculate components
        coverage_units = self.calculate_coverage_units(contract)
        csm = self.calculate_csm(contract, coverage_units)
        fcf = self.calculate_fulfilment_cash_flows(contract)

        # Simplified risk adjustment release (10% per period)
        months_since_inception = ((self.reporting_date - contract.inception_date).days // 30)
        risk_adj_release = contract.risk_adjustment * 0.1 * min(months_since_inception, 10)

        # Calculate insurance revenue
        insurance_revenue = self.calculate_insurance_revenue(csm, risk_adj_release)

        # Insurance contract liability
        remaining_risk_adj = contract.risk_adjustment - risk_adj_release
        insurance_liability = fcf + remaining_risk_adj + csm.closing_balance

        # Insurance service expense (simplified)
        insurance_service_expense = contract.expected_claims / contract.coverage_period_years

        return IFRS17Result(
            contract_id=contract.contract_id,
            reporting_date=self.reporting_date,
            measurement_model=contract.measurement_model,
            csm=csm,
            fulfilment_cash_flows=fcf,
            risk_adjustment=remaining_risk_adj,
            insurance_contract_liability=insurance_liability,
            coverage_units=coverage_units,
            insurance_revenue=insurance_revenue,
            insurance_service_expense=insurance_service_expense
        )

    @staticmethod
    def _annuity_factor(rate: float, periods: int) -> float:
        """Calculate present value annuity factor"""
        if rate == 0:
            return periods
        return (1 - (1 + rate) ** -periods) / rate
