"""Data loading utilities for IFRS 17 contracts"""

import pandas as pd
from datetime import datetime
from typing import List
from .models import InsuranceContract


class DataLoader:
    """Loads insurance contract data from CSV files"""

    @staticmethod
    def load_contracts(file_path: str) -> List[InsuranceContract]:
        """
        Load insurance contracts from CSV file.

        Expected columns:
        - contract_id: str
        - inception_date: YYYY-MM-DD
        - measurement_model: str (BBA, PAA, or GMM)
        - initial_premium: float
        - coverage_period_years: int
        - discount_rate: float
        - risk_adjustment: float
        - expected_claims: float
        - acquisition_costs: float
        """
        df = pd.read_csv(file_path)

        contracts = []
        for _, row in df.iterrows():
            contract = InsuranceContract(
                contract_id=str(row['contract_id']),
                inception_date=datetime.strptime(row['inception_date'], '%Y-%m-%d').date(),
                measurement_model=row['measurement_model'],
                initial_premium=float(row['initial_premium']),
                coverage_period_years=int(row['coverage_period_years']),
                discount_rate=float(row['discount_rate']),
                risk_adjustment=float(row['risk_adjustment']),
                expected_claims=float(row['expected_claims']),
                acquisition_costs=float(row['acquisition_costs'])
            )
            contracts.append(contract)

        return contracts
