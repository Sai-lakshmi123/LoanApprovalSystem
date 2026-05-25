# 🚀 Setup & Deployment Documentation

Everything you need to install, configure, and deploy the Loan Approval System.

## 📖 Quick Overview

This folder contains:
- Installation guides
- Environment setup
- Security configuration
- Deployment scripts
- Security best practices
- Configuration templates

## 📑 Files in This Folder

| File | Purpose |
|------|---------|
| [installation-guide.md](installation-guide.md) | Complete setup instructions (START HERE) |
| [security-best-practices.md](security-best-practices.md) | Secure API key management |
| [security-checklist.md](security-checklist.md) | Pre-deployment security checklist |
| [.env.example](.env.example) | Environment variables template |
| [streamlit-secrets.toml.example](streamlit-secrets.toml.example) | Streamlit config template |
| [setup.sh](setup.sh) | Automated setup script |
| [start-services.sh](start-services.sh) | Start all services |
| [stop-services.sh](stop-services.sh) | Stop all services |
| [github-push-verification.md](github-push-verification.md) | GitHub deployment report |

## 🚀 5-Minute Quick Start

### Step 1: Clone Repository
```bash
git clone https://github.com/Sai-lakshmi123/LoanApprovalSystem.git
cd LoanApprovalSystem/LoanApprovalSystem
```

### Step 2: Create Environment File
```bash
cp .env.example .env
```

### Step 3: Add Your API Key
```bash
# Edit .env and add your Anthropic API Key
nano .env
# Add: ANTHROPIC_API_KEY=sk-ant-your_actual_key_here
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Start Services
```bash
bash start-services.sh
```

### Step 6: Open Web UI
- **Streamlit UI:** http://localhost:8501
- **FastAPI Docs:** http://localhost:8000/docs

Done! ✅

---

## 📋 Detailed Setup Guides

### [Installation Guide](installation-guide.md)
**Recommended:** Start here for complete setup  
Contains:
- System requirements
- Dependencies installation
- Step-by-step configuration
- Service startup
- Verification checks
- Troubleshooting

### [Security Best Practices](security-best-practices.md)
**Important:** Before deployment  
Covers:
- API key protection
- Environment variable setup
- .gitignore configuration
- GitHub secrets setup
- Pre-commit checklist
- Emergency procedures

### [Security Checklist](security-checklist.md)
**Quick Reference:** Before each push  
Includes:
- Pre-deployment checklist
- File verification commands
- Sensitive data checks
- Git verification steps

---

## 🔐 Environment Configuration

### Create .env File
```bash
cp .env.example .env
```

### Edit .env with Your Values
```bash
nano .env
```

### Required Environment Variables

```env
# CRITICAL: Your Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# FastAPI Configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
FASTAPI_RELOAD=true

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Application
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
```

**⚠️ IMPORTANT:** Never commit `.env` file with real API keys!

---

## 🎯 Service Startup

### Option 1: Automated (Recommended)
```bash
bash start-services.sh
```

Automatically starts:
- 4 MCP Servers (ports 3001-3004)
- FastAPI Server (port 8000)
- Streamlit UI (port 8501)

### Option 2: Manual Startup

**Terminal 1: MCP Servers**
```bash
python mcp/application_db.py &
python mcp/risk_rules_db.py &
python mcp/decision_synthesis.py &
python mcp/notification_system.py &
```

**Terminal 2: FastAPI**
```bash
python src/api/main.py
```

**Terminal 3: Streamlit**
```bash
streamlit run src/ui/streamlit_app.py
```

---

## ✅ Verification Checklist

After starting services, verify all are running:

```bash
# Check ports are listening
netstat -tuln | grep -E "3001|3002|3003|3004|8000|8501"

# Or use lsof
lsof -i :3001  # Application DB
lsof -i :3002  # Risk Rules DB
lsof -i :3003  # Decision Synthesis
lsof -i :3004  # Notification System
lsof -i :8000  # FastAPI
lsof -i :8501  # Streamlit
```

Expected output: All ports should show LISTEN status

---

## 🌐 Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Streamlit UI | http://localhost:8501 | Web application |
| FastAPI Docs | http://localhost:8000/docs | API documentation |
| FastAPI Health | http://localhost:8000/health | API health check |
| App DB (MCP) | http://localhost:3001 | Applicant data |
| Risk DB (MCP) | http://localhost:3002 | Risk metrics |
| Decision (MCP) | http://localhost:3003 | Decision factors |
| Notification (MCP) | http://localhost:3004 | Case tracking |

---

## 🔒 Security Practices

### Before First Run

✅ Create `.env` from template  
✅ Add your API key to `.env`  
✅ Verify `.env` is in `.gitignore`  
✅ Never commit `.env` with real keys  
✅ Review security best practices  

### Before Each Push to GitHub

✅ Run `git check-ignore .env`  
✅ Run `git status` and review files  
✅ Check for hardcoded API keys: `grep -r "sk-ant-" .`  
✅ Run security checklist  

### Pre-Deployment

✅ Complete security checklist  
✅ Rotate API keys if exposed  
✅ Set up GitHub Secrets (see [Security Best Practices](security-best-practices.md))  
✅ Review deployment configuration  

---

## 🧹 Stop Services

### Option 1: Automated
```bash
bash stop-services.sh
```

### Option 2: Manual
```bash
# Kill specific processes
pkill -f "python.*application_db"
pkill -f "python.*risk_rules_db"
pkill -f "python.*decision_synthesis"
pkill -f "python.*notification_system"
pkill -f "python.*main.py"
pkill -f "streamlit run"

# Or kill by port
fuser -k 3001/tcp
fuser -k 3002/tcp
fuser -k 3003/tcp
fuser -k 3004/tcp
fuser -k 8000/tcp
fuser -k 8501/tcp
```

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Find what's using the port
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### ImportError for Dependencies
```bash
# Reinstall all dependencies
pip install --upgrade -r requirements.txt
```

### API Key Not Found
```bash
# Verify .env exists and has ANTHROPIC_API_KEY
cat .env | grep ANTHROPIC_API_KEY

# Should output: ANTHROPIC_API_KEY=sk-ant-...
```

### Streamlit Can't Connect to API
```bash
# Verify FastAPI is running
curl http://localhost:8000/health

# Should return: {"status":"healthy",...}
```

---

## 📚 Related Documentation

- **Installation:** [installation-guide.md](installation-guide.md) (detailed steps)
- **Security:** [security-best-practices.md](security-best-practices.md) (keep API safe)
- **Checklist:** [security-checklist.md](security-checklist.md) (pre-deployment)
- **GitHub:** [github-push-verification.md](github-push-verification.md) (deployment report)
- **Architecture:** [Architecture Overview](../architecture/)

---

## 🎯 Next Steps

1. **First Time Setup?**
   - Read [installation-guide.md](installation-guide.md)
   - Follow step-by-step instructions
   - Run `bash start-services.sh`

2. **Ready to Deploy?**
   - Review [security-best-practices.md](security-best-practices.md)
   - Complete [security-checklist.md](security-checklist.md)
   - Push to GitHub

3. **Want to Use the System?**
   - Open http://localhost:8501
   - Submit loan applications
   - View results and analytics

---

**Everything configured? Let's go! 🚀**
