#!/usr/bin/env python3
"""
Install all required dependencies for the Quantum Portfolio Optimizer backend
"""
import subprocess
import sys

def install_requirements():
    """Install all requirements from requirements.txt"""
    try:
        print("📦 Installing Python dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_critical_imports():
    """Check if critical imports work"""
    critical_modules = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'pydantic_settings',
        'loguru',
        'numpy',
        'pandas',
        'cvxpy',
        'qiskit',
        'pyqubo',
        'neal'
    ]
    
    print("\n🔍 Checking critical imports...")
    failed_imports = []
    
    for module in critical_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️  Failed to import: {', '.join(failed_imports)}")
        print("Try running: pip install -r requirements.txt")
        return False
    else:
        print("\n🎉 All critical modules imported successfully!")
        return True

if __name__ == "__main__":
    print("🚀 Quantum Portfolio Optimizer - Dependency Installation")
    print("=" * 60)
    
    if install_requirements():
        if check_critical_imports():
            print("\n✅ Backend is ready to start!")
            print("Run: python start.py")
        else:
            print("\n❌ Some imports failed. Please check the error messages above.")
    else:
        print("\n❌ Failed to install dependencies. Please check your Python environment.")