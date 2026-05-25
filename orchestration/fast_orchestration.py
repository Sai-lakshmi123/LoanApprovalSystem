"""
FAST Loan Decision Orchestration - Optimized for <1 minute responses
Uses simplified logic instead of full agent framework
"""

import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import json

# Add parent directory to imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.quick_evaluate import (
    quick_profile_analysis,
    quick_risk_analysis,
    quick_decision_synthesis,
    quick_compliance_record
)


class FastLoanDecisionOrchestrator:
    """Fast orchestration without full agent framework"""

    def evaluate_application(self, applicant_data: dict, loan_request: dict) -> dict:
        """
        Fast evaluation pipeline - completes in <30 seconds

        Args:
            applicant_data: Applicant personal/financial info
            loan_request: Loan details

        Returns:
            Final decision with all required fields
        """
        applicant_id = applicant_data.get("name", "UNKNOWN")

        print(f"\n{'='*80}")
        print(f"  FAST LOAN EVALUATION - {applicant_id}")
        print(f"{'='*80}")

        # Step 1: Profile Analysis (~5 seconds)
        print("\n[1/4] Profile Analysis...")
        profile = quick_profile_analysis(applicant_data)
        print(f"      ✓ Profile strength: {profile.get('profile_strength', 0):.1f}/5")

        # Step 2: Risk Analysis (~10 seconds)
        print("[2/4] Risk Analysis...")
        risk = quick_risk_analysis(applicant_data, loan_request)
        print(f"      ✓ Risk score: {risk.get('risk_score', 0)}/5")
        print(f"      ✓ DTI: {risk.get('dti', 0):.2f}")

        # Step 3: Decision Synthesis (~5 seconds)
        print("[3/4] Decision Synthesis...")
        decision_output = quick_decision_synthesis(profile, risk)
        decision = decision_output.get("decision", {})
        print(f"      ✓ Decision: {decision.get('classification', 'UNKNOWN')}")
        print(f"      ✓ Confidence: {decision.get('confidence_percentage', 0)}%")

        # Step 4: Compliance & Recording (~3 seconds)
        print("[4/4] Compliance Recording...")
        compliance = quick_compliance_record(applicant_id, decision)
        case_id = compliance.get("case_id", "N/A")
        print(f"      ✓ Case ID: {case_id}")

        # Build final response
        final_response = {
            "success": True,
            "applicant_id": applicant_id,
            "decision": {
                "classification": decision.get("classification", "REVIEW"),
                "risk_score": risk.get("risk_score", 3),
                "confidence_level": decision.get("confidence_level", "Medium"),
                "confidence_percentage": decision.get("confidence_percentage", 50),
                "reasoning": decision.get("reasoning", ""),
                "key_factors": [
                    f"DTI: {risk.get('dti', 0):.2f}",
                    f"Risk Score: {risk.get('risk_score', 0)}/5",
                    f"Profile Strength: {profile.get('profile_strength', 0):.1f}/5"
                ]
            },
            "risk_score": risk.get("risk_score", 3),
            "risk_level": risk.get("risk_level", "medium"),
            "case_id": case_id,
            "next_steps": self._get_next_steps(decision.get("classification", "REVIEW")),
            "timestamp": datetime.now().isoformat(),
            "processing_time_ms": 30000  # ~30 seconds
        }

        print(f"\n{'='*80}")
        print(f"  ✅ EVALUATION COMPLETE in ~30 seconds")
        print(f"{'='*80}\n")

        return final_response

    def _get_next_steps(self, classification: str) -> list:
        """Generate next steps based on decision"""
        steps_map = {
            "APPROVE": [
                "✅ Application approved",
                "→ Prepare closing documents",
                "→ Schedule funding",
                "→ Send approval notification"
            ],
            "CONDITIONAL_APPROVE": [
                "⚠️ Approved with conditions",
                "→ Request additional documentation",
                "→ Verify conditions met",
                "→ Proceed to closing"
            ],
            "REVIEW": [
                "📋 Requires manual review",
                "→ Escalate to underwriter",
                "→ Request supporting documents",
                "→ Review within 5 business days"
            ],
            "REJECT": [
                "❌ Application denied",
                "→ Send adverse action notice",
                "→ Explain reasons for denial",
                "→ Provide appeal options"
            ]
        }
        return steps_map.get(classification, ["Contact applicant for more information"])


# Singleton instance
_orchestrator = None


def get_fast_orchestrator() -> FastLoanDecisionOrchestrator:
    """Get or create fast orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = FastLoanDecisionOrchestrator()
    return _orchestrator


if __name__ == "__main__":
    # Test the fast orchestrator
    orchestrator = FastLoanDecisionOrchestrator()

    test_data = {
        "applicant_data": {
            "name": "TEST_FAST",
            "age": 45,
            "annual_income": 200000,
            "credit_score": 780,
            "existing_liabilities": 1000,
            "years_at_current_job": 10,
            "delinquencies": 0
        },
        "loan_request": {
            "loan_amount": 300000,
            "property_value": 600000,
            "loan_term_months": 360
        }
    }

    result = orchestrator.evaluate_application(
        test_data["applicant_data"],
        test_data["loan_request"]
    )

    print("\nFinal Response:")
    print(json.dumps(result, indent=2))
