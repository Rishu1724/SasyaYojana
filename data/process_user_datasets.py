import pandas as pd
import numpy as np
import os
from pathlib import Path

# Dictionary to store all loaded DataFrames
datasets = {}

# Define the data directory
DATA_DIR = Path(__file__).parent

# List of files to load with their exact names
files_to_load = [
    "Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc.csv",
    "1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻.csv",
    "All India level Average Yield of Principal Crops from 2001-02 to 2015-16.csv",
    "All India level Area Under Principal Crops from 2001-02 to 2015-16.csv",
    "Production of principle crops.csv",
    "price.csv"
]

def load_datasets():
    """Load all CSV files into the datasets dictionary"""
    for file_name in files_to_load:
        try:
            # Construct full file path
            file_path = DATA_DIR / file_name
            
            # Check if file exists
            if not file_path.exists():
                print(f"Warning: File not found - {file_name}")
                continue
                
            # Use the file name (without the extension) as the key
            key = file_name.replace(".csv", "")
            datasets[key] = pd.read_csv(file_path)
            print(f"Successfully loaded: {file_name}")
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
    
    return datasets

def process_nasa_power_data():
    """Process NASA POWER data specifically"""
    key = "1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻"
    if key not in datasets:
        print("NASA POWER data not found")
        return None
    
    df = datasets[key]
    print("\\n--- NASA POWER Data Info ---")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\\nFirst few rows:")
    print(df.head())
    
    # Process the data according to our existing framework
    processed_data = {
        'avg_temperature_c': df['T2M'].mean() if 'T2M' in df.columns else 0,
        'avg_humidity': df['RH2M'].mean() if 'RH2M' in df.columns else 0,
        'avg_rainfall_mm': (df['PRECTOTCORR'].mean() * 3650) if 'PRECTOTCORR' in df.columns else 0,
        'solar_radiation': df['ALLSKY_SFC_SW_DWN'].mean() if 'ALLSKY_SFC_SW_DWN' in df.columns else 0,
        'data_points': len(df)
    }
    
    return processed_data

def process_crop_yield_data():
    """Process crop yield data"""
    key = "All India level Average Yield of Principal Crops from 2001-02 to 2015-16"
    if key not in datasets:
        print("Crop yield data not found")
        return None
    
    df = datasets[key]
    print("\\n--- Crop Yield Data Info ---")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\\nFirst few rows:")
    print(df.head())
    
    # Melt the dataframe to get year-wise data
    if 'Crop' in df.columns:
        melted_df = df.melt(id_vars=['Crop'], var_name='Year', value_name='Yield')
        return melted_df
    return df

def process_crop_area_data():
    """Process crop area data"""
    key = "All India level Area Under Principal Crops from 2001-02 to 2015-16"
    if key not in datasets:
        print("Crop area data not found")
        return None
    
    df = datasets[key]
    print("\\n--- Crop Area Data Info ---")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\\nFirst few rows:")
    print(df.head())
    
    # Melt the dataframe to get year-wise data
    if 'Crop' in df.columns:
        melted_df = df.melt(id_vars=['Crop'], var_name='Year', value_name='Area')
        return melted_df
    return df

def process_crop_production_data():
    """Process crop production data"""
    key = "Production of principle crops"
    if key not in datasets:
        print("Crop production data not found")
        return None
    
    df = datasets[key]
    print("\\n--- Crop Production Data Info ---")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\\nFirst few rows:")
    print(df.head())
    
    # Melt the dataframe to get year-wise data
    if 'Crop' in df.columns:
        melted_df = df.melt(id_vars=['Crop'], var_name='Year', value_name='Production')
        return melted_df
    return df

def process_price_data():
    """Process crop price data"""
    key = "price"
    if key not in datasets:
        print("Price data not found")
        return None
    
    df = datasets[key]
    print("\\n--- Price Data Info ---")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\\nFirst few rows:")
    print(df.head())
    
    return df

def process_damage_data():
    """Process damage data from natural disasters"""
    key = "Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc"
    if key not in datasets:
        print("Damage data not found")
        return None
    
    df = datasets[key]
    print("\\n--- Damage Data Info ---")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\\nFirst few rows:")
    print(df.head())
    
    return df

def create_combined_dataset():
    """Combine all datasets for ML modeling"""
    # Load all datasets
    load_datasets()
    
    # Process individual datasets
    nasa_data = process_nasa_power_data()
    yield_data = process_crop_yield_data()
    area_data = process_crop_area_data()
    production_data = process_crop_production_data()
    price_data = process_price_data()
    damage_data = process_damage_data()
    
    # Combine datasets for modeling
    print("\\n--- Creating Combined Dataset ---")
    
    # Example of how to combine datasets (this would need to be adjusted based on actual data structure)
    combined_features = {}
    
    # Add NASA POWER features
    if nasa_data:
        combined_features.update(nasa_data)
    
    # Add some sample features from other datasets
    if yield_data is not None and len(yield_data) > 0:
        combined_features['avg_yield'] = yield_data['Yield'].mean() if 'Yield' in yield_data.columns else 0
    
    if area_data is not None and len(area_data) > 0:
        combined_features['avg_area'] = area_data['Area'].mean() if 'Area' in area_data.columns else 0
        
    if production_data is not None and len(production_data) > 0:
        combined_features['avg_production'] = production_data['Production'].mean() if 'Production' in production_data.columns else 0
    
    print("Combined features for modeling:")
    for key, value in combined_features.items():
        print(f"  {key}: {value}")
    
    return combined_features

if __name__ == "__main__":
    print("Processing user datasets for Sasya-Mitra AI system...")
    
    # Load all datasets
    load_datasets()
    
    # Print summary of loaded datasets
    print("\\n--- Loaded Datasets Keys ---")
    print(list(datasets.keys()))
    
    # Process each dataset
    process_nasa_power_data()
    process_crop_yield_data()
    process_crop_area_data()
    process_crop_production_data()
    process_price_data()
    process_damage_data()
    
    # Create combined dataset
    combined_features = create_combined_dataset()
    
    print("\\n--- Processing Complete ---")
    print("Datasets are ready for ML model training!")