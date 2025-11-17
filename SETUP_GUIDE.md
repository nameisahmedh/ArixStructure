# 🚀 ArixStructure Setup Guide

## Quick Start (5 minutes)

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Google Gemini API Key (FREE)
1. Go to https://aistudio.google.com/apikey
2. Click "Create API key"
3. Copy the key.

### 3. Configure API Key
Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

### 4. Run Application
```bash
python start.py
```

## Alternative API Key Setup

### Option 1: Environment Variable
```bash
# Windows
set GEMINI_API_KEY=your_gemini_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_gemini_api_key_here
```

### Option 2: .env File
Create `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Verification

Run this to test your setup:
```bash
python -c "import streamlit as st; print('✅ Setup complete!')"
```

## Troubleshooting

**API Key not working?**
- Check for extra spaces in secrets.toml

**Import errors?**
- Run: `pip install -r requirements.txt`
- Use Python 3.8+

**Need help?**
- Check the main README.md
- Create an issue on GitHub

---
**Ready to transform your documents! 🎉**
