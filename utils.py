import streamlit as st
import pandas as pd
import os
import shutil
import time
import io
import json
from datetime import datetime
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    reportlab_available = True
except ImportError:
    print("Warning: reportlab not available. PDF export will be disabled.")
    reportlab_available = False

try:
    import openpyxl
except ImportError:
    print("Warning: openpyxl not available. Excel export will be disabled.")
    openpyxl = None

def init_theme_mode():
    """Initialize theme mode safely"""
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = 'light'

# Only initialize if streamlit is available
try:
    init_theme_mode()
except:
    pass

def get_theme_css():
    """Consistent CSS with Poppins font for all pages"""
    base_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
        
        .stApp {
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
        }
        
        .main-header h1 {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .main-header p {
            color: rgba(255,255,255,0.9);
            font-size: 1.1rem;
            font-weight: 400;
        }
        
        .content-card {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
        }
        
        .stButton > button {
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            border-radius: 10px;
            border: none;
            padding: 0.6rem 1.2rem;
            transition: all 0.3s ease;
            background: #667eea;
            color: white;
        }
        
        .stButton > button:hover {
            background: #5a6fd8;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }
        
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-weight: 600;
        }
        
        .stMetric {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            text-align: center;
        }
        
        .stMetric > div > div {
            font-family: 'Poppins', sans-serif;
        }
        
        .stSelectbox > div > div {
            font-family: 'Poppins', sans-serif;
            border-radius: 8px;
            border: 1px solid #d1d5db;
        }
        
        .stTextInput > div > div > input {
            font-family: 'Poppins', sans-serif;
            border-radius: 8px;
            border: 1px solid #d1d5db;
            padding: 0.75rem;
        }
        
        .stTextArea > div > div > textarea {
            font-family: 'Poppins', sans-serif;
            border-radius: 8px;
            border: 1px solid #d1d5db;
        }
        
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .stExpander {
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        /* Comprehensive Responsive Design */
        
        /* Large Desktop (1200px+) */
        @media (min-width: 1200px) {
            .main-header {
                padding: 2.5rem 3rem;
            }
            
            .content-card {
                padding: 2.5rem;
                margin: 1.5rem 0;
            }
        }
        
        /* Desktop (992px - 1199px) */
        @media (min-width: 992px) and (max-width: 1199px) {
            .main-header {
                padding: 2rem;
            }
            
            .content-card {
                padding: 2rem;
            }
        }
        
        /* Tablet (768px - 991px) */
        @media (min-width: 768px) and (max-width: 991px) {
            .main-header {
                padding: 1.8rem 1.5rem;
            }
            
            .main-header h1 {
                font-size: 2.2rem;
            }
            
            .content-card {
                padding: 1.8rem;
                margin: 1rem 0;
            }
            
            .stButton > button {
                padding: 0.6rem 1.1rem;
                font-size: 0.95rem;
            }
        }
        
        /* Mobile Large (576px - 767px) */
        @media (min-width: 576px) and (max-width: 767px) {
            .main-header {
                padding: 1.5rem 1rem;
            }
            
            .main-header h1 {
                font-size: 2rem;
            }
            
            .main-header p {
                font-size: 1rem;
            }
            
            .content-card {
                padding: 1.5rem;
                margin: 0.8rem 0;
            }
            
            .stButton > button {
                padding: 0.5rem 1rem;
                font-size: 0.9rem;
            }
            
            .stMetric {
                padding: 1.2rem;
            }
        }
        
        /* Mobile Medium (375px - 575px) */
        @media (min-width: 375px) and (max-width: 575px) {
            .main-header {
                padding: 1.2rem 0.8rem;
            }
            
            .main-header h1 {
                font-size: 1.8rem;
            }
            
            .main-header p {
                font-size: 0.95rem;
            }
            
            .content-card {
                padding: 1.2rem;
                margin: 0.6rem 0;
            }
            
            .stButton > button {
                padding: 0.45rem 0.9rem;
                font-size: 0.88rem;
            }
            
            .stMetric {
                padding: 1rem;
            }
            
            .stTextInput > div > div > input {
                padding: 0.65rem;
                font-size: 0.9rem;
            }
        }
        
        /* Mobile Small (320px - 374px) */
        @media (max-width: 374px) {
            .main-header {
                padding: 1rem 0.5rem;
            }
            
            .main-header h1 {
                font-size: 1.6rem;
            }
            
            .main-header p {
                font-size: 0.85rem;
            }
            
            .content-card {
                padding: 1rem;
                margin: 0.5rem 0;
            }
            
            .stButton > button {
                padding: 0.4rem 0.7rem;
                font-size: 0.8rem;
            }
            
            .stMetric {
                padding: 0.8rem;
            }
            
            .stTextInput > div > div > input {
                padding: 0.6rem;
                font-size: 0.85rem;
            }
        }
        
        /* Universal Mobile Fixes */
        @media (max-width: 991px) {
            .stColumns {
                gap: 0.5rem;
            }
            
            .stColumn {
                min-width: 0;
                flex: 1;
            }
            
            .stDataFrame {
                font-size: 0.85rem;
            }
            
            .stExpander {
                margin: 0.5rem 0;
            }
        }
        
        /* Touch-friendly improvements */
        @media (max-width: 767px) {
            .stButton > button {
                min-height: 44px;
                touch-action: manipulation;
            }
            
            .stTextInput > div > div > input {
                min-height: 44px;
            }
            
            .stSelectbox > div > div {
                min-height: 44px;
            }
        }
    """
    
    if st.session_state.theme_mode == 'dark':
        return base_css + """
            .stApp {
                background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%) !important;
                color: #ffffff !important;
            }
            
            .content-card {
                background: #1f2937 !important;
                border-color: #374151 !important;
                color: #ffffff !important;
            }
            
            .content-card h1, .content-card h2, .content-card h3, .content-card h4, .content-card h5, .content-card h6 {
                color: #ffffff !important;
            }
            
            .content-card p, .content-card div, .content-card span, .content-card li, .content-card strong {
                color: #ffffff !important;
            }
            
            .stMetric {
                background: #374151 !important;
                border-color: #4b5563 !important;
                color: #ffffff !important;
            }
            
            .stMetric > div, .stMetric > div > div, .stMetric label, .stMetric [data-testid="metric-container"] {
                color: #ffffff !important;
            }
            
            .stMetric [data-testid="metric-container"] > div {
                color: #ffffff !important;
            }
            
            .stMetric [data-testid="metric-container"] > div > div {
                color: #ffffff !important;
            }
            
            .stSelectbox > div > div {
                background-color: #374151 !important;
                color: #ffffff !important;
                border-color: #4b5563 !important;
            }
            
            .stTextInput > div > div > input {
                background-color: #374151 !important;
                color: #ffffff !important;
                border-color: #4b5563 !important;
            }
            
            .stTextArea > div > div > textarea {
                background-color: #374151 !important;
                color: #ffffff !important;
                border-color: #4b5563 !important;
            }
            
            .stMarkdown, .stMarkdown * {
                color: #ffffff !important;
            }
            
            .stText, .stText * {
                color: #ffffff !important;
            }
            
            .stInfo, .stSuccess, .stWarning, .stError {
                color: #ffffff !important;
            }
            
            .stInfo > div, .stSuccess > div, .stWarning > div, .stError > div {
                color: #ffffff !important;
            }
            
            [data-testid="stSidebar"] {
                background-color: #1f2937 !important;
                color: #ffffff !important;
            }
            
            [data-testid="stSidebar"] * {
                color: #ffffff !important;
            }
            
            .stExpander {
                background-color: #1f2937 !important;
                border-color: #374151 !important;
                color: #ffffff !important;
            }
            
            .stExpander > div, .stExpander * {
                color: #ffffff !important;
            }
            
            .stDataFrame {
                background-color: #1f2937 !important;
                color: #ffffff !important;
            }
            
            /* Fix step boxes in dark mode */
            div[style*="background: #f8fafc"] {
                background: #374151 !important;
                color: #ffffff !important;
            }
            
            div[style*="color: #64748b"] {
                color: #d1d5db !important;
            }
            
            /* Fix metric values and labels */
            [data-testid="metric-container"] * {
                color: #ffffff !important;
            }
            
            /* Fix metric label and value specifically */
            [data-testid="metric-container"] [data-testid="metric-label"] {
                color: #ffffff !important;
            }
            
            [data-testid="metric-container"] [data-testid="metric-value"] {
                color: #ffffff !important;
            }
            
            /* Override any remaining metric text */
            .metric-container, .metric-container * {
                color: #ffffff !important;
            }
            
            /* Fix dataframe text in dark mode */
            .stDataFrame table {
                background-color: #1f2937 !important;
                color: #ffffff !important;
            }
            
            .stDataFrame table th {
                background-color: #374151 !important;
                color: #ffffff !important;
            }
            
            .stDataFrame table td {
                background-color: #1f2937 !important;
                color: #ffffff !important;
            }
            
            /* Fix expander content */
            .stExpander [data-testid="stExpanderDetails"] {
                background-color: #1f2937 !important;
                color: #ffffff !important;
            }
            
            /* Fix text area in dark mode */
            .stTextArea textarea {
                background-color: #374151 !important;
                color: #ffffff !important;
                border-color: #4b5563 !important;
            }
            
            /* Fix code blocks */
            .stCode {
                background-color: #374151 !important;
                color: #ffffff !important;
            }
            
            /* Fix file uploader in dark mode */
            .stFileUploader {
                background-color: #374151 !important;
                border-color: #4b5563 !important;
            }
            
            .stFileUploader > div {
                background-color: #374151 !important;
                color: #ffffff !important;
            }
            
            .stFileUploader label {
                color: #ffffff !important;
            }
            
            .stFileUploader [data-testid="stFileUploaderDropzone"] {
                background-color: #374151 !important;
                border-color: #4b5563 !important;
                color: #ffffff !important;
            }
            
            .stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {
                color: #ffffff !important;
            }
            
            /* Fix form elements labels */
            .stFormSubmitButton, .stFormSubmitButton > button {
                background-color: #667eea !important;
                color: #ffffff !important;
            }
            
            /* Fix help text */
            .stHelp {
                color: #d1d5db !important;
            }
            
            /* Fix browse files button */
            .stFileUploader button {
                background-color: #667eea !important;
                color: #ffffff !important;
                border: none !important;
            }
            
            .stFileUploader button:hover {
                background-color: #5a6fd8 !important;
            }
            
            /* Fix file uploader text */
            .stFileUploader > div > div {
                color: #ffffff !important;
            }
            
            .stFileUploader small {
                color: #d1d5db !important;
            }
            
            /* Fix text input placeholder */
            .stTextInput input::placeholder {
                color: #9ca3af !important;
            }
            
            .stTextInput input {
                color: #ffffff !important;
            }
            
            /* Responsive adjustments for dark mode */
            @media (max-width: 991px) {
                .content-card {
                    background: #1f2937 !important;
                    color: #ffffff !important;
                }
                
                .stMetric {
                    background: #374151 !important;
                    color: #ffffff !important;
                }
                
                .stFileUploader {
                    background-color: #374151 !important;
                }
                
                .stTextInput > div > div > input {
                    background-color: #374151 !important;
                    color: #ffffff !important;
                }
            }
        </style>
        """
    else:
        return base_css + """
            .stApp {
                background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%) !important;
                color: #1a202c !important;
            }
            
            .content-card {
                background: #ffffff !important;
                color: #1a202c !important;
            }
            
            .content-card h1, .content-card h2, .content-card h3, .content-card h4, .content-card h5, .content-card h6 {
                color: #1a202c !important;
            }
            
            .content-card p, .content-card div, .content-card span, .content-card li, .content-card strong {
                color: #1a202c !important;
            }
            
            .stMetric {
                background: #ffffff !important;
                color: #1a202c !important;
            }
            
            .stMetric > div, .stMetric > div > div, .stMetric label {
                color: #1a202c !important;
            }
            
            .stSelectbox > div > div {
                background-color: #ffffff !important;
                color: #1a202c !important;
            }
            
            .stTextInput > div > div > input {
                background-color: #ffffff !important;
                color: #1a202c !important;
            }
            
            .stTextArea > div > div > textarea {
                background-color: #ffffff !important;
                color: #1a202c !important;
            }
            
            .stMarkdown, .stMarkdown * {
                color: #1a202c !important;
            }
            
            .stText, .stText * {
                color: #1a202c !important;
            }
            
            .stInfo, .stSuccess, .stWarning, .stError {
                color: #1a202c !important;
            }
            
            .stInfo > div, .stSuccess > div, .stWarning > div, .stError > div {
                color: #1a202c !important;
            }
            
            [data-testid="stSidebar"] {
                background-color: #ffffff !important;
                color: #1a202c !important;
            }
            
            [data-testid="stSidebar"] * {
                color: #1a202c !important;
            }
            
            .stExpander {
                background-color: #ffffff !important;
                color: #1a202c !important;
            }
            
            .stExpander > div, .stExpander * {
                color: #1a202c !important;
            }
            
            .stDataFrame {
                background-color: #ffffff !important;
                color: #1a202c !important;
            }
            
            /* Fix metric values and labels in light mode */
            [data-testid="metric-container"] * {
                color: #1a202c !important;
            }
            
            [data-testid="metric-container"] [data-testid="metric-label"] {
                color: #1a202c !important;
            }
            
            [data-testid="metric-container"] [data-testid="metric-value"] {
                color: #1a202c !important;
            }
            
            .metric-container, .metric-container * {
                color: #1a202c !important;
            }
            
            /* Fix dataframe text in light mode */
            .stDataFrame table {
                background-color: #ffffff !important;
                color: #1a202c !important;
            }
            
            .stDataFrame table th {
                background-color: #f8fafc !important;
                color: #1a202c !important;
            }
            
            .stDataFrame table td {
                background-color: #ffffff !important;
                color: #1a202c !important;
            }
            
            /* Fix expander content */
            .stExpander [data-testid="stExpanderDetails"] {
                background-color: #ffffff !important;
                color: #1a202c !important;
            }
            
            /* Fix text area in light mode */
            .stTextArea textarea {
                background-color: #ffffff !important;
                color: #1a202c !important;
                border-color: #d1d5db !important;
            }
            
            /* Fix code blocks */
            .stCode {
                background-color: #f8fafc !important;
                color: #1a202c !important;
            }
            
            /* Fix file uploader in light mode */
            .stFileUploader {
                background-color: #ffffff !important;
                border-color: #d1d5db !important;
            }
            
            .stFileUploader > div {
                background-color: #ffffff !important;
                color: #1a202c !important;
            }
            
            .stFileUploader label {
                color: #1a202c !important;
            }
            
            .stFileUploader [data-testid="stFileUploaderDropzone"] {
                background-color: #ffffff !important;
                border-color: #d1d5db !important;
                color: #1a202c !important;
            }
            
            .stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {
                color: #1a202c !important;
            }
            
            .stHelp {
                color: #64748b !important;
            }
            
            /* Fix browse files button in light mode */
            .stFileUploader button {
                background-color: #667eea !important;
                color: #ffffff !important;
                border: none !important;
            }
            
            .stFileUploader button:hover {
                background-color: #5a6fd8 !important;
            }
            
            .stFileUploader > div > div {
                color: #1a202c !important;
            }
            
            .stFileUploader small {
                color: #64748b !important;
            }
            
            /* Fix text input placeholder in light mode */
            .stTextInput input::placeholder {
                color: #6b7280 !important;
            }
            
            .stTextInput input {
                color: #1a202c !important;
            }
            
            /* Responsive adjustments for light mode */
            @media (max-width: 991px) {
                .content-card {
                    background: #ffffff !important;
                    color: #1a202c !important;
                }
                
                .stMetric {
                    background: #ffffff !important;
                    color: #1a202c !important;
                }
                
                .stFileUploader {
                    background-color: #ffffff !important;
                }
                
                .stTextInput > div > div > input {
                    background-color: #ffffff !important;
                    color: #1a202c !important;
                }
            }
        </style>
        """

def init_session_state():
    """Initialize session state variables"""
    defaults = {
        'chat_history': [],
        'doc_data': None,
        'processing_status': None,
        'theme_mode': 'light'
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    init_theme_mode()

def clear_temp_folder():
    """Clear temporary folders"""
    try:
        for folder in ["temp_images", "temp_plots"]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
            os.makedirs(folder, exist_ok=True)
    except Exception as e:
        st.error(f"❌ Error clearing temp folder: {e}")

def process_document_with_progress(file_bytes, filename):
    """Process document with progress indicator"""
    from parser import parse_document
    import llm_handler
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🏗️ Initializing ArixStructure...")
        clear_temp_folder()
        progress_bar.progress(20)
        
        status_text.text(f"📄 Parsing unstructured data from {filename}...")
        doc_data = parse_document(file_bytes, filename)
        progress_bar.progress(50)
        
        if doc_data is None:
            st.error(f"❌ Could not structure {filename}. Unsupported format or corrupted file.")
            return None
        
        if doc_data.get("image_files"):
            status_text.text("🖼️ Structuring image data with AI...")
            doc_data["image_descriptions"] = llm_handler.get_image_descriptions(doc_data["image_files"])
            progress_bar.progress(80)
        else:
            doc_data["image_descriptions"] = []
        
        status_text.text("✅ Data successfully structured!")
        progress_bar.progress(100)
        
        st.session_state.doc_data = doc_data
        st.session_state.last_uploaded_name = filename
        
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
        
        return doc_data
        
    except Exception as e:
        st.error(f"❌ Error structuring document: {e}")
        progress_bar.empty()
        status_text.empty()
        return None

def save_plot_as_image(fig, filename, format="png"):
    """Save plotly figure as image with optimized settings"""
    try:
        if not os.path.exists("temp_plots"):
            os.makedirs("temp_plots")
        
        # Optimize image settings based on format
        if format.lower() in ['png', 'jpg', 'jpeg']:
            width, height, scale = 1400, 900, 2
        elif format.lower() == 'svg':
            width, height, scale = 1200, 800, 1
        else:
            width, height, scale = 1200, 800, 2
        
        # Try kaleido first, fallback to HTML if not available
        try:
            img_bytes = fig.to_image(
                format=format, 
                width=width, 
                height=height, 
                scale=scale,
                engine="kaleido"
            )
        except Exception:
            # Fallback: save as HTML if kaleido not available
            if format.lower() == 'html' or format.lower() not in ['png', 'jpg', 'jpeg', 'svg']:
                filepath = f"temp_plots/{filename}.html"
                fig.write_html(filepath)
                with open(filepath, "rb") as f:
                    img_bytes = f.read()
                return img_bytes, filepath
            else:
                st.warning("⚠️ Kaleido not available. Install with: pip install kaleido")
                # Save as HTML instead
                filepath = f"temp_plots/{filename}.html"
                fig.write_html(filepath)
                with open(filepath, "rb") as f:
                    img_bytes = f.read()
                return img_bytes, filepath
        
        filepath = f"temp_plots/{filename}.{format}"
        with open(filepath, "wb") as f:
            f.write(img_bytes)
        
        return img_bytes, filepath
    except Exception as e:
        st.error(f"❌ Error saving plot: {str(e)[:100]}")
        return None, None

def create_comprehensive_export(table, table_name="table"):
    """Create multiple export formats for a table"""
    df = pd.DataFrame(table)
    exports = {}
    
    # CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    exports['csv'] = csv_buffer.getvalue().encode('utf-8')
    
    # JSON
    json_data = {
        "metadata": {
            "table_name": table_name,
            "rows": len(df),
            "columns": list(df.columns),
            "structured_at": datetime.now().isoformat(),
            "source": "ArixStructure"
        },
        "data": df.to_dict('records')
    }
    exports['json'] = json.dumps(json_data, indent=2).encode('utf-8')
    
    # Excel
    if openpyxl:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=table_name, index=False)
        excel_buffer.seek(0)
        exports['excel'] = excel_buffer.getvalue()
    
    # Text
    text_content = f"ArixStructure - Structured Data Export\nTable: {table_name}\n" + "="*50 + "\n\n"
    text_content += df.to_string(index=False)
    exports['txt'] = text_content.encode('utf-8')
    
    # PDF
    if reportlab_available:
        try:
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            story.append(Paragraph("ArixStructure - Structured Data Export", styles['Title']))
            story.append(Paragraph(f"Table: {table_name}", styles['Heading1']))
            story.append(Spacer(1, 12))
            
            table_text = df.to_string(index=False)
            story.append(Paragraph(table_text.replace('\n', '<br/>'), styles['Normal']))
            
            doc.build(story)
            pdf_buffer.seek(0)
            exports['pdf'] = pdf_buffer.getvalue()
        except:
            exports['pdf'] = None
    else:
        exports['pdf'] = None
    
    return exports