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
        
    def load_nasa_power_data(self, data):
        """
        Load and preprocess NASA POWER data.
        
        Parameters:
        data (pd.DataFrame or str): NASA POWER data DataFrame or file path
        
        Returns:
        pd.DataFrame: Processed NASA POWER data
        """
        # Load the data if it's a file path
        if isinstance(data, str):
            data = pd.read_csv(data)
        elif not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a DataFrame or file path")
        
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
    
    def load_crop_price_data(self, data):
        """
        Load and preprocess crop price data.
        
        Parameters:
        data (pd.DataFrame or str): Crop price data DataFrame or file path
        
        Returns:
        pd.DataFrame: Processed crop price data
        """
        # Load the data if it's a file path
        if isinstance(data, str):
            data = pd.read_csv(data)
        elif not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a DataFrame or file path")
        
        # Handle missing values
        data = data.fillna(0)
        
        # Convert price columns to numeric
        price_columns = [col for col in data.columns if 'price' in col.lower() or 'rate' in col.lower()]
        for col in price_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
            
        return data
    
    def load_yield_data(self, data):
        """
        Load and preprocess crop yield data.
        
        Parameters:
        data (pd.DataFrame or str): Crop yield data DataFrame or file path
        
        Returns:
        pd.DataFrame: Processed crop yield data
        """
        # Load the data if it's a file path
        if isinstance(data, str):
            data = pd.read_csv(data)
        elif not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a DataFrame or file path")
        
        # Handle missing values
        data = data.fillna(0)
        
        # Convert yield columns to numeric
        yield_columns = [col for col in data.columns if 'yield' in col.lower()]
        for col in yield_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
            
        return data
    
    def load_area_data(self, data):
        """
        Load and preprocess crop area data.
        
        Parameters:
        data (pd.DataFrame or str): Crop area data DataFrame or file path
        
        Returns:
        pd.DataFrame: Processed crop area data
        """
        # Load the data if it's a file path
        if isinstance(data, str):
            data = pd.read_csv(data)
        elif not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a DataFrame or file path")
        
        # Handle missing values
        data = data.fillna(0)
        
        # Convert area columns to numeric
        area_columns = [col for col in data.columns if 'area' in col.lower()]
        for col in area_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
            
        return data
    
    def load_production_data(self, data):
        """
        Load and preprocess crop production data.
        
        Parameters:
        data (pd.DataFrame or str): Crop production data DataFrame or file path
        
        Returns:
        pd.DataFrame: Processed crop production data
        """
        # Load the data if it's a file path
        if isinstance(data, str):
            data = pd.read_csv(data)
        elif not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a DataFrame or file path")
        
        # Handle missing values
        data = data.fillna(0)
        
        # Convert production columns to numeric
        production_columns = [col for col in data.columns if 'production' in col.lower()]
        for col in production_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
            
        return data
    
    def load_damage_data(self, data):
        """
        Load and preprocess natural disaster damage data.
        
        Parameters:
        data (pd.DataFrame or str): Damage data DataFrame or file path
        
        Returns:
        pd.DataFrame: Processed damage data
        """
        # Load the data if it's a file path
        if isinstance(data, str):
            data = pd.read_csv(data)
        elif not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a DataFrame or file path")
        
        # Handle missing values
        data = data.fillna(0)
        
        # Convert damage columns to numeric
        damage_columns = [col for col in data.columns if col.lower() in ['flood', 'cyclone', 'landslide']]
        for col in damage_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
            
        return data
    
    def standardize_crop_names(self, name):
        """
        Standardize crop names across different datasets.
        
        Parameters:
        name (str): Original crop name
        
        Returns:
        str: Standardized crop name
        """
        # Remove extra spaces and standardize formatting
        name = name.strip()
        
        # Common standardizations
        standardizations = {
            'Food grains (cereals) - Rice': 'Rice',
            'Food grains (cereals) - Wheat': 'Wheat',
            'Food grains (cereals) - Jowar': 'Jowar',
            'Food grains (cereals) - Bajra': 'Bajra',
            'Food grains (cereals) - Maize': 'Maize',
            'Food grains (cereals) - Ragi': 'Ragi',
            'Foodgrains(cereals) - Rice': 'Rice',
            'Foodgrains(cereals) - Wheat': 'Wheat',
            'Foodgrains(cereals) - Jowar': 'Jowar',
            'Foodgrains(cereals) - Bajra': 'Bajra',
            'Foodgrains(cereals) - Maize': 'Maize',
            'Foodgrains(cereals) - Ragi': 'Ragi',
            'Food Grains (Cereals) - Rice (000 tonnes)': 'Rice',
            'Food Grains (Cereals) - Wheat (000 tonnes)': 'Wheat',
            'Food Grains (Cereals) - Jowar (000 tonnes)': 'Jowar',
            'Food Grains (Cereals) - Bajra (000 tonnes)': 'Bajra',
            'Food Grains (Cereals) - Maize (000 tonnes)': 'Maize',
            'Food Grains (Cereals) - Ragi (000 tonnes)': 'Ragi',
            'Food grains(pulses) - Tur': 'Tur',
            'Food grains(pulses) - Gram': 'Gram',
            'Food grains(pulses) - Other Pulses': 'Other Pulses',
            'Foodgrains(pulses) - Tur': 'Tur',
            'Foodgrains(pulses) - Gram': 'Gram',
            'Foodgrains(pulses) - Other pulses': 'Other Pulses',
            'Food Grains (Pulses) - Tur (000 tonnes)': 'Tur',
            'Food Grains (Pulses) - Gram (000 tonnes)': 'Gram',
            'Food Grains (Pulses) - Other Pulses (000 tonnes)': 'Other Pulses'
        }
        
        # Check if we have a standardization for this name
        if name in standardizations:
            return standardizations[name]
        
        # If not, clean the name
        clean_name = name.replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '').replace(',', '')
        return clean_name
    
    def prepare_crop_data_for_merging(self, df, data_type):
        """
        Prepare crop data for merging by transforming it into a long format.
        
        Parameters:
        df (DataFrame): Crop data
        data_type (str): Type of data ('area', 'yield', or 'production')
        
        Returns:
        DataFrame: Transformed data ready for merging
        """
        if df is None:
            return None
        
        # Melt the dataframe to get crop-wise data
        if 'Year' in df.columns:
            # Get all columns except 'Year'
            crop_columns = [col for col in df.columns if col != 'Year']
            
            # Melt the data
            melted_df = df.melt(id_vars=['Year'], value_vars=crop_columns, 
                               var_name='Crop', value_name=data_type.capitalize())
            
            # Remove 'NA' values and convert to numeric
            melted_df[data_type.capitalize()] = pd.to_numeric(melted_df[data_type.capitalize()], errors='coerce')
            melted_df = melted_df.dropna()
            
            # Standardize crop names
            melted_df['Crop'] = melted_df['Crop'].apply(self.standardize_crop_names)
            
            return melted_df
        
        return None
    
    def create_derived_features(self, datasets):
        """
        Create derived features by merging related datasets.
        
        Parameters:
        datasets (dict): Dictionary containing all loaded datasets
        
        Returns:
        dict: Derived features
        """
        print("\nCreating Derived Features...")
        features = {}
        
        # Prepare datasets for merging
        area_df = self.prepare_crop_data_for_merging(datasets.get('area'), 'area')
        yield_df = self.prepare_crop_data_for_merging(datasets.get('yield'), 'yield')
        production_df = self.prepare_crop_data_for_merging(datasets.get('production'), 'production')
        
        # Check if we have the necessary data
        if area_df is None or yield_df is None or production_df is None:
            print("⚠️  Insufficient data for creating derived features")
            return features
        
        try:
            # Implement the exact merging approach you specified:
            # merged_df = area_df.merge(yield_df, on="Crop").merge(production_df, on="Crop")
            print("Merging datasets using your approach...")
            
            # First merge area and yield data on both Crop and Year for more accurate matching
            merged_df = pd.merge(area_df, yield_df, on=["Crop", "Year"], how="inner", suffixes=('_area', '_yield'))
            
            # Then merge with production data
            merged_df = pd.merge(merged_df, production_df, on=["Crop", "Year"], how="inner", suffixes=('', '_production'))
            
            print(f"✅ Merged datasets. Shape: {merged_df.shape}")
            
            # Calculate derived metrics as you specified:
            # merged_df["yield_per_area"] = merged_df["Production"] / merged_df["Area"]
            print("Calculating derived metrics...")
            
            # Avoid division by zero
            merged_df = merged_df[merged_df["Area"] > 0]
            
            if not merged_df.empty:
                # Calculate yield per area as you specified
                merged_df["yield_per_area"] = merged_df["Production"] / merged_df["Area"]
                
                # Calculate yield efficiency
                merged_df["yield_efficiency"] = merged_df["Yield"] / merged_df["Area"]
                
                # Group by crop and calculate average derived metrics
                derived_metrics = merged_df.groupby('Crop')[['yield_per_area', 'yield_efficiency']].mean()
                
                # Add to features
                for crop, metrics in derived_metrics.iterrows():
                    clean_crop = str(crop).replace(' ', '_').replace('-', '_')
                    features[f'yield_per_area_{clean_crop}'] = metrics['yield_per_area']
                    features[f'yield_efficiency_{clean_crop}'] = metrics['yield_efficiency']
                
                print(f"✅ Created {len(derived_metrics)} derived features")
                print("Sample derived features:")
                for crop, metrics in list(derived_metrics.iterrows())[:3]:
                    print(f"  {crop}: yield_per_area={metrics['yield_per_area']:.4f}, yield_efficiency={metrics['yield_efficiency']:.6f}")
            else:
                print("⚠️  No valid data for creating derived features after cleaning")
        except Exception as e:
            print(f"⚠️  Error creating derived features: {e}")
            import traceback
            traceback.print_exc()
        
        return features
    
    def process_historical_datasets(self, datasets):
        """
        Process all historical datasets to extract features for ML models.
        
        Parameters:
        datasets (dict): Dictionary containing all loaded datasets
        
        Returns:
        dict: Processed features from all datasets
        """
        features = {}
        
        # Process NASA POWER data (weather conditions)
        if 'nasa_power' in datasets and datasets['nasa_power'] is not None:
            nasa_data = datasets['nasa_power']
            if not nasa_data.empty:
                features['avg_temperature'] = nasa_data['T2M'].mean() if 'T2M' in nasa_data.columns else 0
                features['avg_humidity'] = nasa_data['RH2M'].mean() if 'RH2M' in nasa_data.columns else 0
                # Convert precipitation from kg/m2/s to mm/year
                features['avg_rainfall'] = (nasa_data['PRECTOTCORR'].mean() * 3650) if 'PRECTOTCORR' in nasa_data.columns else 0
                features['solar_radiation'] = nasa_data['ALLSKY_SFC_SW_DWN'].mean() if 'ALLSKY_SFC_SW_DWN' in nasa_data.columns else 0
                features['data_points'] = len(nasa_data)
        
        # Process crop area data (2001-2015)
        if 'area' in datasets and datasets['area'] is not None:
            area_data = datasets['area']
            if not area_data.empty:
                # Melt the data to get crop-wise averages
                if 'Crop' in area_data.columns:
                    area_melted = area_data.melt(id_vars=['Crop'], var_name='Year', value_name='Area')
                    area_melted = area_melted.dropna()
                    if not area_melted.empty:
                        # Group by crop and calculate statistics
                        crop_area_stats = area_melted.groupby('Crop')['Area'].agg(['mean', 'std', 'max', 'min']).reset_index()
                        # Add top 10 crops by average area
                        top_crops = crop_area_stats.nlargest(10, 'mean')
                        for i, (_, row) in enumerate(top_crops.iterrows()):
                            crop_name = str(row['Crop']).replace(' ', '_').upper()
                            features[f'area_mean_{i}_{crop_name}'] = row['mean']
                            features[f'area_std_{i}_{crop_name}'] = row['std']
                            features[f'area_max_{i}_{crop_name}'] = row['max']
                            features[f'area_min_{i}_{crop_name}'] = row['min']
        
        # Process crop yield data (2001-2015)
        if 'yield' in datasets and datasets['yield'] is not None:
            yield_data = datasets['yield']
            if not yield_data.empty:
                # Melt the data to get crop-wise averages
                if 'Crop' in yield_data.columns:
                    yield_melted = yield_data.melt(id_vars=['Crop'], var_name='Year', value_name='Yield')
                    yield_melted = yield_melted.dropna()
                    if not yield_melted.empty:
                        # Group by crop and calculate statistics
                        crop_yield_stats = yield_melted.groupby('Crop')['Yield'].agg(['mean', 'std', 'max', 'min']).reset_index()
                        # Add top 10 crops by average yield
                        top_crops = crop_yield_stats.nlargest(10, 'mean')
                        for i, (_, row) in enumerate(top_crops.iterrows()):
                            crop_name = str(row['Crop']).replace(' ', '_').upper()
                            features[f'yield_mean_{i}_{crop_name}'] = row['mean']
                            features[f'yield_std_{i}_{crop_name}'] = row['std']
                            features[f'yield_max_{i}_{crop_name}'] = row['max']
                            features[f'yield_min_{i}_{crop_name}'] = row['min']
        
        # Process production data
        if 'production' in datasets and datasets['production'] is not None:
            prod_data = datasets['production']
            if not prod_data.empty:
                # Melt the data to get crop-wise averages
                if 'Crop' in prod_data.columns:
                    prod_melted = prod_data.melt(id_vars=['Crop'], var_name='Year', value_name='Production')
                    prod_melted = prod_melted.dropna()
                    if not prod_melted.empty:
                        # Group by crop and calculate statistics
                        crop_prod_stats = prod_melted.groupby('Crop')['Production'].agg(['mean', 'std', 'max', 'min']).reset_index()
                        # Add top 10 crops by average production
                        top_crops = crop_prod_stats.nlargest(10, 'mean')
                        for i, (_, row) in enumerate(top_crops.iterrows()):
                            crop_name = str(row['Crop']).replace(' ', '_').upper()
                            features[f'production_mean_{i}_{crop_name}'] = row['mean']
                            features[f'production_std_{i}_{crop_name}'] = row['std']
                            features[f'production_max_{i}_{crop_name}'] = row['max']
                            features[f'production_min_{i}_{crop_name}'] = row['min']
        
        # Process price data (Agmarknet)
        if 'price' in datasets and datasets['price'] is not None:
            price_data = datasets['price']
            if not price_data.empty:
                # Get average prices for different crops
                price_cols = [col for col in price_data.columns if col not in ['YEAR', 'STATE', 'DISTRICT']]
                for i, col in enumerate(price_cols[:10]):  # Top 10 price columns
                    features[f'price_mean_{i}_{col}'] = price_data[col].mean() if col in price_data.columns else 0
                    features[f'price_std_{i}_{col}'] = price_data[col].std() if col in price_data.columns else 0
                    features[f'price_max_{i}_{col}'] = price_data[col].max() if col in price_data.columns else 0
                    features[f'price_min_{i}_{col}'] = price_data[col].min() if col in price_data.columns else 0
        
        # Process damage data
        if 'damage' in datasets and datasets['damage'] is not None:
            damage_data = datasets['damage']
            if not damage_data.empty:
                features['total_flood_damage'] = damage_data['Flood'].sum() if 'Flood' in damage_data.columns else 0
                features['total_cyclone_damage'] = damage_data['Cyclone'].sum() if 'Cyclone' in damage_data.columns else 0
                features['total_landslide_damage'] = damage_data['Landslide'].sum() if 'Landslide' in damage_data.columns else 0
                features['years_of_damage_data'] = len(damage_data)
        
        # Create derived features by merging datasets
        derived_features = self.create_derived_features(datasets)
        features.update(derived_features)
        
        return features
    
    def create_features(self, nasa_data, price_data, yield_data, area_data, production_data=None, damage_data=None):
        """
        Create features for machine learning models.
        
        Parameters:
        nasa_data (pd.DataFrame): NASA POWER data
        price_data (pd.DataFrame): Crop price data
        yield_data (pd.DataFrame): Crop yield data
        area_data (pd.DataFrame): Crop area data
        production_data (pd.DataFrame): Crop production data (optional)
        damage_data (pd.DataFrame): Damage data (optional)
        
        Returns:
        pd.DataFrame: Combined feature dataset
        """
        # Package datasets into a dictionary
        datasets = {
            'nasa_power': nasa_data,
            'price': price_data,
            'yield': yield_data,
            'area': area_data,
            'production': production_data,
            'damage': damage_data
        }
        
        # Process all datasets to extract features
        features_dict = self.process_historical_datasets(datasets)
        
        # Convert to DataFrame
        features_df = pd.DataFrame([features_dict])
        
        # Handle any remaining missing values
        features_df = features_df.fillna(0)
        
        return features_df
    
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
    # production_data = preprocessor.load_production_data('path/to/production_data.csv')
    # damage_data = preprocessor.load_damage_data('path/to/damage_data.csv')
    # features = preprocessor.create_features(nasa_data, price_data, yield_data, area_data, production_data, damage_data)
    # X, y = preprocessor.prepare_model_data(features, target_column='yield')
    pass