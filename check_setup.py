#!/usr/bin/env python3
"""
Quick system check script
Run this to verify your setup is complete
"""

import os
import sys

def check_file(path, required=True):
    """Check if a file exists"""
    exists = os.path.exists(path)
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "(required)" if required else "(optional)"
    print(f"{status} {path} {req_text}")
    return exists

def check_env_var(var_name, required=True):
    """Check if environment variable is set"""
    # Try to load from .env
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, _, _ = line.partition('=')
                    if key.strip() == var_name:
                        status = "✅"
                        print(f"{status} {var_name} - configured in .env")
                        return True
    
    status = "❌" if required else "⚠️"
    req_text = "(required)" if required else "(optional)"
    print(f"{status} {var_name} - not found {req_text}")
    return False

def check_python_package(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        print(f"✅ {package_name} - installed")
        return True
    except ImportError:
        print(f"❌ {package_name} - not installed")
        return False

def main():
    print("=" * 60)
    print("WhatsApp CV Manager - System Check")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Check Python version
    print("Python Version:")
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"⚠️ Python {version.major}.{version.minor}.{version.micro} (3.11+ recommended)")
        all_ok = False
    print()
    
    # Check required files
    print("Required Files:")
    all_ok &= check_file('manage.py', required=True)
    all_ok &= check_file('requirements.txt', required=True)
    all_ok &= check_file('.env', required=True)
    all_ok &= check_file('credentials.json', required=True)
    all_ok &= check_file('cv_manager/settings.py', required=True)
    all_ok &= check_file('webhook/views.py', required=True)
    print()
    
    # Check optional files
    print("Optional Files:")
    check_file('Procfile', required=False)
    check_file('railway.json', required=False)
    check_file('Makefile', required=False)
    print()
    
    # Check environment variables
    print("Environment Variables:")
    all_ok &= check_env_var('GEMINI_API_KEY', required=True)
    all_ok &= check_env_var('WHATSAPP_ACCESS_TOKEN', required=True)
    all_ok &= check_env_var('WHATSAPP_PHONE_NUMBER_ID', required=True)
    all_ok &= check_env_var('WHATSAPP_VERIFY_TOKEN', required=True)
    all_ok &= check_env_var('GOOGLE_SHEET_ID', required=True)
    check_env_var('DJANGO_SECRET_KEY', required=False)
    print()
    
    # Check Python packages
    print("Python Packages:")
    packages = [
        'django',
        'requests',
        'gspread',
        'oauth2client',
        'PyPDF2',
    ]
    
    for package in packages:
        pkg_ok = check_python_package(package)
        all_ok &= pkg_ok
    
    # Special check for google.generativeai
    try:
        import google.generativeai
        print(f"✅ google.generativeai - installed")
    except ImportError:
        print(f"❌ google.generativeai - not installed")
        all_ok = False
    
    print()
    print("=" * 60)
    
    if all_ok:
        print("✅ All checks passed! You're ready to go.")
        print()
        print("Next steps:")
        print("1. Run: python manage.py migrate")
        print("2. Run: python manage.py runserver")
        print("3. In another terminal: ngrok http 8000")
        print("4. Configure WhatsApp webhook")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print()
        print("Common fixes:")
        print("1. Install packages: pip install -r requirements.txt")
        print("2. Create .env: cp .env.example .env (then edit)")
        print("3. Add credentials.json from Google Cloud Console")
    
    print()
    print("For detailed help, see:")
    print("  - README.md")
    print("  - QUICKSTART.md")
    print("  - FAQ.md")
    print()

if __name__ == '__main__':
    main()
