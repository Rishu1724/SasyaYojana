"""
Verification script to check that Sasya-Mitra is properly set up with your datasets.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file_structure():
    """Check that all required files and directories exist"""
    print("Checking file structure...")
    print("=" * 40)
    
    required_paths = [
        "data/",
        "data/Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc.csv",
        "data/1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻.csv",
        "data/All India level Average Yield of Principal Crops from 2001-02 to 2015-16.csv",
        "data/All India level Area Under Principal Crops from 2001-02 to 2015-16.csv",
        "data/Production of principle crops.csv",
        "data/price.csv",
        "models/",
        "models/training/",
        "models/preprocessing/",
        "models/api/",
        "src/",
        "src/utils/datasetHelper.js"
    ]
    
    all_good = True
    project_root = Path(__file__).parent
    
    for path in required_paths:
        full_path = project_root / path
        if full_path.exists():
            print(f"✅ Found: {path}")
        else:
            print(f"❌ Missing: {path}")
            all_good = False
    
    return all_good

def check_python_dependencies():
    """Check that required Python packages are installed"""
    print("\nChecking Python dependencies...")
    print("=" * 40)
    
    required_packages = [
        "pandas",
        "numpy",
        "scikit-learn",
        "xgboost",
        "joblib"
    ]
    
    all_good = True
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is not installed")
            all_good = False
    
    if not all_good:
        print("\nInstall missing packages with:")
        print("pip install pandas numpy scikit-learn xgboost joblib")
    
    return all_good

def check_node_dependencies():
    """Check that required Node packages are installed"""
    print("\nChecking Node dependencies...")
    print("=" * 40)
    
    try:
        # Check if node_modules exists
        node_modules_path = Path(__file__).parent / "node_modules"
        if node_modules_path.exists():
            print("✅ Node dependencies are installed")
            return True
        else:
            print("❌ Node dependencies are not installed")
            print("Install them with: npm install")
            return False
    except Exception as e:
        print(f"❌ Error checking Node dependencies: {e}")
        return False

def test_dataset_processing():
    """Test that dataset processing works"""
    print("\nTesting dataset processing...")
    print("=" * 40)
    
    try:
        # Run the test script
        result = subprocess.run([
            sys.executable, 
            "data/test_dataset_processing.py"
        ], cwd=Path(__file__).parent, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Dataset processing test passed")
            print("Sample output:")
            lines = result.stdout.split('\n')
            for line in lines[:10]:  # Show first 10 lines
                if line.strip():
                    print(f"  {line}")
            return True
        else:
            print("❌ Dataset processing test failed")
            print("Error output:")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("❌ Dataset processing test timed out")
        return False
    except Exception as e:
        print(f"❌ Error running dataset processing test: {e}")
        return False

def show_next_steps():
    """Show recommended next steps"""
    print("\n" + "=" * 50)
    print("NEXT STEPS")
    print("=" * 50)
    print("1. Process your datasets:")
    print("   npm run model:process-data")
    print()
    print("2. Train AI models with your data:")
    print("   npm run model:train-user")
    print()
    print("3. Start the web application:")
    print("   npm run dev")
    print()
    print("4. Access the application at http://localhost:5173")

def main():
    """Main verification function"""
    print("Sasya-Mitra Setup Verification")
    print("=" * 50)
    
    # Check file structure
    file_structure_ok = check_file_structure()
    
    # Check Python dependencies
    python_deps_ok = check_python_dependencies()
    
    # Check Node dependencies
    node_deps_ok = check_node_dependencies()
    
    # Test dataset processing
    dataset_processing_ok = test_dataset_processing()
    
    # Summary
    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)
    print(f"File structure: {'✅ OK' if file_structure_ok else '❌ Issues found'}")
    print(f"Python dependencies: {'✅ OK' if python_deps_ok else '❌ Issues found'}")
    print(f"Node dependencies: {'✅ OK' if node_deps_ok else '❌ Issues found'}")
    print(f"Dataset processing: {'✅ OK' if dataset_processing_ok else '❌ Issues found'}")
    
    all_checks_passed = file_structure_ok and python_deps_ok and node_deps_ok and dataset_processing_ok
    
    if all_checks_passed:
        print("\n🎉 All checks passed! Your Sasya-Mitra setup is ready.")
        show_next_steps()
    else:
        print("\n⚠️  Some checks failed. Please address the issues above.")
        print("Refer to the documentation for detailed setup instructions.")

if __name__ == "__main__":
    main()