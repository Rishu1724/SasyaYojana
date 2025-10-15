# Example: Using Your Datasets with Sasya-Mitra AI Models

This example demonstrates how to use your agricultural datasets with the Sasya-Mitra AI system.

## Step 1: Organize Your Datasets

First, organize your datasets in the following structure:

```
data/
├── nasa_power/
│   └── nasa_power_data.csv
├── crop_prices/
│   └── crop_prices.csv
├── crop_area/
│   └── crop_area.csv
├── crop_yield/
│   └── crop_yield.csv
└── production/
    └── production_data.csv
```

## Step 2: Load and Preprocess Your Data

```python
import pandas as pd
import sys
import os

# Add the models directory to the path
sys.path.append(os.path.join(os.getcwd(), 'models'))

from models.preprocessing.data_processor import AgriDataPreprocessor

# Initialize preprocessor
preprocessor = AgriDataPreprocessor()

# Load your actual datasets
# Replace these paths with the actual paths to your datasets
nasa_file = "data/nasa_power/nasa_power_data.csv"
price_file = "data/crop_prices/crop_prices.csv"
yield_file = "data/crop_yield/crop_yield.csv"
area_file = "data/crop_area/crop_area.csv"

# Load and preprocess data
print("Loading NASA POWER data...")
nasa_data = preprocessor.load_nasa_power_data(nasa_file)

print("Loading crop price data...")
price_data = preprocessor.load_crop_price_data(price_file)

print("Loading crop yield data...")
yield_data = preprocessor.load_yield_data(yield_file)

print("Loading crop area data...")
area_data = preprocessor.load_area_data(area_file)

print("Creating features...")
features = preprocessor.create_features(nasa_data, price_data, yield_data, area_data)

print(f"Processed {len(features)} samples with {len(features.columns)} features")
print("Features:", list(features.columns))
```

## Step 3: Prepare Data for Training

```python
# Prepare data for yield prediction model
# You'll need to determine the target variable based on your data
# This is just an example - adjust based on your actual data structure

# Example: Use maize yield as target variable
if 'yield_0' in features.columns:
    X, y_yield = preprocessor.prepare_model_data(features, target_column='yield_0')
else:
    # Create a synthetic target for demonstration
    X, _ = preprocessor.prepare_model_data(features)
    y_yield = features['rainfall'] * 10 + features['avg_temperature'] * 50

# Prepare data for ROI prediction model
# Example: Calculate ROI based on yield and price
if 'price_0' in features.columns and 'yield_0' in features.columns:
    X_roi, y_roi = preprocessor.prepare_model_data(features, target_column='roi')
else:
    # Create a synthetic target for demonstration
    X_roi, _ = preprocessor.prepare_model_data(features)
    y_roi = (features['rainfall'] / 100) + (features['avg_temperature'] / 10)
```

## Step 4: Train the Models

```python
from models.training.model_trainer import AgriYieldModel, AgriROIModel

# Initialize models
print("Initializing models...")
yield_model = AgriYieldModel()
roi_model = AgriROIModel()

# Train yield prediction model
print("Training yield prediction model...")
yield_metrics = yield_model.train(X, y_yield)
print(f"Yield Model - RF MSE: {yield_metrics['rf_metrics']['mse']:.2f}, R²: {yield_metrics['rf_metrics']['r2']:.2f}")
print(f"Yield Model - XGB MSE: {yield_metrics['xgb_metrics']['mse']:.2f}, R²: {yield_metrics['xgb_metrics']['r2']:.2f}")

# Train ROI prediction model
print("Training ROI prediction model...")
roi_metrics = roi_model.train(X_roi, y_roi)
print(f"ROI Model - MSE: {roi_metrics['mse']:.2f}, R²: {roi_metrics['r2']:.2f}")

# Save models
print("Saving models...")
yield_model.save_model("models/yield_model")
roi_model.save_model("models/roi_model")
print("Models saved successfully!")
```

## Step 5: Generate Recommendations

```python
from models.recommendation.engine import AgriRecommendationEngine, SoilData, WeatherData, EconomicData

# Initialize recommendation engine
engine = AgriRecommendationEngine()

# Example farmer data
soil_data = SoilData(
    ph=6.7,
    organic_carbon=1.2,
    nitrogen=150,
    phosphorus=40,
    potassium=200,
    texture='Loam',
    drainage='Moderate'
)

weather_data = WeatherData(
    rainfall_mm=850,
    temperature_c=28,
    humidity=65,
    solar_radiation=5.5
)

economic_data = EconomicData(
    budget_inr=60000,
    labor_availability='Medium',
    input_cost_type='Organic'
)

# Generate recommendation
recommendation = engine.generate_recommendation(
    soil_data, 
    weather_data, 
    economic_data, 
    land_area_acres=5.0,
    location="Belagavi, Karnataka"
)

print("=== Agricultural Recommendation ===")
print(f"Location: Belagavi, Karnataka")
print(f"Land Area: 5.0 acres")
print(f"Main Crop: {recommendation.main_crop}")
print(f"Intercrop: {recommendation.intercrop}")
print(f"Trees: {', '.join(recommendation.trees)}")
print(f"Layout: {recommendation.layout}")
print(f"Expected Yield: {recommendation.expected_yield_kg:.0f} kg")
print(f"Profit Estimate: ₹{recommendation.profit_estimate_inr:,.0f}")
print(f"ROI: {recommendation.roi:.1f}x")
print("\nSustainability Tips:")
for i, tip in enumerate(recommendation.sustainability_tips, 1):
    print(f"  {i}. {tip}")
```

## Step 6: Start the API Server

```bash
# In a terminal, run:
python models/api/app.py
```

The API will be available at `http://localhost:5000`

## Testing the API

You can test the API with curl or any HTTP client:

```bash
# Test health check
curl http://localhost:5000/health

# Test recommendation endpoint
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Belagavi, Karnataka",
    "land_area_acres": 5,
    "soil": {
      "ph": 6.7,
      "organic_carbon": 1.2,
      "nitrogen": 150,
      "phosphorus": 40,
      "potassium": 200,
      "texture": "Loam",
      "drainage": "Moderate"
    },
    "weather": {
      "rainfall_mm": 850,
      "temperature_c": 28,
      "humidity": 65,
      "solar_radiation": 5.5
    },
    "budget_inr": 60000,
    "labor_availability": "Medium",
    "input_cost_type": "Organic"
  }'
```

## Next Steps

1. Replace the example data paths with your actual dataset paths
2. Adjust the feature engineering based on your data structure
3. Fine-tune the models with your specific requirements
4. Deploy the API to a production environment
5. Integrate with the Sasya-Mitra frontend application

This example provides a foundation for using your agricultural datasets with the Sasya-Mitra AI system. Adjust the code based on your specific data format and requirements.