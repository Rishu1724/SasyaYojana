"""
Train Sasya-Mitra AI models using the user's specific datasets.
"""

import sys
import os
import pandas as pd

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from training.model_trainer import AgriYieldModel, AgriROIModel

# Dictionary to store all loaded DataFrames
datasets = {}

def load_user_datasets():
    """Load all user CSV files into the datasets dictionary"""
    # Define the data directory (relative to this script)
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    
    # List of files to load with their exact names
    files_to_load = [
        "Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc.csv",
        "1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻.csv",
        "All India level Average Yield of Principal Crops from 2001-02 to 2015-16.csv",
        "All India level Area Under Principal Crops from 2001-02 to 2015-16.csv",
        "Production of principle crops.csv",
        "price.csv"
    ]
    
    print("Loading user datasets...")
    
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

def train_models_with_user_data():
    """Train AI models using the user's datasets"""
    print("\n" + "="*50)
    print("SASYA-MITRA AI MODEL TRAINING")
    print("="*50)
    
    # Load user datasets
    datasets = load_user_datasets()
    
    if not datasets:
        print("No datasets loaded. Please check your data files.")
        return
    
    print(f"\nLoaded {len(datasets)} datasets:")
    for key in datasets.keys():
        print(f"  - {key}")
    
    # Initialize models
    print("\nInitializing AI models...")
    yield_model = AgriYieldModel()
    roi_model = AgriROIModel()
    
    # Train yield prediction model
    print("\nTraining Yield Prediction Model...")
    print("-" * 30)
    try:
        yield_metrics = yield_model.train(datasets)
        print("Yield model training completed successfully!")
    except Exception as e:
        print(f"Error training yield model: {e}")
        return
    
    # Train ROI prediction model
    print("\nTraining ROI Prediction Model...")
    print("-" * 30)
    try:
        roi_metrics = roi_model.train(datasets)
        print("ROI model training completed successfully!")
    except Exception as e:
        print(f"Error training ROI model: {e}")
        return
    
    # Display feature importance
    print("\nFeature Importance Analysis...")
    print("-" * 30)
    try:
        # Get feature importance for yield model
        importance = yield_model.get_feature_importance()
        print("Top 5 Important Features for Yield Prediction:")
        print(importance['rf_importance'].head())
    except Exception as e:
        print(f"Could not display feature importance: {e}")
    
    # Save trained models
    print("\nSaving trained models...")
    print("-" * 30)
    try:
        yield_model.save_model("models/saved_models/yield_model")
        roi_model.save_model("models/saved_models/roi_model")
        print("Models saved successfully!")
    except Exception as e:
        print(f"Error saving models: {e}")
        return
    
    print("\n" + "="*50)
    print("TRAINING COMPLETE")
    print("="*50)
    print("Your AI models are now trained and ready to use!")
    print("You can now run the Sasya-Mitra web application to use these models.")

if __name__ == "__main__":
    train_models_with_user_data()