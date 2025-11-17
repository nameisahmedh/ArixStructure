# ArixStructure - AI-Powered Document Analyzer

Transform unstructured documents into structured, queryable data using advanced AI technology.

## 🚀 Features

- **Multi-Format Support**: PDF, DOCX, PPTX, HTML, CSV, TXT
- **AI-Powered Analysis**: Intelligent content extraction and structuring
- **Interactive Visualizations**: 10+ chart types with Plotly
- **Smart Image Extraction**: Extract and analyze images from documents
- **Export Options**: Multiple formats (CSV, JSON, Excel, PDF, HTML)
- **Dark/Light Theme**: Responsive design with theme toggle

## 📋 Requirements

- Python 3.8+
- Google Gemini API Key (free)

## 🛠️ Quick Setup

### 1. Clone & Install
```bash
git clone <your-repo-url>
cd final_project
pip install -r requirements.txt
```

### 2. Configure Gemini API Key
Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

**Get your free API key at:** https://aistudio.google.com/apikey

### 3. Run Application
```bash
streamlit run app.py
```

## 📁 Project Structure

```
final_project/
├── app.py                 # Main application
├── pages/                 # Streamlit pages
│   ├── 01_📊_Dashboard.py
│   ├── 02_🤖_AI_Assistant.py
│   ├── 03_📈_Analytics.py
│   ├── 04_🖼️_Images.py
│   └── 05_📝_Text_Analysis.py
├── parser.py              # Document parsing logic
├── llm_handler.py         # AI/LLM integration
├── utils.py               # Utility functions
├── requirements.txt       # Dependencies
└── .streamlit/           # Configuration
    ├── config.toml
    └── secrets.toml      # Your Gemini API key here
```

## 🎯 Usage

1. **Upload Document**: Use Dashboard to upload files
2. **AI Analysis**: Automatic content extraction and structuring
3. **Explore Data**: Query data with AI Assistant
4. **Create Visualizations**: Generate charts in Analytics
5. **Export Results**: Download in multiple formats

## 🔧 Configuration

### Gemini API Key Setup
1. Visit https://aistudio.google.com/apikey
2. Create a new API key.
3. Add to `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```

### Alternative: Environment Variable
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

## 📊 Supported Formats

| Type | Extensions | Features |
|------|------------|----------|
| **Documents** | PDF, DOCX, PPTX | Text, tables, images |
| **Web** | HTML, HTM | Content, embedded images |
| **Data** | CSV, TXT | Structured data detection |

## 🚀 Quick Start Scripts

### Windows
```bash
python start.py
```

### Advanced Setup
```bash
python run_app.py
```

## 🔒 Security

- API tokens managed via environment variables
- Input validation and sanitization
- Path traversal protection
- No sensitive data in version control

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**"GEMINI_API_KEY not found"**
- Ensure `.streamlit/secrets.toml` exists with your API key.

**"Module not found"**
- Run: `pip install -r requirements.txt`

**"Image extraction failed"**
- Install additional dependencies: `pip install kaleido`

### Support
Create an issue in the repository for help.

---

**Built with ❤️ using Streamlit, AI, and Python**