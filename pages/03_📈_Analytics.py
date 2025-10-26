import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

def create_simple_visualization(df, chart_type, x_col, y_col=None, color_col=None, title="Chart"):
    """Create visualization with proper axis handling and data validation"""
    try:
        # Data validation
        if df.empty:
            st.error("❌ No data available for visualization")
            return None, None
            
        # Clean data
        df_clean = df.copy()
        
        # Set theme
        template = "plotly_dark" if st.session_state.theme_mode == 'dark' else "plotly_white"
        
        # Helper function to format axis titles
        def format_title(col):
            return str(col).replace('_', ' ').title()
        
        # Create visualizations with proper axis handling
        if chart_type == "Bar Chart":
            if y_col and y_col in df_clean.columns:
                fig = px.bar(df_clean, x=x_col, y=y_col, color=color_col, title=title)
            else:
                fig = px.bar(df_clean, x=x_col, title=title)
            fig.update_xaxes(title=format_title(x_col))
            if y_col:
                fig.update_yaxes(title=format_title(y_col))
                

        elif chart_type == "Line Chart":
            if y_col and y_col in df_clean.columns:
                fig = px.line(df_clean, x=x_col, y=y_col, color=color_col, title=title)
                fig.update_xaxes(title=format_title(x_col))
                fig.update_yaxes(title=format_title(y_col))
            else:
                st.error("❌ Line chart requires both X and Y columns")
                return None, None

        elif chart_type == "Scatter Plot":
            if y_col and y_col in df_clean.columns:
                fig = px.scatter(df_clean, x=x_col, y=y_col, color=color_col, title=title)
                fig.update_xaxes(title=format_title(x_col))
                fig.update_yaxes(title=format_title(y_col))
            else:
                st.error("❌ Scatter plot requires both X and Y columns")
                return None, None

        elif chart_type == "Pie Chart":
            if y_col and y_col in df_clean.columns:
                pie_data = df_clean.groupby(x_col)[y_col].sum().head(10)
                fig = px.pie(values=pie_data.values, names=pie_data.index, title=title)
            else:
                value_counts = df_clean[x_col].value_counts().head(10)
                fig = px.pie(values=value_counts.values, names=value_counts.index, title=title)

        elif chart_type == "Histogram":
            fig = px.histogram(df_clean, x=x_col, title=title, color=color_col)
            fig.update_xaxes(title=format_title(x_col))
            fig.update_yaxes(title="Frequency")
        elif chart_type == "Box Plot":
            if y_col and y_col in df_clean.columns:
                fig = px.box(df_clean, x=x_col, y=y_col, color=color_col, title=title)
                fig.update_xaxes(title=format_title(x_col))
                fig.update_yaxes(title=format_title(y_col))
            else:
                fig = px.box(df_clean, y=x_col, title=title)
                fig.update_yaxes(title=format_title(x_col))



        else:
            st.error("❌ Unsupported chart type")
            return None, None
        
        # Apply styling
        fig.update_layout(
            template=template,
            title=title,
            height=500,
            showlegend=True if color_col else False
        )
        
        return fig, {}
        
    except Exception as e:
        st.error(f"❌ Error creating visualization: {str(e)}")
        return None, None

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
        
        # Set proper column names if they're just numbers
        if df.empty:
            st.error("❌ Selected table is empty")
        else:
            # Use first row as headers if they look like headers
            if len(df) > 1:
                first_row = df.iloc[0].astype(str)
                if not first_row.str.isnumeric().all():
                    df.columns = first_row
                    df = df.drop(df.index[0]).reset_index(drop=True)
            
            # Ensure column names are strings
            df.columns = [str(col) for col in df.columns]
        
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
            if chart_type in ["Line Chart", "Area Chart", "Scatter Plot", "Bubble Chart", "Box Plot", "Violin Plot"]:
                y_column = st.selectbox("📏 Y-Axis Column", [None] + df.columns.tolist())
            elif chart_type in ["Bar Chart", "Horizontal Bar", "Pie Chart", "Donut Chart", "Sunburst"]:
                y_column = st.selectbox("📏 Y-Axis Column (Optional)", [None] + df.columns.tolist())
            elif chart_type == "Heatmap":
                y_column = None
                st.info("💡 Heatmap will show correlations between all numeric columns")
            else:
                y_column = None
            
            # Color column (optional)
            if chart_type == "Sunburst":
                color_column = st.selectbox("🎨 Hierarchy Column (Required)", [None] + df.columns.tolist())
            else:
                color_column = st.selectbox("🎨 Color By (Optional)", [None] + df.columns.tolist())
            
            # Chart title with better default
            if y_column and y_column != "None" and y_column is not None:
                default_title = f"{y_column} by {x_column}"
            else:
                default_title = f"{x_column} Distribution"
            chart_title = st.text_input("📝 Chart Title", default_title)
        
        with col2:
            st.markdown("#### 💡 Chart Guidelines")
            
            guidelines = {
                "Bar Chart": "📊 Compare categories vertically. Y-axis optional for counts.",
                "Horizontal Bar": "📊 Compare categories horizontally. Y-axis optional for counts.",
                "Line Chart": "📈 Show trends over time. Requires numeric Y-axis.",
                "Area Chart": "📈 Show trends with filled area. Requires numeric Y-axis.",
                "Scatter Plot": "🔵 Show correlations. Requires numeric X and Y axes.",
                "Bubble Chart": "🫧 Scatter plot with size dimension. Requires numeric X and Y.",
                "Pie Chart": "🥧 Show proportions as slices. Y-axis optional for counts.",
                "Donut Chart": "🍩 Pie chart with center hole. Y-axis optional for counts.",
                "Histogram": "📊 Show data distribution. Requires numeric X-axis.",
                "Box Plot": "📦 Show quartiles and outliers. Y-axis optional.",
                "Violin Plot": "🎻 Show distribution shape. Y-axis optional.",
                "Heatmap": "🔥 Show correlations between numeric columns.",
                "Sunburst": "☀️ Show hierarchical data. Requires hierarchy column."
            }
            
            st.info(guidelines.get(chart_type, "Select a chart type for guidelines"))
        
        # Generate chart
        if st.button("🎨 Generate Visualization", use_container_width=True, type="primary"):
            with st.spinner("🎨 Creating visualization..."):
                result = create_simple_visualization(
                    df, chart_type, x_column, y_column, 
                    color_column if color_column and color_column not in ["None", None] else None, 
                    chart_title
                )
                
                if result and len(result) == 2:
                    fig, config = result
                    
                    # Display chart with full interactivity
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Interactive features info
                    st.info("🎯 **Interactive Features**: Zoom, Pan, Select, Download, Reset, Hover for details")
                    
                    # Export and data options
                    st.markdown("#### 📥 Export & Data Options")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        # Image export
                        img_bytes, filepath = save_plot_as_image(fig, f"chart_{selected_idx+1}", export_format.lower())
                        if img_bytes:
                            st.download_button(
                                f"📥 {export_format} Image",
                                data=img_bytes,
                                file_name=f"{chart_title.replace(' ', '_')}.{export_format.lower()}",
                                mime=f"image/{export_format.lower()}"
                            )
                    
                    with col2:
                        # HTML export
                        html_str = fig.to_html(include_plotlyjs='cdn', config=config)
                        st.download_button(
                            "🌐 Interactive HTML",
                            data=html_str,
                            file_name=f"{chart_title.replace(' ', '_')}.html",
                            mime="text/html"
                        )
                    
                    with col3:
                        # JSON export
                        json_str = fig.to_json()
                        st.download_button(
                            "📄 Chart JSON",
                            data=json_str,
                            file_name=f"{chart_title.replace(' ', '_')}.json",
                            mime="application/json"
                        )
                    
                    with col4:
                        # Copy chart data
                        if st.button("📋 Copy Chart Data", key="copy_chart_data"):
                            chart_cols = [col for col in [x_column, y_column, color_column] if col and col not in ["None", None]]
                            if chart_cols:
                                chart_data = df[chart_cols].copy()
                                st.code(chart_data.to_string(index=False), language="text")
                    
                    # Data summary for the chart
                    with st.expander("📊 Chart Data Summary", expanded=False):
                        chart_cols = [col for col in [x_column, y_column, color_column] if col and col not in ["None", None]]
                        if chart_cols:
                            chart_data = df[chart_cols]
                        else:
                            chart_data = df[[x_column]]
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Data Used in Chart:**")
                            st.dataframe(chart_data.head(10), use_container_width=True)
                        
                        with col2:
                            st.markdown("**Statistics:**")
                            numeric_data = chart_data.select_dtypes(include=[np.number])
                            if not numeric_data.empty:
                                st.dataframe(numeric_data.describe(), use_container_width=True)
                            else:
                                st.info("No numeric data for statistics")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick chart templates
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### ⚡ Quick Chart Templates")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Quick Bar Chart", use_container_width=True):
                if len(df.columns) >= 1:
                    try:
                        fig = px.bar(df, x=df.columns[0], title=f"{df.columns[0]} Distribution")
                        fig.update_layout(template="plotly_dark" if st.session_state.theme_mode == 'dark' else "plotly_white")
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error creating bar chart: {e}")
        
        with col2:
            if st.button("📈 Quick Line Chart", use_container_width=True):
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) >= 2:
                    try:
                        fig = px.line(df, x=numeric_cols[0], y=numeric_cols[1], title=f"{numeric_cols[1]} vs {numeric_cols[0]}")
                        fig.update_layout(template="plotly_dark" if st.session_state.theme_mode == 'dark' else "plotly_white")
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error creating line chart: {e}")
                else:
                    st.info("Need at least 2 numeric columns for line chart")
        
        with col3:
            if st.button("🥧 Quick Pie Chart", use_container_width=True):
                if len(df.columns) >= 1:
                    try:
                        value_counts = df[df.columns[0]].value_counts().head(10)
                        fig = px.pie(values=value_counts.values, names=value_counts.index, title=f"{df.columns[0]} Distribution")
                        fig.update_layout(template="plotly_dark" if st.session_state.theme_mode == 'dark' else "plotly_white")
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error creating pie chart: {e}")
        
        with col4:
            if st.button("🔥 Quick Heatmap", use_container_width=True):
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) >= 2:
                    try:
                        corr_matrix = df[numeric_cols].corr()
                        fig = px.imshow(corr_matrix, text_auto=True, title="Correlation Heatmap")
                        fig.update_layout(template="plotly_dark" if st.session_state.theme_mode == 'dark' else "plotly_white")
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error creating heatmap: {e}")
                else:
                    st.info("Need at least 2 numeric columns for heatmap")
        
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