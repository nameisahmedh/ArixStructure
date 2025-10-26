import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sys
sys.path.append('..')
from utils import (
    get_theme_css, init_session_state,
    create_comprehensive_export, save_plot_as_image
)

st.set_page_config(
    page_title="📈 Analytics - ArixStructure",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize and apply theme
init_session_state()
st.markdown(get_theme_css(), unsafe_allow_html=True)

# Sidebar
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
    <h1>📈 Data Analytics & Visualizations</h1>
    <p>Transform your structured data into beautiful, insightful visualizations</p>
</div>
""", unsafe_allow_html=True)

# Navigation buttons
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
    if st.button("🖼️ Images", use_container_width=True):
        st.switch_page("pages/04_🖼️_Images.py")
with col5:
    if st.button("📝 Text Analysis", use_container_width=True):
        st.switch_page("pages/05_📝_Text_Analysis.py")

st.divider()

def create_proper_visualization(df, chart_type, x_col, y_col=None, color_col=None, title="Chart"):
    """Create visualization with proper axis handling and data validation"""
    try:
        # Data validation
        if df.empty:
            st.error("❌ No data available for visualization")
            return None
            
        # Clean data
        df_clean = df.copy()
        
        # Handle missing values
        if x_col in df_clean.columns:
            df_clean = df_clean.dropna(subset=[x_col])
        if y_col and y_col in df_clean.columns:
            df_clean = df_clean.dropna(subset=[y_col])
            
        if df_clean.empty:
            st.error("❌ No valid data after cleaning")
            return None
        
        # Set theme
        template = "plotly_dark" if st.session_state.theme_mode == 'dark' else "plotly_white"
        
        # Helper function to format axis titles
        def format_title(col):
            return str(col).replace('_', ' ').title()
        
        # Create visualizations with proper axis handling
        if chart_type == "Bar Chart":
            if y_col and y_col in df_clean.columns:
                # Ensure y_col is numeric
                if not pd.api.types.is_numeric_dtype(df_clean[y_col]):
                    try:
                        df_clean[y_col] = pd.to_numeric(df_clean[y_col], errors='coerce')
                        df_clean = df_clean.dropna(subset=[y_col])
                    except:
                        st.error(f"❌ Cannot convert {y_col} to numeric values")
                        return None
                
                fig = px.bar(df_clean, x=x_col, y=y_col, color=color_col, title=title)
                fig.update_xaxes(title=format_title(x_col))
                fig.update_yaxes(title=format_title(y_col))
            else:
                # Count plot
                value_counts = df_clean[x_col].value_counts().head(20)
                fig = px.bar(x=value_counts.index, y=value_counts.values, title=f"{title} - Distribution")
                fig.update_xaxes(title=format_title(x_col))
                fig.update_yaxes(title="Count")
                
        elif chart_type == "Line Chart":
            if y_col and y_col in df_clean.columns:
                if not pd.api.types.is_numeric_dtype(df_clean[y_col]):
                    try:
                        df_clean[y_col] = pd.to_numeric(df_clean[y_col], errors='coerce')
                        df_clean = df_clean.dropna(subset=[y_col])
                    except:
                        st.error(f"❌ Cannot convert {y_col} to numeric values")
                        return None
                
                df_clean = df_clean.sort_values(x_col)
                fig = px.line(df_clean, x=x_col, y=y_col, color=color_col, title=title)
                fig.update_xaxes(title=format_title(x_col))
                fig.update_yaxes(title=format_title(y_col))
            else:
                st.error("❌ Line chart requires both X and Y columns")
                return None
                
        elif chart_type == "Scatter Plot":
            if y_col and y_col in df_clean.columns:
                for col in [x_col, y_col]:
                    if not pd.api.types.is_numeric_dtype(df_clean[col]):
                        try:
                            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                        except:
                            st.error(f"❌ Cannot convert {col} to numeric values")
                            return None
                
                df_clean = df_clean.dropna(subset=[x_col, y_col])
                fig = px.scatter(df_clean, x=x_col, y=y_col, color=color_col, title=title)
                fig.update_xaxes(title=format_title(x_col))
                fig.update_yaxes(title=format_title(y_col))
            else:
                st.error("❌ Scatter plot requires both X and Y columns")
                return None
                
        elif chart_type == "Pie Chart":
            if y_col and y_col in df_clean.columns:
                if not pd.api.types.is_numeric_dtype(df_clean[y_col]):
                    try:
                        df_clean[y_col] = pd.to_numeric(df_clean[y_col], errors='coerce')
                        df_clean = df_clean.dropna(subset=[y_col])
                    except:
                        st.error(f"❌ Cannot convert {y_col} to numeric values")
                        return None
                
                pie_data = df_clean.groupby(x_col)[y_col].sum().head(10)
                fig = px.pie(values=pie_data.values, names=pie_data.index, title=title)
            else:
                value_counts = df_clean[x_col].value_counts().head(10)
                fig = px.pie(values=value_counts.values, names=value_counts.index, title=f"{title} - Distribution")
                
        elif chart_type == "Histogram":
            if not pd.api.types.is_numeric_dtype(df_clean[x_col]):
                try:
                    df_clean[x_col] = pd.to_numeric(df_clean[x_col], errors='coerce')
                    df_clean = df_clean.dropna(subset=[x_col])
                except:
                    st.error(f"❌ Cannot create histogram: {x_col} is not numeric")
                    return None
            
            fig = px.histogram(df_clean, x=x_col, title=title, nbins=30)
            fig.update_xaxes(title=format_title(x_col))
            fig.update_yaxes(title="Frequency")
            
        elif chart_type == "Box Plot":
            if y_col and y_col in df_clean.columns:
                if not pd.api.types.is_numeric_dtype(df_clean[y_col]):
                    try:
                        df_clean[y_col] = pd.to_numeric(df_clean[y_col], errors='coerce')
                        df_clean = df_clean.dropna(subset=[y_col])
                    except:
                        st.error(f"❌ Cannot convert {y_col} to numeric values")
                        return None
                
                fig = px.box(df_clean, x=x_col, y=y_col, title=title)
                fig.update_xaxes(title=format_title(x_col))
                fig.update_yaxes(title=format_title(y_col))
            else:
                if not pd.api.types.is_numeric_dtype(df_clean[x_col]):
                    try:
                        df_clean[x_col] = pd.to_numeric(df_clean[x_col], errors='coerce')
                        df_clean = df_clean.dropna(subset=[x_col])
                    except:
                        st.error(f"❌ Cannot create box plot: {x_col} is not numeric")
                        return None
                
                fig = px.box(df_clean, y=x_col, title=title)
                fig.update_yaxes(title=format_title(x_col))
        
        else:
            st.error("❌ Unsupported chart type")
            return None
        
        # Apply theme and styling
        fig.update_layout(
            template=template,
            title_font_size=16,
            title_x=0.5,
            showlegend=True if color_col else False,
            height=500,
            margin=dict(l=50, r=50, t=80, b=50),
            font=dict(family="Poppins, sans-serif")
        )
        
        return fig
        
    except Exception as e:
        st.error(f"❌ Error creating visualization: {str(e)}")
        return None

# Sidebar for settings
with st.sidebar:
    st.markdown("### 🎨 Visualization Settings")
    
    export_format = st.selectbox("📥 Export Format", ["PNG", "JPG", "SVG", "PDF", "HTML"])
    chart_width = st.slider("📏 Chart Width", 600, 1400, 1000)
    chart_height = st.slider("📐 Chart Height", 400, 1000, 600)

# Main content
if st.session_state.doc_data:
    tables = st.session_state.doc_data.get('tables', [])
    
    if not tables:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.info("📊 No tables found in the document for analysis")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Table selector
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Select Data for Analysis")
        
        selected_idx = st.selectbox(
            "Choose table:",
            options=list(range(len(tables))),
            format_func=lambda x: f"Table {x+1} ({len(tables[x])} rows × {len(tables[x][0]) if tables[x] else 0} columns)"
        )
        
        table = tables[selected_idx]
        df = pd.DataFrame(table)
        
        # Data preview
        with st.expander("📋 Data Preview", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)
        
        # Data info
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Rows", len(df))
        with col2:
            st.metric("📋 Columns", len(df.columns))
        with col3:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            st.metric("🔢 Numeric Columns", len(numeric_cols))
        with col4:
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            st.metric("📝 Text Columns", len(categorical_cols))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Visualization builder
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🎨 Create Visualization")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Chart configuration
            col_a, col_b = st.columns(2)
            
            with col_a:
                chart_type = st.selectbox(
                    "📊 Chart Type", 
                    ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram", "Box Plot"]
                )
            
            with col_b:
                x_column = st.selectbox("📐 X-Axis Column", df.columns.tolist())
            
            # Y-axis selection based on chart type
            if chart_type in ["Line Chart", "Scatter Plot", "Box Plot"]:
                y_column = st.selectbox("📏 Y-Axis Column", [None] + df.columns.tolist())
            elif chart_type in ["Bar Chart", "Pie Chart"]:
                y_column = st.selectbox("📏 Y-Axis Column (Optional)", [None] + df.columns.tolist())
            else:
                y_column = None
            
            # Color column (optional)
            color_column = st.selectbox("🎨 Color By (Optional)", [None] + df.columns.tolist())
            
            # Chart title
            chart_title = st.text_input("📝 Chart Title", f"{chart_type}: {x_column} Analysis")
        
        with col2:
            st.markdown("#### 💡 Chart Guidelines")
            
            guidelines = {
                "Bar Chart": "📊 Best for comparing categories. Y-axis optional for count plots.",
                "Line Chart": "📈 Best for trends over time. Requires numeric Y-axis.",
                "Scatter Plot": "🔵 Best for correlations. Requires numeric X and Y axes.",
                "Pie Chart": "🥧 Best for proportions. Y-axis optional for count plots.",
                "Histogram": "📊 Best for distributions. Requires numeric X-axis.",
                "Box Plot": "📦 Best for outliers and quartiles. Y-axis optional."
            }
            
            st.info(guidelines.get(chart_type, "Select a chart type for guidelines"))
        
        # Generate chart
        if st.button("🎨 Generate Visualization", use_container_width=True, type="primary"):
            with st.spinner("🎨 Creating visualization..."):
                fig = create_proper_visualization(
                    df, chart_type, x_column, y_column, 
                    color_column if color_column != "None" else None, 
                    chart_title
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Export options
                    st.markdown("#### 📥 Export Options")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        img_bytes, filepath = save_plot_as_image(fig, f"chart_{selected_idx+1}", export_format.lower())
                        if img_bytes:
                            st.download_button(
                                f"📥 Download {export_format}",
                                data=img_bytes,
                                file_name=f"chart_{selected_idx+1}.{export_format.lower()}",
                                mime=f"image/{export_format.lower()}"
                            )
                    
                    with col2:
                        html_str = fig.to_html(include_plotlyjs='cdn')
                        st.download_button(
                            "🌐 Download HTML",
                            data=html_str,
                            file_name=f"chart_{selected_idx+1}.html",
                            mime="text/html"
                        )
                    
                    with col3:
                        json_str = fig.to_json()
                        st.download_button(
                            "📄 Download JSON",
                            data=json_str,
                            file_name=f"chart_{selected_idx+1}.json",
                            mime="application/json"
                        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Data export
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 💾 Export Structured Data")
        
        exports = create_comprehensive_export(table, f"table_{selected_idx+1}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.download_button("📊 CSV", data=exports['csv'], file_name=f"table_{selected_idx+1}.csv", mime="text/csv")
        with col2:
            st.download_button("📄 JSON", data=exports['json'], file_name=f"table_{selected_idx+1}.json", mime="application/json")
        with col3:
            if exports.get('excel'):
                st.download_button("📈 Excel", data=exports['excel'], file_name=f"table_{selected_idx+1}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with col4:
            st.download_button("📝 Text", data=exports['txt'], file_name=f"table_{selected_idx+1}.txt", mime="text/plain")
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # No document loaded
    st.markdown("### 📈 Analytics Dashboard Ready!")
    st.write("Upload a document with structured data to create beautiful visualizations")
    
    st.markdown("#### ✨ What You Can Create:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📊 Charts & Graphs**")
        st.write("• Bar charts for comparisons")
        st.write("• Line charts for trends")
        st.write("• Pie charts for proportions")
    
    with col2:
        st.markdown("**📈 Advanced Analytics**")
        st.write("• Scatter plots for correlations")
        st.write("• Histograms for distributions")
        st.write("• Box plots for outliers")
    
    with col3:
        st.markdown("**📥 Export Options**")
        st.write("• High-quality PNG/JPG images")
        st.write("• Interactive HTML charts")
        st.write("• Data in CSV/JSON/Excel")
    
    st.info("📄 **Upload a Document First** - Go to the Dashboard to upload a document containing tables or data, then return here to create amazing visualizations!")
    st.markdown('</div>', unsafe_allow_html=True)