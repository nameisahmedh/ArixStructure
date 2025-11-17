#!/usr/bin/env python3
"""
Test Google Gemini API key and connectivity
"""
import os
import streamlit as st
import google.generativeai as genai

def test_gemini_api():
    """Test if Gemini API key is working"""
    print("🔍 Testing Google Gemini API Key...")

    # Get API key
    api_key = None
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        print("✅ API Key found in secrets.toml")
    except (KeyError, AttributeError, st.errors.StreamlitSecretNotFoundError):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            print("✅ API Key found in environment")
        else:
            print("❌ No GEMINI_API_KEY found")
            return False

    if not api_key:
        print("❌ Invalid API key format.")
        return False

    print(f"✅ API Key format valid: {api_key[:8]}...")

    # Test API connectivity
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello, how are you?")

        if response.text and len(response.text) > 5:
            print("✅ Gemini API is working!")
            return True
        else:
            print("❌ Gemini API returned an empty response.")
            return False

    except Exception as e:
        print(f"❌ Gemini API failed: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini_api()
    if success:
        print("\n🎉 Gemini API Key is working! AI features should be available.")
    else:
        print("\n❌ Gemini API Key issues detected. AI features will be limited.")
        print("\n💡 Solutions:")
        print("1. Get API key at: https://aistudio.google.com/apikey")
        print("2. Add to .streamlit/secrets.toml: GEMINI_API_KEY = \"your_gemini_api_key\"")
        print("3. Or set environment: export GEMINI_API_KEY=\"your_gemini_api_key\"")
