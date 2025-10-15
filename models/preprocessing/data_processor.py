"""
Data preprocessing utilities for agricultural datasets.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

class AgriDataPreprocessor:
    """
    Preprocessing class for agricultural datasets.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def load_nasa_power_data(self, file_path):
        """
        Load and preprocess NASA POWER data.
        
        Parameters:
        file_path (str): Path to the NASA POWER CSV file
        
        Returns:
        pd.DataFrame: Processed NASA POWER data
        """
        # Load the data
        data = pd.read_csv(file_path)
        
        # Handle missing values
        data = data.fillna(method='ffill').fillna(method='bfill')
        
        # Feature engineering
        # Calculate additional features from the raw data
        if 'T2M' in data.columns and 'T2M_MAX' in data.columns and 'T2M_MIN' in data.columns:
            data['TEMP_RANGE'] = data['T2M_MAX'] - data['T2M_MIN']
            
        if 'PRECTOTCORR' in data.columns:
            # Convert from kg/m2/s to mm/day
            data['RAINFALL_MM'] = data['PRECTOTCORR'] * 86400
            
        return data
    
    def load_crop_price_data(self, file_path):
        """
        Load and preprocess crop price data.
        
        Parameters:
        file_path (str): Path to the crop price CSV file
        
        Returns:
        pd.DataFrame: Processed crop price data
        """
        # Load the data
        data = pd.read_csv(file_path)
        
        # Handle missing values
        data = data.fillna(0)
        
        # Convert price columns to numeric
        price_columns = [col for col in data.columns if 'price' in col.lower() or 'rate' in col.lower()]
        for col in price_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
            
        return data
    
    def load_yield_data(self, file_path):
        """
        Load and preprocess crop yield data.
        
        Parameters:
        file_path (str): Path to the crop yield CSV file
        
        Returns:
        pd.DataFrame: Processed crop yield data
        """
        # Load the data
        data = pd.read_csv(file_path)
        
        # Handle missing values
        data = data.fillna(0)
        
        # Convert yield columns to numeric
        yield_columns = [col for col in data.columns if 'yield' in col.lower()]
        for col in yield_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
            
        return data
    
    def load_area_data(self, file_path):
        """
        Load and preprocess crop area data.
        
        Parameters:
        file_path (str): Path to the crop area CSV file
        
        Returns:
        pd.DataFrame: Processed crop area data
        """
        # Load the data
        data = pd.read_csv(file_path)
        
        # Handle missing values
        data = data.fillna(0)
        
        # Convert area columns to numeric
        area_columns = [col for col in data.columns if 'area' in col.lower()]
        for col in area_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
            
        return data
    
    def create_features(self, nasa_data, price_data, yield_data, area_data):
        """
        Create features for machine learning models.
        
        Parameters:
        nasa_data (pd.DataFrame): NASA POWER data
        price_data (pd.DataFrame): Crop price data
        yield_data (pd.DataFrame): Crop yield data
        area_data (pd.DataFrame): Crop area data
        
        Returns:
        pd.DataFrame: Combined feature dataset
        """
        # Merge datasets on common keys (year, state, district, etc.)
        # This is a simplified example - actual implementation would depend on your data structure
        
        # For now, let's create a basic feature set
        features = pd.DataFrame()
        
        # Add weather features
        if 'T2M' in nasa_data.columns:
            features['avg_temperature'] = nasa_data['T2M']
        if 'RAINFALL_MM' in nasa_data.columns:
            features['rainfall'] = nasa_data['RAINFALL_MM']
        if 'RH2M' in nasa_data.columns:
            features['humidity'] = nasa_data['RH2M']
        if 'ALLSKY_SFC_SW_DWN' in nasa_data.columns:
            features['solar_radiation'] = nasa_data['ALLSKY_SFC_SW_DWN']
        if 'TEMP_RANGE' in nasa_data.columns:
            features['temp_range'] = nasa_data['TEMP_RANGE']
            
        # Add price features (simplified)
        price_cols = [col for col in price_data.columns if col not in ['year', 'state', 'district']]
        for i, col in enumerate(price_cols[:5]):  # Take first 5 price columns as example
            features[f'price_{i}'] = price_data[col] if len(price_data) == len(features) else 0
            
        # Add yield features (simplified)
        yield_cols = [col for col in yield_data.columns if col not in ['year', 'state', 'district']]
        for i, col in enumerate(yield_cols[:5]):  # Take first 5 yield columns as example
            features[f'yield_{i}'] = yield_data[col] if len(yield_data) == len(features) else 0
            
        # Add area features (simplified)
        area_cols = [col for col in area_data.columns if col not in ['year', 'state', 'district']]
        for i, col in enumerate(area_cols[:5]):  # Take first 5 area columns as example
            features[f'area_{i}'] = area_data[col] if len(area_data) == len(features) else 0
            
        # Handle any remaining missing values
        features = features.fillna(0)
        
        return features
    
    def prepare_model_data(self, features, target_column=None):
        """
        Prepare data for machine learning models.
        
        Parameters:
        features (pd.DataFrame): Feature dataset
        target_column (str): Name of the target column (if any)
        
        Returns:
        tuple: (X, y) or (X, None) if no target
        """
        if target_column and target_column in features.columns:
            X = features.drop(columns=[target_column])
            y = features[target_column]
            return X, y
        else:
            return features, None
    
    def scale_features(self, X_train, X_test=None):
        """
        Scale features using StandardScaler.
        
        Parameters:
        X_train (pd.DataFrame): Training features
        X_test (pd.DataFrame): Test features (optional)
        
        Returns:
        tuple: Scaled features (X_train_scaled, X_test_scaled)
        """
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        if X_test is not None:
            X_test_scaled = self.scaler.transform(X_test)
            return X_train_scaled, X_test_scaled
        
        return X_train_scaled, None

# Example usage
if __name__ == "__main__":
    # This would be used when you have your actual data files
    # preprocessor = AgriDataPreprocessor()
    # nasa_data = preprocessor.load_nasa_power_data('path/to/nasa_data.csv')
    # price_data = preprocessor.load_crop_price_data('path/to/price_data.csv')
    # yield_data = preprocessor.load_yield_data('path/to/yield_data.csv')
    # area_data = preprocessor.load_area_data('path/to/area_data.csv')
    # features = preprocessor.create_features(nasa_data, price_data, yield_data, area_data)
    # X, y = preprocessor.prepare_model_data(features, target_column='yield')
    pass