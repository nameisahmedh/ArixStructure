# Setup Instructions

## Quick Start

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure API Token**
```bash
# Option 1: Environment variable
export HF_TOKEN=your_hugging_face_token

# Option 2: Secrets file
echo 'HF_TOKEN = "your_token_here"' > .streamlit/secrets.toml
```

3. **Run Application**
```bash
streamlit run app.py
```

## Development Setup

1. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Development Dependencies**
```bash
pip install -r requirements.txt
pip install pytest black flake8  # Optional dev tools
```

3. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your actual tokens
```

## Production Deployment

1. **Environment Variables**
   - Set `HF_TOKEN` in your deployment environment
   - Configure any additional secrets

2. **Streamlit Configuration**
   - The app includes production-ready config in `.streamlit/config.toml`
   - Modify as needed for your deployment platform

3. **Security Checklist**
   - ✅ No hardcoded secrets
   - ✅ Input validation enabled
   - ✅ CORS properly configured
   - ✅ File upload limits set

## Troubleshooting

### Common Issues

1. **Missing Kaleido Error**
```bash
pip install kaleido
```

2. **Font Loading Issues**
   - Clear browser cache
   - Restart Streamlit server

3. **API Token Issues**
   - Verify token is valid
   - Check environment variable is set
   - Ensure secrets.toml is properly formatted

### Performance Tips

- Use smaller files for testing
- Clear temp directories regularly
- Monitor memory usage with large documents

## File Structure

```
final_project/
├── 📄 Core Files
│   ├── app.py              # Main application
│   ├── parser.py           # Document parsing
│   ├── llm_handler.py      # AI integration
│   └── utils.py            # Utilities
├── 📁 Pages
│   └── pages/              # Streamlit pages
├── ⚙️ Configuration
│   ├── .streamlit/         # Streamlit config
│   ├── requirements.txt    # Dependencies
│   └── .env.example        # Environment template
└── 📚 Documentation
    ├── README.md           # Main documentation
    └── SETUP.md            # This file
```