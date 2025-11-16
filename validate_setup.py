#!/usr/bin/env python3
"""
Setup validation script for ArixStructure
"""
import os
import sys

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check required packages"""
    required = [
        'streamlit', 'pandas', 'plotly', 'requests', 
        'pdfplumber', 'fitz', 'docx', 'pptx', 'bs4'
    ]
    
    missing = []
    for pkg in required:
        try:
            if pkg == 'fitz':
                import fitz
            elif pkg == 'docx':
                import docx
            elif pkg == 'pptx':
                from pptx import Presentation
            elif pkg == 'bs4':
                from bs4 import BeautifulSoup
            else:
                __import__(pkg)
            print(f"✅ {pkg}")
        except ImportError:
            missing.append(pkg)
            print(f"❌ {pkg}")
    
    return len(missing) == 0

def check_token():
    """Check HF token configuration"""
    secrets_file = ".streamlit/secrets.toml"
    env_token = os.getenv("HF_TOKEN")
    
    if os.path.exists(secrets_file):
        try:
            with open(secrets_file, 'r') as f:
                content = f.read()
                if 'HF_TOKEN' in content and 'hf_' in content:
                    print("✅ HF Token configured in secrets.toml")
                    return True
        except:
            pass
    
    if env_token and env_token.startswith('hf_'):
        print("✅ HF Token configured in environment")
        return True
    
    print("⚠️  HF Token not configured (AI features limited)")
    return False

def main():
    print("🔍 ArixStructure Setup Validation")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("HF Token", check_token)
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n{name}:")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 Setup validation passed! Ready to run ArixStructure.")
        print("Run: python start.py")
    else:
        print("❌ Setup issues found. Please fix them before running.")
        print("See SETUP_GUIDE.md for help.")

if __name__ == "__main__":
    main()