# Sasya-Mitra AI Model Development Guide

## Overview

This guide explains how to develop and deploy AI models for the Sasya-Mitra agricultural advisory system using your datasets:
1. NASA POWER data (Rainfall, Temperature, Humidity, Radiation)
2. Crop price datasets
3. All India level Area Under Principal Crops (2001-02 to 2015-16)
4. All India level Average Yield of Principal Crops (2001-02 to 2015-16)
5. Production of principal crops

## Directory Structure

```
models/
├── preprocessing/          # Data preprocessing utilities
├── training/              # Model training scripts
├── recommendation/        # Recommendation engine
├── api/                   # API endpoints
├── requirements.txt       # Python dependencies
└── README.md             # This file

notebooks/
└── model_development.ipynb  # Jupyter notebook for model development

data/
├── nasa_power/           # NASA POWER data
├── crop_prices/          # Crop price datasets
├── crop_area/            # Area under crops data
├── crop_yield/           # Crop yield data
└── production/           # Production data
```

## Setting Up the Environment

1. Install Python 3.8 or higher
2. Install required packages:
   ```bash
   pip install -r models/requirements.txt
   ```

## Data Preparation

### 1. NASA POWER Data
- Place your NASA POWER CSV files in `data/nasa_power/`
- Expected columns: YEAR, T2M (temperature), RH2M (humidity), PRECTOTCORR (precipitation), ALLSKY_SFC_SW_DWN (solar radiation)

### 2. Crop Price Data
- Place your crop price CSV files in `data/crop_prices/`
- Expected columns: YEAR, [CROP_NAME]_PRICE for each crop

### 3. Crop Area Data
- Place your area data CSV files in `data/crop_area/`
- Expected columns: YEAR, [CROP_NAME]_AREA for each crop

### 4. Crop Yield Data
- Place your yield data CSV files in `data/crop_yield/`
- Expected columns: YEAR, [CROP_NAME]_YIELD for each crop

### 5. Production Data
- Place your production data CSV files in `data/production/`
- Expected columns: YEAR, [CROP_NAME]_PRODUCTION for each crop

## Model Development Process

### 1. Data Preprocessing
Use the `AgriDataPreprocessor` class in `models/preprocessing/data_processor.py`:

```python
from preprocessing.data_processor import AgriDataPreprocessor

preprocessor = AgriDataPreprocessor()

# Load and preprocess datasets
nasa_data = preprocessor.load_nasa_power_data('data/nasa_power/your_file.csv')
price_data = preprocessor.load_crop_price_data('data/crop_prices/your_file.csv')
yield_data = preprocessor.load_yield_data('data/crop_yield/your_file.csv')
area_data = preprocessor.load_area_data('data/crop_area/your_file.csv')

# Create features for training
features = preprocessor.create_features(nasa_data, price_data, yield_data, area_data)
```

### 2. Model Training
Use the model training scripts in `models/training/`:

```python
from training.model_trainer import AgriYieldModel, AgriROIModel

# Initialize models
yield_model = AgriYieldModel()
roi_model = AgriROIModel()

# Prepare training data
X, y_yield = preprocessor.prepare_model_data(features, target_column='yield')
X, y_roi = preprocessor.prepare_model_data(features, target_column='roi')

# Train models
yield_metrics = yield_model.train(X, y_yield)
roi_metrics = roi_model.train(X, y_roi)

# Save models
yield_model.save_model("models/yield_model")
roi_model.save_model("models/roi_model")
```

### 3. Recommendation Engine
The recommendation engine in `models/recommendation/engine.py` combines the models with expert rules:

```python
from recommendation.engine import AgriRecommendationEngine, SoilData, WeatherData, EconomicData

engine = AgriRecommendationEngine()

# Create input data objects
soil_data = SoilData(ph=6.7, organic_carbon=1.2, nitrogen=150, phosphorus=40, potassium=200, texture='Loam', drainage='Moderate')
weather_data = WeatherData(rainfall_mm=850, temperature_c=28, humidity=65, solar_radiation=5.5)
economic_data = EconomicData(budget_inr=60000, labor_availability='Medium', input_cost_type='Organic')

# Generate recommendation
recommendation = engine.generate_recommendation(soil_data, weather_data, economic_data, 5.0, "Belagavi, Karnataka")
```

### 4. API Deployment
Run the API server:
```bash
python models/api/app.py
```

The API will be available at `http://localhost:5000` with the following endpoints:
- `POST /predict/yield` - Predict crop yield
- `POST /predict/roi` - Predict return on investment
- `POST /recommend` - Generate complete recommendations
- `POST /preprocess` - Preprocess agricultural data

## Using Your Datasets

### Step 1: Data Integration
1. Place your CSV files in the appropriate directories under `data/`
2. Update the data loading functions in `data_processor.py` to match your CSV structure
3. Ensure consistent column names and data types

### Step 2: Feature Engineering
Modify the `create_features` method in `data_processor.py` to:
1. Extract relevant features from your datasets
2. Handle missing values appropriately
3. Normalize/standardize numerical features
4. Encode categorical variables

### Step 3: Model Training
1. Load your datasets using the preprocessor
2. Create feature matrices and target vectors
3. Split data into training and testing sets
4. Train the models using your data
5. Evaluate model performance
6. Save trained models

### Step 4: Model Deployment
1. Update the API endpoints in `models/api/app.py` to load your trained models
2. Test the API with sample requests
3. Deploy the API to a server or cloud platform

## Example Usage

See `notebooks/model_development.ipynb` for a complete example of how to:
1. Load and preprocess your datasets
2. Train machine learning models
3. Generate agricultural recommendations
4. Evaluate model performance

## Next Steps

1. Replace sample data with your actual datasets
2. Fine-tune model hyperparameters for better performance
3. Add more features from your datasets
4. Implement cross-validation for robust evaluation
5. Deploy the API to a production environment
6. Integrate with the existing Sasya-Mitra frontend

## Troubleshooting

### Common Issues
1. **Missing Data**: Use forward-fill/backward-fill or interpolation to handle missing values
2. **Inconsistent Formats**: Standardize date formats, numerical representations, and column names
3. **Memory Issues**: Process large datasets in chunks or use data sampling
4. **Performance**: Optimize feature engineering and use efficient data structures

### Getting Help
If you encounter issues:
1. Check the console output for error messages
2. Verify your data files are in the correct format
3. Ensure all required dependencies are installed
4. Consult the documentation for each library used