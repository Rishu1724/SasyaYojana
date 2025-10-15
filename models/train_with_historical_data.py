"""
Training script that uses historical datasets to train machine learning models.
This script demonstrates how to use your historical datasets:
1. All India Level Crop Area (2001–2015)
2. Average Yield of Principal Crops (2001–2015)
3. Production of Principal Crops
4. Price Dataset (Agmarknet)
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Add the models directory to the path
sys.path.append(str(Path(__file__).parent))

from preprocessing.data_processor import AgriDataPreprocessor
from training.model_trainer import AgriYieldModel, AgriROIModel

class HistoricalDataTrainer:
    """
    Trainer that uses historical agricultural datasets for machine learning.
    """
    
    def __init__(self, data_dir="."):
        self.data_dir = Path(data_dir)
        self.preprocessor = AgriDataPreprocessor()
        self.datasets = {}
        print(f"Initializing trainer with data directory: {self.data_dir}")
        print(f"Current working directory: {Path.cwd()}")
        print(f"Data directory exists: {self.data_dir.exists()}")
        if self.data_dir.exists():
            print(f"Files in data directory: {list(self.data_dir.iterdir())}")
        
    def load_historical_datasets(self):
        """
        Load all historical datasets for training.
        """
        print("Loading historical datasets for training...")
        print("=" * 50)
        
        # Expected files with their exact names
        dataset_files = {
            'nasa_power': "1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻.csv",
            'area': "All India level Area Under Principal Crops from 2001-02 to 2015-16.csv",
            'yield': "All India level Average Yield of Principal Crops from 2001-02 to 2015-16.csv",
            'production': "Production of principle crops.csv",
            'price': "price.csv",
            'damage': "Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc.csv"
        }
        
        loaded_datasets = {}
        
        for key, filename in dataset_files.items():
            file_path = self.data_dir / filename
            print(f"Checking for {key} at: {file_path}")
            print(f"File exists: {file_path.exists()}")
            if file_path.exists():
                try:
                    # Load the dataset
                    data = pd.read_csv(file_path)
                    loaded_datasets[key] = data
                    print(f"✅ Loaded {key}: {filename}")
                    print(f"   Shape: {data.shape}")
                    print(f"   Columns: {list(data.columns)[:5]}{'...' if len(data.columns) > 5 else ''}")
                except Exception as e:
                    print(f"❌ Error loading {key} ({filename}): {e}")
                    loaded_datasets[key] = None
            else:
                print(f"⚠️  Missing {key}: {filename}")
                loaded_datasets[key] = None
        
        self.datasets = loaded_datasets
        return loaded_datasets
    
    def load_historical_features(self):
        """
        Load preprocessed historical features from the CSV file.
        """
        features_file = self.data_dir / "historical_features.csv"
        print(f"Checking for historical features at: {features_file}")
        print(f"File exists: {features_file.exists()}")
        if features_file.exists():
            try:
                features_df = pd.read_csv(features_file)
                print(f"✅ Loaded historical features from: {features_file}")
                print(f"   Shape: {features_df.shape}")
                return features_df
            except Exception as e:
                print(f"❌ Error loading historical features: {e}")
                return None
        else:
            print(f"⚠️  Historical features file not found: {features_file}")
            return None
    
    def preprocess_datasets(self):
        """
        Preprocess all loaded datasets using the AgriDataPreprocessor.
        """
        if not self.datasets:
            print("No datasets loaded. Please load datasets first.")
            return None
            
        print("\nPreprocessing datasets...")
        print("=" * 30)
        
        preprocessed_datasets = {}
        
        # Preprocess NASA POWER data
        if self.datasets.get('nasa_power') is not None:
            try:
                preprocessed_datasets['nasa_power'] = self.preprocessor.load_nasa_power_data(self.datasets['nasa_power'])
                print("✅ Preprocessed NASA POWER data")
            except Exception as e:
                print(f"❌ Error preprocessing NASA POWER data: {e}")
                preprocessed_datasets['nasa_power'] = None
        
        # Preprocess crop price data
        if self.datasets.get('price') is not None:
            try:
                preprocessed_datasets['price'] = self.preprocessor.load_crop_price_data(self.datasets['price'])
                print("✅ Preprocessed crop price data")
            except Exception as e:
                print(f"❌ Error preprocessing crop price data: {e}")
                preprocessed_datasets['price'] = None
        
        # Preprocess crop yield data
        if self.datasets.get('yield') is not None:
            try:
                preprocessed_datasets['yield'] = self.preprocessor.load_yield_data(self.datasets['yield'])
                print("✅ Preprocessed crop yield data")
            except Exception as e:
                print(f"❌ Error preprocessing crop yield data: {e}")
                preprocessed_datasets['yield'] = None
        
        # Preprocess crop area data
        if self.datasets.get('area') is not None:
            try:
                preprocessed_datasets['area'] = self.preprocessor.load_area_data(self.datasets['area'])
                print("✅ Preprocessed crop area data")
            except Exception as e:
                print(f"❌ Error preprocessing crop area data: {e}")
                preprocessed_datasets['area'] = None
        
        # Preprocess production data
        if self.datasets.get('production') is not None:
            try:
                preprocessed_datasets['production'] = self.preprocessor.load_production_data(self.datasets['production'])
                print("✅ Preprocessed crop production data")
            except Exception as e:
                print(f"❌ Error preprocessing crop production data: {e}")
                preprocessed_datasets['production'] = None
        
        # Preprocess damage data
        if self.datasets.get('damage') is not None:
            try:
                preprocessed_datasets['damage'] = self.preprocessor.load_damage_data(self.datasets['damage'])
                print("✅ Preprocessed damage data")
            except Exception as e:
                print(f"❌ Error preprocessing damage data: {e}")
                preprocessed_datasets['damage'] = None
        
        return preprocessed_datasets
    
    def train_yield_model(self, preprocessed_datasets):
        """
        Train the yield prediction model using historical datasets.
        """
        print("\nTraining Yield Prediction Model...")
        print("=" * 35)
        
        # Initialize model
        yield_model = AgriYieldModel()
        
        # Package datasets in the expected format
        model_datasets = {
            '1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻': preprocessed_datasets.get('nasa_power'),
            'All India level Average Yield of Principal Crops from 2001-02 to 2015-16': preprocessed_datasets.get('yield'),
            'All India level Area Under Principal Crops from 2001-02 to 2015-16': preprocessed_datasets.get('area'),
            'Production of principle crops': preprocessed_datasets.get('production'),
            'price': preprocessed_datasets.get('price'),
            'Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc': preprocessed_datasets.get('damage')
        }
        
        # Train the model
        try:
            metrics = yield_model.train(model_datasets)
            print("✅ Yield model training completed successfully!")
            
            # Display metrics
            if isinstance(metrics, dict) and 'rf_metrics' in metrics:
                print(f"\nRandom Forest Performance:")
                print(f"  MSE: {metrics['rf_metrics']['mse']:.4f}")
                print(f"  MAE: {metrics['rf_metrics']['mae']:.4f}")
                print(f"  R²: {metrics['rf_metrics']['r2']:.4f}")
                
                print(f"\nXGBoost Performance:")
                print(f"  MSE: {metrics['xgb_metrics']['mse']:.4f}")
                print(f"  MAE: {metrics['xgb_metrics']['mae']:.4f}")
                print(f"  R²: {metrics['xgb_metrics']['r2']:.4f}")
            
            # Save the model
            model_path = "saved_models/yield_model"
            yield_model.save_model(model_path)
            print(f"✅ Yield model saved to: {model_path}")
            
            return yield_model
            
        except Exception as e:
            print(f"❌ Error training yield model: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def train_roi_model(self, preprocessed_datasets):
        """
        Train the ROI prediction model using historical datasets.
        """
        print("\nTraining ROI Prediction Model...")
        print("=" * 32)
        
        # Initialize model
        roi_model = AgriROIModel()
        
        # Package datasets in the expected format
        model_datasets = {
            '1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻': preprocessed_datasets.get('nasa_power'),
            'All India level Average Yield of Principal Crops from 2001-02 to 2015-16': preprocessed_datasets.get('yield'),
            'All India level Area Under Principal Crops from 2001-02 to 2015-16': preprocessed_datasets.get('area'),
            'Production of principle crops': preprocessed_datasets.get('production'),
            'price': preprocessed_datasets.get('price'),
            'Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc': preprocessed_datasets.get('damage')
        }
        
        # Train the model
        try:
            metrics = roi_model.train(model_datasets)
            print("✅ ROI model training completed successfully!")
            
            # Display metrics
            if isinstance(metrics, dict) and 'mse' in metrics:
                print(f"\nROI Model Performance:")
                print(f"  MSE: {metrics['mse']:.4f}")
                print(f"  MAE: {metrics['mae']:.4f}")
                print(f"  R²: {metrics['r2']:.4f}")
            
            # Save the model
            model_path = "saved_models/roi_model"
            roi_model.save_model(model_path)
            print(f"✅ ROI model saved to: {model_path}")
            
            return roi_model
            
        except Exception as e:
            print(f"❌ Error training ROI model: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def analyze_feature_importance(self, yield_model, roi_model):
        """
        Analyze feature importance from trained models.
        """
        print("\nAnalyzing Feature Importance...")
        print("=" * 32)
        
        # Analyze yield model feature importance
        if yield_model and yield_model.is_trained:
            try:
                importance = yield_model.get_feature_importance()
                print("\nTop 10 Important Features for Yield Prediction (Random Forest):")
                print(importance['rf_importance'].head(10))
                
                print("\nTop 10 Important Features for Yield Prediction (XGBoost):")
                print(importance['xgb_importance'].head(10))
            except Exception as e:
                print(f"❌ Error analyzing yield model feature importance: {e}")
        
        # Analyze ROI model feature importance
        if roi_model and roi_model.is_trained:
            try:
                importance = roi_model.get_feature_importance()
                print("\nTop 10 Important Features for ROI Prediction:")
                print(importance.head(10))
            except Exception as e:
                print(f"❌ Error analyzing ROI model feature importance: {e}")
    
    def run_training_pipeline(self):
        """
        Run the complete training pipeline using historical datasets.
        """
        print("SASYA-MITRA HISTORICAL DATA TRAINING PIPELINE")
        print("=" * 50)
        
        # Step 1: Load datasets
        loaded_datasets = self.load_historical_datasets()
        if not any(dataset is not None for dataset in loaded_datasets.values()):
            print("❌ No datasets could be loaded. Please check your data files.")
            return None, None
        
        # Step 2: Load historical features if available
        historical_features = self.load_historical_features()
        if historical_features is not None:
            print(f"✅ Loaded {len(historical_features.columns)} historical features")
        
        # Step 3: Preprocess datasets
        preprocessed_datasets = self.preprocess_datasets()
        if not preprocessed_datasets:
            print("❌ Failed to preprocess datasets.")
            return None, None
        
        # Step 4: Train yield model
        yield_model = self.train_yield_model(preprocessed_datasets)
        
        # Step 5: Train ROI model
        roi_model = self.train_roi_model(preprocessed_datasets)
        
        # Step 6: Analyze feature importance
        self.analyze_feature_importance(yield_model, roi_model)
        
        print("\n" + "=" * 50)
        print("TRAINING PIPELINE COMPLETE")
        print("=" * 50)
        
        if yield_model and yield_model.is_trained:
            print("✅ Yield prediction model successfully trained")
        else:
            print("⚠️  Yield prediction model training failed")
            
        if roi_model and roi_model.is_trained:
            print("✅ ROI prediction model successfully trained")
        else:
            print("⚠️  ROI prediction model training failed")
        
        print("\nThe trained models can now be used to:")
        print("1. Predict crop yields based on weather and historical data")
        print("2. Estimate ROI for different crops")
        print("3. Recommend the best crops for specific conditions")
        print("4. Provide data-driven agricultural advice")
        
        return yield_model, roi_model

if __name__ == "__main__":
    # Create trainer and run training pipeline
    trainer = HistoricalDataTrainer(".")
    yield_model, roi_model = trainer.run_training_pipeline()