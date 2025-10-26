import streamlit as st
from utils import get_theme_css, init_session_state

st.set_page_config(
    page_title="ArixStructure - Transform Unstructured Data",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    <h1>🏗️ ArixStructure</h1>
    <p>Transform Unstructured Data into Structured Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Navigation buttons
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/01_📊_Dashboard.py")
with col2:
    if st.button("🤖 AI Assistant", use_container_width=True):
        st.switch_page("pages/02_🤖_AI_Assistant.py")
with col3:
    if st.button("📈 Analytics", use_container_width=True):
        st.switch_page("pages/03_📈_Analytics.py")
with col4:
    if st.button("🖼️ Images", use_container_width=True):
        st.switch_page("pages/04_🖼️_Images.py")
with col5:
    if st.button("📝 Text Analysis", use_container_width=True):
        st.switch_page("pages/05_📝_Text_Analysis.py")

st.divider()

# Hero metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("⚡ Time Saved", "80%", help="Reduce manual data processing time")
with col2:
    st.metric("🚀 Processing Speed", "5x Faster", help="Faster than manual document analysis")
with col3:
    st.metric("📋 Supported Formats", "6+", help="PDF, DOCX, PPTX, HTML, CSV, TXT")
with col4:
    st.metric("🎯 Chart Types", "10+", help="Multiple visualization options available")

st.divider()

# Main content
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 🚀 Key Features")
    
    st.markdown("#### 🤖 AI-Powered Extraction")
    st.write("Advanced AI algorithms automatically detect and extract text, tables, images, and metadata from any document format with high precision.")
    
    st.markdown("#### 🏗️ Smart Data Structuring")
    st.write("Convert unorganized, chaotic data into clean, structured formats like JSON, CSV, Excel with intelligent schema detection.")
    
    st.markdown("#### 📊 Interactive Data Analytics")
    st.write("Generate beautiful, interactive visualizations and perform deep statistical analysis on your newly structured data.")
    
    st.markdown("#### 💬 Natural Language Queries")
    st.write("Ask questions about your data in plain English and get intelligent, contextual responses powered by advanced AI.")
    
    st.markdown("#### 📥 Multi-Format Export")
    st.write("Export your structured data and visualizations in multiple formats: CSV, JSON, Excel, PDF, PNG, and more.")

with col2:
    st.markdown("### 🎯 How It Works")
    
    # Process steps
    steps = [
        ("📤", "Upload", "Upload your unstructured document"),
        ("🧠", "Analyze", "AI analyzes and extracts content"),
        ("🏗️", "Structure", "Convert to organized data formats"),
        ("📊", "Visualize", "Create charts and insights"),
        ("📥", "Export", "Download in preferred formats")
    ]
    
    for i, (icon, title, desc) in enumerate(steps, 1):
        bg_color = "#374151" if st.session_state.theme_mode == 'dark' else "#f8fafc"
        text_color = "#ffffff" if st.session_state.theme_mode == 'dark' else "#1a202c"
        desc_color = "#d1d5db" if st.session_state.theme_mode == 'dark' else "#64748b"
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 1rem 0; padding: 1rem; background: {bg_color}; border-radius: 10px; border-left: 4px solid #667eea; color: {text_color};">
            <div style="font-size: 1.5rem; margin-right: 1rem; width: 40px; color: {text_color};">{icon}</div>
            <div>
                <strong style="color: {text_color};">{i}. {title}</strong><br>
                <small style="color: {desc_color};">{desc}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Current document status
if st.session_state.get('doc_data'):
    st.markdown("### 📊 Current Document Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        doc_name = st.session_state.get("last_uploaded_name", "Unknown")
        display_name = doc_name[:20] + "..." if len(doc_name) > 20 else doc_name
        st.metric("📄 Document", display_name)
    
    with col2:
        tables_count = len(st.session_state.doc_data.get('tables', []))
        st.metric("📊 Tables", tables_count)
    
    with col3:
        images_count = len(st.session_state.doc_data.get('image_files', []))
        st.metric("🖼️ Images", images_count)
    
    with col4:
        text_length = len(st.session_state.doc_data.get('full_text', ''))
        st.metric("📝 Characters", f"{text_length:,}")
    
    st.success("✅ **Document Successfully Structured!** Your data is ready for analysis. Use the navigation buttons above to explore different features.")

else:
    # Getting started section
    st.markdown("### 🚀 Ready to Get Started?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📤 Step 1: Upload")
        st.write("Click **📊 Dashboard** to upload your unstructured document (PDF, Word, PowerPoint, etc.)")
        
    with col2:
        st.markdown("#### 🏗️ Step 2: Structure")
        st.write("Watch as ArixStructure automatically transforms your data into organized, queryable formats")
        
    with col3:
        st.markdown("#### 📊 Step 3: Analyze")
        st.write("Use AI Assistant, Analytics, and other tools to gain insights from your structured data")
    
    st.info("💡 **Pro Tip:** Start by clicking **📊 Dashboard** to upload your first document and experience the power of ArixStructure!")

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

# Footer
st.markdown("---")
st.markdown("**🏗️ ArixStructure** - Transforming Unstructured Data into Structured Intelligence")
st.caption("Built with ❤️ by Ahmed Batch20 • Powered by AI • Designed for Efficiency")