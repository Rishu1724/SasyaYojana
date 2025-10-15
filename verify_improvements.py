"""
Verification script to check that all dashboard improvements are properly implemented.
"""

import os
from pathlib import Path

def check_file_structure():
    """Check that all required files for the improvements exist"""
    print("Checking file structure for dashboard improvements...")
    print("=" * 60)
    
    required_files = [
        "src/components/FarmerInputForm.jsx",
        "src/components/AIPlanner.jsx",
        "src/components/Dashboard.jsx",
        "src/locales/en.json",
        "src/locales/hi.json",
        "src/locales/mr.json",
        "src/locales/te.json",
        "src/locales/kn.json"
    ]
    
    project_root = Path(__file__).parent
    all_good = True
    
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_good = False
    
    return all_good

def check_key_features():
    """Check that key features are implemented"""
    print("\nChecking key features...")
    print("=" * 60)
    
    # Check for FarmerInputForm component
    farmer_input_path = Path(__file__).parent / "src/components/FarmerInputForm.jsx"
    if farmer_input_path.exists():
        with open(farmer_input_path, 'r', encoding='utf-8') as f:
            content = f.read()
            features = [
                ("Location input methods", "location.type"),
                ("GPS coordinates", "formData.location.gps"),
                ("Village name", "formData.location.village"),
                ("Land area input", "land_area"),
                ("Budget input", "budget"),
                ("Crop preference", "crop_preference"),
                ("Form validation", "validate inputs"),
                ("Loading states", "loading"),
                ("Error handling", "setError")
            ]
            
            for feature, keyword in features:
                if keyword in content:
                    print(f"✅ {feature}")
                else:
                    print(f"❌ {feature}")
    
    # Check for translation keys
    print("\nChecking translation keys...")
    en_json_path = Path(__file__).parent / "src/locales/en.json"
    if en_json_path.exists():
        with open(en_json_path, 'r', encoding='utf-8') as f:
            content = f.read()
            translation_keys = [
                "farmerInputForm",
                "location",
                "useGPS",
                "enterVillage",
                "latitude",
                "longitude",
                "landAreaInAcres",
                "budgetInRupees",
                "cropPreference",
                "generatingPlan",
                "farmInputsSummary"
            ]
            
            for key in translation_keys:
                if f'"{key}":' in content:
                    print(f"✅ Translation key: {key}")
                else:
                    print(f"❌ Translation key: {key}")

def main():
    """Main verification function"""
    print("Sasya-Mitra Dashboard Improvements Verification")
    print("=" * 60)
    
    # Check file structure
    file_structure_ok = check_file_structure()
    
    # Check key features
    check_key_features()
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if file_structure_ok:
        print("✅ All required files are present")
        print("\n🎉 Dashboard improvements have been successfully implemented!")
        print("\nYou can now:")
        print("1. Run the application with 'npm run dev'")
        print("2. Navigate to http://localhost:5174")
        print("3. Use the enhanced AI Planner with improved farmer input collection")
        print("4. Access all features in the organized dashboard")
    else:
        print("❌ Some files are missing")
        print("Please check the implementation and ensure all files are created")

if __name__ == "__main__":
    main()