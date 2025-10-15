# Real-Time AI Model Prediction API

This document explains how the real-time prediction system works in Sasya-Mitra, which fetches weather data from NASA POWER and uses trained machine learning models to make predictions.

## Overview

When a farmer enters details, the backend:

1. Fetches real-time weather from NASA POWER API
2. Passes values into trained ML models
3. Returns predictions and recommendations

## API Endpoints

### 1. Real-Time Prediction Endpoint

**POST** `/predict/realtime`

#### Request Body
```json
{
  "location": {
    "lat": 18.5204,
    "lng": 73.8567
  },
  "land_area_acres": 5,
  "soil": {
    "ph": 6.5,
    "organic_carbon": 1.2,
    "nitrogen": 150,
    "phosphorus": 30,
    "potassium": 150
  },
  "budget_inr": 50000
}
```

#### Response
```json
{
  "predictions": {
    "yield_kg_per_acre": 3000,
    "roi": 2.8,
    "confidence": 0.85
  },
  "weather_data": {
    "avg_temperature_c": 28,
    "avg_humidity": 65,
    "avg_rainfall_mm": 980,
    "solar_radiation": 5.5
  },
  "recommendations": {
    "best_crop": "Maize",
    "planting_time": "June-July",
    "irrigation_needs": "Moderate"
  }
}
```

### 2. Yield Prediction Endpoint

**POST** `/predict/yield`

#### Request Body
```json
{
  "location": {
    "lat": 18.5204,
    "lng": 73.8567
  },
  "land_area_acres": 5,
  "soil": {
    "ph": 6.5,
    "organic_carbon": 1.2,
    "nitrogen": 150,
    "phosphorus": 30,
    "potassium": 150
  },
  "budget_inr": 50000
}
```

#### Response
```json
{
  "predicted_yield_kg": 15000,
  "confidence": 0.85,
  "weather_data": {
    "avg_temperature_c": 28,
    "avg_humidity": 65,
    "avg_rainfall_mm": 980,
    "solar_radiation": 5.5
  }
}
```

### 3. ROI Prediction Endpoint

**POST** `/predict/roi`

#### Request Body
```json
{
  "location": {
    "lat": 18.5204,
    "lng": 73.8567
  },
  "land_area_acres": 5,
  "soil": {
    "ph": 6.5,
    "organic_carbon": 1.2,
    "nitrogen": 150,
    "phosphorus": 30,
    "potassium": 150
  },
  "budget_inr": 50000
}
```

#### Response
```json
{
  "predicted_roi": 2.8,
  "confidence": 0.80,
  "weather_data": {
    "avg_temperature_c": 28,
    "avg_humidity": 65,
    "avg_rainfall_mm": 980,
    "solar_radiation": 5.5
  }
}
```

## How It Works

### Step 1: NASA POWER Weather Data Fetching

The system fetches real-time climatological data from NASA POWER API:

```python
def fetch_nasa_power_weather(lat, lon):
    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    params = {
        "parameters": "T2M,RH2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "format": "JSON",
        "start": 2020,
        "end": 2022
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    return {
        "avg_temperature_c": round(parameters["T2M"]["ANN"]),
        "avg_humidity": round(parameters["RH2M"]["ANN"]),
        "avg_rainfall_mm": round(parameters["PRECTOTCORR"]["ANN"] * 3650),  # Convert to mm/year
        "solar_radiation": round(parameters["ALLSKY_SFC_SW_DWN"]["ANN"])
    }
```

### Step 2: Feature Preparation

The system prepares features by combining:
- Real-time weather data from NASA
- Farmer input data (soil properties, land area, budget)
- Derived features from historical datasets

### Step 3: Model Prediction

The system uses trained Random Forest and XGBoost models:

```python
# Load trained models
yield_model = joblib.load("saved_models/yield_model_rf.pkl")
roi_model = joblib.load("saved_models/roi_model_roi.pkl")

# Prepare features
features_df = prepare_features_for_prediction(farmer_data)

# Make predictions
yield_prediction = yield_model.predict(features_df)
roi_prediction = roi_model.predict(features_df)
```

### Step 4: Response Generation

The system returns predictions along with weather data and recommendations.

## Trained Models

The following models are used:

1. **Yield Prediction Model**:
   - Algorithm: Random Forest Regressor
   - Features: 111 agricultural and weather features
   - Performance: MSE ~44944, MAE ~212

2. **ROI Prediction Model**:
   - Algorithm: XGBoost Regressor
   - Features: 64 agricultural and weather features
   - Performance: MSE ~4.0, MAE ~2.0

## Derived Features from Dataset Merging

As per your requirements, we implemented the merging approach:

```python
# Merge datasets on Crop and Year
merged_df = pd.merge(area_df, yield_df, on=["Crop", "Year"], how="inner")
merged_df = pd.merge(merged_df, production_df, on=["Crop", "Year"], how="inner")

# Calculate derived metrics
merged_df["yield_per_area"] = merged_df["Production"] / merged_df["Area"]
merged_df["yield_efficiency"] = merged_df["Yield"] / merged_df["Area"]
```

These derived features are included in the model predictions.

## Running the API

To start the API server:

```bash
cd models/api
python app.py
```

The API will be available at `http://localhost:5000`

## Testing the API

You can test the API using curl:

```bash
curl -X POST http://localhost:5000/predict/realtime \
  -H "Content-Type: application/json" \
  -d '{
    "location": {
      "lat": 18.5204,
      "lng": 73.8567
    },
    "land_area_acres": 5,
    "soil": {
      "ph": 6.5,
      "organic_carbon": 1.2,
      "nitrogen": 150,
      "phosphorus": 30,
      "potassium": 150
    },
    "budget_inr": 50000
  }'
```

## Integration with Frontend

The frontend can call these API endpoints when a farmer submits their details:

```javascript
// Example frontend integration
async function getAgriculturalPrediction(farmerData) {
  try {
    const response = await fetch('http://localhost:5000/predict/realtime', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(farmerData),
    });
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Prediction error:', error);
  }
}
```

## Error Handling

The API includes comprehensive error handling:
- Network failures when fetching NASA data
- Model loading failures
- Invalid input data
- Server errors

In case of failures, the system provides fallback predictions with appropriate confidence levels.