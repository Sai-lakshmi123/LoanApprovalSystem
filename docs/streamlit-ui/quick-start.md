# Streamlit UI Quick Start Guide

## ⚡ Start Using the UI in 3 Minutes

### Step 1: Ensure FastAPI & MCP Servers Are Running

**You should have 5 terminals running from the FastAPI setup:**
- Terminal 1: `python mcp/server.py`
- Terminal 2: `python mcp/riskrulesdb/server.py`
- Terminal 3: `python mcp/decisionsynthesis/server.py`
- Terminal 4: `python mcp/notificationsystem/server.py`
- Terminal 5: `python src/api/main.py`

**If not running, start them now:**

```bash
# Each command in a separate terminal, from the project root
python mcp/server.py
python mcp/riskrulesdb/server.py
python mcp/decisionsynthesis/server.py
python mcp/notificationsystem/server.py
python src/api/main.py
```

### Step 2: Start Streamlit UI

Open **Terminal 6** and run:

```bash
cd /path/to/LoanApprovalSystem/LoanApprovalSystem
streamlit run src/ui/streamlit_app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

  Press Ctrl+c to quit
```

### Step 3: Open Browser

```
http://localhost:8501
```

You should see:
- 🏦 **Loan Approval System** title
- ✅ **Connected to API** status
- **📋 New Application** tab
- **📊 Results** tab
- **📈 History** tab

---

## 🎯 Using the UI

### Submit Your First Application

1. **Click "New Application" tab** (should already be selected)

2. **Fill out the form** with sample data:
   - Age: **45**
   - Annual Income: **$200,000**
   - Employment Type: **employed**
   - Credit Score: **780**
   - Loan Amount: **$300,000**
   - Tenure: **360** months
   - Monthly Liabilities: **$1,000**
   - Location: **CA**
   - (Leave other fields at defaults)

3. **Click "📤 Submit Application"** button

4. **Wait for processing** (2-4 seconds)
   - You'll see a spinning indicator: "📊 Evaluating loan application..."
   - Success message appears when done
   - 🎉 Balloons animation!

5. **Click "📊 Results" tab** to see:
   - ✅ **APPROVE** (or REJECT/REVIEW)
   - Risk Score: **1.8/5.0**
   - Confidence: **85%**
   - Detailed reasoning
   - Key decision factors
   - Next steps

---

## 📋 Form Guide

### Required Fields
- Age (18-100)
- Annual Income
- Employment Type (dropdown)
- Credit Score (300-850)
- Loan Amount
- Tenure (12-360 months)
- Location (dropdown)
- Existing Liabilities

### Optional Fields
- Email
- Phone
- Monthly Expenses (auto-calculated if not provided)
- Delinquencies
- Credit Inquiries
- Credit Utilization
- Years at Job
- Existing Loans
- Property Value

### Smart Defaults
If you don't fill these, they auto-calculate:
- **Monthly Expenses** = Monthly Liabilities × 2
- **Property Value** = Loan Amount × 1.5
- **Applicant ID** = Auto-generated with timestamp

---

## 🎨 Understanding Results

### Decision Status (Color Coded)

| Status | Color | Meaning |
|--------|-------|---------|
| APPROVE | 🟢 Green | Loan approved - proceed with documents |
| REJECT | 🔴 Red | Loan rejected - does not meet criteria |
| REVIEW | 🟡 Yellow | Manual review - needs underwriter evaluation |

### Risk Score (0-5)

| Range | Level | Color |
|-------|-------|-------|
| 0-2.0 | Low | 🟢 Green |
| 2.0-3.5 | Medium | 🟡 Yellow |
| 3.5-5.0 | High | 🔴 Red |

### Confidence Level

- **Very High** (90-100%): Certain decision
- **High** (75-89%): Very confident
- **Medium** (50-74%): Somewhat confident
- **Low** (25-49%): Less certain
- **Very Low** (0-24%): Uncertain (escalated)

---

## 📊 View Your History

1. **Click "📈 History" tab**

2. **See Summary:**
   - Total Applications
   - Total Approved
   - Total Rejected
   - Under Review

3. **View Charts:**
   - Decision Distribution (bar chart)
   - Decision Breakdown (pie chart)
   - Risk Score Trend (line chart)

4. **View Applications Table:**
   - Sortable by any column
   - Click on columns to sort

5. **Export History:**
   - Click "📥 Download as CSV"
   - Opens file in your downloads folder

---

## 💾 Export Decisions

### As JSON
1. Go to **Results** tab
2. Click **"📥 Download as JSON"**
3. Get complete decision data
4. Perfect for integration with other systems

### As Text Report
1. Go to **Results** tab
2. Click **"📄 Download as Text"**
3. Get human-readable report
4. Perfect for printing or sharing

### Example JSON:
```json
{
  "success": true,
  "applicant_id": "APPL001",
  "decision": {
    "classification": "APPROVE",
    "risk_score": 1.8,
    "confidence_percentage": 85,
    "reasoning": "Strong financial profile..."
  },
  "case_id": "CASE-APPL001-1234567890",
  "processing_time_ms": 2500
}
```

---

## 🧪 Test Scenarios

### Test 1: Strong Applicant (Should APPROVE)
```
Age: 45
Income: $200,000
Credit Score: 780
Delinquencies: 0
Years at Job: 10
Monthly Liabilities: $1,000
Loan Amount: $300,000
```
**Expected:** ✅ APPROVE (85%+ confidence)

### Test 2: High-Risk Applicant (Should REVIEW/REJECT)
```
Age: 35
Income: $60,000
Credit Score: 580
Delinquencies: 2
Years at Job: 1
Monthly Liabilities: $2,500
Loan Amount: $300,000
```
**Expected:** 🟡 REVIEW or ❌ REJECT (45-65% confidence)

### Test 3: Moderate Applicant (Should REVIEW)
```
Age: 40
Income: $120,000
Credit Score: 720
Delinquencies: 0
Years at Job: 5
Monthly Liabilities: $1,500
Loan Amount: $280,000
```
**Expected:** 🟡 REVIEW (60-75% confidence)

---

## ⚠️ Troubleshooting

### "⚠️ API Server not available"

**Problem:** Streamlit shows this warning

**Solution:**
1. Go to Terminal 5
2. Run: `python src/api/main.py`
3. Refresh Streamlit page (F5)

### Form Not Submitting

**Problem:** Submit button doesn't work

**Solution:**
1. Check that all required fields are filled
2. Verify age is between 18-100
3. Verify credit score is between 300-850
4. Check that FastAPI is running
5. Refresh page and try again

### "Cannot connect to the API"

**Problem:** Connection error after submitting

**Solution:**
1. Ensure FastAPI server is running
2. Check Terminal 5 for errors
3. Verify API is on http://localhost:8000
4. Try restarting FastAPI

### Slow Response (> 10 seconds)

**Problem:** Application taking too long

**Solution:**
1. Check that all MCP servers are running
2. Verify no other heavy processes running
3. Restart MCP servers
4. Check your network connection

---

## 📱 Mobile Access

### Use from Another Computer

1. **Find your IP address:**
   ```bash
   ipconfig getifaddr en0  # Mac
   hostname -I             # Linux
   ipconfig                # Windows
   ```

2. **From other computer, visit:**
   ```
   http://your-ip:8501
   ```

### Example:
```
Your IP: 192.168.1.100
Visit: http://192.168.1.100:8501
```

---

## 🔧 Common Customizations

### Change API URL

Edit `.streamlit/secrets.toml`:
```toml
api_url = "http://your-server:8000"
```

Then refresh Streamlit.

### Change Port

```bash
streamlit run src/ui/streamlit_app.py --server.port 8502
```

### Change Theme

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
```

---

## 🚀 Tips & Tricks

1. **Use Tab Key** to navigate form fields quickly
2. **Slider Fields** can be dragged or clicked
3. **Click on Results columns** to expand more details
4. **Use History** to find previous applications
5. **Download decisions** for your records
6. **Try different ages** to see how it affects decisions
7. **Export to JSON** to integrate with other systems
8. **Clear History** button at top to reset

---

## 📚 Full Documentation

For complete details, see:
- **STREAMLIT_UI_GUIDE.md** - Complete feature documentation
- **API_DOCUMENTATION.md** - API endpoint details
- **ERROR_HANDLING_GUIDE.md** - Error scenarios and recovery

---

## ✅ Success Checklist

- [ ] All 5 MCP servers running
- [ ] FastAPI server running on port 8000
- [ ] Streamlit server running on port 8501
- [ ] Opened http://localhost:8501 in browser
- [ ] See "✅ Connected to API" message
- [ ] Filled out a sample application
- [ ] Submitted and got a decision
- [ ] Viewed results in Results tab
- [ ] Checked History tab
- [ ] Downloaded a decision as JSON

**If all checked ✓, you're ready to go!**

---

## ⏱️ Typical Workflow

```
1. Open http://localhost:8501 (5 sec)
2. Fill form with applicant data (30 sec)
3. Click Submit (2-4 sec)
4. View decision in Results tab (instant)
5. Review key factors (10 sec)
6. Download report if needed (1 sec)
7. Repeat with next applicant (2 min per application)
```

**Total time per application: ~3-5 minutes**

---

## 🎓 Learning Path

**First Time:**
1. Read this Quick Start (5 min)
2. Start UI (2 min)
3. Submit one application (5 min)
4. View results (2 min)
5. Done! (14 min total)

**Want to Learn More:**
1. Read STREAMLIT_UI_GUIDE.md (20 min)
2. Try different scenarios (15 min)
3. Export data (5 min)
4. Review History (5 min)

**Want to Integrate:**
1. Read API_DOCUMENTATION.md (30 min)
2. Review JSON exports (10 min)
3. Plan integration (varies)

---

## 🎉 You're Ready!

```bash
# Terminal 6
streamlit run src/ui/streamlit_app.py
```

Then visit: **http://localhost:8501**

---

**Version:** 2.0  
**Last Updated:** 2026-05-25  
**Status:** Ready to Use ✅

**Questions?** Check STREAMLIT_UI_GUIDE.md or API_DOCUMENTATION.md
