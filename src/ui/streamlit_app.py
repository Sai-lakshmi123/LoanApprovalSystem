"""
Streamlit UI for Loan Approval System
A comprehensive chatbot-style interface for loan application evaluation

Run with: streamlit run src/ui/streamlit_app.py
"""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Loan Approval System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main theme */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --danger-color: #d62728;
        --warning-color: #ff9896;
    }

    /* Decision status badges */
    .decision-approve {
        background-color: #d4edda;
        color: #155724;
        padding: 12px 20px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        font-weight: bold;
        font-size: 18px;
    }

    .decision-reject {
        background-color: #f8d7da;
        color: #721c24;
        padding: 12px 20px;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        font-weight: bold;
        font-size: 18px;
    }

    .decision-review {
        background-color: #fff3cd;
        color: #856404;
        padding: 12px 20px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        font-weight: bold;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== Configuration ====================

API_BASE_URL = st.secrets.get("api_url", "http://localhost:8000")
EVALUATE_LOAN_ENDPOINT = f"{API_BASE_URL}/evaluate-loan"
HEALTH_CHECK_ENDPOINT = f"{API_BASE_URL}/health"

# Employment type options
EMPLOYMENT_TYPES = [
    "employed",
    "self-employed",
    "retired",
    "student",
    "unemployed"
]

# Location options (for demo)
LOCATIONS = [
    "CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI",
    "NJ", "VA", "WA", "AZ", "MA", "TN", "IN", "MD", "MO", "WI",
    "CO", "MN", "SC", "AL", "LA", "KY", "OR", "OK", "CT", "UT"
]

# ==================== Session State ====================

if 'application_history' not in st.session_state:
    st.session_state.application_history = []

if 'current_result' not in st.session_state:
    st.session_state.current_result = None

if 'api_connected' not in st.session_state:
    st.session_state.api_connected = False

# ==================== Helper Functions ====================

def check_api_connection() -> bool:
    """Check if FastAPI server is running"""
    try:
        response = requests.get(HEALTH_CHECK_ENDPOINT, timeout=5)
        return response.status_code == 200
    except:
        return False

def submit_loan_application(form_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Submit loan application to FastAPI endpoint"""
    try:
        response = requests.post(
            EVALUATE_LOAN_ENDPOINT,
            json=form_data,
            timeout=120
        )

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.Timeout:
        st.error("Request timeout (5 minutes). The API is still processing your application. Please try again.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API. Make sure the FastAPI server is running.")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def display_decision_status(classification: str, confidence: int):
    """Display decision status with color coding"""
    if classification == "APPROVE":
        st.markdown(f"""
        <div class="decision-approve">
            ✅ APPROVED ({confidence}% confidence)
        </div>
        """, unsafe_allow_html=True)
        return "approve"
    elif classification == "REJECT":
        st.markdown(f"""
        <div class="decision-reject">
            ❌ REJECTED ({confidence}% confidence)
        </div>
        """, unsafe_allow_html=True)
        return "reject"
    else:  # REVIEW
        st.markdown(f"""
        <div class="decision-review">
            ⚠️ REQUIRES REVIEW ({confidence}% confidence)
        </div>
        """, unsafe_allow_html=True)
        return "review"

def get_risk_color(risk_score: float) -> str:
    """Get color based on risk score"""
    if risk_score < 2.0:
        return "🟢"  # Green - Low risk
    elif risk_score < 3.5:
        return "🟡"  # Yellow - Medium risk
    else:
        return "🔴"  # Red - High risk

def get_risk_level(risk_score: float) -> str:
    """Get risk level based on score"""
    if risk_score < 2.0:
        return "Low"
    elif risk_score < 3.5:
        return "Medium"
    else:
        return "High"

# ==================== Main App ====================

def main():
    # Header
    st.title("🏦 Loan Approval System")
    st.markdown("**AI-Powered Loan Decision Engine**")

    # Check API connection
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        if check_api_connection():
            st.session_state.api_connected = True
            st.success("✅ Connected to API")
        else:
            st.session_state.api_connected = False
            st.warning("⚠️ API Server not available. Start with: python src/api/main.py")

    with col2:
        total_apps = len(st.session_state.application_history)
        if total_apps > 0:
            approved = sum(1 for app in st.session_state.application_history if app.get('decision') == 'APPROVE')
            rejected = sum(1 for app in st.session_state.application_history if app.get('decision') == 'REJECT')
            review = sum(1 for app in st.session_state.application_history if app.get('decision') == 'REVIEW')
            st.metric("Applications", f"{total_apps} (✅{approved} ❌{rejected} ⚠️{review})")
        else:
            st.metric("Applications", "0")

    with col3:
        if st.button("🔄 Clear History", key="clear_history"):
            st.session_state.application_history = []
            st.session_state.current_result = None
            st.rerun()

    st.divider()

    # ==================== Main Content ====================

    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📋 New Application", "📊 Results", "📈 History"])

    # ==================== TAB 1: APPLICATION FORM ====================
    with tab1:
        st.subheader("Loan Application Form")

        if not st.session_state.api_connected:
            st.error("""
            ⚠️ **API Server is not running!**

            Please start the FastAPI server:
            ```bash
            python src/api/main.py
            ```
            """)
            return

        # Create form
        with st.form("loan_application_form", clear_on_submit=False):
            # Personal Information Section
            st.markdown("### 👤 Personal Information")
            col1, col2, col3 = st.columns(3)

            with col1:
                applicant_id = st.text_input(
                    "Applicant ID",
                    value=f"APPL_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    help="Unique identifier for this application"
                )

            with col2:
                age = st.number_input(
                    "Age",
                    min_value=18,
                    max_value=100,
                    value=40,
                    help="Applicant's age (18-100)"
                )

            with col3:
                email = st.text_input(
                    "Email (Optional)",
                    placeholder="john.doe@example.com"
                )

            phone = st.text_input(
                "Phone (Optional)",
                placeholder="+1-555-0100"
            )

            # Financial Information Section
            st.markdown("### 💰 Financial Information")
            col1, col2, col3 = st.columns(3)

            with col1:
                annual_income = st.number_input(
                    "Annual Income ($)",
                    min_value=1000,
                    value=120000,
                    step=10000,
                    help="Applicant's gross annual income"
                )

            with col2:
                existing_liabilities = st.number_input(
                    "Monthly Liabilities ($)",
                    min_value=0,
                    value=1500,
                    step=100,
                    help="Current monthly debt obligations"
                )

            with col3:
                monthly_expenses = st.number_input(
                    "Monthly Expenses ($)",
                    min_value=0,
                    value=3000,
                    step=100,
                    help="Estimated monthly living expenses"
                )

            # Credit Information Section
            st.markdown("### 📊 Credit Information")
            col1, col2, col3 = st.columns(3)

            with col1:
                credit_score = st.slider(
                    "Credit Score",
                    min_value=300,
                    max_value=850,
                    value=700,
                    step=10,
                    help="Credit score range: 300-850"
                )

            with col2:
                delinquencies = st.number_input(
                    "Delinquencies",
                    min_value=0,
                    max_value=10,
                    value=0,
                    help="Number of past delinquencies"
                )

            with col3:
                inquiries_last_6_months = st.number_input(
                    "Recent Inquiries (6 months)",
                    min_value=0,
                    max_value=20,
                    value=1,
                    help="Number of credit inquiries in last 6 months"
                )

            credit_utilization = st.slider(
                "Credit Utilization Ratio",
                min_value=0.0,
                max_value=1.0,
                value=0.45,
                step=0.05,
                help="Percentage of available credit being used"
            )

            existing_loans = st.number_input(
                "Number of Existing Loans",
                min_value=0,
                max_value=20,
                value=2,
                help="Current number of active loans"
            )

            # Employment Information Section
            st.markdown("### 💼 Employment Information")
            col1, col2 = st.columns(2)

            with col1:
                employment_type = st.selectbox(
                    "Employment Type",
                    options=EMPLOYMENT_TYPES,
                    help="Type of employment"
                )

            with col2:
                years_at_current_job = st.number_input(
                    "Years at Current Job",
                    min_value=0,
                    max_value=60,
                    value=5,
                    help="Years employed at current position"
                )

            # Loan Information Section
            st.markdown("### 🏠 Loan Information")
            col1, col2, col3 = st.columns(3)

            with col1:
                loan_amount = st.number_input(
                    "Loan Amount ($)",
                    min_value=10000,
                    value=250000,
                    step=10000,
                    help="Requested loan amount"
                )

            with col2:
                property_value = st.number_input(
                    "Property Value ($)",
                    min_value=10000,
                    value=400000,
                    step=10000,
                    help="Estimated property value (for mortgages)"
                )

            with col3:
                tenure_months = st.number_input(
                    "Loan Tenure (months)",
                    min_value=12,
                    max_value=360,
                    value=360,
                    step=12,
                    help="Requested loan term in months"
                )

            # Location Section
            st.markdown("### 📍 Location")
            location = st.selectbox(
                "State/Location",
                options=LOCATIONS,
                help="Applicant's geographic location"
            )

            # Submit Button
            st.divider()
            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                submit_button = st.form_submit_button(
                    "📤 Submit Application",
                    use_container_width=True
                )

            with col2:
                reset_button = st.form_submit_button(
                    "🔄 Reset Form",
                    use_container_width=True
                )

            # Handle form submission
            if submit_button:
                # Validate and prepare data
                application_data = {
                    "applicant_id": applicant_id,
                    "age": int(age),
                    "annual_income": float(annual_income),
                    "employment_type": employment_type,
                    "credit_score": int(credit_score),
                    "loan_amount": float(loan_amount),
                    "tenure_months": int(tenure_months),
                    "existing_liabilities": float(existing_liabilities),
                    "location": location,
                    "monthly_expenses": float(monthly_expenses),
                    "delinquencies": int(delinquencies),
                    "inquiries_last_6_months": int(inquiries_last_6_months),
                    "credit_utilization": float(credit_utilization),
                    "years_at_current_job": int(years_at_current_job),
                    "existing_loans": int(existing_loans),
                    "property_value": float(property_value),
                    "email": email if email else None,
                    "phone": phone if phone else None
                }

                # Show processing message
                with st.spinner("📊 Evaluating loan application..."):
                    result = submit_loan_application(application_data)

                if result:
                    # Store result in session state
                    st.session_state.current_result = result

                    # Add to history
                    history_item = {
                        "applicant_id": applicant_id,
                        "timestamp": datetime.now().isoformat(),
                        "decision": result['decision']['classification'],
                        "risk_score": result['risk_score'],
                        "case_id": result['case_id']
                    }
                    st.session_state.application_history.insert(0, history_item)

                    st.success("✅ Application evaluated successfully!")
                    st.balloons()

            if reset_button:
                st.session_state.current_result = None
                st.rerun()

    # ==================== TAB 2: RESULTS ====================
    with tab2:
        st.subheader("Application Results")

        if st.session_state.current_result is None:
            st.info("📝 Submit an application in the 'New Application' tab to see results here.")
        else:
            result = st.session_state.current_result
            decision = result['decision']

            # Decision Status
            st.markdown("### Decision Status")
            display_decision_status(
                decision['classification'],
                decision['confidence_percentage']
            )

            # Key Metrics
            st.markdown("### Key Metrics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                risk_color = get_risk_color(result['risk_score'])
                st.metric(
                    "Risk Score",
                    f"{result['risk_score']:.2f}/5.0",
                    delta=None,
                    help="Lower is better"
                )
                st.caption(f"{risk_color} {get_risk_level(result['risk_score'])} Risk")

            with col2:
                st.metric(
                    "Confidence",
                    f"{decision['confidence_percentage']}%",
                    help="Decision confidence level"
                )

            with col3:
                st.metric(
                    "Case ID",
                    result['case_id'][-8:],
                    help="Unique case identifier"
                )

            with col4:
                st.metric(
                    "Processing Time",
                    f"{result['processing_time_ms']:.0f}ms",
                    help="Time to evaluate"
                )

            st.divider()

            # Decision Details
            st.markdown("### Decision Details")
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("**Classification**")
                st.write(decision['classification'])

                st.markdown("**Confidence Level**")
                st.write(decision['confidence_level'])

                st.markdown("**Risk Score**")
                st.write(f"{decision['risk_score']:.2f} out of 5.0")

            with col2:
                st.markdown("**Reasoning**")
                st.write(decision['reasoning'])

            st.divider()

            # Key Decision Factors
            if decision.get('key_factors'):
                st.markdown("### Key Decision Factors")
                for i, factor in enumerate(decision['key_factors'], 1):
                    st.write(f"{i}. {factor}")

            st.divider()

            # Next Steps
            if result.get('next_steps'):
                st.markdown("### Next Steps")
                for i, step in enumerate(result['next_steps'], 1):
                    st.write(f"{i}. {step}")

            st.divider()

            # Error Information (if any)
            if result.get('error_handling'):
                error_info = result['error_handling']
                if error_info.get('critical_errors') or error_info.get('error_escalation'):
                    st.markdown("### ⚠️ Error Information")

                    if error_info.get('error_escalation'):
                        st.warning("This application has been escalated for manual review")

                    if error_info.get('critical_errors'):
                        st.write("Critical errors encountered:")
                        for error in error_info['critical_errors']:
                            st.write(f"- {error.get('agent', 'Unknown')}: {error.get('error', 'Unknown error')}")

                    if error_info.get('retry_statistics'):
                        st.write("Retry statistics:")
                        st.json(error_info['retry_statistics'])

            st.divider()

            # Application Details Summary
            with st.expander("📋 Full Application Details"):
                st.json(st.session_state.current_result, expanded=False)

            # Export Options
            st.markdown("### Export Options")
            col1, col2 = st.columns(2)

            with col1:
                json_str = json.dumps(result, indent=2, default=str)
                st.download_button(
                    label="📥 Download as JSON",
                    data=json_str,
                    file_name=f"loan_decision_{result['case_id']}.json",
                    mime="application/json"
                )

            with col2:
                # Create a simple text report
                report = f"""
LOAN APPLICATION DECISION REPORT
{'='*60}

Case ID: {result['case_id']}
Applicant ID: {result['applicant_id']}
Timestamp: {result['timestamp']}
Processing Time: {result['processing_time_ms']:.0f}ms

DECISION
{'='*60}
Status: {decision['classification']}
Confidence: {decision['confidence_percentage']}% ({decision['confidence_level']})
Risk Score: {result['risk_score']:.2f}/5.0
Risk Level: {result['risk_level']}

REASONING
{'='*60}
{decision['reasoning']}

KEY DECISION FACTORS
{'='*60}
{chr(10).join([f"• {factor}" for factor in decision.get('key_factors', [])])}

NEXT STEPS
{'='*60}
{chr(10).join([f"• {step}" for step in result.get('next_steps', [])])}

WORKFLOW STATUS
{'='*60}
Status: {result['workflow_status']}
Execution Path: {' → '.join(result.get('execution_path', []))}
"""
                st.download_button(
                    label="📄 Download as Text",
                    data=report,
                    file_name=f"loan_decision_{result['case_id']}.txt",
                    mime="text/plain"
                )

    # ==================== TAB 3: HISTORY ====================
    with tab3:
        st.subheader("Application History")

        if len(st.session_state.application_history) == 0:
            st.info("📝 No applications submitted yet.")
        else:
            # Create a dataframe from history
            history_df = pd.DataFrame(st.session_state.application_history)

            # Format the dataframe for display
            display_df = history_df.copy()
            display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            display_df = display_df.rename(columns={
                'applicant_id': 'Applicant ID',
                'timestamp': 'Timestamp',
                'decision': 'Decision',
                'risk_score': 'Risk Score',
                'case_id': 'Case ID'
            })

            # Display statistics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                total = len(history_df)
                st.metric("Total Applications", total)

            with col2:
                approved = len(history_df[history_df['decision'] == 'APPROVE'])
                st.metric("Approved", approved)

            with col3:
                rejected = len(history_df[history_df['decision'] == 'REJECT'])
                st.metric("Rejected", rejected)

            with col4:
                review = len(history_df[history_df['decision'] == 'REVIEW'])
                st.metric("Under Review", review)

            st.divider()

            # Decision Distribution
            st.markdown("### Decision Distribution")
            decision_counts = history_df['decision'].value_counts()

            # Display as bar chart
            st.bar_chart(decision_counts)

            # Show statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Applications", len(history_df))
            with col2:
                approvals = len(history_df[history_df['decision'] == 'APPROVE'])
                st.metric("Approvals", approvals)
            with col3:
                reviews = len(history_df[history_df['decision'] == 'REVIEW'])
                st.metric("Under Review", reviews)

            st.divider()

            # Risk Score Distribution
            st.markdown("### Risk Score Distribution")
            st.line_chart(history_df['risk_score'].reset_index(drop=True))

            st.divider()

            # Full History Table
            st.markdown("### Application Details")
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            # Export history
            st.markdown("### Export History")
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="application_history.csv",
                mime="text/csv"
            )

    # ==================== Footer ====================
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("**🏦 Loan Approval System v2.0**")

    with col2:
        st.markdown(f"API: `{API_BASE_URL}`")

    with col3:
        st.markdown(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ==================== Entry Point ====================

if __name__ == "__main__":
    main()
