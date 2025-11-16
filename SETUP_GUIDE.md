# 🚀 ArixStructure Setup Guide

## Quick Start (5 minutes)

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Hugging Face Token (FREE)
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name it "ArixStructure" 
4. Select "Read" access
5. Copy the token (starts with `hf_`)

### 3. Configure Token
Create `.streamlit/secrets.toml`:
```toml
HF_TOKEN = "hf_your_actual_token_here"
```

### 4. Run Application
```bash
python start.py
```

## Alternative Token Setup

### Option 1: Environment Variable
```bash
# Windows
set HF_TOKEN=hf_your_token_here

# Linux/Mac
export HF_TOKEN=hf_your_token_here
```

### Option 2: .env File
Create `.env` file:
```
HF_TOKEN=hf_your_token_here
```

## Verification

Run this to test your setup:
```bash
python -c "import streamlit as st; print('✅ Setup complete!')"
```

## Troubleshooting

**Token not working?**
- Ensure token starts with `hf_`
- Check for extra spaces in secrets.toml
- Verify token has "Read" permissions

**Import errors?**
- Run: `pip install -r requirements.txt`
- Use Python 3.8+

**Need help?**
- Check the main README.md
- Create an issue on GitHub

---
**Ready to transform your documents! 🎉**