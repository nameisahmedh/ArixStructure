import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_theme_css, init_session_state

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
    metadata = st.session_state.doc_data.get('metadata', {})
    
    # Filter valid images
    valid_images = []
    for img_path in images:
        if os.path.exists(img_path) and os.path.getsize(img_path) > 0:
            valid_images.append(img_path)
    
    if not valid_images:
        st.info("🖼️ No images found in the document")
        
        # Show extraction info
        if metadata.get('extraction_method'):
            st.markdown(f"**📄 Document Type:** {metadata.get('extraction_method', 'Unknown')}")
            
        if 'images_found' in metadata:
            st.markdown(f"**🔍 Images Detected:** {metadata.get('images_found', 0)}")
            if metadata.get('images_found', 0) > 0:
                st.warning("⚠️ Images were detected but could not be processed. This may be due to unsupported image formats or corrupted image data.")
    else:
        st.markdown("### 📊 Image Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🖼️ Total Images", len(valid_images))
        
        with col2:
            described_count = len([d for d in descriptions if d and d.get('description')])
            st.metric("🤖 AI Described", described_count)
        
        with col3:
            total_size = 0
            for img_path in valid_images:
                try:
                    total_size += os.path.getsize(img_path)
                except (OSError, FileNotFoundError):
                    pass  # Skip files that can't be accessed
            st.metric("💾 Total Size", f"{total_size / 1024:.1f} KB")
        
        with col4:
            doc_type = metadata.get('extraction_method', 'Unknown').replace('python-', '').upper()
            st.metric("📄 Source Type", doc_type)
        
        st.divider()
        
        # Image filtering options
        st.markdown("### 🔍 Filter & Sort Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sort_option = st.selectbox(
                "📊 Sort by:",
                ["Original Order", "File Size", "Alphabetical"],
                key="sort_images"
            )
        
        with col2:
            show_descriptions = st.checkbox("🤖 Show AI Descriptions", value=True)
        
        with col3:
            images_per_row = st.selectbox("🖼️ Images per row:", [2, 3, 4], index=1)
        
        # Sort images based on selection
        sorted_images = valid_images.copy()
        if sort_option == "File Size":
            sorted_images.sort(key=lambda x: os.path.getsize(x) if os.path.exists(x) else 0, reverse=True)
        elif sort_option == "Alphabetical":
            sorted_images.sort(key=lambda x: os.path.basename(x))
        
        st.divider()
        st.markdown("### 🖼️ Image Gallery")
        
        # Display images in grid
        for i in range(0, len(sorted_images), images_per_row):
            cols = st.columns(images_per_row)
            
            for j in range(images_per_row):
                if i + j < len(sorted_images):
                    img_path = sorted_images[i + j]
                    img_index = valid_images.index(img_path)  # Get original index for descriptions
                    
                    with cols[j]:
                        st.markdown('<div class="content-card">', unsafe_allow_html=True)
                        
                        try:
                            # Get image info
                            img_size = os.path.getsize(img_path)
                            img_name = os.path.basename(img_path)
                            
                            st.image(img_path, caption=f"{img_name} ({img_size/1024:.1f} KB)", use_column_width=True)
                            
                            # Show AI description if available and enabled
                            if show_descriptions and img_index < len(descriptions) and descriptions[img_index] and descriptions[img_index].get('description'):
                                description = descriptions[img_index]['description']
                                if len(description) > 150:
                                    description = description[:150] + "..."
                                st.markdown(f"**🤖 AI Description:** {description}")
                            
                            # Download button
                            try:
                                with open(img_path, "rb") as f:
                                    img_bytes = f.read()
                                
                                # Determine file extension
                                _, ext = os.path.splitext(img_path)
                                if not ext:
                                    ext = '.png'
                                
                                st.download_button(
                                    f"📥 Download",
                                    data=img_bytes,
                                    file_name=f"image_{img_index+1}{ext}",
                                    mime=f"image/{ext[1:]}",
                                    key=f"download_{i}_{j}",
                                    use_container_width=True
                                )
                            except (OSError, FileNotFoundError) as e:
                                st.error(f"❌ Download error: {str(e)[:50]}")
                            
                        except (OSError, FileNotFoundError, IOError) as e:
                            st.error(f"❌ Error loading image: {str(e)[:100]}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
        
        # Bulk download option
        if len(valid_images) > 1:
            st.divider()
            st.markdown("### 📦 Bulk Download")
            
            if st.button("📥 Download All Images as ZIP", use_container_width=True):
                try:
                    import zipfile
                    import tempfile
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                        with zipfile.ZipFile(tmp_file.name, 'w') as zip_file:
                            for i, img_path in enumerate(valid_images):
                                if os.path.exists(img_path):
                                    _, ext = os.path.splitext(img_path)
                                    if not ext:
                                        ext = '.png'
                                    zip_file.write(img_path, f"image_{i+1}{ext}")
                        
                        with open(tmp_file.name, 'rb') as f:
                            zip_data = f.read()
                        
                        st.download_button(
                            "📥 Download ZIP File",
                            data=zip_data,
                            file_name="extracted_images.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                        
                        try:
                            os.unlink(tmp_file.name)
                        except OSError:
                            pass  # File already deleted
                        
                except (OSError, zipfile.BadZipFile, IOError) as e:
                    st.error(f"❌ Error creating ZIP file: {str(e)[:100]}")

else:
    st.markdown("### 🖼️ Image Gallery Ready!")
    st.write("Ready to explore and analyze images from your documents!")
    
    st.markdown("#### ✨ What You Can Do:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🖼️ Advanced Image Extraction**")
        st.write("Extract images from PDF, DOCX, PPTX, and HTML files with intelligent filtering and validation.")
        
        st.markdown("**💾 Multiple Download Options**")
        st.write("Download individual images or bulk download all images as a ZIP file.")
        
        st.markdown("**🔍 Smart Filtering**")
        st.write("Sort and filter images by size, type, or alphabetical order for better organization.")
    
    with col2:
        st.markdown("**🤖 AI-Powered Descriptions**")
        st.write("Get intelligent descriptions and insights about the visual content in your documents.")
        
        st.markdown("**📊 Image Analytics**")
        st.write("View detailed information about image sizes, formats, and extraction metadata.")
        
        st.markdown("**🎨 Gallery View**")
        st.write("Customizable gallery layout with responsive design for optimal viewing experience.")
    
    st.markdown("#### 📋 Supported Image Sources:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📄 PDF Documents**")
        st.write("• Embedded images")
        st.write("• Scanned content")
        st.write("• Vector graphics")
    
    with col2:
        st.markdown("**📃 Office Documents**")
        st.write("• DOCX images")
        st.write("• PPTX slides")
        st.write("• Embedded media")
    
    with col3:
        st.markdown("**🌐 Web Content**")
        st.write("• HTML images")
        st.write("• Base64 encoded")
        st.write("• Inline graphics")
    
    st.info("📄 **Upload a Document First** - Go to the Dashboard to upload a document containing images, then return here to start exploring!")