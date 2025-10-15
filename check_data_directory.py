"""
Script to check the data directory and provide instructions for placing datasets.
"""

import os
from pathlib import Path

def check_data_directory():
    """Check the data directory and list required files"""
    # Define the data directory
    DATA_DIR = Path(__file__).parent / "data"
    
    print("Sasya-Mitra Data Directory Check")
    print("=" * 40)
    
    # Check if data directory exists
    if not DATA_DIR.exists():
        print("[ERROR] Data directory not found!")
        print("Please create a 'data' directory in the project root.")
        return False
    
    print(f"[SUCCESS] Data directory found: {DATA_DIR}")
    
    # List of required files
    required_files = [
        "Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc.csv",
        "1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻.csv",
        "All India level Average Yield of Principal Crops from 2001-02 to 2015-16.csv",
        "All India level Area Under Principal Crops from 2001-02 to 2015-16.csv",
        "Production of principle crops.csv",
        "price.csv"
    ]
    
    print("\nRequired dataset files:")
    print("-" * 30)
    
    missing_files = []
    found_files = []
    
    for file_name in required_files:
        file_path = DATA_DIR / file_name
        if file_path.exists():
            print(f"[FOUND] {file_name}")
            found_files.append(file_name)
        else:
            print(f"[MISSING] {file_name}")
            missing_files.append(file_name)
    
    print(f"\nSummary:")
    print(f"  Found: {len(found_files)} files")
    print(f"  Missing: {len(missing_files)} files")
    
    if missing_files:
        print(f"\nPlease place the following files in the data directory:")
        for file_name in missing_files:
            print(f"  - {file_name}")
        
        print(f"\nData directory path: {DATA_DIR}")
        print(f"You can copy files to this directory using File Explorer or command line.")
        
        return False
    else:
        print(f"\n[SUCCESS] All required dataset files are present!")
        return True

if __name__ == "__main__":
    check_data_directory()