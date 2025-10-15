"""
Example script showing how to use the trained models for predictions.
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path

def load_trained_models():
    """
    Load the trained models from disk.
    
    Returns:
    tuple: (yield_model, roi_model)
    """
    try:
        # Load yield prediction models
        rf_model = joblib.load("saved_models/yield_model_rf.pkl")
        xgb_model = joblib.load("saved_models/yield_model_xgb.pkl")
        scaler = joblib.load("saved_models/yield_model_scaler.pkl")
        feature_names = joblib.load("saved_models/yield_model_features.pkl")
        
        # Load ROI prediction model
        roi_model = joblib.load("saved_models/roi_model_roi.pkl")
        roi_scaler = joblib.load("saved_models/roi_model_scaler.pkl")
        roi_feature_names = joblib.load("saved_models/roi_model_features.pkl")
        
        print("✅ Loaded all trained models successfully")
        return {
            'yield_rf': rf_model,
            'yield_xgb': xgb_model,
            'yield_scaler': scaler,
            'yield_features': feature_names,
            'roi': roi_model,
            'roi_scaler': roi_scaler,
            'roi_features': roi_feature_names
        }
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return None

def create_sample_input_data():
    """
    Create sample input data for prediction.
    
    Returns:
    dict: Sample input data
    """
    # Sample weather conditions
    sample_data = {
        'avg_temperature': 26.5,  # Celsius
        'avg_humidity': 68.0,     # Percentage
        'avg_rainfall': 1150.0,   # mm/year
        'solar_radiation': 210.0, # W/m2
        # Sample crop data
        'yield_mean_0_RICE': 3100.0,     # kg/ha
        'yield_mean_1_WHEAT': 2600.0,    # kg/ha
        'area_mean_0_RICE': 2050000.0,   # hectares
        'area_mean_1_WHEAT': 850000.0,   # hectares
        'production_mean_0_RICE': 2800000.0,  # tons
        'production_mean_1_WHEAT': 2500000.0, # tons
        # Sample price data
        'price_mean_0_RICE': 21.0,  # Rs/kg
        'price_mean_1_WHEAT': 16.0, # Rs/kg
        # Damage data
        'total_flood_damage': 150.0,
        'total_cyclone_damage': 75.0,
        'total_landslide_damage': 25.0,
        # Derived features from our merging approach
        'yield_per_area_RICE': 1.37,  # Production/Area ratio
        'yield_efficiency_RICE': 0.0015,  # Yield/Area ratio
        'yield_per_area_WHEAT': 2.94,  # Production/Area ratio
        'yield_efficiency_WHEAT': 0.0031  # Yield/Area ratio
    }
    
    return sample_data

def prepare_features_for_prediction(sample_data, feature_names):
    """
    Prepare features for model prediction.
    
    Parameters:
    sample_data (dict): Sample input data
    feature_names (list): List of feature names the model expects
    
    Returns:
    pd.DataFrame: Prepared feature matrix
    """
    # Create a DataFrame with all required features
    features = {}
    
    # Fill in the provided data
    for key, value in sample_data.items():
        features[key] = value
    
    # Fill missing features with 0
    for feature in feature_names:
        if feature not in features:
            features[feature] = 0.0
    
    # Ensure correct order of features
    ordered_features = {feature: features[feature] for feature in feature_names}
    
    # Convert to DataFrame
    X = pd.DataFrame([ordered_features])
    
    return X

def make_predictions(models, sample_data):
    """
    Make predictions using the trained models.
    
    Parameters:
    models (dict): Loaded models
    sample_data (dict): Sample input data
    
    Returns:
    dict: Predictions from all models
    """
    print("Making predictions with trained models...")
    
    # Prepare features for yield prediction
    X_yield = prepare_features_for_prediction(sample_data, models['yield_features'])
    
    # Make yield predictions
    yield_rf_pred = models['yield_rf'].predict(X_yield)[0]
    yield_xgb_pred = models['yield_xgb'].predict(X_yield)[0]
    
    # Ensemble prediction (average)
    yield_ensemble_pred = (yield_rf_pred + yield_xgb_pred) / 2
    
    # Prepare features for ROI prediction
    X_roi = prepare_features_for_prediction(sample_data, models['roi_features'])
    
    # Make ROI prediction
    roi_pred = models['roi'].predict(X_roi)[0]
    
    return {
        'yield_rf': yield_rf_pred,
        'yield_xgb': yield_xgb_pred,
        'yield_ensemble': yield_ensemble_pred,
        'roi': roi_pred
    }

def main():
    """
    Main function to demonstrate model usage.
    """
    print("SASYA-MITRA: Using Trained Models for Predictions")
    print("=" * 50)
    
    # Load trained models
    models = load_trained_models()
    if not models:
        print("❌ Failed to load models. Please train models first.")
        return
    
    # Create sample input data
    sample_data = create_sample_input_data()
    print("\nSample Input Data:")
    for key, value in list(sample_data.items())[:10]:  # Show first 10 features
        print(f"  {key}: {value}")
    print("  ...")
    
    # Make predictions
    predictions = make_predictions(models, sample_data)
    
    # Display results
    print("\n" + "=" * 50)
    print("PREDICTION RESULTS")
    print("=" * 50)
    print(f"Yield Prediction (Random Forest): {predictions['yield_rf']:.2f} kg/ha")
    print(f"Yield Prediction (XGBoost): {predictions['yield_xgb']:.2f} kg/ha")
    print(f"Yield Prediction (Ensemble): {predictions['yield_ensemble']:.2f} kg/ha")
    print(f"ROI Prediction: {predictions['roi']:.2f}%")
    
    # Provide recommendations based on predictions
    print("\n" + "=" * 50)
    print("RECOMMENDATIONS")
    print("=" * 50)
    
    if predictions['yield_ensemble'] > 3000:
        print("✅ High yield predicted. This is a good crop choice.")
    elif predictions['yield_ensemble'] > 2000:
        print("⚠️ Moderate yield predicted. Consider crop management practices.")
    else:
        print("❌ Low yield predicted. Consider alternative crops or interventions.")
    
    if predictions['roi'] > 15:
        print("✅ High ROI predicted. This crop is financially attractive.")
    elif predictions['roi'] > 10:
        print("⚠️ Moderate ROI predicted. Evaluate market conditions.")
    else:
        print("❌ Low ROI predicted. Consider alternative crops or markets.")
    
    print("\n" + "=" * 50)
    print("PREDICTION COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()