# ArixStructure - Transform Unstructured Data

ArixStructure is a powerful Streamlit application that transforms unstructured documents into structured, queryable data using AI-powered analysis.

## 🚀 Features

- **Multi-Format Support**: PDF, DOCX, PPTX, HTML, CSV, TXT
- **AI-Powered Analysis**: Intelligent content extraction and structuring
- **Interactive Visualizations**: 10+ chart types with Plotly
- **Smart Column Extraction**: AI identifies relevant data columns
- **Export Options**: Multiple formats (CSV, JSON, Excel, PDF, HTML)
- **Dark/Light Theme**: Responsive design with theme toggle

## 📋 Requirements

- Python 3.8+
- Streamlit
- Required packages (see requirements.txt)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd final_project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Hugging Face token:
   - Copy `.env.example` to `.env`
   - Add your HF token: `HF_TOKEN=your_token_here`
   - Or add it to `.streamlit/secrets.toml`

4. Run the application:
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
└── .streamlit/           # Streamlit configuration
    └── config.toml
```

## 🔧 Configuration

### Environment Variables
- `HF_TOKEN`: Your Hugging Face API token

### Streamlit Config
The app includes optimized Streamlit configuration for performance and security.

## 🎯 Usage

1. **Upload Document**: Use the Dashboard to upload your unstructured file
2. **AI Analysis**: The system automatically extracts and structures content
3. **Explore Data**: Use AI Assistant to query your data
4. **Create Visualizations**: Generate charts and graphs in Analytics
5. **Export Results**: Download in multiple formats

## 🔒 Security

- API tokens are managed securely via environment variables
- URL validation prevents SSRF attacks
- Input sanitization and validation throughout
- No sensitive data is committed to version control

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions, please create an issue in the repository.

---

Built with ❤️ using Streamlit, Plotly, and AI