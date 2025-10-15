"""
Script to help install required Python dependencies for Sasya-Mitra.
"""

import subprocess
import sys

def install_package(package):
    """Install a Python package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"[SUCCESS] Installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install {package}: {e}")
        return False

def check_package(package):
    """Check if a Python package is installed"""
    try:
        __import__(package)
        print(f"[INSTALLED] {package}")
        return True
    except ImportError:
        print(f"[MISSING] {package}")
        return False

def main():
    """Main function to install dependencies"""
    print("Sasya-Mitra Dependency Installer")
    print("=" * 40)
    
    # List of required packages
    required_packages = [
        "pandas",
        "numpy",
        "scikit-learn",
        "xgboost",
        "joblib"
    ]
    
    # Check which packages are already installed
    print("Checking installed packages...")
    missing_packages = []
    
    for package in required_packages:
        if not check_package(package):
            missing_packages.append(package)
    
    # Install missing packages
    if missing_packages:
        print(f"\nInstalling {len(missing_packages)} missing packages...")
        print("-" * 40)
        
        for package in missing_packages:
            install_package(package)
        
        print("\n[COMPLETE] Dependency installation finished!")
    else:
        print("\n[SUCCESS] All required packages are already installed!")
    
    print("\nNext steps:")
    print("1. Place your dataset CSV files in the 'data/' directory")
    print("2. Run 'python data/test_dataset_processing.py' to verify datasets")
    print("3. Run 'npm run model:train-user' to train AI models with your data")

if __name__ == "__main__":
    main()