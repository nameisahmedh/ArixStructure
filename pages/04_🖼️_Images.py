import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_theme_css, init_session_state
import os

st.set_page_config(
    page_title="🖼️ Images - ArixStructure",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_session_state()
st.markdown(get_theme_css(), unsafe_allow_html=True)

with st.sidebar:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### ⚙️ Settings")
    with col2:
        if st.button("🌓", help="Toggle dark/light theme"):
            st.session_state.theme_mode = 'dark' if st.session_state.theme_mode == 'light' else 'light'
            st.rerun()

st.markdown("""
<div class="main-header">
    <h1>🖼️ Image Analysis & Gallery</h1>
    <p>🔍 Explore and analyze extracted images with AI descriptions</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/01_📊_Dashboard.py")
with col3:
    if st.button("🤖 AI Assistant", use_container_width=True):
        st.switch_page("pages/02_🤖_AI_Assistant.py")
with col4:
    if st.button("📈 Analytics", use_container_width=True):
        st.switch_page("pages/03_📈_Analytics.py")
with col5:
    if st.button("📝 Text Analysis", use_container_width=True):
        st.switch_page("pages/05_📝_Text_Analysis.py")

st.divider()


if st.session_state.doc_data:
    images = st.session_state.doc_data.get('image_files', [])
    descriptions = st.session_state.doc_data.get('image_descriptions', [])
    
    if not images:
        st.info("🖼️ No images found in the document")
    else:
        st.markdown("### 📊 Image Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🖼️ Total Images", len(images))
        
        with col2:
            described_count = len([d for d in descriptions if d.get('description')])
            st.metric("🤖 AI Described", described_count)
        
        with col3:
            total_size = 0
            for img_path in images:
                try:
                    total_size += os.path.getsize(img_path)
                except:
                    pass
            st.metric("💾 Total Size", f"{total_size / 1024:.1f} KB")
        
        st.divider()
        
        st.markdown("### 🖼️ Image Gallery")
        
        cols = st.columns(min(3, len(images)))
        
        for i, img_path in enumerate(images):
            col_idx = i % len(cols)
            
            with cols[col_idx]:
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                
                try:
                    st.image(img_path, caption=f"Image {i+1}", use_column_width=True)
                except Exception as e:
                    st.error(f"❌ Error loading image {i+1}: {e}")
                
                if i < len(descriptions) and descriptions[i].get('description'):
                    st.markdown(f"**🤖 AI Description:** {descriptions[i]['description'][:100]}...")
                
                try:
                    with open(img_path, "rb") as f:
                        img_bytes = f.read()
                    st.download_button(
                        f"📥 Download",
                        data=img_bytes,
                        file_name=f"image_{i+1}.png",
                        mime="image/png",
                        key=f"download_{i}"
                    )
                except:
                    st.button("❌ Download Error", disabled=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("### 🖼️ Image Gallery Ready!")
    st.write("Ready to explore and analyze images from your documents!")
    
    st.markdown("#### ✨ What You Can Do:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🖼️ Image Analysis**")
        st.write("View and analyze images extracted from your documents with AI-powered descriptions.")
        
        st.markdown("**💾 Download Options**")
        st.write("Download individual images or get comprehensive analysis reports.")
    
    with col2:
        st.markdown("**🤖 AI Descriptions**")
        st.write("Get intelligent descriptions and insights about the visual content in your documents.")
        
        st.markdown("**📈 Visual Insights**")
        st.write("Understand the context and meaning of images within your document structure.")
    
    st.info("📄 **Upload a Document First** - Go to the Dashboard to upload a document containing images, then return here to start exploring!")