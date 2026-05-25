# 🔒 Security Best Practices - Loan Approval System

## ⚠️ CRITICAL: Never Commit Sensitive Data to GitHub!

### 📋 Files & Data That Should NEVER Be Committed

#### 🔑 API Keys & Credentials
- `.env` (environment variables with real values)
- `.env.local`, `.env.*.local`
- `.env.production` 
- `anthropic_api_key`
- `ANTHROPIC_API_KEY` (from environment)
- Any file containing `secret`, `credential`, `password`, `token`, `apikey`, `api_key`, `access_key`, `private`

#### 🔐 Configuration Files with Secrets
- `.streamlit/secrets.toml` (Streamlit secrets)
- `.streamlit/secrets.yaml`
- `credentials.json`
- `secrets.json`
- `config.json` (if contains secrets)
- `private/` directory
- `secrets/` directory

#### ☁️ Cloud Provider Credentials
- AWS credentials files
- Google Cloud credentials
- Azure credentials
- Any service account keys

#### 🔒 Security Files
- `*.pem`, `*.key`, `*.ppk`, `*.pub` (SSH/SSL keys)
- `*.p8`, `*.p12`, `*.pfx`, `*.jks` (Certificate files)
- `.keystore`, `.keystores`

---

## ✅ What IS Safe to Commit

### Publicly Shareable Files
- `README.md`
- `requirements.txt` (dependencies, no secrets)
- `.gitignore` (this list of ignored files)
- `.env.example` (TEMPLATE without real values)
- `.streamlit/config.toml` (configuration, no secrets)
- `.streamlit/secrets.toml.example` (TEMPLATE)
- Source code (`src/`, `agents/`, `orchestration/`)
- Test files (`tests/`)
- Documentation files

---

## 🚀 Setup Instructions for Developers

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/LoanApprovalSystem.git
cd LoanApprovalSystem/LoanApprovalSystem
```

### Step 2: Create Environment Files from Templates
```bash
# Copy environment variable template
cp .env.example .env

# Copy Streamlit secrets template
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

### Step 3: Add Your Actual Secrets
Edit `.env`:
```bash
nano .env
```

Add your actual values:
```env
ANTHROPIC_API_KEY=sk-ant-your_actual_key_here_xxxxx
DATABASE_URL=postgresql://user:password@localhost/dbname
JWT_SECRET_KEY=your_actual_secret_key_here
```

Edit `.streamlit/secrets.toml`:
```bash
nano .streamlit/secrets.toml
```

### Step 4: Verify .gitignore is Correct
```bash
# Check that sensitive files are ignored
git check-ignore .env .streamlit/secrets.toml
# Output should show both files are ignored
```

### Step 5: Verify Before Committing
```bash
# Show all files that WILL be committed (should have NO secrets)
git status

# Show all files that WILL be ignored (should include .env, secrets, etc)
git ls-files --others --ignored --exclude-standard
```

---

## 🚨 If You Accidentally Committed Secrets

### Immediate Actions:
1. **Do NOT push to GitHub yet**
2. **Rotate all exposed credentials immediately**
3. **Remove from Git history** (cannot be undone once pushed)

### To Remove from Git History:
```bash
# Remove file from history (before pushing)
git rm --cached .env
git commit --amend -m "Remove .env from history"

# Or use git filter-branch for published repositories
git filter-branch --tree-filter 'rm -f .env' HEAD
```

### If Already Pushed to GitHub:
1. **Immediately rotate all API keys** (generate new ones)
2. **Create new encrypted credentials**
3. **Contact GitHub support** for history removal
4. **Create a security advisory** in your repo

---

## 🔑 Anthropic API Key Protection

### Where to Store:
- ✅ `.env` file (local only, NOT in git)
- ✅ Environment variable: `export ANTHROPIC_API_KEY=sk-ant-...`
- ✅ GitHub Secrets (for CI/CD pipelines)
- ✅ `.streamlit/secrets.toml` (local only, NOT in git)

### Where NOT to Store:
- ❌ Hardcoded in source code
- ❌ Committed to Git repository
- ❌ Included in Docker images
- ❌ Logged or printed to console
- ❌ Shared in pull request descriptions
- ❌ Stored in browser local storage

### Getting Your API Key:
1. Go to: https://console.anthropic.com/
2. Navigate to "API Keys"
3. Click "Create new key"
4. Copy the key (starts with `sk-ant-`)
5. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-xxxxx`
6. **Never share or commit this key!**

---

## 🔐 GitHub Secrets for CI/CD

### Setting Up GitHub Secrets:
1. Go to: GitHub > Repository > Settings > Secrets and variables > Actions
2. Click "New repository secret"
3. Name: `ANTHROPIC_API_KEY`
4. Value: Your actual API key (paste the `sk-ant-` key)
5. Click "Add secret"

### Using in GitHub Actions:
```yaml
name: Deploy
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    steps:
      - uses: actions/checkout@v2
      - run: python src/api/main.py
```

---

## 📝 Pre-Commit Checklist

Before every commit, verify:

```bash
# 1. Check for .env file
git check-ignore .env
# Expected: ".env" is in .gitignore

# 2. Check for secrets.toml
git check-ignore .streamlit/secrets.toml
# Expected: ".streamlit/secrets.toml" is in .gitignore

# 3. Review files to be committed
git diff --cached
# Should NOT contain: api keys, passwords, tokens, credentials

# 4. See what will be committed
git status
# Should NOT show: .env, secrets.toml, credentials, keys

# 5. List ignored files
git ls-files --others --ignored --exclude-standard
# Should include: .env, .streamlit/secrets.toml, venv/, __pycache__/
```

---

## 🛡️ Additional Security Practices

### Code Review
- Always review code before pushing
- Look for hardcoded secrets
- Use `git show` to check commits

### Scanning Tools
```bash
# Scan for secrets before commit
git-secrets --scan

# Or use truffleHog
trufflehog filesystem .
```

### Environment Variables
```python
# Good - Load from .env
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Bad - Hardcoded
api_key = "sk-ant-xxxxx"  # DO NOT DO THIS!
```

### Logging
```python
# Good - Don't log secrets
logger.info(f"API key: {api_key[:10]}...")  # Only show first 10 chars

# Bad - Logs entire key
logger.info(f"API key: {api_key}")  # DO NOT DO THIS!
```

---

## 📚 File Structure Reference

```
LoanApprovalSystem/
├── .gitignore                          # ✅ Contains all security patterns
├── .env.example                        # ✅ SAFE: Template without values
├── .env                                # ❌ NOT IN GIT: Real secrets
├── .streamlit/
│   ├── config.toml                    # ✅ SAFE: Configuration only
│   ├── secrets.toml.example           # ✅ SAFE: Template
│   └── secrets.toml                   # ❌ NOT IN GIT: Real API URL/keys
├── src/
│   ├── api/
│   │   └── main.py                   # ✅ SAFE: Source code
│   └── ui/
│       └── streamlit_app.py          # ✅ SAFE: Source code
├── agents/                             # ✅ SAFE: Agent code
├── orchestration/                      # ✅ SAFE: Orchestration code
├── tests/                              # ✅ SAFE: Test code
├── README.md                           # ✅ SAFE: Documentation
├── requirements.txt                    # ✅ SAFE: Dependencies
└── SECURITY_BEST_PRACTICES.md         # ✅ SAFE: This file
```

---

## ✅ Quick Security Checklist

- [ ] `.env` is in `.gitignore`
- [ ] `.streamlit/secrets.toml` is in `.gitignore`
- [ ] Created `.env` from `.env.example`
- [ ] Created `.streamlit/secrets.toml` from template
- [ ] Added real API keys to `.env`
- [ ] Never hardcoded secrets in source code
- [ ] `.gitignore` includes all patterns from this repo
- [ ] Verified with `git check-ignore .env`
- [ ] Reviewed `git status` before every push
- [ ] No secrets visible in `git log`
- [ ] Set up GitHub Secrets for CI/CD

---

## 🆘 Emergency: Exposed API Key

If your Anthropic API key was accidentally pushed:

1. **Immediately:**
   ```bash
   # Go to https://console.anthropic.com/
   # Delete the exposed key
   # Create a new API key
   # Update .env with new key
   ```

2. **Clean Git History:**
   ```bash
   git filter-branch --tree-filter 'rm -f .env' HEAD
   git push origin --force-with-lease
   ```

3. **Monitor:**
   - Check API logs for unauthorized usage
   - Monitor billing for unusual activity
   - Update all deployed applications

---

## 📖 References

- [GitHub: Removing Sensitive Data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [Anthropic Security](https://www.anthropic.com/security)
- [OWASP: Sensitive Data Exposure](https://owasp.org/www-project-top-ten/2021/A01_2021-Broken_Access_Control/)
- [Git-secrets Tool](https://github.com/awslabs/git-secrets)

---

**Last Updated:** 2026-05-25
**Status:** ✅ Ready for Production

Remember: **Security is everyone's responsibility!** 🔒
