"""
Smart Document Analyzer - Launcher Script
This script helps launch the application with proper error handling and setup validation.
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'streamlit', 'pandas', 'pdfplumber', 'fitz', 'PIL', 
        'docx', 'pptx', 'bs4', 'huggingface_hub', 'requests', 'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        # Handle special cases
        if package == 'fitz':
            package_name = 'PyMuPDF'
        elif package == 'PIL':
            package_name = 'Pillow'
        elif package == 'docx':
            package_name = 'python-docx'
        elif package == 'pptx':
            package_name = 'python-pptx'
        elif package == 'bs4':
            package_name = 'beautifulsoup4'
        else:
            package_name = package
            
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append(package_name)
        else:
            print(f"✅ {package_name}")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    return True

def check_secrets():
    """Check if Hugging Face token is configured."""
    secrets_path = ".streamlit/secrets.toml"
    
    if not os.path.exists(secrets_path):
        print(f"❌ Missing secrets file: {secrets_path}")
        print("Create the file and add your Hugging Face token:")
        print('HF_TOKEN = "your_token_here"')
        return False
    
    try:
        with open(secrets_path, 'r') as f:
            content = f.read()
            if 'HF_TOKEN' in content:
                print("✅ Hugging Face token configured")
                return True
            else:
                print("❌ HF_TOKEN not found in secrets.toml")
                return False
    except Exception as e:
        print("❌ Error reading secrets file")
        return False

def create_temp_directory():
    """Ensure temp_images directory exists."""
    if not os.path.exists("temp_images"):
        os.makedirs("temp_images")
        print("✅ Created temp_images directory")
    else:
        print("✅ temp_images directory exists")

def launch_app(app_file="app.py"):
    """Launch the Streamlit application."""
    if not os.path.exists(app_file):
        print(f"❌ Application file not found: {app_file}")
        return False
    
    print(f"\n🚀 Launching {app_file}...")
    print("📝 The application will open in your default web browser")
    print("🛑 Press Ctrl+C to stop the application\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_file], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError:
        print("❌ Error launching application")
        return False
    except FileNotFoundError:
        print("❌ Streamlit not found. Install it with: pip install streamlit")
        return False
    except Exception:
        print("❌ Unexpected error occurred while launching application")
        return False
    
    return True

def main():
    """Main launcher function."""
    print("📊 Smart Document Analyzer - Setup Validator")
    print("=" * 50)
    
    # Check system requirements
    print("\n🔍 Checking system requirements...")
    if not check_python_version():
        return
    
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        return
    
    print("\n🔐 Checking configuration...")
    if not check_secrets():
        return
    
    print("\n📁 Setting up directories...")
    create_temp_directory()
    
    print("\n✅ All checks passed!")
    
    # Launch the application
    launch_app("app.py")

if __name__ == "__main__":
    main()