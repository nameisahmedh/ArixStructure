#!/usr/bin/env python3
"""
Test Hugging Face token and API connectivity
"""
import os
import requests
import streamlit as st

def test_hf_token():
    """Test if HF token is working"""
    print("🔍 Testing Hugging Face Token...")
    
    # Get token
    try:
        token = st.secrets["HF_TOKEN"]
        print("✅ Token found in secrets.toml")
    except:
        token = os.getenv("HF_TOKEN")
        if token:
            print("✅ Token found in environment")
        else:
            print("❌ No HF_TOKEN found")
            return False
    
    if not token or not token.startswith('hf_'):
        print("❌ Invalid token format (should start with 'hf_')")
        return False
    
    print(f"✅ Token format valid: {token[:10]}...")
    
    # Test API connectivity
    headers = {"Authorization": f"Bearer {token}"}
    
    # Try latest working models
    test_models = [
        "microsoft/DialoGPT-medium",
        "facebook/blenderbot_small-90M",
        "HuggingFaceH4/zephyr-7b-beta",
        "facebook/opt-350m",
        "sshleifer/distilbart-cnn-12-6"
    ]
    
    for model in test_models:
        try:
            print(f"🧪 Testing model: {model}")
            url = f"https://api-inference.huggingface.co/models/{model}"
            
            response = requests.post(
                url,
                headers=headers,
                json={"inputs": "Hello, how are you?"},
                timeout=10
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ {model} is working!")
                return True
            elif response.status_code == 503:
                print(f"⏳ {model} is loading...")
            elif response.status_code == 410:
                print(f"❌ {model} is deprecated")
            else:
                print(f"❌ {model} error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {model} failed: {e}")
    
    print("❌ No working models found")
    return False

if __name__ == "__main__":
    success = test_hf_token()
    if success:
        print("\n🎉 HF Token is working! AI features should be available.")
    else:
        print("\n❌ HF Token issues detected. AI features will be limited.")
        print("\n💡 Solutions:")
        print("1. Get token at: https://huggingface.co/settings/tokens")
        print("2. Add to .streamlit/secrets.toml: HF_TOKEN = \"hf_your_token\"")
        print("3. Or set environment: export HF_TOKEN=\"hf_your_token\"")