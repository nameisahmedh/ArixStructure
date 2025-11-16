import streamlit as st
import pandas as pd
import os
import urllib.parse
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import (
    get_theme_css, init_session_state,
    process_document_with_progress
)

st.set_page_config(
    page_title="📊 Dashboard - ArixStructure",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize and apply theme
init_session_state()
st.markdown(get_theme_css(), unsafe_allow_html=True)

# Theme toggle
with st.sidebar:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### ⚙️ Settings")
    with col2:
        if st.button("🌓", help="Toggle dark/light theme"):
            st.session_state.theme_mode = 'dark' if st.session_state.theme_mode == 'light' else 'light'
            st.rerun()

# Main header
st.markdown("""
<div class="main-header">
    <h1>📊 Dashboard</h1>
    <p>Upload and transform unstructured documents into structured data</p>
</div>
""", unsafe_allow_html=True)

# Navigation buttons in stable container
nav_container = st.container()
with nav_container:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("🏠 Home", use_container_width=True, key="dash_home"):
            st.switch_page("app.py")
    with col2:
        if st.button("🤖 AI Assistant", use_container_width=True, key="dash_ai"):
            st.switch_page("pages/02_🤖_AI_Assistant.py")
    with col3:
        if st.button("📈 Analytics", use_container_width=True, key="dash_analytics"):
            st.switch_page("pages/03_📈_Analytics.py")
    with col4:
        if st.button("🖼️ Images", use_container_width=True, key="dash_images"):
            st.switch_page("pages/04_🖼️_Images.py")
    with col5:
        if st.button("📝 Text Analysis", use_container_width=True, key="dash_text"):
            st.switch_page("pages/05_📝_Text_Analysis.py")

st.divider()

# Document upload section
with st.sidebar:
    st.markdown("### 🏗️ Structure Your Data")
    
    st.markdown("#### 📁 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose unstructured file",
        type=["pdf", "docx", "pptx", "txt", "html", "htm", "csv"],
        help="📋 Supported: PDF, Word, PowerPoint, Text, HTML, CSV"
    )
    
    if uploaded_file and st.session_state.get("last_uploaded_name") != uploaded_file.name:
        doc_data = process_document_with_progress(uploaded_file.getvalue(), uploaded_file.name)
        if doc_data:
            st.success(f"✅ Successfully structured '{uploaded_file.name}'")
            st.balloons()
            st.rerun()
    
    st.divider()
    
    st.markdown("#### 🌐 Fetch from Web")
    url_input = st.text_input("🔗 Enter webpage URL:", placeholder="https://example.com/document")
    
    if st.button("🚀 Fetch & Structure", use_container_width=True):
        if url_input.strip():
            url = url_input.strip()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # URL validation
            from urllib.parse import urlparse
            parsed = urlparse(url)
            if not parsed.netloc or parsed.scheme not in ['http', 'https']:
                st.error("❌ Invalid URL format")
            elif parsed.netloc in ['localhost', '127.0.0.1'] or parsed.netloc.startswith('192.168.') or parsed.netloc.startswith('10.'):
                st.error("❌ Local/private URLs not allowed for security")
            else:
                try:
                    with st.spinner(f"🔄 Fetching and structuring content..."):
                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                        response = requests.get(url, headers=headers, timeout=10, allow_redirects=False)
                        response.raise_for_status()
                        
                        # Check content size
                        if len(response.content) > 10 * 1024 * 1024:  # 10MB limit
                            st.error("❌ Content too large (max 10MB)")
                        else:
                            filename = os.path.basename(urllib.parse.urlparse(url).path) or "webpage.html"
                            doc_data = process_document_with_progress(response.content, filename)
                            
                            if doc_data:
                                st.success("✅ Successfully structured web content")
                                st.balloons()
                                st.rerun()
                        
                except requests.RequestException as e:
                    st.error(f"❌ Network error: {str(e)[:100]}")
                except Exception as e:
                    st.error(f"❌ Error processing URL: {str(e)[:100]}")
        else:
            st.warning("⚠️ Please enter a valid URL")

# Main content
if st.session_state.doc_data:
    # Success message
    st.success("🏗️ **Data Successfully Structured!** Your unstructured document has been transformed into organized, queryable data.")
    
    # Document Overview
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Structured Data Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        doc_name = st.session_state.get("last_uploaded_name", "Unknown")
        display_name = doc_name[:15] + "..." if len(doc_name) > 15 else doc_name
        st.metric("📄 Source Document", display_name, help="Original unstructured document")
    
    with col2:
        tables_count = len(st.session_state.doc_data.get('tables', []))
        st.metric("📊 Structured Tables", tables_count, help="Tables extracted and structured")
    
    with col3:
        images_count = len(st.session_state.doc_data.get('image_files', []))
        st.metric("🖼️ Images Processed", images_count, help="Images extracted and analyzed")
    
    with col4:
        text_length = len(st.session_state.doc_data.get('full_text', ''))
        st.metric("📝 Text Characters", f"{text_length:,}", help="Total text content structured")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("### 🎯 What Would You Like to Do Next?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🤖 Ask AI About Your Data", use_container_width=True, help="Get intelligent insights about your structured data", type="primary"):
            st.switch_page("pages/02_🤖_AI_Assistant.py")
        
        if st.button("📈 Create Visualizations", use_container_width=True, help="Generate charts and graphs from your structured data"):
            st.switch_page("pages/03_📈_Analytics.py")
    
    with col2:
        if st.button("🖼️ Explore Images", use_container_width=True, help="View and analyze extracted images"):
            st.switch_page("pages/04_🖼️_Images.py")
        
        if st.button("📝 Analyze Text Content", use_container_width=True, help="Deep dive into text analytics"):
            st.switch_page("pages/05_📝_Text_Analysis.py")
    
    # Data Preview
    st.markdown("### 📋 Structured Data Preview")
    
    # Tables preview
    tables = st.session_state.doc_data.get('tables', [])
    if tables:
        st.markdown("#### 📊 Extracted Tables")
        
        for i, table in enumerate(tables[:2]):  # Show first 2 tables
            with st.expander(f"📊 Table {i+1} ({len(table)} rows × {len(table[0]) if table else 0} columns)", expanded=i==0):
                df = pd.DataFrame(table)
                st.dataframe(df.head(5), use_container_width=True)
                
                if len(df) > 5:
                    st.info(f"Showing first 5 rows of {len(df)} total rows")
        
        if len(tables) > 2:
            st.info(f"📊 {len(tables) - 2} more tables available. Go to Analytics to explore all tables.")
    
    # Text preview
    text_content = st.session_state.doc_data.get('full_text', '')
    if text_content:
        st.markdown("#### 📝 Text Content Preview")
        
        with st.expander("📄 View Text Content", expanded=False):
            preview_text = text_content[:1000] + "..." if len(text_content) > 1000 else text_content
            st.text_area("Extracted Text", preview_text, height=200, disabled=True)
            
            if len(text_content) > 1000:
                st.info(f"Showing first 1000 characters of {len(text_content):,} total characters")
    
    # Images preview
    images = st.session_state.doc_data.get('image_files', [])
    if images:
        st.markdown("#### 🖼️ Extracted Images")
        
        cols = st.columns(min(3, len(images)))
        for i, img_path in enumerate(images[:3]):
            with cols[i]:
                try:
                    st.image(img_path, caption=f"Image {i+1}", use_column_width=True)
                except:
                    st.error(f"❌ Could not load image {i+1}")
        
        if len(images) > 3:
            st.info(f"🖼️ {len(images) - 3} more images available. Go to Images section to view all.")

else:
    # Welcome screen
    st.markdown("### 🏗️ Welcome to ArixStructure Dashboard!")
    st.write("Transform your unstructured documents into organized, queryable structured data")
    
    # Process steps
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("#### 1. 📥 Upload")
        st.write("Upload your unstructured document (PDF, Word, PowerPoint, etc.)")
    
    with col2:
        st.markdown("#### 2. 🧠 AI Analysis")
        st.write("Our AI extracts and analyzes all content intelligently")
    
    with col3:
        st.markdown("#### 3. 🏗️ Structure")
        st.write("Convert raw data into organized, queryable formats")
    
    with col4:
        st.markdown("#### 4. 📊 Analyze")
        st.write("Query, visualize, and export your structured data")
    
    st.info("💡 **Get Started:** Use the file uploader in the sidebar to upload your first document!")
    
    # Supported formats
    st.markdown("### 📋 Supported File Formats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📄 Documents**")
        st.write("• PDF files (.pdf)")
        st.write("• Word documents (.docx)")
        st.write("• PowerPoint presentations (.pptx)")
    
    with col2:
        st.markdown("**🌐 Web Content**")
        st.write("• HTML pages (.html, .htm)")
        st.write("• Web URLs (live fetching)")
        st.write("• Online documents")
    
    with col3:
        st.markdown("**📊 Data Files**")
        st.write("• CSV files (.csv)")
        st.write("• Text files (.txt)")
        st.write("• Structured data formats")