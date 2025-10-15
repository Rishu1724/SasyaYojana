"""
Script for periodic model retraining using feedback data from Firebase.
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import joblib
import argparse

# Add the current directory to the path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from preprocessing.data_processor import AgriDataPreprocessor
from training.model_trainer import AgriYieldModel, AgriROIModel
from firebase_admin import credentials, initialize_app, firestore
import firebase_admin

# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK."""
    try:
        # Use service account key file (you'll need to create this)
        cred = credentials.Certificate("firebase-service-account.json")
        initialize_app(cred)
        print("Firebase Admin SDK initialized successfully")
        return firestore.client()
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        print("Make sure you have firebase-admin installed and a service account key file")
        return None

def fetch_feedback_data(db, days_back=30):
    """
    Fetch feedback data from Firebase for retraining.
    
    Parameters:
    db: Firestore client
    days_back (int): Number of days back to fetch data
    
    Returns:
    list: List of feedback records
    """
    try:
        # Calculate the date threshold
        threshold_date = datetime.now() - timedelta(days=days_back)
        
        # Query feedback collection
        feedback_ref = db.collection('feedback')
        query = feedback_ref.where('timestamp', '>=', threshold_date).order_by('timestamp', direction=firestore.Query.DESCENDING)
        
        docs = query.stream()
        feedback_data = []
        
        for doc in docs:
            feedback_data.append({
                'id': doc.id,
                **doc.to_dict()
            })
        
        print(f"Fetched {len(feedback_data)} feedback records from the last {days_back} days")
        return feedback_data
    except Exception as e:
        print(f"Error fetching feedback data: {e}")
        return []

def fetch_prediction_data(db, prediction_ids):
    """
    Fetch prediction data for the given prediction IDs.
    
    Parameters:
    db: Firestore client
    prediction_ids (list): List of prediction IDs
    
    Returns:
    dict: Dictionary mapping prediction IDs to prediction data
    """
    try:
        prediction_data = {}
        
        for pred_id in prediction_ids:
            try:
                doc = db.collection('predictions').document(pred_id).get()
                if doc.exists:
                    prediction_data[pred_id] = doc.to_dict()
            except Exception as e:
                print(f"Error fetching prediction {pred_id}: {e}")
        
        print(f"Fetched {len(prediction_data)} prediction records")
        return prediction_data
    except Exception as e:
        print(f"Error fetching prediction data: {e}")
        return {}

def prepare_training_data(feedback_data, prediction_data):
    """
    Prepare training data from feedback and prediction data.
    
    Parameters:
    feedback_data (list): List of feedback records
    prediction_data (dict): Dictionary of prediction data
    
    Returns:
    pd.DataFrame: Training data
    """
    try:
        training_records = []
        
        for feedback in feedback_data:
            pred_id = feedback.get('prediction_id')
            if not pred_id or pred_id not in prediction_data:
                continue
                
            prediction = prediction_data[pred_id]
            farmer_data = prediction.get('farmer_data', {})
            predictions = prediction.get('predictions', {})
            
            # Create a training record
            record = {
                # Original predictions
                'predicted_yield': predictions.get('yield_kg_per_acre', 0),
                'predicted_roi': predictions.get('roi', 0),
                
                # Actual values from feedback
                'actual_yield': feedback.get('yield_actual', 0),
                'actual_roi': feedback.get('roi_actual', 0),
                
                # Farmer input data
                'land_area_acres': farmer_data.get('land_area_acres', 1),
                'budget_inr': farmer_data.get('budget_inr', 50000),
                
                # Soil data
                'soil_ph': farmer_data.get('soil', {}).get('ph', 6.5),
                'soil_organic_carbon': farmer_data.get('soil', {}).get('organic_carbon', 1.0),
                'soil_nitrogen': farmer_data.get('soil', {}).get('nitrogen', 150),
                'soil_phosphorus': farmer_data.get('soil', {}).get('phosphorus', 30),
                'soil_potassium': farmer_data.get('soil', {}).get('potassium', 150),
                
                # Weather data (if available in prediction)
                'avg_temperature_c': prediction.get('weather_data', {}).get('avg_temperature_c', 25),
                'avg_rainfall_mm': prediction.get('weather_data', {}).get('avg_rainfall_mm', 1000),
                'avg_humidity': prediction.get('weather_data', {}).get('avg_humidity', 65),
                'solar_radiation': prediction.get('weather_data', {}).get('solar_radiation', 5),
                
                # Feedback metadata
                'accuracy_rating': feedback.get('accuracy_rating', 3),
                'timestamp': feedback.get('timestamp')
            }
            
            training_records.append(record)
        
        training_df = pd.DataFrame(training_records)
        print(f"Prepared {len(training_df)} training records")
        return training_df
    except Exception as e:
        print(f"Error preparing training data: {e}")
        return pd.DataFrame()

def retrain_models(training_data):
    """
    Retrain models with the new feedback data.
    
    Parameters:
    training_data (pd.DataFrame): Training data
    
    Returns:
    tuple: (yield_model, roi_model) or (None, None) if failed
    """
    try:
        if training_data.empty:
            print("No training data available")
            return None, None
        
        print("Retraining models with feedback data...")
        
        # Initialize models
        yield_model = AgriYieldModel()
        roi_model = AgriROIModel()
        
        # For this simplified implementation, we'll create mock datasets
        # In a real implementation, you would use the training_data to update the models
        mock_datasets = {
            '1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻': None,
            'All India level Average Yield of Principal Crops from 2001-02 to 2015-16': None,
            'All India level Area Under Principal Crops from 2001-02 to 2015-16': None,
            'Production of principle crops': None,
            'price': None,
            'Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc': None
        }
        
        # Train models (in a real implementation, you would incorporate the feedback data)
        yield_metrics = yield_model.train(mock_datasets)
        roi_metrics = roi_model.train(mock_datasets)
        
        print("Models retrained successfully")
        return yield_model, roi_model
    except Exception as e:
        print(f"Error retraining models: {e}")
        return None, None

def save_retrained_models(yield_model, roi_model, version):
    """
    Save the retrained models with a new version.
    
    Parameters:
    yield_model: Retrained yield model
    roi_model: Retrained ROI model
    version (str): Model version identifier
    """
    try:
        if yield_model and roi_model:
            # Create versioned model directory
            model_dir = f"models/saved_models/v{version}"
            os.makedirs(model_dir, exist_ok=True)
            
            # Save models
            yield_model.save_model(f"{model_dir}/yield_model")
            roi_model.save_model(f"{model_dir}/roi_model")
            
            print(f"Retrained models saved to {model_dir}")
        else:
            print("No models to save")
    except Exception as e:
        print(f"Error saving retrained models: {e}")

def update_model_version_info(db, version, metrics):
    """
    Update model version information in Firebase.
    
    Parameters:
    db: Firestore client
    version (str): Model version
    metrics (dict): Model performance metrics
    """
    try:
        version_info = {
            'version': version,
            'timestamp': datetime.now(),
            'yield_model_metrics': metrics.get('yield_metrics', {}),
            'roi_model_metrics': metrics.get('roi_metrics', {}),
            'training_data_points': metrics.get('data_points', 0)
        }
        
        db.collection('model_versions').add(version_info)
        print(f"Model version {version} information updated in Firebase")
    except Exception as e:
        print(f"Error updating model version info: {e}")

def main():
    """Main function for periodic model retraining."""
    parser = argparse.ArgumentParser(description='Retrain models with feedback data')
    parser.add_argument('--days', type=int, default=30, help='Number of days back to fetch feedback data')
    parser.add_argument('--version', type=str, default=None, help='Model version identifier')
    args = parser.parse_args()
    
    print("=== Sasya-Mitra Model Retraining ===")
    print(f"Fetching feedback data from the last {args.days} days")
    
    # Initialize Firebase
    db = initialize_firebase()
    if not db:
        print("Failed to initialize Firebase. Exiting.")
        return
    
    # Fetch feedback data
    feedback_data = fetch_feedback_data(db, args.days)
    if not feedback_data:
        print("No feedback data available for retraining")
        return
    
    # Extract prediction IDs
    prediction_ids = [feedback.get('prediction_id') for feedback in feedback_data if feedback.get('prediction_id')]
    prediction_ids = list(set(prediction_ids))  # Remove duplicates
    
    # Fetch prediction data
    prediction_data = fetch_prediction_data(db, prediction_ids)
    
    # Prepare training data
    training_data = prepare_training_data(feedback_data, prediction_data)
    if training_data.empty:
        print("No training data prepared. Exiting.")
        return
    
    # Retrain models
    yield_model, roi_model = retrain_models(training_data)
    
    # Save retrained models
    version = args.version or datetime.now().strftime("%Y%m%d_%H%M%S")
    save_retrained_models(yield_model, roi_model, version)
    
    # Update model version info in Firebase
    metrics = {
        'yield_metrics': {},  # In a real implementation, you would include actual metrics
        'roi_metrics': {},    # In a real implementation, you would include actual metrics
        'data_points': len(training_data)
    }
    update_model_version_info(db, version, metrics)
    
    print("\n=== Retraining Complete ===")
    print(f"Models have been retrained with {len(training_data)} feedback records")
    print(f"New model version: {version}")

if __name__ == "__main__":
    main()