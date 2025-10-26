"""Markdown report generator for IFRS 17 results"""

from datetime import date
from typing import List
from .models import IFRS17Result


class MarkdownReportGenerator:
    """Generates markdown reports from IFRS 17 calculation results"""

    def __init__(self, reporting_date: date, company_name: str = "Insurance Company"):
        self.reporting_date = reporting_date
        self.company_name = company_name

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

        # Header with emoji
        md.append(f"# 📊 IFRS 17 Actuarial Report\n")
        md.append(f"\n## 🏢 {self.company_name}\n")
        md.append(f"📅 **Reporting Date:** {self.reporting_date.strftime('%B %d, %Y')}\n")
        md.append("\n" + "="*80 + "\n")

        # Executive Summary
        md.append("\n## 📈 Executive Summary\n")
        md.append(f"This report presents the IFRS 17 measurement results for **{len(results)} insurance contracts** ")
        md.append(f"as of {self.reporting_date.strftime('%Y-%m-%d')}.\n")

        # Calculate net result
        net_result = total_revenue - total_expense
        net_emoji = "✅" if net_result >= 0 else "⚠️"

        md.append(f"\n### 🎯 Key Metrics\n\n")
        md.append(f"| Metric | Amount |\n")
        md.append(f"|--------|--------|\n")
        md.append(f"| 💰 Total Insurance Contract Liability | **${total_liability:,.2f}** |\n")
        md.append(f"| 📊 Total Contractual Service Margin (CSM) | **${total_csm:,.2f}** |\n")
        md.append(f"| 💵 Total Insurance Revenue | **${total_revenue:,.2f}** |\n")
        md.append(f"| 💸 Total Insurance Service Expense | **${total_expense:,.2f}** |\n")
        md.append(f"| {net_emoji} Net Insurance Result | **${net_result:,.2f}** |\n")

        # Summary Table
        md.append("\n## 📋 Portfolio Summary\n")
        md.append("\n### 🧮 Liability Breakdown\n\n")
        md.append("| Component | Amount ($) |\n")
        md.append("|-----------|------------|\n")
        md.append(f"| 💵 Fulfilment Cash Flows | {total_fcf:,.2f} |\n")
        md.append(f"| ⚠️ Risk Adjustment | {total_risk_adj:,.2f} |\n")
        md.append(f"| 📊 Contractual Service Margin | {total_csm:,.2f} |\n")
        md.append(f"| **💰 Total Liability** | **{total_liability:,.2f}** |\n")

        # Contract Details
        md.append("\n" + "="*80 + "\n")
        md.append("\n## 📑 Contract-Level Details\n")

        for result in results:
            md.append(f"\n### 📄 Contract {result.contract_id}\n")
            md.append(f"🔍 **Measurement Model:** `{result.measurement_model}`\n\n")

            # Balance Sheet Components
            md.append("#### 📊 Balance Sheet Components\n\n")
            md.append("| Component | Amount ($) |\n")
            md.append("|-----------|------------|\n")
            md.append(f"| 💵 Fulfilment Cash Flows | {result.fulfilment_cash_flows:,.2f} |\n")
            md.append(f"| ⚠️ Risk Adjustment | {result.risk_adjustment:,.2f} |\n")
            md.append(f"| 📈 CSM | {result.csm.closing_balance:,.2f} |\n")
            md.append(f"| **💰 Insurance Contract Liability** | **{result.insurance_contract_liability:,.2f}** |\n")

            # CSM Movement
            md.append(f"\n#### 🔄 CSM Movement Analysis\n\n")
            md.append("| Movement | Amount ($) |\n")
            md.append("|----------|------------|\n")
            md.append(f"| 🏁 Opening Balance | {result.csm.opening_balance:,.2f} |\n")
            md.append(f"| ➕ Interest Accretion | {result.csm.interest_accretion:,.2f} |\n")
            md.append(f"| 🔧 Changes in Estimates | {result.csm.changes_in_estimates:,.2f} |\n")
            md.append(f"| ➖ Release for Service | ({result.csm.release_for_service:,.2f}) |\n")
            md.append(f"| **🎯 Closing Balance** | **{result.csm.closing_balance:,.2f}** |\n")

            # P&L Impact
            contract_net = result.insurance_revenue - result.insurance_service_expense
            contract_emoji = "✅" if contract_net >= 0 else "⚠️"

            md.append(f"\n#### 💼 P&L Impact\n\n")
            md.append("| Item | Amount ($) |\n")
            md.append("|------|------------|\n")
            md.append(f"| 💵 Insurance Revenue | {result.insurance_revenue:,.2f} |\n")
            md.append(f"| 💸 Insurance Service Expense | ({result.insurance_service_expense:,.2f}) |\n")
            md.append(f"| **{contract_emoji} Net Insurance Result** | **{contract_net:,.2f}** |\n")
            md.append("\n" + "-"*80 + "\n")

        # Methodology
        md.append("\n" + "="*80 + "\n")
        md.append("\n## 📚 Methodology\n\n")
        md.append("This report applies the **Building Block Approach (BBA)** under IFRS 17.\n\n")

        md.append("### 🎯 Key Assumptions\n\n")
        md.append("- 📊 Coverage units are allocated on a straight-line basis over the coverage period\n")
        md.append("- 📈 CSM is released in proportion to coverage units provided\n")
        md.append("- 💰 Interest accretion is calculated using contract discount rates\n")
        md.append("- ⚠️ Risk adjustment is released over the coverage period\n\n")

        md.append("### 🧩 Components Explained\n\n")
        md.append("| Component | Description |\n")
        md.append("|-----------|-------------|\n")
        md.append("| 💵 **Fulfilment Cash Flows (FCF)** | Present value of expected cash flows |\n")
        md.append("| ⚠️ **Risk Adjustment (RA)** | Compensation required for bearing uncertainty |\n")
        md.append("| 📊 **Contractual Service Margin (CSM)** | Unearned profit recognized over coverage period |\n")

        # Footer
        md.append("\n" + "="*80 + "\n")
        md.append(f"\n📅 *Report generated automatically on {date.today().strftime('%B %d, %Y')}*\n\n")
        md.append("🤖 *This report is generated using the IFRS 17 automated reporting system*\n")
        md.append("\n✨ *For more information, please contact your actuarial team*\n")

        return ''.join(md)
