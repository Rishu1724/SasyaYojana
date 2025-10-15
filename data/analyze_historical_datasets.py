"""
Script to analyze and process historical agricultural datasets for machine learning.
This script specifically handles:
1. All India Level Crop Area (2001–2015)
2. Average Yield of Principal Crops (2001–2015)
3. Production of Principal Crops
4. Price Dataset (Agmarknet)
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt

# Set style for better-looking plots
plt.style.use('ggplot')

class HistoricalDatasetAnalyzer:
    """
    Analyzer for historical agricultural datasets.
    """
    
    def __init__(self, data_dir="."):
        self.data_dir = Path(data_dir)
        self.datasets = {}
        
    def load_datasets(self):
        """
        Load all historical datasets.
        """
        # List of expected files
        expected_files = {
            'area': "All India level Area Under Principal Crops from 2001-02 to 2015-16.csv",
            'yield': "All India level Average Yield of Principal Crops from 2001-02 to 2015-16.csv",
            'production': "Production of principle crops.csv",
            'price': "price.csv",
            'nasa_power': "1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻.csv",
            'damage': "Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc.csv"
        }
        
        print("Loading historical datasets...")
        print("=" * 50)
        
        for key, filename in expected_files.items():
            file_path = self.data_dir / filename
            if file_path.exists():
                try:
                    self.datasets[key] = pd.read_csv(file_path)
                    print(f"✅ Loaded {key}: {filename}")
                    print(f"   Shape: {self.datasets[key].shape}")
                except Exception as e:
                    print(f"❌ Error loading {key}: {e}")
                    self.datasets[key] = None
            else:
                print(f"⚠️  Missing {key}: {filename}")
                self.datasets[key] = None
        
        return self.datasets
    
    def analyze_crop_area_data(self):
        """
        Analyze All India Level Crop Area (2001–2015).
        """
        if 'area' not in self.datasets or self.datasets['area'] is None:
            print("Crop area data not available")
            return None
            
        df = self.datasets['area']
        print("\n" + "=" * 50)
        print("ANALYZING CROP AREA DATA (2001-2015)")
        print("=" * 50)
        
        # Basic info
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Check for missing values
        print(f"\nMissing values:")
        print(df.isnull().sum())
        
        # Melt the data for analysis
        if 'Crop' in df.columns:
            melted_df = df.melt(id_vars=['Crop'], var_name='Year', value_name='Area')
            melted_df = melted_df.dropna()
            
            print(f"\nMelted data shape: {melted_df.shape}")
            
            # Top crops by average area
            crop_area_avg = melted_df.groupby('Crop')['Area'].mean().sort_values(ascending=False)
            print(f"\nTop 10 crops by average area (hectares):")
            for i, (crop, area) in enumerate(crop_area_avg.head(10).items()):
                print(f"  {i+1:2d}. {crop}: {area:,.0f}")
            
            # Area trends over time
            yearly_area = melted_df.groupby('Year')['Area'].sum()
            print(f"\nTotal area trends (hectares):")
            for year, area in yearly_area.items():
                print(f"  {year}: {area:,.0f}")
            
            return {
                'melted_data': melted_df,
                'top_crops': crop_area_avg.head(10),
                'yearly_trends': yearly_area
            }
        
        return None
    
    def analyze_crop_yield_data(self):
        """
        Analyze Average Yield of Principal Crops (2001–2015).
        """
        if 'yield' not in self.datasets or self.datasets['yield'] is None:
            print("Crop yield data not available")
            return None
            
        df = self.datasets['yield']
        print("\n" + "=" * 50)
        print("ANALYZING CROP YIELD DATA (2001-2015)")
        print("=" * 50)
        
        # Basic info
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Check for missing values
        print(f"\nMissing values:")
        print(df.isnull().sum())
        
        # Melt the data for analysis
        if 'Crop' in df.columns:
            melted_df = df.melt(id_vars=['Crop'], var_name='Year', value_name='Yield')
            melted_df = melted_df.dropna()
            
            print(f"\nMelted data shape: {melted_df.shape}")
            
            # Top crops by average yield
            crop_yield_avg = melted_df.groupby('Crop')['Yield'].mean().sort_values(ascending=False)
            print(f"\nTop 10 crops by average yield (kg/ha):")
            for i, (crop, yield_val) in enumerate(crop_yield_avg.head(10).items()):
                print(f"  {i+1:2d}. {crop}: {yield_val:,.0f}")
            
            # Yield trends over time
            yearly_yield = melted_df.groupby('Year')['Yield'].mean()
            print(f"\nAverage yield trends (kg/ha):")
            for year, yield_val in yearly_yield.items():
                print(f"  {year}: {yield_val:,.0f}")
            
            return {
                'melted_data': melted_df,
                'top_crops': crop_yield_avg.head(10),
                'yearly_trends': yearly_yield
            }
        
        return None
    
    def analyze_production_data(self):
        """
        Analyze Production of Principal Crops.
        """
        if 'production' not in self.datasets or self.datasets['production'] is None:
            print("Crop production data not available")
            return None
            
        df = self.datasets['production']
        print("\n" + "=" * 50)
        print("ANALYZING CROP PRODUCTION DATA")
        print("=" * 50)
        
        # Basic info
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Check for missing values
        print(f"\nMissing values:")
        print(df.isnull().sum())
        
        # Melt the data for analysis
        if 'Crop' in df.columns:
            melted_df = df.melt(id_vars=['Crop'], var_name='Year', value_name='Production')
            melted_df = melted_df.dropna()
            
            print(f"\nMelted data shape: {melted_df.shape}")
            
            # Top crops by average production
            crop_production_avg = melted_df.groupby('Crop')['Production'].mean().sort_values(ascending=False)
            print(f"\nTop 10 crops by average production (tonnes):")
            for i, (crop, production) in enumerate(crop_production_avg.head(10).items()):
                print(f"  {i+1:2d}. {crop}: {production:,.0f}")
            
            return {
                'melted_data': melted_df,
                'top_crops': crop_production_avg.head(10)
            }
        
        return None
    
    def analyze_price_data(self):
        """
        Analyze Price Dataset (Agmarknet).
        """
        if 'price' not in self.datasets or self.datasets['price'] is None:
            print("Crop price data not available")
            return None
            
        df = self.datasets['price']
        print("\n" + "=" * 50)
        print("ANALYZING CROP PRICE DATA (AGMARKNET)")
        print("=" * 50)
        
        # Basic info
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Check for missing values
        print(f"\nMissing values:")
        print(df.isnull().sum())
        
        # Price columns (excluding metadata columns)
        price_cols = [col for col in df.columns if col not in ['YEAR', 'STATE', 'DISTRICT']]
        print(f"\nPrice columns: {len(price_cols)}")
        
        # Average prices
        avg_prices = {}
        for col in price_cols[:10]:  # Top 10 price columns
            avg_prices[col] = df[col].mean()
        
        print(f"\nAverage prices for top commodities:")
        for i, (commodity, price) in enumerate(list(avg_prices.items())[:10]):
            print(f"  {i+1:2d}. {commodity}: ₹{price:,.2f}")
        
        return {
            'price_columns': price_cols,
            'average_prices': avg_prices
        }
    
    def analyze_nasa_power_data(self):
        """
        Analyze NASA POWER weather data.
        """
        if 'nasa_power' not in self.datasets or self.datasets['nasa_power'] is None:
            print("NASA POWER data not available")
            return None
            
        df = self.datasets['nasa_power']
        print("\n" + "=" * 50)
        print("ANALYZING NASA POWER WEATHER DATA")
        print("=" * 50)
        
        # Basic info
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Check for missing values
        print(f"\nMissing values:")
        print(df.isnull().sum())
        
        # Key weather parameters
        weather_stats = {}
        if 'T2M' in df.columns:
            weather_stats['avg_temperature'] = df['T2M'].mean()
            weather_stats['min_temperature'] = df['T2M'].min()
            weather_stats['max_temperature'] = df['T2M'].max()
            
        if 'RH2M' in df.columns:
            weather_stats['avg_humidity'] = df['RH2M'].mean()
            
        if 'PRECTOTCORR' in df.columns:
            # Convert to mm/year
            weather_stats['avg_rainfall'] = df['PRECTOTCORR'].mean() * 3650
            weather_stats['min_rainfall'] = df['PRECTOTCORR'].min() * 3650
            weather_stats['max_rainfall'] = df['PRECTOTCORR'].max() * 3650
            
        if 'ALLSKY_SFC_SW_DWN' in df.columns:
            weather_stats['avg_solar_radiation'] = df['ALLSKY_SFC_SW_DWN'].mean()
            
        print(f"\nWeather statistics:")
        for param, value in weather_stats.items():
            if 'temperature' in param:
                print(f"  {param}: {value:.2f} °C")
            elif 'rainfall' in param:
                print(f"  {param}: {value:.0f} mm/year")
            elif 'humidity' in param:
                print(f"  {param}: {value:.1f} %")
            else:
                print(f"  {param}: {value:.2f}")
        
        return {
            'weather_stats': weather_stats
        }
    
    def correlate_datasets(self):
        """
        Find correlations between different datasets to understand which crops grow best under which conditions.
        """
        print("\n" + "=" * 50)
        print("CORRELATING DATASETS")
        print("=" * 50)
        
        # This would be implemented based on actual data structure
        print("Dataset correlation analysis would be implemented here.")
        print("This helps determine which crops grow best under which weather/price conditions.")
        
        return {}
    
    def generate_features_for_ml(self):
        """
        Generate features for machine learning models from historical datasets.
        """
        print("\n" + "=" * 50)
        print("GENERATING FEATURES FOR ML MODELS")
        print("=" * 50)
        
        features = {}
        
        # From crop area data
        area_analysis = self.analyze_crop_area_data()
        if area_analysis:
            for i, (crop, area) in enumerate(area_analysis['top_crops'].items()):
                features[f'area_top_{i}_{crop}'] = area
        
        # From crop yield data
        yield_analysis = self.analyze_crop_yield_data()
        if yield_analysis:
            for i, (crop, yield_val) in enumerate(yield_analysis['top_crops'].items()):
                features[f'yield_top_{i}_{crop}'] = yield_val
        
        # From production data
        production_analysis = self.analyze_production_data()
        if production_analysis:
            for i, (crop, production) in enumerate(production_analysis['top_crops'].items()):
                features[f'production_top_{i}_{crop}'] = production
        
        # From price data
        price_analysis = self.analyze_price_data()
        if price_analysis:
            for i, (commodity, price) in enumerate(list(price_analysis['average_prices'].items())[:5]):
                features[f'price_top_{i}_{commodity}'] = price
        
        # From NASA POWER data
        nasa_analysis = self.analyze_nasa_power_data()
        if nasa_analysis:
            features.update(nasa_analysis['weather_stats'])
        
        print(f"\nGenerated {len(features)} features for ML models:")
        for feature, value in list(features.items())[:10]:  # Show first 10
            print(f"  {feature}: {value}")
        if len(features) > 10:
            print(f"  ... and {len(features) - 10} more features")
        
        return features
    
    def save_analysis_report(self, features):
        """
        Save analysis report to a file.
        """
        report_path = self.data_dir / "dataset_analysis_report.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("SASYA-MITRA HISTORICAL DATASET ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("LOADED DATASETS:\n")
            for key, dataset in self.datasets.items():
                if dataset is not None:
                    f.write(f"  {key}: {dataset.shape}\n")
                else:
                    f.write(f"  {key}: Not available\n")
            
            f.write(f"\nGENERATED FEATURES FOR ML ({len(features)} total):\n")
            for feature, value in features.items():
                f.write(f"  {feature}: {value}\n")
        
        print(f"\n✅ Analysis report saved to: {report_path}")
    
    def run_complete_analysis(self):
        """
        Run complete analysis of all historical datasets.
        """
        print("SASYA-MITRA HISTORICAL DATASET ANALYSIS")
        print("=" * 50)
        
        # Load datasets
        self.load_datasets()
        
        # Generate features for ML
        features = self.generate_features_for_ml()
        
        # Save report
        self.save_analysis_report(features)
        
        print("\n" + "=" * 50)
        print("ANALYSIS COMPLETE")
        print("=" * 50)
        print("✅ Historical datasets have been analyzed")
        print("✅ Features extracted for machine learning")
        print("✅ Report generated")
        print("\nNext steps:")
        print("1. Use these features to train ML models")
        print("2. Identify which crops grow best under which conditions")
        print("3. Determine profitability based on price data")
        
        return features

if __name__ == "__main__":
    # Create analyzer and run complete analysis
    analyzer = HistoricalDatasetAnalyzer(".")
    features = analyzer.run_complete_analysis()