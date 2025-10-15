# Sasya-Mitra Dataset Integration Guide

This guide explains how to integrate your agricultural datasets with the Sasya-Mitra AI system.

## Your Datasets

You've provided the following datasets:

1. **Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc.csv** - Natural disaster impact data
2. **1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻.csv** - Weather and climate data
3. **All India level Average Yield of Principal Crops from 2001-02 to 2015-16.csv** - Historical crop yield data
4. **All India level Area Under Principal Crops from 2001-02 to 2015-16.csv** - Crop cultivation area data
5. **Production of principle crops.csv** - Crop production data
6. **price.csv** - Crop price data

## How to Process Your Datasets

### 1. Place Your Datasets

Place all your CSV files in the `data/` directory of the Sasya-Mitra project:

```
SasyaYojana/
├── data/
│   ├── Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc.csv
│   ├── 1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻.csv
│   ├── All India level Average Yield of Principal Crops from 2001-02 to 2015-16.csv
│   ├── All India level Area Under Principal Crops from 2001-02 to 2015-16.csv
│   ├── Production of principle crops.csv
│   └── price.csv
```

### 2. Process Your Datasets

Run the Python script to process your datasets:

```bash
cd data
python process_user_datasets.py
```

This will:
- Load all your datasets
- Process each dataset according to its type
- Extract relevant features for AI modeling
- Combine datasets for comprehensive analysis

### 3. Train AI Models

After processing your datasets, you can train the AI models:

```bash
cd models
python train_models.py
```

This will:
- Train yield prediction models using Random Forest and XGBoost
- Train ROI prediction models
- Evaluate model performance
- Save trained models for future use

## How Your Data is Used in Sasya-Mitra

### Weather Intelligence (NASA POWER Data)
- Temperature, humidity, rainfall, and solar radiation data
- Used for crop suitability analysis
- Integrated with real-time weather forecasting

### Economic Intelligence (Price Data)
- Historical crop price trends
- Used for profitability analysis
- Integrated with market forecasting

### Agricultural Intelligence (Yield, Area, Production Data)
- Historical crop performance data
- Used for yield prediction models
- Combined with weather and economic data for comprehensive analysis

### Risk Intelligence (Damage Data)
- Historical natural disaster impact data
- Used for risk assessment and mitigation planning
- Integrated with crop selection recommendations

## Accessing Processed Data in the Frontend

The processed data is accessible through the AgroIntel service in the frontend:

```javascript
import agroIntelService from './src/services/agroIntelService';

// Get real-time predictions
const predictions = await agroIntelService.fetchRealTimePredictions({
  location: { lat: 18.5204, lng: 73.8567 },
  land_area_acres: 5,
  soil: {
    ph: 6.5,
    organic_carbon: 1.2,
    nitrogen: 150,
    phosphorus: 30,
    potassium: 150
  },
  budget_inr: 50000
});
```

## Next Steps

1. Run the data processing script to see how your datasets are processed
2. Train the AI models using your data
3. Test the AI recommendations in the Sasya-Mitra web application
4. Customize the models based on your specific agricultural needs

For any questions or support, please refer to the main documentation or contact the development team.