import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_theme_css, init_session_state
import pandas as pd
import re
from collections import Counter
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="📝 Text Analysis - ArixStructure",
    page_icon="📝",
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
    <h1>📝 Text Analysis & Processing</h1>
    <p>🔍 Deep dive into your document's textual content with advanced analytics</p>
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
    if st.button("🖼️ Images", use_container_width=True):
        st.switch_page("pages/04_🖼️_Images.py")

st.divider()

def analyze_text_content(text):
    if not text:
        return {}
    
    char_count = len(text)
    word_count = len(text.split())
    sentence_count = len(re.findall(r'[.!?]+', text))
    paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
    
    words = re.findall(r'\b\w+\b', text.lower())
    word_freq = Counter(words)
    
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
    filtered_words = {word: count for word, count in word_freq.items() if word not in stop_words and len(word) > 2}
    
    sentences = re.split(r'[.!?]+', text)
    sentence_lengths = [len(sentence.split()) for sentence in sentences if sentence.strip()]
    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
    
    reading_time_minutes = word_count / 200
    
    numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
    dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b', text)
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    
    return {
        'char_count': char_count,
        'word_count': word_count,
        'sentence_count': sentence_count,
        'paragraph_count': paragraph_count,
        'word_freq': word_freq,
        'filtered_words': filtered_words,
        'sentence_lengths': sentence_lengths,
        'avg_sentence_length': avg_sentence_length,
        'reading_time_minutes': reading_time_minutes,
        'numbers': numbers,
        'dates': dates,
        'emails': emails,
        'urls': urls
    }

if st.session_state.doc_data:
    text_content = st.session_state.doc_data.get('full_text', '')
    
    if not text_content:
        st.info("📝 No text content found in the document")
    else:
        analysis = analyze_text_content(text_content)
        
        st.markdown("### 📊 Text Overview")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("📝 Characters", f"{analysis['char_count']:,}")
        
        with col2:
            st.metric("🔤 Words", f"{analysis['word_count']:,}")
        
        with col3:
            st.metric("📄 Sentences", f"{analysis['sentence_count']:,}")
        
        with col4:
            st.metric("📋 Paragraphs", f"{analysis['paragraph_count']:,}")
        
        with col5:
            reading_time = analysis['reading_time_minutes']
            if reading_time < 1:
                time_str = f"{reading_time * 60:.0f}s"
            else:
                time_str = f"{reading_time:.1f}m"
            st.metric("⏱️ Reading Time", time_str)
        
        st.divider()
        

        
        tab1, tab2, tab3 = st.tabs(["📊 Word Analysis", "🔍 Content Extraction", "📄 Full Text"])
        
        with tab1:
            st.markdown("### 📊 Word Frequency Analysis")
            
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔝 Most Frequent Words")
                
                if analysis['filtered_words']:
                    top_words = dict(sorted(analysis['filtered_words'].items(), key=lambda x: x[1], reverse=True)[:20])
                    
                    word_df = pd.DataFrame(list(top_words.items()), columns=['Word', 'Frequency'])
                    word_df['Percentage'] = (word_df['Frequency'] / analysis['word_count'] * 100).round(2)
                    
                    st.dataframe(word_df, use_container_width=True)
                    
                    csv_data = word_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "📥 Download Word Frequency (CSV)",
                        data=csv_data,
                        file_name="word_frequency.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("🔍 No words found for analysis.")
            
            with col2:
                st.markdown("#### 📈 Word Statistics")
                
                unique_words = len(set(analysis['word_freq'].keys()))
                avg_word_length = sum(len(word) * count for word, count in analysis['word_freq'].items()) / analysis['word_count'] if analysis['word_count'] > 0 else 0
                
                st.metric("🔤 Unique Words", f"{unique_words:,}")
                st.metric("📏 Avg Word Length", f"{avg_word_length:.1f} chars")
                st.metric("📊 Vocabulary Richness", f"{(unique_words / analysis['word_count'] * 100):.1f}%" if analysis['word_count'] > 0 else "0%")
                
                if analysis['filtered_words']:
                    fig = px.bar(
                        x=list(dict(sorted(analysis['filtered_words'].items(), key=lambda x: x[1], reverse=True)[:10]).values()),
                        y=list(dict(sorted(analysis['filtered_words'].items(), key=lambda x: x[1], reverse=True)[:10]).keys()),
                        orientation='h',
                        title="Top 10 Words"
                    )
                    template = "plotly_dark" if st.session_state.theme_mode == 'dark' else "plotly_white"
                    fig.update_layout(template=template, height=400)
                    st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### 🔍 Content Extraction")
            
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔢 Numbers Found")
                if analysis['numbers']:
                    st.markdown(f"**Total Numbers:** {len(analysis['numbers'])}")
                    numbers_to_show = analysis['numbers'][:20]
                    st.markdown("**Sample Numbers:**")
                    st.code(", ".join(numbers_to_show))
                    if len(analysis['numbers']) > 20:
                        st.markdown(f"*... and {len(analysis['numbers']) - 20} more*")
                else:
                    st.info("🔍 No numbers found in the text.")
                
                st.markdown("#### 📅 Dates Found")
                if analysis['dates']:
                    st.markdown(f"**Total Dates:** {len(analysis['dates'])}")
                    for date in analysis['dates'][:10]:
                        st.markdown(f"- {date}")
                    if len(analysis['dates']) > 10:
                        st.markdown(f"*... and {len(analysis['dates']) - 10} more*")
                else:
                    st.info("📅 No dates found in the text.")
            
            with col2:
                st.markdown("#### 📧 Email Addresses")
                if analysis['emails']:
                    st.markdown(f"**Total Emails:** {len(analysis['emails'])}")
                    for email in analysis['emails']:
                        st.markdown(f"- {email}")
                else:
                    st.info("📧 No email addresses found.")
                
                st.markdown("#### 🌐 URLs Found")
                if analysis['urls']:
                    st.markdown(f"**Total URLs:** {len(analysis['urls'])}")
                    for url in analysis['urls'][:5]:
                        st.markdown(f"- {url}")
                    if len(analysis['urls']) > 5:
                        st.markdown(f"*... and {len(analysis['urls']) - 5} more*")
                else:
                    st.info("🌐 No URLs found in the text.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown("### 📄 Full Text Content")
            
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    "📥 Download Text (TXT)",
                    data=text_content,
                    file_name="extracted_text.txt",
                    mime="text/plain"
                )
            
            with col2:
                summary = f"""Text Analysis Summary
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

BASIC STATISTICS:
- Characters: {analysis['char_count']:,}
- Words: {analysis['word_count']:,}
- Sentences: {analysis['sentence_count']:,}
- Paragraphs: {analysis['paragraph_count']:,}
- Reading Time: {analysis['reading_time_minutes']:.1f} minutes

FULL TEXT:
{text_content}
"""
                st.download_button(
                    "📊 Download Analysis Report",
                    data=summary,
                    file_name="text_analysis_report.txt",
                    mime="text/plain"
                )
            
            with col3:
                import json
                analysis_json = {
                    'metadata': {
                        'generated_at': datetime.now().isoformat(),
                        'document_name': st.session_state.get('last_uploaded_name', 'Unknown')
                    },
                    'statistics': {
                        'char_count': analysis['char_count'],
                        'word_count': analysis['word_count'],
                        'sentence_count': analysis['sentence_count'],
                        'paragraph_count': analysis['paragraph_count'],
                        'reading_time_minutes': analysis['reading_time_minutes']
                    }
                }
                
                json_data = json.dumps(analysis_json, indent=2).encode('utf-8')
                st.download_button(
                    "📄 Download JSON Report",
                    data=json_data,
                    file_name="text_analysis.json",
                    mime="application/json"
                )
            
            st.text_area("📄 Document Text:", value=text_content, height=400)
            
            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("### 📝 Text Analysis Ready!")
    st.write("Ready to perform deep textual analysis on your documents!")
    
    st.markdown("#### ✨ What You Can Analyze:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📊 Word Analysis**")
        st.write("• Word frequency analysis")
        st.write("• Vocabulary richness metrics")
        st.write("• Statistical insights")
    
    with col2:
        st.markdown("**🔍 Content Extraction**")
        st.write("• Numbers and dates")
        st.write("• Email addresses")
        st.write("• URLs and links")
    
    with col3:
        st.markdown("**📈 Text Metrics**")
        st.write("• Reading time estimation")
        st.write("• Sentence structure analysis")
        st.write("• Document statistics")
    
    st.info("📄 **Upload a Document First** - Go to the Dashboard to upload a document with rich textual content, then return here to start your analysis!")