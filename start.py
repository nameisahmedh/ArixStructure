#!/usr/bin/env python3
"""
Simple launcher for ArixStructure application
"""
import subprocess
import sys
import os

def main():
    print("🏗️ ArixStructure - Document Structure Analyzer")
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
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Launch the app
    print("\n🚀 Starting ArixStructure...")
    print("📝 The application will open in your default web browser")
    print("🛑 Press Ctrl+C to stop the application\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()