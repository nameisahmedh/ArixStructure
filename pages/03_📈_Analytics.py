import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sys
import os
from datetime import datetime
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

# Navigation buttons in stable container
nav_container = st.container()
with nav_container:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("🏠 Home", use_container_width=True, key="nav_home"):
            st.switch_page("app.py")
    with col2:
        if st.button("📊 Dashboard", use_container_width=True, key="nav_dash"):
            st.switch_page("pages/01_📊_Dashboard.py")
    with col3:
        if st.button("🤖 AI Assistant", use_container_width=True, key="nav_ai"):
            st.switch_page("pages/02_🤖_AI_Assistant.py")
    with col4:
        if st.button("🖼️ Images", use_container_width=True, key="nav_images"):
            st.switch_page("pages/04_🖼️_Images.py")
    with col5:
        if st.button("📝 Text Analysis", use_container_width=True, key="nav_text"):
            st.switch_page("pages/05_📝_Text_Analysis.py")

st.divider()

def create_simple_visualization(df, chart_type, x_col, y_col=None, color_col=None, title="Chart"):
    """Create visualization with proper axis handling and data validation"""
    try:
        # Data validation
        if df.empty:
            st.error("❌ No data available for visualization")
            return None, None
            
        # Clean data and handle missing values
        df_clean = df.copy()
        
        # Convert numeric columns properly
        for col in df_clean.columns:
            if df_clean[col].dtype == 'object':
                # Try to convert to numeric if possible
                numeric_series = pd.to_numeric(df_clean[col], errors='coerce')
                if not numeric_series.isna().all():
                    df_clean[col] = numeric_series
        
        # Set theme
        template = "plotly_dark" if st.session_state.theme_mode == 'dark' else "plotly_white"
        
        # Helper function to format axis titles
        def format_title(col):
            return str(col).replace('_', ' ').title()
        
        # Helper function to get data range with padding
        def get_axis_range(data, padding=0.1):
            if pd.api.types.is_numeric_dtype(data):
                data_clean = data.dropna()
                if len(data_clean) > 0:
                    min_val = data_clean.min()
                    max_val = data_clean.max()
                    range_size = max_val - min_val
                    if range_size > 0:
                        return [min_val - range_size * padding, max_val + range_size * padding]
            return None
        
        # Create visualizations with proper axis handling
        if chart_type == "Bar Chart":
            if y_col and y_col in df_clean.columns:
                # Remove rows with NaN values in key columns
                df_plot = df_clean.dropna(subset=[x_col, y_col])
                fig = px.bar(df_plot, x=x_col, y=y_col, color=color_col, title=title)
                
                # Set custom y-axis range
                y_range = get_axis_range(df_plot[y_col])
                if y_range:
                    fig.update_yaxes(range=y_range)
            else:
                df_plot = df_clean.dropna(subset=[x_col])
                value_counts = df_plot[x_col].value_counts()
                fig = px.bar(x=value_counts.index, y=value_counts.values, title=title)
                fig.update_xaxes(title=format_title(x_col))
                fig.update_yaxes(title="Count")
                
                # Set custom y-axis range for counts
                y_range = get_axis_range(pd.Series(value_counts.values))
                if y_range:
                    fig.update_yaxes(range=y_range)
            
            fig.update_xaxes(title=format_title(x_col))
            if y_col:
                fig.update_yaxes(title=format_title(y_col))

        elif chart_type == "Line Chart":
            if y_col and y_col in df_clean.columns:
                df_plot = df_clean.dropna(subset=[x_col, y_col])
                fig = px.line(df_plot, x=x_col, y=y_col, color=color_col, title=title)
                
                # Set custom axis ranges
                x_range = get_axis_range(df_plot[x_col])
                y_range = get_axis_range(df_plot[y_col])
                
                if x_range:
                    fig.update_xaxes(range=x_range)
                if y_range:
                    fig.update_yaxes(range=y_range)
                    
                fig.update_xaxes(title=format_title(x_col))
                fig.update_yaxes(title=format_title(y_col))
            else:
                st.error("❌ Line chart requires both X and Y columns")
                return None, None

        elif chart_type == "Scatter Plot":
            if y_col and y_col in df_clean.columns:
                df_plot = df_clean.dropna(subset=[x_col, y_col])
                fig = px.scatter(df_plot, x=x_col, y=y_col, color=color_col, title=title)
                
                # Set custom axis ranges
                x_range = get_axis_range(df_plot[x_col])
                y_range = get_axis_range(df_plot[y_col])
                
                if x_range:
                    fig.update_xaxes(range=x_range)
                if y_range:
                    fig.update_yaxes(range=y_range)
                    
                fig.update_xaxes(title=format_title(x_col))
                fig.update_yaxes(title=format_title(y_col))
            else:
                st.error("❌ Scatter plot requires both X and Y columns")
                return None, None

        elif chart_type == "Pie Chart":
            if y_col and y_col in df_clean.columns:
                df_plot = df_clean.dropna(subset=[x_col, y_col])
                pie_data = df_plot.groupby(x_col)[y_col].sum().head(10)
                # Filter out zero or negative values for pie chart
                pie_data = pie_data[pie_data > 0]
                if len(pie_data) > 0:
                    fig = px.pie(values=pie_data.values, names=pie_data.index, title=title)
                else:
                    st.error("❌ No positive values found for pie chart")
                    return None, None
            else:
                df_plot = df_clean.dropna(subset=[x_col])
                value_counts = df_plot[x_col].value_counts().head(10)
                fig = px.pie(values=value_counts.values, names=value_counts.index, title=title)

        elif chart_type == "Histogram":
            df_plot = df_clean.dropna(subset=[x_col])
            if pd.api.types.is_numeric_dtype(df_plot[x_col]):
                # Calculate optimal number of bins
                n_bins = min(50, max(10, int(np.sqrt(len(df_plot)))))
                fig = px.histogram(df_plot, x=x_col, title=title, color=color_col, nbins=n_bins)
                
                # Set custom x-axis range
                x_range = get_axis_range(df_plot[x_col])
                if x_range:
                    fig.update_xaxes(range=x_range)
            else:
                fig = px.histogram(df_plot, x=x_col, title=title, color=color_col)
                
            fig.update_xaxes(title=format_title(x_col))
            fig.update_yaxes(title="Frequency")
            
        elif chart_type == "Box Plot":
            if y_col and y_col in df_clean.columns:
                df_plot = df_clean.dropna(subset=[x_col, y_col])
                fig = px.box(df_plot, x=x_col, y=y_col, color=color_col, title=title)
                
                # Set custom y-axis range
                y_range = get_axis_range(df_plot[y_col])
                if y_range:
                    fig.update_yaxes(range=y_range)
                    
                fig.update_xaxes(title=format_title(x_col))
                fig.update_yaxes(title=format_title(y_col))
            else:
                df_plot = df_clean.dropna(subset=[x_col])
                if pd.api.types.is_numeric_dtype(df_plot[x_col]):
                    fig = px.box(df_plot, y=x_col, title=title)
                    
                    # Set custom y-axis range
                    y_range = get_axis_range(df_plot[x_col])
                    if y_range:
                        fig.update_yaxes(range=y_range)
                        
                    fig.update_yaxes(title=format_title(x_col))
                else:
                    st.error("❌ Box plot requires numeric data")
                    return None, None

        elif chart_type == "Heatmap":
            numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) >= 2:
                df_numeric = df_clean[numeric_cols].dropna()
                if len(df_numeric) > 1:
                    corr_matrix = df_numeric.corr()
                    fig = px.imshow(
                        corr_matrix, 
                        text_auto='.2f', 
                        title=title,
                        color_continuous_scale='RdBu_r',
                        zmin=-1, zmax=1
                    )
                    fig.update_xaxes(title="Variables")
                    fig.update_yaxes(title="Variables")
                else:
                    st.error("❌ Not enough data for heatmap")
                    return None, None
            else:
                st.error("❌ Heatmap requires at least 2 numeric columns")
                return None, None

        elif chart_type == "Area Chart":
            if y_col and y_col in df_clean.columns:
                df_plot = df_clean.dropna(subset=[x_col, y_col])
                fig = px.area(df_plot, x=x_col, y=y_col, color=color_col, title=title)
                
                x_range = get_axis_range(df_plot[x_col])
                y_range = get_axis_range(df_plot[y_col])
                
                if x_range:
                    fig.update_xaxes(range=x_range)
                if y_range:
                    fig.update_yaxes(range=y_range)
                    
                fig.update_xaxes(title=format_title(x_col))
                fig.update_yaxes(title=format_title(y_col))
            else:
                st.error("❌ Area chart requires both X and Y columns")
                return None, None

        elif chart_type == "Violin Plot":
            if y_col and y_col in df_clean.columns:
                df_plot = df_clean.dropna(subset=[x_col, y_col])
                fig = px.violin(df_plot, x=x_col, y=y_col, color=color_col, title=title)
                
                y_range = get_axis_range(df_plot[y_col])
                if y_range:
                    fig.update_yaxes(range=y_range)
                    
                fig.update_xaxes(title=format_title(x_col))
                fig.update_yaxes(title=format_title(y_col))
            else:
                df_plot = df_clean.dropna(subset=[x_col])
                if pd.api.types.is_numeric_dtype(df_plot[x_col]):
                    fig = px.violin(df_plot, y=x_col, title=title)
                    
                    y_range = get_axis_range(df_plot[x_col])
                    if y_range:
                        fig.update_yaxes(range=y_range)
                        
                    fig.update_yaxes(title=format_title(x_col))
                else:
                    st.error("❌ Violin plot requires numeric data")
                    return None, None

        elif chart_type == "Sunburst":
            if color_col and color_col in df_clean.columns:
                df_plot = df_clean.dropna(subset=[x_col, color_col])
                if y_col and y_col in df_plot.columns:
                    fig = px.sunburst(df_plot, path=[x_col, color_col], values=y_col, title=title)
                else:
                    value_counts = df_plot.groupby([x_col, color_col]).size().reset_index(name='count')
                    fig = px.sunburst(value_counts, path=[x_col, color_col], values='count', title=title)
            else:
                st.error("❌ Sunburst chart requires a hierarchy column")
                return None, None

        else:
            st.error("❌ Unsupported chart type")
            return None, None
        
        # Apply enhanced styling
        fig.update_layout(
            template=template,
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'family': 'Poppins'}
            },
            height=600,
            showlegend=True if color_col else False,
            font={'family': 'Poppins'},
            margin=dict(l=60, r=60, t=80, b=60),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        # Enhanced axis styling
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            showline=True,
            linewidth=1,
            linecolor='rgba(128,128,128,0.5)',
            title_font={'size': 14, 'family': 'Poppins'}
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            showline=True,
            linewidth=1,
            linecolor='rgba(128,128,128,0.5)',
            title_font={'size': 14, 'family': 'Poppins'}
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
            
            # Ensure column names are strings and unique
            df.columns = [str(col) for col in df.columns]
            
            # Handle duplicate column names
            cols = df.columns.tolist()
            seen = {}
            for i, col in enumerate(cols):
                if col in seen:
                    seen[col] += 1
                    cols[i] = f"{col}_{seen[col]}"
                else:
                    seen[col] = 0
            df.columns = cols
        
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
        
        # AI Column Extraction
        st.markdown("### 🤖 AI Column Extraction")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            extraction_query = st.text_input(
                "🔍 Search for columns (use keywords):",
                placeholder="e.g., 'region', 'sales', 'date', 'profit' - or use exact column names"
            )
        
        with col2:
            if st.button("🤖 Extract Columns", use_container_width=True):
                if extraction_query:
                    with st.spinner("🤖 AI analyzing columns..."):
                        try:
                            from llm_handler import get_text_response
                            
                            column_info = []
                            for col in df.columns:
                                sample_values = df[col].dropna().head(3).tolist()
                                col_type = str(df[col].dtype)
                                column_info.append(f"Column: {col}, Type: {col_type}, Sample: {sample_values}")
                            
                            context = chr(10).join(column_info)
                            prompt = f"Based on this user request: '{extraction_query}', analyze these columns and return ONLY the column names that match the request, separated by commas. Return format: column1,column2,column3 (no spaces, no explanations)"
                            
                            # Smart column matching without AI
                            query_lower = extraction_query.lower()
                            available_cols = df.columns.tolist()
                            suggested_cols = []
                            
                            # Direct keyword matching
                            keywords = query_lower.split()
                            
                            for col in available_cols:
                                col_lower = col.lower()
                                # Check if any keyword matches column name
                                for keyword in keywords:
                                    if (keyword in col_lower or col_lower in keyword or 
                                        keyword == col_lower or 
                                        any(k in col_lower for k in [keyword[:4], keyword[:3]]) if len(keyword) > 3 else False):
                                        if col not in suggested_cols:
                                            suggested_cols.append(col)
                                        break
                            
                            # If no direct matches, try semantic matching
                            if not suggested_cols:
                                semantic_matches = {
                                    'sales': ['sales', 'revenue', 'income', 'total'],
                                    'date': ['date', 'time', 'day', 'month', 'year'],
                                    'region': ['region', 'area', 'location', 'place'],
                                    'product': ['product', 'item', 'goods'],
                                    'category': ['category', 'type', 'class'],
                                    'profit': ['profit', 'margin', 'earnings'],
                                    'cost': ['cost', 'price', 'expense'],
                                    'quantity': ['quantity', 'units', 'amount', 'count']
                                }
                                
                                for keyword in keywords:
                                    for semantic_key, semantic_values in semantic_matches.items():
                                        if keyword in semantic_values:
                                            for col in available_cols:
                                                if any(sv in col.lower() for sv in semantic_values):
                                                    if col not in suggested_cols:
                                                        suggested_cols.append(col)
                            
                            # Try AI response as backup
                            ai_response = None
                            try:
                                ai_response = get_text_response(prompt, context)
                                if ai_response and "AI service" not in ai_response:
                                    st.info(f"💡 AI Suggestion: {ai_response}")
                            except:
                                pass
                                
                            suggested_cols = list(set(suggested_cols))
                            
                            if suggested_cols:
                                st.success(f"🎯 Found {len(suggested_cols)} matching columns: {', '.join(suggested_cols)}")
                                    
                                    extracted_df = df[suggested_cols]
                                    st.dataframe(extracted_df.head(10), use_container_width=True)
                                    
                                    col_a, col_b, col_c = st.columns(3)
                                    with col_a:
                                        csv_data = extracted_df.to_csv(index=False).encode('utf-8')
                                        st.download_button(
                                            "📊 Download CSV",
                                            data=csv_data,
                                            file_name=f"extracted_columns.csv",
                                            mime="text/csv"
                                        )
                                    with col_b:
                                        json_data = extracted_df.to_json(orient='records', indent=2).encode('utf-8')
                                        st.download_button(
                                            "📄 Download JSON",
                                            data=json_data,
                                            file_name=f"extracted_columns.json",
                                            mime="application/json"
                                        )
                                    with col_c:
                                        if st.button("📈 Visualize Extracted Data"):
                                            st.session_state['extracted_df'] = extracted_df.copy()
                                            st.session_state['use_extracted'] = True
                                            st.session_state['extracted_columns'] = suggested_cols
                                            st.success("✅ Extracted data ready for visualization! Scroll down to create charts.")
                                            st.rerun()
                            else:
                                st.warning(f"❌ No matching columns found for '{extraction_query}'")
                                st.info(f"**Available columns**: {', '.join(available_cols)}")
                                st.write("💡 **Tip**: Try keywords like 'sales', 'date', 'region', or use exact column names")
                                
                                # Show suggestions based on available columns
                                suggestions = []
                                for col in available_cols[:5]:  # Show first 5 as examples
                                    suggestions.append(f"'{col.lower()}'")
                                if suggestions:
                                    st.write(f"**Try searching for**: {', '.join(suggestions)}")
                        except Exception as e:
                            st.error(f"❌ Error in column extraction: {str(e)[:100]}")
                            # Still show available columns as fallback
                            st.info(f"**Available columns**: {', '.join(df.columns.tolist())}")
                else:
                    st.warning("Please enter a description of what columns to extract")
                    st.write("**Examples**: 'region', 'sales data', 'date columns', 'financial information'")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Visualization builder
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🎨 Create Visualization")
        
        # Use extracted data if available
        if st.session_state.get('use_extracted', False) and 'extracted_df' in st.session_state:
            viz_df = st.session_state['extracted_df'].copy()
            extracted_cols = st.session_state.get('extracted_columns', [])
            
            # Ensure viz_df has proper data types
            for col in viz_df.columns:
                if viz_df[col].dtype == 'object':
                    numeric_series = pd.to_numeric(viz_df[col], errors='coerce')
                    if not numeric_series.isna().all():
                        viz_df[col] = numeric_series
            
            st.success(f"🎯 Using AI-extracted columns: {', '.join(extracted_cols)}")
            
            # Show extracted data info
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.metric("Extracted Columns", len(viz_df.columns))
            with col_info2:
                st.metric("Data Rows", len(viz_df))
            with col_info3:
                if st.button("🔄 Use Full Table", key="switch_to_full"):
                    st.session_state['use_extracted'] = False
                    st.rerun()
                    
            # Show preview of extracted data
            with st.expander("📋 Extracted Data Preview", expanded=True):
                st.dataframe(viz_df.head(10), use_container_width=True)
                
                # Show data types
                st.markdown("**Column Types:**")
                type_info = []
                for col in viz_df.columns:
                    col_type = "Numeric" if pd.api.types.is_numeric_dtype(viz_df[col]) else "Text"
                    type_info.append(f"• {col}: {col_type}")
                st.write("\n".join(type_info))
        else:
            viz_df = df
            if st.session_state.get('extracted_df') is not None:
                if st.button("🎯 Use Extracted Columns", key="switch_to_extracted"):
                    st.session_state['use_extracted'] = True
                    st.rerun()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Chart configuration
            col_a, col_b = st.columns(2)
            
            with col_a:
                chart_type = st.selectbox(
                    "📊 Chart Type", 
                    ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram", "Box Plot", "Heatmap", "Area Chart", "Violin Plot", "Sunburst"]
                )
            
            with col_b:
                x_column = st.selectbox("📐 X-Axis Column", viz_df.columns.tolist())
            
            # Y-axis selection based on chart type
            if chart_type in ["Line Chart", "Area Chart", "Scatter Plot", "Bubble Chart", "Box Plot", "Violin Plot"]:
                y_column = st.selectbox("📏 Y-Axis Column", [None] + viz_df.columns.tolist())
            elif chart_type in ["Bar Chart", "Horizontal Bar", "Pie Chart", "Donut Chart", "Sunburst"]:
                y_column = st.selectbox("📏 Y-Axis Column (Optional)", [None] + viz_df.columns.tolist())
            elif chart_type == "Heatmap":
                y_column = None
                st.info("💡 Heatmap will show correlations between all numeric columns")
            else:
                y_column = None
            
            # Color column (optional)
            if chart_type == "Sunburst":
                color_column = st.selectbox("🎨 Hierarchy Column (Required)", [None] + viz_df.columns.tolist())
            else:
                color_column = st.selectbox("🎨 Color By (Optional)", [None] + viz_df.columns.tolist())
            
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
        
        # Generate chart with better UI
        st.markdown("---")
        col_gen1, col_gen2 = st.columns([3, 1])
        with col_gen1:
            generate_btn = st.button("🎨 Generate Visualization", use_container_width=True, type="primary")
        with col_gen2:
            if st.button("🔄 Reset to Full Data", use_container_width=True):
                if 'extracted_df' in st.session_state:
                    del st.session_state['extracted_df']
                if 'use_extracted' in st.session_state:
                    del st.session_state['use_extracted']
                st.success("✅ Reset to full table data")
                st.rerun()
        
        if generate_btn:
            # Validate data before visualization
            if viz_df.empty:
                st.error("❌ No data available for visualization")
            elif x_column not in viz_df.columns:
                st.error(f"❌ Column '{x_column}' not found in data")
            else:
                with st.spinner("🎨 Creating your visualization..."):
                    # Show what data is being used
                    data_source = "AI-extracted data" if st.session_state.get('use_extracted', False) else "full table data"
                    st.info(f"📈 Creating {chart_type.lower()} using {data_source} ({len(viz_df)} rows, {len(viz_df.columns)} columns)")
                    
                    result = create_simple_visualization(
                        viz_df, chart_type, x_column, y_column, 
                        color_column if color_column and color_column not in ["None", None] else None, 
                        chart_title
                    )
                    
                    if result and len(result) == 2:
                        fig, config = result
                    
                    # Create stable container for chart
                    chart_container = st.container()
                    
                    with chart_container:
                        # Success message
                        st.success("✅ **Visualization Created Successfully!**")
                        
                        # Display chart with stable container
                        st.plotly_chart(fig, use_container_width=True, config={
                            'displayModeBar': True,
                            'displaylogo': False,
                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                            'toImageButtonOptions': {
                                'format': 'png',
                                'filename': chart_title.replace(' ', '_'),
                                'height': 600,
                                'width': 1000,
                                'scale': 2
                            }
                        })
                        
                        # Interactive features info
                        st.info("🎯 **Interactive Features**: Zoom, Pan, Select, Download, Reset, Hover for details")
                    
                    # Export and analysis options in stable container
                    export_container = st.container()
                    
                    with export_container:
                        st.markdown("#### 📥 Export & Analysis Options")
                        
                        col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        # Image export with better error handling
                        try:
                            img_bytes, filepath = save_plot_as_image(fig, f"chart_{selected_idx+1}", export_format.lower())
                            if img_bytes:
                                st.download_button(
                                    f"📥 {export_format}",
                                    data=img_bytes,
                                    file_name=f"{chart_title.replace(' ', '_')}.{export_format.lower()}",
                                    mime=f"image/{export_format.lower()}" if export_format.lower() != 'html' else "text/html",
                                    help=f"Download chart as {export_format} file"
                                )
                            else:
                                st.warning(f"⚠️ {export_format} export not available")
                        except Exception as e:
                            st.error(f"❌ Export error: {str(e)[:50]}...")
                    
                    with col2:
                        # HTML export
                        html_str = fig.to_html(include_plotlyjs='cdn', config=config)
                        st.download_button(
                            "🌐 HTML",
                            data=html_str,
                            file_name=f"{chart_title.replace(' ', '_')}.html",
                            mime="text/html"
                        )
                    
                    with col3:
                        # Analysis Report
                        chart_cols = [col for col in [x_column, y_column, color_column] if col and col not in ["None", None]]
                        if chart_cols:
                            chart_data = df[chart_cols].copy()
                            analysis_text = f"""CHART ANALYSIS REPORT

Chart Title: {chart_title}
Chart Type: {chart_type}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DATA SUMMARY:
Total Records: {len(chart_data)}
Columns Analyzed: {', '.join(chart_cols)}

STATISTICAL SUMMARY:
{chart_data.describe().to_string() if not chart_data.select_dtypes(include=[np.number]).empty else 'No numeric data for statistics'}

DATA PREVIEW:
{chart_data.head(20).to_string(index=False)}
"""
                            st.download_button(
                                "📄 Report",
                                data=analysis_text.encode('utf-8'),
                                file_name=f"{chart_title.replace(' ', '_')}_analysis.txt",
                                mime="text/plain"
                            )
                    
                    with col4:
                        # Data export
                        if chart_cols:
                            chart_data = df[chart_cols].copy()
                            csv_data = chart_data.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                "📊 Data CSV",
                                data=csv_data,
                                file_name=f"{chart_title.replace(' ', '_')}_data.csv",
                                mime="text/csv"
                            )
                    
                    with col5:
                        # JSON export
                        json_str = fig.to_json()
                        st.download_button(
                            "📄 JSON",
                            data=json_str,
                            file_name=f"{chart_title.replace(' ', '_')}.json",
                            mime="application/json"
                        )
                    
                    # Data summary for the chart
                    with st.expander("📊 Chart Data Summary", expanded=False):
                        chart_cols = [col for col in [x_column, y_column, color_column] if col and col not in ["None", None]]
                        if chart_cols:
                            chart_data = viz_df[chart_cols]
                        else:
                            chart_data = viz_df[[x_column]]
                        
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