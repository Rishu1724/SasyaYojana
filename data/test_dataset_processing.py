"""
Test script to verify that user datasets can be processed correctly.
"""

import pandas as pd
import os
from pathlib import Path
import sys

# Handle encoding issues on Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')

def test_dataset_loading():
    """Test that all user datasets can be loaded correctly"""
    # Define the data directory
    DATA_DIR = Path(__file__).parent
    
    # List of files to test
    files_to_test = [
        "Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc.csv",
        "1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻.csv",
        "All India level Average Yield of Principal Crops from 2001-02 to 2015-16.csv",
        "All India level Area Under Principal Crops from 2001-02 to 2015-16.csv",
        "Production of principle crops.csv",
        "price.csv"
    ]
    
    print("Testing dataset loading...")
    print("=" * 50)
    
    all_loaded = True
    datasets = {}
    
    for file_name in files_to_test:
        try:
            # Construct full file path
            file_path = DATA_DIR / file_name
            
            # Check if file exists
            if not file_path.exists():
                print(f"[MISSING] {file_name}")
                all_loaded = False
                continue
                
            # Try to load the CSV file
            df = pd.read_csv(file_path)
            datasets[file_name] = df
            
            print(f"[LOADED] {file_name}")
            print(f"   Shape: {df.shape}")
            print(f"   Columns: {list(df.columns)[:5]}{'...' if len(df.columns) > 5 else ''}")
            print()
            
        except Exception as e:
            print(f"[ERROR] loading {file_name}: {e}")
            all_loaded = False
            print()
    
    if all_loaded:
        print("[SUCCESS] All datasets loaded successfully!")
    else:
        print("[WARNING] Some datasets failed to load. Please check the errors above.")
    
    return all_loaded, datasets

def test_data_processing(datasets):
    """Test basic processing of loaded datasets"""
    print("\nTesting data processing...")
    print("=" * 50)
    
    # Test NASA POWER data processing
    nasa_key = "1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻.csv"
    if nasa_key in datasets:
        df = datasets[nasa_key]
        print("NASA POWER Data Processing:")
        if 'T2M' in df.columns:
            print(f"   Average Temperature: {df['T2M'].mean():.2f} K")
        if 'RH2M' in df.columns:
            print(f"   Average Humidity: {df['RH2M'].mean():.2f} %")
        if 'PRECTOTCORR' in df.columns:
            # Convert to mm/year
            avg_rainfall = df['PRECTOTCORR'].mean() * 3650
            print(f"   Average Rainfall: {avg_rainfall:.2f} mm/year")
        if 'ALLSKY_SFC_SW_DWN' in df.columns:
            print(f"   Average Solar Radiation: {df['ALLSKY_SFC_SW_DWN'].mean():.2f} W/m²")
        print()
    
    # Test crop yield data processing
    yield_key = "All India level Average Yield of Principal Crops from 2001-02 to 2015-16.csv"
    if yield_key in datasets:
        df = datasets[yield_key]
        print("Crop Yield Data Processing:")
        print(f"   Number of crops: {len(df)}")
        if 'Crop' in df.columns:
            print(f"   Sample crops: {list(df['Crop'])[:5]}")
        print()
    
    # Test price data processing
    price_key = "price.csv"
    if price_key in datasets:
        df = datasets[price_key]
        print("Price Data Processing:")
        print(f"   Data shape: {df.shape}")
        print(f"   Column names: {list(df.columns)[:5]}")
        print()

if __name__ == "__main__":
    print("Sasya-Mitra Dataset Processing Test")
    print("====================================")
    
    # Test dataset loading
    success, datasets = test_dataset_loading()
    
    if success:
        # Test data processing
        test_data_processing(datasets)
        
        print("[SUCCESS] All tests completed successfully!")
        print("\nNext steps:")
        print("1. Run 'npm run model:process-data' to process your datasets")
        print("2. Run 'npm run model:train-user' to train AI models with your data")
    else:
        print("[FAILURE] Tests failed. Please check your dataset files.")