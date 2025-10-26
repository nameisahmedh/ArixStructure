import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_theme_css, init_session_state
import llm_handler

st.set_page_config(
    page_title="🤖 AI Assistant - ArixStructure",
    page_icon="🤖",
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
    <h1>🤖 AI Assistant</h1>
    <p>🔍 Ask intelligent questions about your structured data</p>
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
    if st.button("📈 Analytics", use_container_width=True):
        st.switch_page("pages/03_📈_Analytics.py")
with col4:
    if st.button("🖼️ Images", use_container_width=True):
        st.switch_page("pages/04_🖼️_Images.py")
with col5:
    if st.button("📝 Text Analysis", use_container_width=True):
        st.switch_page("pages/05_📝_Text_Analysis.py")

st.divider()

def process_intelligent_query(query, doc_data):
    """Enhanced AI query processing with better accuracy"""
    query_lower = query.lower()
    results = {
        'type': 'text',
        'content': '',
        'tables': [],
        'images': [],
        'specific_data': None
    }
    
    # Enhanced context building
    def build_enhanced_context(tables, full_text):
        context = f"Document Summary: {full_text[:500]}...\n\n"
        context += f"Total Tables: {len(tables)}\n\n"
        
        for i, table in enumerate(tables):
            if table:
                headers = table[0] if table else []
                sample_data = table[1:3] if len(table) > 1 else []
                context += f"Table {i+1} ({len(table)} rows, {len(headers)} columns):\n"
                context += f"Headers: {', '.join(str(h) for h in headers)}\n"
                if sample_data:
                    context += "Sample data:\n"
                    for row in sample_data:
                        context += f"  {', '.join(str(cell) for cell in row)}\n"
                context += "\n"
        return context
    
    # Table-related queries
    if any(word in query_lower for word in ['table', 'data', 'row', 'column', 'chart', 'extract', 'show']):
        results['type'] = 'table'
        tables = doc_data.get('tables', [])
        
        if 'table' in query_lower:
            import re
            # Specific table number
            table_nums = re.findall(r'table\s*(\d+)', query_lower)
            if table_nums:
                table_idx = int(table_nums[0]) - 1
                if 0 <= table_idx < len(tables):
                    results['tables'] = [tables[table_idx]]
                    results['specific_data'] = f"Table {table_nums[0]}"
                    
                    # Enhanced table analysis
                    table = tables[table_idx]
                    headers = table[0] if table else []
                    data_rows = table[1:] if len(table) > 1 else []
                    
                    analysis = f"Table {table_nums[0]} Analysis:\n"
                    analysis += f"- Rows: {len(table)}\n"
                    analysis += f"- Columns: {len(headers)}\n"
                    analysis += f"- Headers: {', '.join(str(h) for h in headers)}\n"
                    
                    # Detect data types
                    if data_rows:
                        numeric_cols = []
                        text_cols = []
                        for i, header in enumerate(headers):
                            sample_values = [row[i] for row in data_rows[:5] if i < len(row)]
                            if any(str(val).replace('.', '').replace('-', '').isdigit() for val in sample_values):
                                numeric_cols.append(header)
                            else:
                                text_cols.append(header)
                        
                        if numeric_cols:
                            analysis += f"- Numeric columns: {', '.join(str(col) for col in numeric_cols)}\n"
                        if text_cols:
                            analysis += f"- Text columns: {', '.join(str(col) for col in text_cols)}\n"
                    
                    results['content'] = analysis
            
            # Size-based queries
            elif any(phrase in query_lower for phrase in ['more rows', 'most rows', 'largest', 'biggest']):
                if tables:
                    max_rows = max(len(table) for table in tables)
                    largest_idx = next(i for i, table in enumerate(tables) if len(table) == max_rows)
                    
                    results['tables'] = [tables[largest_idx]]
                    results['specific_data'] = f"Largest table (Table {largest_idx + 1})"
                    results['content'] = f"Found the largest table: Table {largest_idx + 1} with {max_rows} rows and {len(tables[largest_idx][0]) if tables[largest_idx] else 0} columns."
            
            elif any(phrase in query_lower for phrase in ['fewer rows', 'smallest', 'least rows']):
                if tables:
                    min_rows = min(len(table) for table in tables)
                    smallest_idx = next(i for i, table in enumerate(tables) if len(table) == min_rows)
                    
                    results['tables'] = [tables[smallest_idx]]
                    results['specific_data'] = f"Smallest table (Table {smallest_idx + 1})"
                    results['content'] = f"Found the smallest table: Table {smallest_idx + 1} with {min_rows} rows and {len(tables[smallest_idx][0]) if tables[smallest_idx] else 0} columns."
            
            # All tables overview
            elif any(phrase in query_lower for phrase in ['all tables', 'what tables', 'list tables']):
                results['tables'] = tables
                overview = f"Document contains {len(tables)} tables:\n\n"
                for i, table in enumerate(tables):
                    headers = table[0] if table else []
                    overview += f"Table {i+1}: {len(table)} rows, {len(headers)} columns\n"
                    if headers:
                        overview += f"  Headers: {', '.join(str(h) for h in headers[:5])}{'...' if len(headers) > 5 else ''}\n"
                results['content'] = overview
            
            else:
                results['tables'] = tables
        
        # Enhanced LLM context for better accuracy
        if not results['content'] and results['tables']:
            enhanced_context = build_enhanced_context(results['tables'], doc_data.get('full_text', ''))
            results['content'] = llm_handler.get_text_response(f"Query: {query}\n\nContext: {enhanced_context}", "")
        elif not results['tables']:
            results['content'] = "No tables found in the document."
    
    # Image queries
    elif any(word in query_lower for word in ['image', 'picture', 'photo', 'figure']):
        results['type'] = 'image'
        results['images'] = doc_data.get('image_descriptions', [])
        
        if results['images']:
            # Enhanced image context
            image_context = f"Found {len(results['images'])} images:\n\n"
            for i, img in enumerate(results['images']):
                image_context += f"Image {i+1}: {img.get('description', 'No description')}\n"
            
            results['content'] = llm_handler.get_image_query_response(f"{query}\n\nContext: {image_context}", results['images'])
        else:
            results['content'] = "No images found in the document."
    
    # General text queries with enhanced context
    else:
        full_text = doc_data.get('full_text', '')
        tables = doc_data.get('tables', [])
        
        # Build comprehensive context
        enhanced_context = f"Document Text: {full_text}\n\n"
        if tables:
            enhanced_context += f"Available Tables ({len(tables)} total):\n"
            for i, table in enumerate(tables):
                headers = table[0] if table else []
                enhanced_context += f"Table {i+1}: {', '.join(str(h) for h in headers[:3])}{'...' if len(headers) > 3 else ''}\n"
        
        results['content'] = llm_handler.get_text_response(f"Query: {query}\n\nContext: {enhanced_context}", "")
    
    return results

if st.session_state.doc_data:
    # Current document info
    doc_name = st.session_state.get('last_uploaded_name', 'Unknown Document')
    st.markdown(f"**📄 Analyzing:** {doc_name}")
    
    # Sample questions
    st.markdown("### 💡 Sample Questions You Can Ask")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("• What tables are in this document?")
        st.markdown("• Summarize the main content")
        st.markdown("• What are the key findings?")
    
    with col2:
        st.markdown("• Show me the data insights")
        st.markdown("• What images are included?")
        st.markdown("• Extract numerical data")
    
    # Chat interface
    st.markdown("### 💬 Ask Your Question")
    
    # Handle clear input
    input_value = ""
    if st.session_state.get('clear_input', False):
        st.session_state.clear_input = False
        input_value = ""
    
    user_question = st.text_input(
        "🤔 What would you like to know about your document?",
        value=input_value,
        placeholder="e.g., What are the main topics? Show me table 1. What images are included?",
        key="ai_input_field"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        analyze_btn = st.button("🚀 Ask AI", use_container_width=True, type="primary")
    with col2:
        if st.button("🧹 Clear Input", use_container_width=True):
            st.session_state.clear_input = True
            st.rerun()
    
    # Process query and show response
    if analyze_btn and user_question:
        with st.spinner("🤖 AI is thinking..."):
            results = process_intelligent_query(user_question, st.session_state.doc_data)
            
            # Add to chat history
            chat_entry = {
                'question': user_question,
                'answer': results['content'],
                'type': results['type'],
                'timestamp': pd.Timestamp.now()
            }
            st.session_state.chat_history.append(chat_entry)
            
            # Display response
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("### 🤖 AI Response")
            
            st.markdown(f"**❓ Your Question:** {user_question}")
            st.markdown(f"**💡 AI Answer:** {results['content']}")
            
            # AI Response Export Options
            st.markdown("#### 📥 Export AI Response")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Download AI response as text
                response_text = f"Question: {user_question}\n\nAnswer: {results['content']}"
                st.download_button(
                    "📄 Download Response",
                    data=response_text,
                    file_name="ai_response.txt",
                    mime="text/plain"
                )
            
            with col2:
                # Copy AI response
                if st.button("📋 Copy Response"):
                    st.code(response_text, language="text")
            
            with col3:
                # Download as JSON
                response_json = {
                    "question": user_question,
                    "answer": results['content'],
                    "timestamp": pd.Timestamp.now().isoformat(),
                    "type": results['type']
                }
                import json
                st.download_button(
                    "📄 Download JSON",
                    data=json.dumps(response_json, indent=2),
                    file_name="ai_response.json",
                    mime="application/json"
                )
            
            # Display retrieved content
            if results['type'] == 'table' and results['tables']:
                st.markdown("**📊 Retrieved Tables:**")
                for i, table in enumerate(results['tables']):
                    df = pd.DataFrame(table)
                    st.dataframe(df, use_container_width=True)
                    
                    # Quick export options
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        csv_data = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            "📥 Download CSV",
                            data=csv_data,
                            file_name=f"table_{i+1}.csv",
                            mime="text/csv",
                            key=f"csv_{i}"
                        )
                    with col2:
                        json_data = df.to_json(orient='records', indent=2).encode('utf-8')
                        st.download_button(
                            "📥 Download JSON",
                            data=json_data,
                            file_name=f"table_{i+1}.json",
                            mime="application/json",
                            key=f"json_{i}"
                        )
                    with col3:
                        if st.button(f"📋 Copy Table {i+1}", key=f"copy_{i}"):
                            st.code(df.to_string(index=False))
            
            elif results['type'] == 'image' and results['images']:
                st.markdown("**🖼️ Retrieved Images:**")
                for i, img_desc in enumerate(results['images']):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image(img_desc['path'], caption=f"Image {i+1}")
                    with col2:
                        st.markdown(f"**Description:** {img_desc['description']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat history
    if st.session_state.chat_history:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 📚 Chat History")
        
        with st.expander(f"💬 Previous Conversations ({len(st.session_state.chat_history)} total)", expanded=False):
            for i, chat in enumerate(reversed(st.session_state.chat_history)):
                st.markdown(f"**🕐 {chat['timestamp'].strftime('%H:%M:%S')}**")
                st.markdown(f"**❓ Q:** {chat['question']}")
                answer_preview = chat['answer'][:200] + "..." if len(chat['answer']) > 200 else chat['answer']
                st.markdown(f"**💡 A:** {answer_preview}")
                if i < len(st.session_state.chat_history) - 1:
                    st.divider()
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # No document loaded
    st.markdown("### 🤖 AI Assistant Ready!")
    st.write("I'm ready to help you analyze your documents with intelligent Q&A!")
    
    st.markdown("#### ✨ What I Can Do:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Table Analysis**")
        st.write("Ask about specific tables, data patterns, and numerical insights from your structured data.")
        
        st.markdown("**📝 Content Summarization**")
        st.write("Get summaries, key points, and main themes extracted from your documents.")
    
    with col2:
        st.markdown("**🖼️ Image Understanding**")
        st.write("Analyze and describe images, charts, and visual content found in documents.")
        
        st.markdown("**🔍 Smart Search**")
        st.write("Find specific information and get detailed answers about your document content.")
    
    st.markdown("#### 💡 Example Questions You Can Ask:")
    questions = [
        "What are the main topics in this document?",
        "Show me table 2 and explain the data",
        "What images are included and what do they show?",
        "Summarize the key findings in 3 bullet points",
        "What trends can you identify in the data?",
        "Extract all the numerical data from the tables"
    ]
    
    for question in questions:
        st.write(f"• {question}")
    
    st.info("📄 **Upload a Document First** - Go to the Dashboard to upload a document, then come back here to start asking questions!")