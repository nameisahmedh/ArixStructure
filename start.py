#!/usr/bin/env python3
"""
Quick launcher for ArixStructure application
"""
import subprocess
import sys
import os

def main():
    print("🏗️ ArixStructure - AI Document Analyzer")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found in current directory")
        print("Please run this script from the project directory")
        return
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit found")
    except ImportError:
        print("❌ Streamlit not installed")
        print("Installing dependencies...")
        if not os.path.exists("requirements.txt"):
            print("❌ requirements.txt not found")
            return
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return
    
    # Check for HF token
    secrets_file = ".streamlit/secrets.toml"
    if not os.path.exists(secrets_file):
        print("⚠️  Warning: Hugging Face token not configured")
        print("Create .streamlit/secrets.toml with your HF token for AI features")
        print("Get token at: https://huggingface.co/settings/tokens")
    
    # Launch the app
    print("\n🚀 Starting ArixStructure...")
    print("📝 The application will open in your default web browser")
    print("🛑 Press Ctrl+C to stop the application\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting application: {e}")
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it first.")

if __name__ == "__main__":
    main()