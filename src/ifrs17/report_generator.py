"""Markdown report generator for IFRS 17 results"""

from datetime import date
from typing import List
from .models import IFRS17Result


class MarkdownReportGenerator:
    """Generates markdown reports from IFRS 17 calculation results"""

    def __init__(self, reporting_date: date, company_name: str = "Insurance Company"):
        self.reporting_date = reporting_date
        self.company_name = company_name

    @staticmethod
    def _format_amount(amount: float, show_currency: bool = True) -> str:
        """Format amount with improved readability"""
        prefix = "$" if show_currency else ""
        # Handle negative zero edge case
        if abs(amount) < 0.01:  # Treat values very close to zero as zero
            amount = 0.0
        if amount < 0:
            return f'<span class="negative">{prefix}({abs(amount):,.2f})</span>'
        return f"{prefix}{amount:,.2f}"

    def generate(self, results: List[IFRS17Result], output_path: str):
        """Generate comprehensive IFRS 17 markdown report"""

        # Calculate totals
        total_liability = sum(r.insurance_contract_liability for r in results)
        total_csm = sum(r.csm.closing_balance for r in results)
        total_fcf = sum(r.fulfilment_cash_flows for r in results)
        total_risk_adj = sum(r.risk_adjustment for r in results)
        total_revenue = sum(r.insurance_revenue for r in results)
        total_expense = sum(r.insurance_service_expense for r in results)

        # Build markdown content
        md_content = self._build_report(
            results, total_liability, total_csm, total_fcf,
            total_risk_adj, total_revenue, total_expense
        )

        # Write to file
        with open(output_path, 'w') as f:
            f.write(md_content)

    def _build_report(self, results: List[IFRS17Result], total_liability: float,
                      total_csm: float, total_fcf: float, total_risk_adj: float,
                      total_revenue: float, total_expense: float) -> str:
        """Build the markdown report content"""

        md = []

        # Header with single emoji
        md.append(f"# 📊 IFRS 17 Actuarial Report\n")
        md.append(f"\n## {self.company_name}\n")
        md.append(f"**Reporting Date:** {self.reporting_date.strftime('%B %d, %Y')}\n")
        md.append("\n" + "="*80 + "\n")

        # Executive Summary
        md.append("\n## Executive Summary\n")
        md.append(f"This report presents the IFRS 17 measurement results for **{len(results)} insurance contracts** ")
        md.append(f"as of {self.reporting_date.strftime('%Y-%m-%d')}.\n")

        # Calculate net result
        net_result = total_revenue - total_expense
        net_emoji = "✅" if net_result >= 0 else "⚠️"

        md.append(f"\n### Key Metrics\n\n")
        md.append(f"| Metric | Amount |\n")
        md.append(f"|--------|--------|\n")
        md.append(f"| Total Insurance Contract Liability | **{self._format_amount(total_liability)}** |\n")
        md.append(f"| Total Contractual Service Margin (CSM) | **{self._format_amount(total_csm)}** |\n")
        md.append(f"| Total Insurance Revenue | **{self._format_amount(total_revenue)}** |\n")
        md.append(f"| Total Insurance Service Expense | **{self._format_amount(total_expense)}** |\n")
        md.append(f"| {net_emoji} Net Insurance Result | **{self._format_amount(net_result)}** |\n")

        # Summary Table
        md.append("\n## Portfolio Summary\n")
        md.append("\n### Liability Breakdown\n\n")
        md.append("| Component | Amount |\n")
        md.append("|-----------|--------|\n")
        md.append(f"| Fulfilment Cash Flows | {self._format_amount(total_fcf)} |\n")
        md.append(f"| Risk Adjustment | {self._format_amount(total_risk_adj)} |\n")
        md.append(f"| Contractual Service Margin | {self._format_amount(total_csm)} |\n")
        md.append(f"| **Total Liability** | **{self._format_amount(total_liability)}** |\n")

        # Contract Details - Summary Table
        md.append("\n## Contract-Level Details\n")
        md.append("\n### Balance Sheet Summary by Contract\n\n")
        md.append("| Contract ID | Model | FCF | Risk Adj. | CSM | Total Liability |\n")
        md.append("|-------------|-------|-----|-----------|-----|----------------|\n")
        for result in results:
            md.append(f"| {result.contract_id} | {result.measurement_model} | ")
            md.append(f"{self._format_amount(result.fulfilment_cash_flows)} | ")
            md.append(f"{self._format_amount(result.risk_adjustment)} | ")
            md.append(f"{self._format_amount(result.csm.closing_balance)} | ")
            md.append(f"**{self._format_amount(result.insurance_contract_liability)}** |\n")

        # P&L Summary by Contract
        md.append("\n### Income Statement Summary by Contract\n\n")
        md.append("| Contract ID | Revenue | Expense | Net Result | Status |\n")
        md.append("|-------------|---------|---------|------------|--------|\n")
        for result in results:
            contract_net = result.insurance_revenue - result.insurance_service_expense
            status = "✅" if contract_net >= 0 else "⚠️"
            md.append(f"| {result.contract_id} | ")
            md.append(f"{self._format_amount(result.insurance_revenue)} | ")
            md.append(f"{self._format_amount(-result.insurance_service_expense)} | ")
            md.append(f"**{self._format_amount(contract_net)}** | {status} |\n")

        # CSM Movement Summary
        md.append("\n### CSM Movement Summary by Contract\n\n")
        md.append("| Contract ID | Opening | Interest | Changes | Release | Closing |\n")
        md.append("|-------------|---------|----------|---------|---------|--------|\n")
        for result in results:
            md.append(f"| {result.contract_id} | ")
            md.append(f"{self._format_amount(result.csm.opening_balance)} | ")
            md.append(f"{self._format_amount(result.csm.interest_accretion)} | ")
            md.append(f"{self._format_amount(result.csm.changes_in_estimates)} | ")
            md.append(f"{self._format_amount(-result.csm.release_for_service)} | ")
            md.append(f"**{self._format_amount(result.csm.closing_balance)}** |\n")

        # Methodology - Compact version
        md.append("\n## Methodology Notes\n\n")
        md.append("This report applies the **Building Block Approach (BBA)** under IFRS 17. ")
        md.append("Coverage units are allocated on a straight-line basis, ")
        md.append("CSM is released in proportion to coverage units provided, ")
        md.append("and interest accretion uses contract discount rates.\n\n")

        md.append("### Component Definitions\n\n")
        md.append("| Component | Definition |\n")
        md.append("|-----------|------------|\n")
        md.append("| **FCF** | Fulfilment Cash Flows - Present value of expected cash flows |\n")
        md.append("| **Risk Adj.** | Risk Adjustment - Compensation for bearing uncertainty |\n")
        md.append("| **CSM** | Contractual Service Margin - Unearned profit over coverage period |\n")

        # Footer
        md.append("\n" + "="*80 + "\n")
        md.append(f"\n*Report generated automatically on {date.today().strftime('%B %d, %Y')}*\n\n")
        md.append("*This report is generated using the IFRS 17 automated reporting system*\n")
        md.append("\n*For more information, please contact your actuarial team*\n")

        return ''.join(md)
