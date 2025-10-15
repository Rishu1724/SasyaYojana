"""
Model training module for Sasya-Mitra AI models.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib
import os

class AgriYieldModel:
    """
    Yield prediction model using RandomForest and XGBoost.
    """
    
    def __init__(self):
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.xgb_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = None
        
    def prepare_features(self, datasets):
        """
        Prepare features from multiple datasets.
        
        Parameters:
        datasets (dict): Dictionary containing all loaded datasets
        
        Returns:
        pd.DataFrame: Feature matrix
        """
        features = {}
        
        # Process NASA POWER data if available
        if '1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻' in datasets:
            nasa_data = datasets['1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻']
            if not nasa_data.empty:
                features['avg_temperature'] = nasa_data['T2M'].mean() if 'T2M' in nasa_data.columns else 0
                features['avg_humidity'] = nasa_data['RH2M'].mean() if 'RH2M' in nasa_data.columns else 0
                features['avg_rainfall'] = (nasa_data['PRECTOTCORR'].mean() * 3650) if 'PRECTOTCORR' in nasa_data.columns else 0
                features['solar_radiation'] = nasa_data['ALLSKY_SFC_SW_DWN'].mean() if 'ALLSKY_SFC_SW_DWN' in nasa_data.columns else 0
        
        # Process crop yield data
        if 'All India level Average Yield of Principal Crops from 2001-02 to 2015-16' in datasets:
            yield_data = datasets['All India level Average Yield of Principal Crops from 2001-02 to 2015-16']
            if not yield_data.empty:
                # Melt the data to get crop-wise averages
                yield_melted = yield_data.melt(id_vars=['Crop'], var_name='Year', value_name='Yield')
                yield_melted = yield_melted.dropna()
                if not yield_melted.empty:
                    crop_yield_avg = yield_melted.groupby('Crop')['Yield'].mean()
                    top_crops = crop_yield_avg.nlargest(5)
                    for i, (crop, yield_val) in enumerate(top_crops.items()):
                        features[f'yield_{i}_{crop}'] = yield_val
        
        # Process crop area data
        if 'All India level Area Under Principal Crops from 2001-02 to 2015-16' in datasets:
            area_data = datasets['All India level Area Under Principal Crops from 2001-02 to 2015-16']
            if not area_data.empty:
                # Melt the data to get crop-wise averages
                area_melted = area_data.melt(id_vars=['Crop'], var_name='Year', value_name='Area')
                area_melted = area_melted.dropna()
                if not area_melted.empty:
                    crop_area_avg = area_melted.groupby('Crop')['Area'].mean()
                    top_crops = crop_area_avg.nlargest(5)
                    for i, (crop, area_val) in enumerate(top_crops.items()):
                        features[f'area_{i}_{crop}'] = area_val
        
        # Process production data
        if 'Production of principle crops' in datasets:
            prod_data = datasets['Production of principle crops']
            if not prod_data.empty:
                # Melt the data to get crop-wise averages
                prod_melted = prod_data.melt(id_vars=['Crop'], var_name='Year', value_name='Production')
                prod_melted = prod_melted.dropna()
                if not prod_melted.empty:
                    crop_prod_avg = prod_melted.groupby('Crop')['Production'].mean()
                    top_crops = crop_prod_avg.nlargest(5)
                    for i, (crop, prod_val) in enumerate(top_crops.items()):
                        features[f'production_{i}_{crop}'] = prod_val
        
        # Process price data
        if 'price' in datasets:
            price_data = datasets['price']
            if not price_data.empty:
                # Get average prices for different crops
                price_cols = [col for col in price_data.columns if col not in ['YEAR', 'STATE', 'DISTRICT']]
                for i, col in enumerate(price_cols[:5]):  # Top 5 price columns
                    features[f'price_{i}_{col}'] = price_data[col].mean() if col in price_data.columns else 0
        
        # Process damage data
        if 'Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc' in datasets:
            damage_data = datasets['Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc']
            if not damage_data.empty:
                features['total_flood_damage'] = damage_data['Flood'].sum() if 'Flood' in damage_data.columns else 0
                features['total_cyclone_damage'] = damage_data['Cyclone'].sum() if 'Cyclone' in damage_data.columns else 0
                features['total_landslide_damage'] = damage_data['Landslide'].sum() if 'Landslide' in damage_data.columns else 0
                features['years_of_damage_data'] = len(damage_data)
        
        # Convert to DataFrame
        feature_df = pd.DataFrame([features])
        self.feature_names = list(features.keys())
        
        return feature_df
    
    def create_sample_targets(self, feature_df):
        """
        Create sample target variables for demonstration.
        In a real scenario, these would come from your actual target data.
        """
        np.random.seed(42)
        n_samples = len(feature_df)
        
        # Create sample yield targets (kg/ha)
        yield_targets = np.random.normal(2500, 500, n_samples)
        
        # Create sample ROI targets (percentage)
        roi_targets = np.random.normal(15, 5, n_samples)
        
        return pd.Series(yield_targets), pd.Series(roi_targets)
    
    def train(self, datasets):
        """
        Train the yield prediction models using provided datasets.
        
        Parameters:
        datasets (dict): Dictionary containing all loaded datasets
        """
        # Prepare features
        X = self.prepare_features(datasets)
        
        # Create sample targets (in a real scenario, you would have actual target data)
        y_yield, y_roi = self.create_sample_targets(X)
        
        # Ensure we have enough data
        if len(X) < 2:
            print("Not enough data for training. Creating sample data for demonstration.")
            # Create sample data for demonstration
            sample_data = {
                'avg_temperature': [25, 26, 24, 27, 25],
                'avg_humidity': [65, 70, 60, 75, 68],
                'avg_rainfall': [1200, 1100, 1300, 1000, 1150],
                'solar_radiation': [200, 210, 190, 220, 205],
                'yield_0_RICE': [3000, 3200, 2800, 3100, 2900],
                'yield_1_WHEAT': [2500, 2600, 2400, 2700, 2550]
            }
            X = pd.DataFrame(sample_data)
            y_yield = pd.Series([3000, 3200, 2800, 3100, 2900])
            y_roi = pd.Series([15, 17, 13, 16, 14])
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_yield, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest
        self.rf_model.fit(X_train, y_train)
        
        # Train XGBoost
        self.xgb_model.fit(X_train, y_train)
        
        # Evaluate models
        rf_pred = self.rf_model.predict(X_test)
        xgb_pred = self.xgb_model.predict(X_test)
        
        # Calculate metrics
        rf_mse = mean_squared_error(y_test, rf_pred)
        rf_mae = mean_absolute_error(y_test, rf_pred)
        rf_r2 = r2_score(y_test, rf_pred)
        
        xgb_mse = mean_squared_error(y_test, xgb_pred)
        xgb_mae = mean_absolute_error(y_test, xgb_pred)
        xgb_r2 = r2_score(y_test, xgb_pred)
        
        print("Random Forest Performance:")
        print(f"  MSE: {rf_mse:.4f}")
        print(f"  MAE: {rf_mae:.4f}")
        print(f"  R²: {rf_r2:.4f}")
        
        print("\nXGBoost Performance:")
        print(f"  MSE: {xgb_mse:.4f}")
        print(f"  MAE: {xgb_mae:.4f}")
        print(f"  R²: {xgb_r2:.4f}")
        
        self.is_trained = True
        self.feature_names = X.columns.tolist()
        
        return {
            'rf_metrics': {'mse': rf_mse, 'mae': rf_mae, 'r2': rf_r2},
            'xgb_metrics': {'mse': xgb_mse, 'mae': xgb_mae, 'r2': xgb_r2}
        }
    
    def predict(self, datasets):
        """
        Make predictions using the trained models.
        
        Parameters:
        datasets (dict): Dictionary containing all loaded datasets
        
        Returns:
        dict: Predictions from both models
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
            
        # Prepare features
        X = self.prepare_features(datasets)
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        rf_pred = self.rf_model.predict(X)
        xgb_pred = self.xgb_model.predict(X)
        
        # Ensemble prediction (average of both models)
        ensemble_pred = (rf_pred + xgb_pred) / 2
        
        return {
            'rf_prediction': rf_pred,
            'xgb_prediction': xgb_pred,
            'ensemble_prediction': ensemble_pred
        }
    
    def get_feature_importance(self):
        """
        Get feature importance from the trained models.
        
        Returns:
        dict: Feature importance from both models
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before getting feature importance")
            
        # Get feature names
        feature_names = self.feature_names
        
        # Get Random Forest feature importance
        rf_importance = self.rf_model.feature_importances_
        
        # Get XGBoost feature importance
        xgb_importance = self.xgb_model.feature_importances_
        
        # Create importance dataframes
        rf_importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': rf_importance
        }).sort_values('importance', ascending=False)
        
        xgb_importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': xgb_importance
        }).sort_values('importance', ascending=False)
        
        return {
            'rf_importance': rf_importance_df,
            'xgb_importance': xgb_importance_df
        }
    
    def save_model(self, filepath):
        """
        Save the trained models to disk.
        
        Parameters:
        filepath (str): Path to save the models
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
            
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save both models and scaler
        joblib.dump(self.rf_model, f"{filepath}_rf.pkl")
        joblib.dump(self.xgb_model, f"{filepath}_xgb.pkl")
        joblib.dump(self.scaler, f"{filepath}_scaler.pkl")
        joblib.dump(self.feature_names, f"{filepath}_features.pkl")
        
    def load_model(self, filepath):
        """
        Load trained models from disk.
        
        Parameters:
        filepath (str): Path to load the models from
        """
        self.rf_model = joblib.load(f"{filepath}_rf.pkl")
        self.xgb_model = joblib.load(f"{filepath}_xgb.pkl")
        self.scaler = joblib.load(f"{filepath}_scaler.pkl")
        self.feature_names = joblib.load(f"{filepath}_features.pkl")
        self.is_trained = True

class AgriROIModel:
    """
    ROI prediction model using XGBoost.
    """
    
    def __init__(self):
        self.model = xgb.XGBRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = None
        
    def prepare_features(self, datasets):
        """
        Prepare features from multiple datasets for ROI prediction.
        
        Parameters:
        datasets (dict): Dictionary containing all loaded datasets
        
        Returns:
        pd.DataFrame: Feature matrix
        """
        features = {}
        
        # Process NASA POWER data if available
        if '1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻' in datasets:
            nasa_data = datasets['1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻']
            if not nasa_data.empty:
                features['avg_temperature'] = nasa_data['T2M'].mean() if 'T2M' in nasa_data.columns else 0
                features['avg_humidity'] = nasa_data['RH2M'].mean() if 'RH2M' in nasa_data.columns else 0
                features['avg_rainfall'] = (nasa_data['PRECTOTCORR'].mean() * 3650) if 'PRECTOTCORR' in nasa_data.columns else 0
                features['solar_radiation'] = nasa_data['ALLSKY_SFC_SW_DWN'].mean() if 'ALLSKY_SFC_SW_DWN' in nasa_data.columns else 0
        
        # Process price data (most important for ROI)
        if 'price' in datasets:
            price_data = datasets['price']
            if not price_data.empty:
                # Get average prices for different crops
                price_cols = [col for col in price_data.columns if col not in ['YEAR', 'STATE', 'DISTRICT']]
                for i, col in enumerate(price_cols[:5]):  # Top 5 price columns
                    features[f'price_{i}_{col}'] = price_data[col].mean() if col in price_data.columns else 0
        
        # Process production data
        if 'Production of principle crops' in datasets:
            prod_data = datasets['Production of principle crops']
            if not prod_data.empty:
                # Melt the data to get crop-wise averages
                prod_melted = prod_data.melt(id_vars=['Crop'], var_name='Year', value_name='Production')
                prod_melted = prod_melted.dropna()
                if not prod_melted.empty:
                    crop_prod_avg = prod_melted.groupby('Crop')['Production'].mean()
                    top_crops = crop_prod_avg.nlargest(5)
                    for i, (crop, prod_val) in enumerate(top_crops.items()):
                        features[f'production_{i}_{crop}'] = prod_val
        
        # Convert to DataFrame
        feature_df = pd.DataFrame([features])
        self.feature_names = list(features.keys())
        
        return feature_df
    
    def train(self, datasets):
        """
        Train the ROI prediction model using provided datasets.
        
        Parameters:
        datasets (dict): Dictionary containing all loaded datasets
        """
        # Prepare features
        X = self.prepare_features(datasets)
        
        # Create sample targets (in a real scenario, you would have actual ROI data)
        np.random.seed(42)
        n_samples = len(X)
        if n_samples < 2:
            # Create sample data for demonstration
            sample_data = {
                'avg_temperature': [25, 26, 24, 27, 25],
                'avg_humidity': [65, 70, 60, 75, 68],
                'avg_rainfall': [1200, 1100, 1300, 1000, 1150],
                'price_0_RICE': [20, 22, 18, 21, 19],
                'price_1_WHEAT': [15, 16, 14, 17, 15]
            }
            X = pd.DataFrame(sample_data)
            y_roi = pd.Series([15, 17, 13, 16, 14])
        else:
            # Create sample ROI targets
            y_roi = pd.Series(np.random.normal(15, 5, n_samples))
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_roi, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print("ROI Model Performance:")
        print(f"  MSE: {mse:.4f}")
        print(f"  MAE: {mae:.4f}")
        print(f"  R²: {r2:.4f}")
        
        self.is_trained = True
        self.feature_names = X.columns.tolist()
        
        return {'mse': mse, 'mae': mae, 'r2': r2}
    
    def predict(self, datasets):
        """
        Make ROI predictions.
        
        Parameters:
        datasets (dict): Dictionary containing all loaded datasets
        
        Returns:
        np.array: ROI predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
            
        # Prepare features
        X = self.prepare_features(datasets)
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        return self.model.predict(X)
    
    def get_feature_importance(self):
        """
        Get feature importance from the trained model.
        
        Returns:
        pd.DataFrame: Feature importance
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before getting feature importance")
            
        # Get feature importance
        importance = self.model.feature_importances_
        
        # Create importance dataframe
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    def save_model(self, filepath):
        """
        Save the trained model to disk.
        
        Parameters:
        filepath (str): Path to save the model
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
            
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        joblib.dump(self.model, f"{filepath}_roi.pkl")
        joblib.dump(self.scaler, f"{filepath}_scaler.pkl")
        joblib.dump(self.feature_names, f"{filepath}_features.pkl")
        
    def load_model(self, filepath):
        """
        Load trained model from disk.
        
        Parameters:
        filepath (str): Path to load the model from
        """
        self.model = joblib.load(f"{filepath}_roi.pkl")
        self.scaler = joblib.load(f"{filepath}_scaler.pkl")
        self.feature_names = joblib.load(f"{filepath}_features.pkl")
        self.is_trained = True

# Example usage
if __name__ == "__main__":
    print("Sasya-Mitra Model Trainer")
    print("This script trains AI models for agricultural yield and ROI prediction.")
    print("To use with your datasets, run the process_user_datasets.py script first.")