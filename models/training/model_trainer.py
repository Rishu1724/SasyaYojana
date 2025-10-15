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
            if nasa_data is not None and not nasa_data.empty:
                try:
                    features['avg_temperature'] = nasa_data['T2M'].mean() if 'T2M' in nasa_data.columns else 0
                    features['avg_humidity'] = nasa_data['RH2M'].mean() if 'RH2M' in nasa_data.columns else 0
                    features['avg_rainfall'] = (nasa_data['PRECTOTCORR'].mean() * 3650) if 'PRECTOTCORR' in nasa_data.columns else 0
                    features['solar_radiation'] = nasa_data['ALLSKY_SFC_SW_DWN'].mean() if 'ALLSKY_SFC_SW_DWN' in nasa_data.columns else 0
                except Exception as e:
                    print(f"Warning: Error processing NASA POWER data: {e}")
                    features['avg_temperature'] = 0
                    features['avg_humidity'] = 0
                    features['avg_rainfall'] = 0
                    features['solar_radiation'] = 0
        
        # Process crop yield data (2001-2015)
        if 'All India level Average Yield of Principal Crops from 2001-02 to 2015-16' in datasets:
            yield_data = datasets['All India level Average Yield of Principal Crops from 2001-02 to 2015-16']
            if yield_data is not None and not yield_data.empty:
                try:
                    # Melt the data to get crop-wise averages
                    yield_melted = yield_data.melt(id_vars=['Year'], var_name='Crop', value_name='Yield')
                    yield_melted = yield_melted.dropna()
                    # Convert to numeric, handling 'NA' values
                    yield_melted['Yield'] = pd.to_numeric(yield_melted['Yield'], errors='coerce')
                    yield_melted = yield_melted.dropna()
                    if not yield_melted.empty:
                        crop_yield_avg = yield_melted.groupby('Crop')['Yield'].mean()
                        top_crops = crop_yield_avg.nlargest(10)  # Increased to top 10 crops
                        for i, (crop, yield_val) in enumerate(top_crops.items()):
                            crop_name = str(crop).replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '').replace(',', '').upper()
                            features[f'yield_mean_{i}_{crop_name}'] = yield_val
                            # Add standard deviation if available
                            crop_std = yield_melted[yield_melted['Crop'] == crop]['Yield'].std()
                            features[f'yield_std_{i}_{crop_name}'] = crop_std if not np.isnan(crop_std) else 0
                except Exception as e:
                    print(f"Warning: Error processing crop yield data: {e}")
        
        # Process crop area data (2001-2015)
        if 'All India level Area Under Principal Crops from 2001-02 to 2015-16' in datasets:
            area_data = datasets['All India level Area Under Principal Crops from 2001-02 to 2015-16']
            if area_data is not None and not area_data.empty:
                try:
                    # Melt the data to get crop-wise averages
                    area_melted = area_data.melt(id_vars=['Year'], var_name='Crop', value_name='Area')
                    area_melted = area_melted.dropna()
                    # Convert to numeric, handling 'NA' values
                    area_melted['Area'] = pd.to_numeric(area_melted['Area'], errors='coerce')
                    area_melted = area_melted.dropna()
                    if not area_melted.empty:
                        crop_area_avg = area_melted.groupby('Crop')['Area'].mean()
                        top_crops = crop_area_avg.nlargest(10)  # Increased to top 10 crops
                        for i, (crop, area_val) in enumerate(top_crops.items()):
                            crop_name = str(crop).replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '').replace(',', '').upper()
                            features[f'area_mean_{i}_{crop_name}'] = area_val
                            # Add standard deviation if available
                            crop_std = area_melted[area_melted['Crop'] == crop]['Area'].std()
                            features[f'area_std_{i}_{crop_name}'] = crop_std if not np.isnan(crop_std) else 0
                except Exception as e:
                    print(f"Warning: Error processing crop area data: {e}")
        
        # Process production data
        if 'Production of principle crops' in datasets:
            prod_data = datasets['Production of principle crops']
            if prod_data is not None and not prod_data.empty:
                try:
                    # Melt the data to get crop-wise averages
                    prod_melted = prod_data.melt(id_vars=['Year'], var_name='Crop', value_name='Production')
                    prod_melted = prod_melted.dropna()
                    # Convert to numeric, handling 'NA' values
                    prod_melted['Production'] = pd.to_numeric(prod_melted['Production'], errors='coerce')
                    prod_melted = prod_melted.dropna()
                    if not prod_melted.empty:
                        crop_prod_avg = prod_melted.groupby('Crop')['Production'].mean()
                        top_crops = crop_prod_avg.nlargest(10)  # Increased to top 10 crops
                        for i, (crop, prod_val) in enumerate(top_crops.items()):
                            crop_name = str(crop).replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '').replace(',', '').upper()
                            features[f'production_mean_{i}_{crop_name}'] = prod_val
                            # Add standard deviation if available
                            crop_std = prod_melted[prod_melted['Crop'] == crop]['Production'].std()
                            features[f'production_std_{i}_{crop_name}'] = crop_std if not np.isnan(crop_std) else 0
                except Exception as e:
                    print(f"Warning: Error processing crop production data: {e}")
        
        # Process price data (Agmarknet)
        if 'price' in datasets:
            price_data = datasets['price']
            if price_data is not None and not price_data.empty:
                try:
                    # Get average prices for different crops
                    price_cols = [col for col in price_data.columns if col not in ['YEAR', 'STATE', 'DISTRICT']]
                    for i, col in enumerate(price_cols[:10]):  # Top 10 price columns
                        # Convert to numeric, handling non-numeric values
                        price_data[col] = pd.to_numeric(price_data[col], errors='coerce')
                        features[f'price_mean_{i}_{col}'] = price_data[col].mean() if col in price_data.columns else 0
                        features[f'price_std_{i}_{col}'] = price_data[col].std() if col in price_data.columns else 0
                        features[f'price_max_{i}_{col}'] = price_data[col].max() if col in price_data.columns else 0
                        features[f'price_min_{i}_{col}'] = price_data[col].min() if col in price_data.columns else 0
                except Exception as e:
                    print(f"Warning: Error processing crop price data: {e}")
        
        # Process damage data
        if 'Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc' in datasets:
            damage_data = datasets['Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc']
            if damage_data is not None and not damage_data.empty:
                try:
                    # Convert damage columns to numeric
                    for col in ['Flood', 'Cyclone', 'Landslide']:
                        if col in damage_data.columns:
                            damage_data[col] = pd.to_numeric(damage_data[col], errors='coerce')
                    features['total_flood_damage'] = damage_data['Flood'].sum() if 'Flood' in damage_data.columns else 0
                    features['total_cyclone_damage'] = damage_data['Cyclone'].sum() if 'Cyclone' in damage_data.columns else 0
                    features['total_landslide_damage'] = damage_data['Landslide'].sum() if 'Landslide' in damage_data.columns else 0
                    features['years_of_damage_data'] = len(damage_data)
                    # Add average damage per year
                    if len(damage_data) > 0:
                        features['avg_flood_damage'] = features['total_flood_damage'] / len(damage_data)
                        features['avg_cyclone_damage'] = features['total_cyclone_damage'] / len(damage_data)
                        features['avg_landslide_damage'] = features['total_landslide_damage'] / len(damage_data)
                except Exception as e:
                    print(f"Warning: Error processing damage data: {e}")
                    features['total_flood_damage'] = 0
                    features['total_cyclone_damage'] = 0
                    features['total_landslide_damage'] = 0
                    features['years_of_damage_data'] = 0
        
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
        
        # Create sample yield targets (kg/ha) based on features
        # More realistic approach using feature values
        base_yield = 2500
        temp_factor = feature_df.get('avg_temperature', pd.Series([25] * n_samples)) - 25
        rainfall_factor = feature_df.get('avg_rainfall', pd.Series([1000] * n_samples)) - 1000
        yield_targets = base_yield + temp_factor * 10 + rainfall_factor * 0.1 + np.random.normal(0, 300, n_samples)
        
        # Create sample ROI targets (percentage) based on price and yield features
        price_factor = feature_df.get('price_mean_0_MANGO_PRICE', pd.Series([50] * n_samples)) - 50
        roi_targets = 15 + price_factor * 0.1 + np.random.normal(0, 3, n_samples)
        
        return pd.Series(yield_targets), pd.Series(roi_targets)
    
    def train(self, datasets):
        """
        Train the yield prediction models using provided datasets.
        
        Parameters:
        datasets (dict): Dictionary containing all loaded datasets
        """
        # Prepare features
        X = self.prepare_features(datasets)
        
        # Handle any remaining missing values
        X = X.fillna(0)
        
        print(f"Prepared feature matrix with shape: {X.shape}")
        print(f"Feature columns: {list(X.columns)}")
        
        # Create targets based on features for more realistic training
        y_yield, y_roi = self.create_sample_targets(X)
        
        # Ensure we have enough data
        if len(X) < 2:  # Need at least 2 samples for train/test split
            print("Not enough data for training. Creating sample data for demonstration.")
            # Create sample data for demonstration
            sample_data = {
                'avg_temperature': [25, 26, 24, 27, 25],
                'avg_humidity': [65, 70, 60, 75, 68],
                'avg_rainfall': [1200, 1100, 1300, 1000, 1150],
                'solar_radiation': [200, 210, 190, 220, 205],
                'yield_mean_0_RICE': [3000, 3200, 2800, 3100, 2900],
                'yield_mean_1_WHEAT': [2500, 2600, 2400, 2700, 2550],
                'area_mean_0_RICE': [2000000, 2100000, 1900000, 2050000, 1950000],
                'price_mean_0_RICE': [20, 22, 18, 21, 19],
                'price_mean_1_WHEAT': [15, 16, 14, 17, 15]
            }
            X = pd.DataFrame(sample_data)
            # Create more realistic targets
            y_yield = pd.Series([3000, 3200, 2800, 3100, 2900])
            y_roi = pd.Series([15, 17, 13, 16, 14])
        elif len(X) < 5:  # If we have some data but not enough for a good split
            # Duplicate the data to have enough samples
            n_duplicates = 5 // len(X) + 1
            X = pd.concat([X] * n_duplicates, ignore_index=True)
            y_yield = pd.concat([y_yield] * n_duplicates, ignore_index=True)
            y_roi = pd.concat([y_roi] * n_duplicates, ignore_index=True)
        
        # Split the data - ensure we have enough samples
        if len(X) >= 2:
            test_size = min(0.2, 1.0 / len(X))  # Adjust test size if needed
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_yield, test_size=test_size, random_state=42
            )
        else:
            # Fallback if we still don't have enough data
            X_train, X_test, y_train, y_test = X, X, y_yield, y_yield
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest with the approach you shared
        print("Training Random Forest model...")
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.rf_model.fit(X_train, y_train)
        
        # Train XGBoost
        print("Training XGBoost model...")
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
        
        # Handle any remaining missing values
        X = X.fillna(0)
        
        # Ensure feature columns match training data
        if self.feature_names:
            # Add missing columns with 0 values
            for col in self.feature_names:
                if col not in X.columns:
                    X[col] = 0
            # Remove extra columns
            X = X[self.feature_names]
        
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
            if nasa_data is not None and not nasa_data.empty:
                try:
                    features['avg_temperature'] = nasa_data['T2M'].mean() if 'T2M' in nasa_data.columns else 0
                    features['avg_humidity'] = nasa_data['RH2M'].mean() if 'RH2M' in nasa_data.columns else 0
                    features['avg_rainfall'] = (nasa_data['PRECTOTCORR'].mean() * 3650) if 'PRECTOTCORR' in nasa_data.columns else 0
                    features['solar_radiation'] = nasa_data['ALLSKY_SFC_SW_DWN'].mean() if 'ALLSKY_SFC_SW_DWN' in nasa_data.columns else 0
                except Exception as e:
                    print(f"Warning: Error processing NASA POWER data: {e}")
                    features['avg_temperature'] = 0
                    features['avg_humidity'] = 0
                    features['avg_rainfall'] = 0
                    features['solar_radiation'] = 0
        
        # Process price data (most important for ROI)
        if 'price' in datasets:
            price_data = datasets['price']
            if price_data is not None and not price_data.empty:
                try:
                    # Get average prices for different crops
                    price_cols = [col for col in price_data.columns if col not in ['YEAR', 'STATE', 'DISTRICT']]
                    for i, col in enumerate(price_cols[:10]):  # Top 10 price columns
                        # Convert to numeric, handling non-numeric values
                        price_data[col] = pd.to_numeric(price_data[col], errors='coerce')
                        features[f'price_mean_{i}_{col}'] = price_data[col].mean() if col in price_data.columns else 0
                        features[f'price_std_{i}_{col}'] = price_data[col].std() if col in price_data.columns else 0
                        features[f'price_max_{i}_{col}'] = price_data[col].max() if col in price_data.columns else 0
                        features[f'price_min_{i}_{col}'] = price_data[col].min() if col in price_data.columns else 0
                except Exception as e:
                    print(f"Warning: Error processing crop price data: {e}")
        
        # Process production data
        if 'Production of principle crops' in datasets:
            prod_data = datasets['Production of principle crops']
            if prod_data is not None and not prod_data.empty:
                try:
                    # Melt the data to get crop-wise averages
                    prod_melted = prod_data.melt(id_vars=['Year'], var_name='Crop', value_name='Production')
                    prod_melted = prod_melted.dropna()
                    # Convert to numeric, handling 'NA' values
                    prod_melted['Production'] = pd.to_numeric(prod_melted['Production'], errors='coerce')
                    prod_melted = prod_melted.dropna()
                    if not prod_melted.empty:
                        crop_prod_avg = prod_melted.groupby('Crop')['Production'].mean()
                        top_crops = crop_prod_avg.nlargest(10)  # Increased to top 10 crops
                        for i, (crop, prod_val) in enumerate(top_crops.items()):
                            crop_name = str(crop).replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '').replace(',', '').upper()
                            features[f'production_mean_{i}_{crop_name}'] = prod_val
                except Exception as e:
                    print(f"Warning: Error processing crop production data: {e}")
        
        # Process yield data for ROI calculation
        if 'All India level Average Yield of Principal Crops from 2001-02 to 2015-16' in datasets:
            yield_data = datasets['All India level Average Yield of Principal Crops from 2001-02 to 2015-16']
            if yield_data is not None and not yield_data.empty:
                try:
                    # Melt the data to get crop-wise averages
                    yield_melted = yield_data.melt(id_vars=['Year'], var_name='Crop', value_name='Yield')
                    yield_melted = yield_melted.dropna()
                    # Convert to numeric, handling 'NA' values
                    yield_melted['Yield'] = pd.to_numeric(yield_melted['Yield'], errors='coerce')
                    yield_melted = yield_melted.dropna()
                    if not yield_melted.empty:
                        crop_yield_avg = yield_melted.groupby('Crop')['Yield'].mean()
                        top_crops = crop_yield_avg.nlargest(10)  # Increased to top 10 crops
                        for i, (crop, yield_val) in enumerate(top_crops.items()):
                            crop_name = str(crop).replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '').replace(',', '').upper()
                            features[f'yield_mean_{i}_{crop_name}'] = yield_val
                except Exception as e:
                    print(f"Warning: Error processing crop yield data: {e}")
        
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
        
        # Handle any remaining missing values
        X = X.fillna(0)
        
        print(f"Prepared feature matrix with shape: {X.shape}")
        print(f"Feature columns: {list(X.columns)}")
        
        # Create more realistic ROI targets based on features
        np.random.seed(42)
        n_samples = len(X)
        
        if n_samples < 2:  # Need at least 2 samples for train/test split
            # Create sample data for demonstration
            sample_data = {
                'avg_temperature': [25, 26, 24, 27, 25],
                'avg_humidity': [65, 70, 60, 75, 68],
                'avg_rainfall': [1200, 1100, 1300, 1000, 1150],
                'price_mean_0_RICE': [20, 22, 18, 21, 19],
                'price_mean_1_WHEAT': [15, 16, 14, 17, 15],
                'yield_mean_0_RICE': [3000, 3200, 2800, 3100, 2900],
                'yield_mean_1_WHEAT': [2500, 2600, 2400, 2700, 2550]
            }
            X = pd.DataFrame(sample_data)
            # Create more realistic ROI targets
            y_roi = pd.Series([15, 17, 13, 16, 14])
        elif n_samples < 5:  # If we have some data but not enough for a good split
            # Duplicate the data to have enough samples
            n_duplicates = 5 // n_samples + 1
            X = pd.concat([X] * n_duplicates, ignore_index=True)
            # Create ROI targets based on price and yield features
            price_factor = X.get('price_mean_0_RICE', pd.Series([20] * len(X))) - 20
            yield_factor = X.get('yield_mean_0_RICE', pd.Series([3000] * len(X))) - 3000
            y_roi = 15 + price_factor * 0.1 + yield_factor * 0.001 + np.random.normal(0, 2, len(X))
        else:
            # Create ROI targets based on price and yield features
            price_factor = X.get('price_mean_0_RICE', pd.Series([20] * n_samples)) - 20
            yield_factor = X.get('yield_mean_0_RICE', pd.Series([3000] * n_samples)) - 3000
            y_roi = 15 + price_factor * 0.1 + yield_factor * 0.001 + np.random.normal(0, 2, n_samples)
        
        # Split the data - ensure we have enough samples
        if len(X) >= 2:
            test_size = min(0.2, 1.0 / len(X))  # Adjust test size if needed
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_roi, test_size=test_size, random_state=42
            )
        else:
            # Fallback if we still don't have enough data
            X_train, X_test, y_train, y_test = X, X, y_roi, y_roi
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train the model with the approach you shared
        print("Training ROI model...")
        self.model = xgb.XGBRegressor(n_estimators=100, random_state=42)
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
        
        # Handle any remaining missing values
        X = X.fillna(0)
        
        # Ensure feature columns match training data
        if self.feature_names:
            # Add missing columns with 0 values
            for col in self.feature_names:
                if col not in X.columns:
                    X[col] = 0
            # Remove extra columns
            X = X[self.feature_names]
        
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