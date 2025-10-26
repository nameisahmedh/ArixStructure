# ArixStructure - Document Structure Analyzer

Transform unstructured documents into structured, queryable data with AI-powered analysis.

## Features

- 📄 **Multi-format Support**: PDF, Word, PowerPoint, HTML, CSV, TXT
- 🏗️ **Smart Data Structuring**: Automatically extract tables, text, and images
- 🤖 **AI Assistant**: Ask intelligent questions about your documents
- 📊 **Data Visualization**: Create beautiful charts and graphs
- 🖼️ **Image Analysis**: AI-powered image descriptions
- 📝 **Text Analytics**: Deep text analysis with statistics
- 📥 **Export Options**: Multiple formats (CSV, JSON, Excel, PDF)

## Quick Start

### Option 1: Using the Batch File (Recommended)
```bash
# Double-click run.bat or run from command prompt
run.bat
```

### Option 2: Using Python Launcher
```bash
python start.py
```

### Option 3: Direct Streamlit Command
```bash
# Install dependencies first
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Setup Instructions

1. **Clone or Download** the project to your local machine

2. **Install Python 3.8+** if not already installed

3. **Configure Hugging Face Token**:
   - Get a free token from [Hugging Face](https://huggingface.co/settings/tokens)
   - Update `.streamlit/secrets.toml` with your token:
     ```toml
     HF_TOKEN = "your_token_here"
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Upload Document**: Go to Dashboard and upload your unstructured document
2. **AI Analysis**: Use the AI Assistant to ask questions about your data
3. **Visualize**: Create charts and graphs in the Analytics section
4. **Explore Images**: View and analyze extracted images
5. **Text Analysis**: Perform deep text analytics
6. **Export**: Download your structured data in various formats

## Supported File Types

- **Documents**: PDF (.pdf), Word (.docx), PowerPoint (.pptx)
- **Web**: HTML (.html, .htm), URLs
- **Data**: CSV (.csv), Text (.txt)

## Requirements

- Python 3.8+
- Streamlit
- Required packages (see requirements.txt)
- Hugging Face API token (free)

## Troubleshooting

### Common Issues:

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Hugging Face Token Error**: Ensure your token is correctly set in `.streamlit/secrets.toml`

3. **File Upload Issues**: Check file format is supported and file isn't corrupted

4. **Virtual Environment**: If using a virtual environment, make sure it's activated

### Getting Help:

- Check the console output for detailed error messages
- Ensure all required packages are installed
- Verify your Hugging Face token is valid

## Project Structure

```
final_project/
├── app.py                 # Main application
├── utils.py              # Utility functions
├── parser.py             # Document parsing logic
├── llm_handler.py        # AI/LLM integration
├── requirements.txt      # Dependencies
├── start.py             # Python launcher
├── run.bat              # Windows batch launcher
├── .streamlit/
│   └── secrets.toml     # Configuration
└── pages/               # Streamlit pages
    ├── 01_📊_Dashboard.py
    ├── 02_🤖_AI_Assistant.py
    ├── 03_📈_Analytics.py
    ├── 04_🖼️_Images.py
    └── 05_📝_Text_Analysis.py
```

## License

This project is for educational and personal use.