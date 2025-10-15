"""
Example script showing how to train models with your datasets.
"""

import pandas as pd
import numpy as np
import os
import sys

# Add the current directory to the path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from preprocessing.data_processor import AgriDataPreprocessor
from training.model_trainer import AgriYieldModel, AgriROIModel

def load_user_datasets():
    """
    Load your actual agricultural datasets.
    """
    print("Loading your agricultural datasets...")
    
    # Define the data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    
    # Dictionary to store all loaded DataFrames
    datasets = {}
    
    # List of files to load with their exact names
    files_to_load = [
        "Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc.csv",
        "1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻.csv",
        "All India level Average Yield of Principal Crops from 2001-02 to 2015-16.csv",
        "All India level Area Under Principal Crops from 2001-02 to 2015-16.csv",
        "Production of principle crops.csv",
        "price.csv"
    ]
    
    for file_name in files_to_load:
        try:
            # Construct full file path
            file_path = os.path.join(data_dir, file_name)
            
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"Warning: File not found - {file_name}")
                continue
                
            # Use the file name (without the extension) as the key
            key = file_name.replace(".csv", "")
            datasets[key] = pd.read_csv(file_path)
            print(f"Successfully loaded: {file_name}")
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
    
    return datasets

def load_and_preprocess_data():
    """
    Load and preprocess your agricultural datasets.
    """
    print("Loading and preprocessing datasets...")
    
    # Load user datasets
    datasets = load_user_datasets()
    
    if not datasets:
        print("No datasets loaded. Creating sample data for demonstration.")
        return create_sample_data()
    
    # Initialize preprocessor
    preprocessor = AgriDataPreprocessor()
    
    # Process each dataset
    processed_datasets = {}
    
    # Process NASA POWER data
    nasa_key = "1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻"
    if nasa_key in datasets:
        processed_datasets['nasa_power'] = preprocessor.load_nasa_power_data(datasets[nasa_key])
    
    # Process crop price data
    if "price" in datasets:
        processed_datasets['price'] = preprocessor.load_crop_price_data(datasets["price"])
    
    # Process yield data
    yield_key = "All India level Average Yield of Principal Crops from 2001-02 to 2015-16"
    if yield_key in datasets:
        processed_datasets['yield'] = preprocessor.load_yield_data(datasets[yield_key])
    
    # Process area data
    area_key = "All India level Area Under Principal Crops from 2001-02 to 2015-16"
    if area_key in datasets:
        processed_datasets['area'] = preprocessor.load_area_data(datasets[area_key])
    
    # Process production data
    if "Production of principle crops" in datasets:
        processed_datasets['production'] = preprocessor.load_production_data(datasets["Production of principle crops"])
    
    # Process damage data
    damage_key = "Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc"
    if damage_key in datasets:
        processed_datasets['damage'] = preprocessor.load_damage_data(datasets[damage_key])
    
    # Create features
    features = preprocessor.create_features(
        processed_datasets.get('nasa_power'),
        processed_datasets.get('price'),
        processed_datasets.get('yield'),
        processed_datasets.get('area'),
        processed_datasets.get('production'),
        processed_datasets.get('damage')
    )
    
    return features, datasets

def create_sample_data():
    """
    Create sample data for demonstration when user datasets are not available.
    """
    print("Creating sample data for demonstration...")
    
    # Sample NASA POWER data
    nasa_data = pd.DataFrame({
        'YEAR': [2010, 2011, 2012, 2013, 2014, 2015],
        'T2M': [26.5, 27.1, 26.8, 27.3, 26.9, 27.0],
        'RH2M': [62.1, 63.5, 61.8, 64.2, 62.7, 63.0],
        'PRECTOTCORR': [0.005, 0.006, 0.004, 0.007, 0.005, 0.006],  # kg/m2/s
        'ALLSKY_SFC_SW_DWN': [5.2, 5.4, 5.1, 5.6, 5.3, 5.2]
    })
    
    # Sample crop price data
    price_data = pd.DataFrame({
        'YEAR': [2010, 2011, 2012, 2013, 2014, 2015],
        'MAIZE_PRICE': [1800, 1900, 1850, 1950, 1880, 1920],
        'COWPEA_PRICE': [4500, 4700, 4600, 4800, 4650, 4750],
        'MANGO_PRICE': [50, 55, 52, 58, 54, 56]
    })
    
    # Sample yield data
    yield_data = pd.DataFrame({
        'YEAR': [2010, 2011, 2012, 2013, 2014, 2015],
        'MAIZE_YIELD': [3800, 3900, 3850, 3950, 3880, 3920],
        'COWPEA_YIELD': [900, 950, 920, 980, 940, 960]
    })
    
    # Sample area data
    area_data = pd.DataFrame({
        'YEAR': [2010, 2011, 2012, 2013, 2014, 2015],
        'MAIZE_AREA': [1200000, 1250000, 1220000, 1280000, 1240000, 1260000],
        'COWPEA_AREA': [800000, 820000, 810000, 840000, 825000, 830000]
    })
    
    # Initialize preprocessor
    preprocessor = AgriDataPreprocessor()
    
    # Preprocess the data
    nasa_data = preprocessor.load_nasa_power_data(nasa_data)
    price_data = preprocessor.load_crop_price_data(price_data)
    yield_data = preprocessor.load_yield_data(yield_data)
    area_data = preprocessor.load_area_data(area_data)
    
    # Create features
    features = preprocessor.create_features(nasa_data, price_data, yield_data, area_data)
    
    return features, {
        'nasa_power': nasa_data,
        'price': price_data,
        'yield': yield_data,
        'area': area_data
    }

def train_yield_model(datasets):
    """
    Train the yield prediction model with your datasets.
    """
    print("Training yield prediction model...")
    
    # Initialize model
    model = AgriYieldModel()
    
    # Train the model using your datasets
    metrics = model.train(datasets)
    
    print("Yield model training completed.")
    
    # Display metrics if available
    if isinstance(metrics, dict) and 'rf_metrics' in metrics:
        print(f"Random Forest - MSE: {metrics['rf_metrics']['mse']:.2f}, R²: {metrics['rf_metrics']['r2']:.2f}")
        print(f"XGBoost - MSE: {metrics['xgb_metrics']['mse']:.2f}, R²: {metrics['xgb_metrics']['r2']:.2f}")
    
    # Save the model
    model.save_model("models/saved_models/yield_model")
    print("Yield model saved to models/saved_models/yield_model")
    
    return model

def train_roi_model(datasets):
    """
    Train the ROI prediction model with your datasets.
    """
    print("Training ROI prediction model...")
    
    # Initialize model
    model = AgriROIModel()
    
    # Train the model using your datasets
    metrics = model.train(datasets)
    
    print("ROI model training completed.")
    
    # Display metrics if available
    if isinstance(metrics, dict) and 'mse' in metrics:
        print(f"MSE: {metrics['mse']:.2f}, R²: {metrics['r2']:.2f}")
    
    # Save the model
    model.save_model("models/saved_models/roi_model")
    print("ROI model saved to models/saved_models/roi_model")
    
    return model

def main():
    """
    Main function to demonstrate the model training process with your datasets.
    """
    print("=== Sasya-Mitra AI Model Training ===")
    print("Using your agricultural datasets")
    print()
    
    # Load and preprocess data
    try:
        features, datasets = load_and_preprocess_data()
        print(f"Successfully processed datasets with {len(datasets)} data sources")
    except Exception as e:
        print(f"Error processing datasets: {e}")
        print("Creating sample data for demonstration...")
        features, datasets = create_sample_data()
    
    # Show feature information
    if hasattr(features, 'shape'):
        print(f"Created feature matrix with shape: {features.shape}")
    else:
        print(f"Created feature data: {type(features)}")
    
    # Train yield model
    try:
        yield_model = train_yield_model(datasets)
    except Exception as e:
        print(f"Error training yield model: {e}")
    
    # Train ROI model
    try:
        roi_model = train_roi_model(datasets)
    except Exception as e:
        print(f"Error training ROI model: {e}")
    
    print("\n=== Training Complete ===")
    print("Models have been trained and saved.")
    print("To use these models:")
    print("1. Run the Sasya-Mitra web application")
    print("2. The AI recommendations will automatically use your trained models")
    print("3. For retraining, run this script again with updated datasets")

if __name__ == "__main__":
    main()