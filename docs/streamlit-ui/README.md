# 🎨 Streamlit UI Documentation

Interactive web application for loan submission and result viewing.

## 📖 Quick Overview

- **Framework:** Streamlit
- **Port:** 8501
- **URL:** http://localhost:8501
- **File:** `src/ui/streamlit_app.py`
- **Features:** Form submission, real-time results, history, analytics

## 📑 Files in This Folder

| File | Purpose |
|------|---------|
| [quick-start.md](quick-start.md) | Get the UI running in 5 minutes |
| [ui-guide.md](ui-guide.md) | Feature walkthrough and usage |
| [implementation-summary.md](implementation-summary.md) | Technical details |
| [creation-notes.md](creation-notes.md) | Development notes |

## 🚀 Quick Start

### 1. Prerequisites
- FastAPI server running on port 8000
- All 4 MCP servers running (ports 3001-3004)

### 2. Start Streamlit UI
```bash
streamlit run src/ui/streamlit_app.py
```

UI opens at: `http://localhost:8501`

### 3. Submit a Loan Application
- Go to "📋 New Application" tab
- Fill in applicant details
- Click "Submit Application"
- Wait for result (< 30 seconds)

## 🎯 Main Features

### Tab 1: 📋 New Application
**Submit a new loan application**

**Sections:**
1. **Personal Information**
   - Applicant name
   - Age
   - Location

2. **Financial Information**
   - Annual income
   - Monthly expenses
   - Existing liabilities

3. **Credit Information**
   - Credit score
   - Credit history duration

4. **Employment Details**
   - Employment type (Salaried/Self-employed/Unemployed)
   - Years at current job

5. **Loan Details**
   - Loan amount
   - Loan tenure (months)

6. **Submit Button**
   - Validates all inputs
   - Sends to FastAPI
   - Shows loading indicator
   - Displays result

---

### Tab 2: 📊 Results
**View latest evaluation results**

**Displays:**
- **Decision Status**
  - 🟢 APPROVE (Green)
  - 🔴 REJECT (Red)
  - 🟡 REVIEW (Yellow)

- **Decision Details**
  - Risk Score (1-5)
  - Confidence Level (%)
  - Decision Reasoning

- **Decision Factors**
  - List of key factors
  - Explanation of each

- **Next Steps**
  - Recommended actions
  - Case ID
  - Timestamp

---

### Tab 3: 📈 History
**Track all applications and analytics**

**Features:**
- Application history with timestamps
- Decision summary statistics
- Charts and visualizations
- Export capability (optional)

---

## 🖼️ User Interface Layout

```
┌─────────────────────────────────────────────────┐
│   LOAN APPROVAL SYSTEM                          │
│   By Sai-lakshmi123                             │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ [📋 New Application] [📊 Results] [📈 History]  │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Tab Content Area                                │
│                                                 │
│ • Form inputs (Tab 1)                           │
│ • Results display (Tab 2)                       │
│ • Analytics (Tab 3)                             │
│                                                 │
└─────────────────────────────────────────────────┘
```

## 📝 Form Validation

| Field | Validation | Error Message |
|-------|-----------|---|
| Age | 18-80 | Invalid age range |
| Income | > 0 | Must be positive |
| Credit Score | 300-850 | Outside valid range |
| Loan Amount | > 0 | Must be positive |
| Employment Type | Must be one of 3 options | Invalid selection |

## 🔄 Workflow

```
1. User fills form
   ↓
2. Click Submit
   ↓
3. Form validation
   ↓
4. Send to FastAPI /evaluate-loan
   ↓
5. Show loading spinner
   ↓
6. Receive response (< 30 sec)
   ↓
7. Display result on Results tab
   ↓
8. Store in session history
```

## 💾 Session Management

- **Session State:** Uses Streamlit's `st.session_state`
- **History Storage:** Stored in session (not persistent)
- **Auto-refresh:** Results update in real-time
- **State Variables:**
  - `application_history` - List of submitted applications
  - `latest_result` - Most recent evaluation
  - `api_url` - FastAPI endpoint URL

## 🎨 Styling

- **Color Scheme:**
  - Approve: 🟢 Green (#1ABC9C)
  - Reject: 🔴 Red (#E74C3C)
  - Review: 🟡 Yellow (#F39C12)

- **Layout:** Responsive columns and containers
- **Theme:** Streamlit default light theme

## 🔗 API Integration

**Endpoint Called:**
```
POST http://localhost:8000/evaluate-loan
```

**Request:**
```json
{
  "applicant_id": "APPL_20260525...",
  "age": 45,
  "annual_income": 200000,
  ...
}
```

**Response Handling:**
- Success: Parse result and display
- Error: Show error message
- Timeout: Display retry option

## ⚙️ Configuration

**File:** `src/ui/streamlit_app.py`

Key settings:
```python
API_URL = "http://localhost:8000"
API_TIMEOUT = 120  # seconds
REFRESH_INTERVAL = 5  # seconds
```

## 🧪 Testing the UI

### Test 1: Submit Valid Application
- Fill form with valid data
- Click Submit
- Expected: See APPROVE/REJECT/REVIEW result

### Test 2: Test History
- Submit multiple applications
- Go to History tab
- Expected: All applications listed

### Test 3: Test Form Validation
- Leave required fields empty
- Click Submit
- Expected: Validation error message

## 🐛 Troubleshooting

**"Cannot connect to API" error?**
- Verify FastAPI is running: `curl http://localhost:8000/health`
- Check API URL in code matches actual server
- See [Error Handling Guide](../api-integration/error-handling-guide.md)

**"Request timeout" error?**
- Check FastAPI is responsive
- MCP servers may be slow - increase timeout
- Review [Performance Guide](../fastapi/implementation-summary.md)

**Form not submitting?**
- Check all required fields filled
- Open browser console (F12) for JavaScript errors
- Review Streamlit logs

## 📱 Browser Compatibility

- Chrome / Chromium: ✅ Fully supported
- Firefox: ✅ Fully supported
- Safari: ✅ Fully supported
- Edge: ✅ Fully supported

## 🔐 Security

- **API Key:** Passed via .env to FastAPI (not exposed in UI)
- **Input Validation:** All inputs validated on backend
- **HTTPS:** Recommended for production
- **Session:** Browser session storage only

See [Security Best Practices](../setup-deployment/security-best-practices.md)

## 📊 Code Structure

**Main File:** `src/ui/streamlit_app.py`

Components:
- Page configuration
- API client functions
- Session state initialization
- 3 main tabs (form, results, history)
- Helper functions for display

## 🔗 Related Documentation

- **Architecture:** [System Design](../architecture/system-design.md)
- **FastAPI:** [API Documentation](../fastapi/)
- **Testing:** [UI Testing Guide](../testing/test-scenarios.md)
- **Setup:** [Installation Guide](../setup-deployment/installation-guide.md)

## 🚀 Deployment

### Local Development
```bash
streamlit run src/ui/streamlit_app.py
```

### Production
See [Deployment Guide](../setup-deployment/installation-guide.md)

---

**Next Steps:**
1. Read [quick-start.md](quick-start.md)
2. Follow [ui-guide.md](ui-guide.md) for feature walkthrough
3. Submit your first loan application!
4. Explore Results and History tabs

Ready to use the UI? 🎨✨
