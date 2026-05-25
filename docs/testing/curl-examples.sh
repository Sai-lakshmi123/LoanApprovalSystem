#!/bin/bash
#
# FastAPI Loan Evaluation Service - cURL Test Script
#
# Tests the /evaluate-loan endpoint with various loan applications
#
# Usage: bash examples/curl_tests.sh
#
# Make sure the API is running:
#   python src/api/main.py
#

set -e

API_URL="http://localhost:8000"
ENDPOINT="$API_URL/evaluate-loan"

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
  echo ""
  echo -e "${BLUE}=================================================================================${NC}"
  echo -e "${BLUE}  $1${NC}"
  echo -e "${BLUE}=================================================================================${NC}"
  echo ""
}

print_section() {
  echo -e "${YELLOW}>>> $1${NC}"
  echo "-------"
}

print_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
  echo -e "${RED}❌ $1${NC}"
}

# Check API is running
check_api() {
  print_header "CHECKING API CONNECTION"

  if curl -s "$API_URL/health" > /dev/null 2>&1; then
    print_success "API is running at $API_URL"
    curl -s "$API_URL/health" | jq '.'
    return 0
  else
    print_error "Cannot connect to API at $API_URL"
    echo "Start the API with: python src/api/main.py"
    return 1
  fi
}

# Test 1: Health Check
test_health() {
  print_header "TEST 1: HEALTH CHECK"
  print_section "GET /health"

  curl -s "$API_URL/health" | jq '.'
}

# Test 2: List Agents
test_agents() {
  print_header "TEST 2: LIST AGENTS"
  print_section "GET /agents"

  curl -s "$API_URL/agents" | jq '.'
}

# Test 3: Strong Applicant (Auto-Approve)
test_strong_applicant() {
  print_header "TEST 3: STRONG APPLICANT (Expected: APPROVE)"
  print_section "POST /evaluate-loan"

  echo "Request:"
  cat << 'EOF'
{
  "applicant_id": "STRONG001",
  "age": 45,
  "annual_income": 200000,
  "employment_type": "employed",
  "credit_score": 780,
  "loan_amount": 300000,
  "tenure_months": 360,
  "existing_liabilities": 1000,
  "location": "CA",
  "delinquencies": 0,
  "inquiries_last_6_months": 0,
  "credit_utilization": 0.20,
  "years_at_current_job": 10,
  "existing_loans": 1,
  "property_value": 600000
}
EOF

  echo ""
  echo "Response:"
  curl -s -X POST "$ENDPOINT" \
    -H "Content-Type: application/json" \
    -d '{
      "applicant_id": "STRONG001",
      "age": 45,
      "annual_income": 200000,
      "employment_type": "employed",
      "credit_score": 780,
      "loan_amount": 300000,
      "tenure_months": 360,
      "existing_liabilities": 1000,
      "location": "CA",
      "delinquencies": 0,
      "inquiries_last_6_months": 0,
      "credit_utilization": 0.20,
      "years_at_current_job": 10,
      "existing_loans": 1,
      "property_value": 600000
    }' | jq '.'
}

# Test 4: High-Risk Applicant (Escalation)
test_high_risk_applicant() {
  print_header "TEST 4: HIGH-RISK APPLICANT (Expected: REVIEW or REJECT)"
  print_section "POST /evaluate-loan"

  echo "Request:"
  cat << 'EOF'
{
  "applicant_id": "HIGHRISK001",
  "age": 35,
  "annual_income": 60000,
  "employment_type": "employed",
  "credit_score": 580,
  "loan_amount": 300000,
  "tenure_months": 360,
  "existing_liabilities": 2500,
  "location": "TX",
  "delinquencies": 2,
  "inquiries_last_6_months": 5,
  "credit_utilization": 0.85,
  "years_at_current_job": 1,
  "existing_loans": 3,
  "property_value": 320000
}
EOF

  echo ""
  echo "Response:"
  curl -s -X POST "$ENDPOINT" \
    -H "Content-Type: application/json" \
    -d '{
      "applicant_id": "HIGHRISK001",
      "age": 35,
      "annual_income": 60000,
      "employment_type": "employed",
      "credit_score": 580,
      "loan_amount": 300000,
      "tenure_months": 360,
      "existing_liabilities": 2500,
      "location": "TX",
      "delinquencies": 2,
      "inquiries_last_6_months": 5,
      "credit_utilization": 0.85,
      "years_at_current_job": 1,
      "existing_loans": 3,
      "property_value": 320000
    }' | jq '.'
}

# Test 5: Moderate Applicant (Review)
test_moderate_applicant() {
  print_header "TEST 5: MODERATE APPLICANT (Expected: REVIEW)"
  print_section "POST /evaluate-loan"

  echo "Request:"
  cat << 'EOF'
{
  "applicant_id": "MODERATE001",
  "age": 40,
  "annual_income": 120000,
  "employment_type": "employed",
  "credit_score": 720,
  "loan_amount": 280000,
  "tenure_months": 360,
  "existing_liabilities": 1500,
  "location": "NY",
  "delinquencies": 0,
  "inquiries_last_6_months": 2,
  "credit_utilization": 0.45,
  "years_at_current_job": 5,
  "existing_loans": 2,
  "property_value": 450000
}
EOF

  echo ""
  echo "Response:"
  curl -s -X POST "$ENDPOINT" \
    -H "Content-Type: application/json" \
    -d '{
      "applicant_id": "MODERATE001",
      "age": 40,
      "annual_income": 120000,
      "employment_type": "employed",
      "credit_score": 720,
      "loan_amount": 280000,
      "tenure_months": 360,
      "existing_liabilities": 1500,
      "location": "NY",
      "delinquencies": 0,
      "inquiries_last_6_months": 2,
      "credit_utilization": 0.45,
      "years_at_current_job": 5,
      "existing_loans": 2,
      "property_value": 450000
    }' | jq '.'
}

# Test 6: Minimal Required Fields
test_minimal_fields() {
  print_header "TEST 6: MINIMAL REQUIRED FIELDS"
  print_section "POST /evaluate-loan (only required fields)"

  echo "Request:"
  cat << 'EOF'
{
  "applicant_id": "MINIMAL001",
  "age": 35,
  "annual_income": 100000,
  "employment_type": "employed",
  "credit_score": 700,
  "loan_amount": 250000,
  "tenure_months": 360,
  "existing_liabilities": 1000,
  "location": "CA"
}
EOF

  echo ""
  echo "Response:"
  curl -s -X POST "$ENDPOINT" \
    -H "Content-Type: application/json" \
    -d '{
      "applicant_id": "MINIMAL001",
      "age": 35,
      "annual_income": 100000,
      "employment_type": "employed",
      "credit_score": 700,
      "loan_amount": 250000,
      "tenure_months": 360,
      "existing_liabilities": 1000,
      "location": "CA"
    }' | jq '.'
}

# Test 7: Validation Error - Invalid Age
test_validation_age() {
  print_header "TEST 7: VALIDATION ERROR - INVALID AGE"
  print_section "POST /evaluate-loan (age < 18)"

  echo "Request (Invalid: age=15):"
  curl -s -X POST "$ENDPOINT" \
    -H "Content-Type: application/json" \
    -d '{
      "applicant_id": "INVALID001",
      "age": 15,
      "annual_income": 100000,
      "employment_type": "employed",
      "credit_score": 700,
      "loan_amount": 250000,
      "tenure_months": 360,
      "existing_liabilities": 1000,
      "location": "CA"
    }' | jq '.'

  print_success "Validation correctly rejected invalid age"
}

# Test 8: Validation Error - Invalid Credit Score
test_validation_credit_score() {
  print_header "TEST 8: VALIDATION ERROR - INVALID CREDIT SCORE"
  print_section "POST /evaluate-loan (credit_score > 850)"

  echo "Request (Invalid: credit_score=900):"
  curl -s -X POST "$ENDPOINT" \
    -H "Content-Type: application/json" \
    -d '{
      "applicant_id": "INVALID002",
      "age": 35,
      "annual_income": 100000,
      "employment_type": "employed",
      "credit_score": 900,
      "loan_amount": 250000,
      "tenure_months": 360,
      "existing_liabilities": 1000,
      "location": "CA"
    }' | jq '.'

  print_success "Validation correctly rejected invalid credit score"
}

# Test 9: Validation Error - Invalid Employment Type
test_validation_employment() {
  print_header "TEST 9: VALIDATION ERROR - INVALID EMPLOYMENT TYPE"
  print_section "POST /evaluate-loan (invalid employment_type)"

  echo "Request (Invalid: employment_type='invalid'):"
  curl -s -X POST "$ENDPOINT" \
    -H "Content-Type: application/json" \
    -d '{
      "applicant_id": "INVALID003",
      "age": 35,
      "annual_income": 100000,
      "employment_type": "invalid_type",
      "credit_score": 700,
      "loan_amount": 250000,
      "tenure_months": 360,
      "existing_liabilities": 1000,
      "location": "CA"
    }' | jq '.'

  print_success "Validation correctly rejected invalid employment type"
}

# Main execution
main() {
  print_header "FASTAPI LOAN EVALUATION SERVICE - cURL TEST SUITE"

  # Check API is running
  if ! check_api; then
    exit 1
  fi

  # Run tests
  test_health
  sleep 1

  test_agents
  sleep 1

  test_strong_applicant
  sleep 2

  test_high_risk_applicant
  sleep 2

  test_moderate_applicant
  sleep 2

  test_minimal_fields
  sleep 2

  test_validation_age
  sleep 1

  test_validation_credit_score
  sleep 1

  test_validation_employment

  # Summary
  print_header "TEST SUITE COMPLETE"
  print_success "All tests completed!"
  echo ""
  echo "Next steps:"
  echo "  1. Review the responses above"
  echo "  2. Check decision classifications (APPROVE/REJECT/REVIEW)"
  echo "  3. Verify confidence levels and risk scores"
  echo "  4. Confirm validation errors are properly handled"
  echo ""
  echo "API Documentation:"
  echo "  Swagger UI: http://localhost:8000/docs"
  echo "  ReDoc: http://localhost:8000/redoc"
  echo ""
}

# Run main function
main
