import streamlit as st

# Test import
try:
    import llm_handler
    st.success("✅ llm_handler imported successfully!")
    st.write("Available functions:")
    st.write("- get_text_response")
    st.write("- get_image_descriptions") 
    st.write("- get_image_query_response")
    st.write("- get_specific_table_indices")
except Exception as e:
    st.error(f"❌ Import failed: {e}")
    st.write("Error details:", str(e))