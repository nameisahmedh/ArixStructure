#!/usr/bin/env python3
"""
Test script to verify ArixStructure setup
"""
import sys
import os

def test_python_version():
    """Test Python version"""
    print("🐍 Testing Python version...")
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required, found {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def test_imports():
    """Test required imports"""
    print("\n📦 Testing imports...")
    
    required_modules = [
        ('streamlit', 'streamlit'),
        ('pandas', 'pandas'),
        ('plotly', 'plotly.express'),
        ('pdfplumber', 'pdfplumber'),
        ('fitz', 'PyMuPDF'),
        ('PIL', 'Pillow'),
        ('docx', 'python-docx'),
        ('pptx', 'python-pptx'),
        ('bs4', 'beautifulsoup4'),
        ('huggingface_hub', 'huggingface-hub'),
        ('requests', 'requests'),
        ('openpyxl', 'openpyxl'),
        ('reportlab', 'reportlab')
    ]
    
    missing = []
    
    for module, package in required_modules:
        try:
            __import__(module)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True

def test_files():
    """Test required files exist"""
    print("\n📁 Testing files...")
    
    required_files = [
        'app.py',
        'utils.py', 
        'parser.py',
        'llm_handler.py',
        'requirements.txt',
        '.streamlit/secrets.toml'
    ]
    
    missing = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        return False
    
    return True

def test_secrets():
    """Test Hugging Face token configuration"""
    print("\n🔐 Testing secrets configuration...")
    
    try:
        with open('.streamlit/secrets.toml', 'r') as f:
            content = f.read()
            if 'HF_TOKEN' in content and len(content.strip()) > 20:
                print("✅ Hugging Face token configured")
                return True
            else:
                print("❌ HF_TOKEN not found or invalid")
                print("Please add your Hugging Face token to .streamlit/secrets.toml")
                return False
    except Exception as e:
        print(f"❌ Error reading secrets: {e}")
        return False

def main():
    """Run all tests"""
    print("🏗️ ArixStructure Setup Test")
    print("=" * 40)
    
    tests = [
        test_python_version,
        test_imports,
        test_files,
        test_secrets
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 40)
    
    if all(results):
        print("🎉 All tests passed! ArixStructure is ready to run.")
        print("\nTo start the application:")
        print("  • Double-click run.bat")
        print("  • Or run: python start.py")
        print("  • Or run: streamlit run app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nFor help:")
        print("  • Check README.md")
        print("  • Run: pip install -r requirements.txt")
        print("  • Configure .streamlit/secrets.toml")
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()