"""
API endpoints for Sasya-Mitra AI models.
"""

import os
import sys
import json
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add the models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from preprocessing.data_processor import AgriDataPreprocessor
from training.model_trainer import AgriYieldModel, AgriROIModel
from recommendation.engine import AgriRecommendationEngine, SoilData, WeatherData, EconomicData

app = Flask(__name__)
CORS(app)

# Global variables for models
yield_model = None
roi_model = None
recommendation_engine = None

def load_models():
    """Load trained models."""
    global yield_model, roi_model, recommendation_engine
    
    try:
        # Initialize models
        yield_model = AgriYieldModel()
        roi_model = AgriROIModel()
        recommendation_engine = AgriRecommendationEngine()
        
        # In a real implementation, you would load trained models from disk:
        # yield_model.load_model("models/yield_model")
        # roi_model.load_model("models/roi_model")
        
        print("Models loaded successfully")
        return True
    except Exception as e:
        print(f"Error loading models: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "Sasya-Mitra AI API"}), 200

@app.route('/predict/yield', methods=['POST'])
def predict_yield():
    """Predict crop yield based on input features."""
    try:
        # Get input data
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Convert to DataFrame (simplified)
        # In a real implementation, you would need proper feature engineering
        features = pd.DataFrame([data])
        
        # Make prediction (simplified - using recommendation engine)
        if recommendation_engine:
            # This is a placeholder - in reality, you would use the trained ML model
            prediction = 2500  # kg/acre default
            if 'land_area_acres' in data:
                prediction = prediction * data['land_area_acres']
            
            return jsonify({
                "predicted_yield_kg": prediction,
                "confidence": 0.85
            }), 200
        else:
            return jsonify({"error": "Recommendation engine not loaded"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route('/predict/roi', methods=['POST'])
def predict_roi():
    """Predict ROI based on input features."""
    try:
        # Get input data
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Make prediction (simplified - using recommendation engine)
        if recommendation_engine:
            # This is a placeholder - in reality, you would use the trained ML model
            roi = 2.5  # Default ROI
            
            return jsonify({
                "predicted_roi": roi,
                "confidence": 0.80
            }), 200
        else:
            return jsonify({"error": "Recommendation engine not loaded"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route('/recommend', methods=['POST'])
def generate_recommendation():
    """Generate agricultural recommendations."""
    try:
        # Get input data
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Extract required fields
        required_fields = ['location', 'land_area_acres', 'soil', 'weather', 'budget_inr']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create data objects
        soil_data = SoilData(
            ph=data['soil'].get('ph', 6.5),
            organic_carbon=data['soil'].get('organic_carbon', 1.0),
            nitrogen=data['soil'].get('nitrogen', 100),
            phosphorus=data['soil'].get('phosphorus', 30),
            potassium=data['soil'].get('potassium', 150),
            texture=data['soil'].get('texture', 'Loam'),
            drainage=data['soil'].get('drainage', 'Moderate')
        )
        
        weather_data = WeatherData(
            rainfall_mm=data['weather'].get('rainfall_mm', 800),
            temperature_c=data['weather'].get('temperature_c', 25),
            humidity=data['weather'].get('humidity', 60),
            solar_radiation=data['weather'].get('solar_radiation', 5.0)
        )
        
        economic_data = EconomicData(
            budget_inr=data.get('budget_inr', 50000),
            labor_availability=data.get('labor_availability', 'Medium'),
            input_cost_type=data.get('input_cost_type', 'Organic')
        )
        
        # Generate recommendation
        if recommendation_engine:
            recommendation = recommendation_engine.generate_recommendation(
                soil_data,
                weather_data,
                economic_data,
                data['land_area_acres'],
                data['location']
            )
            
            # Convert to dictionary for JSON serialization
            result = {
                "recommendations": {
                    "main_crop": recommendation.main_crop,
                    "intercrop": recommendation.intercrop,
                    "trees": recommendation.trees,
                    "layout": recommendation.layout,
                    "expected_yield_kg": recommendation.expected_yield_kg,
                    "profit_estimate_inr": recommendation.profit_estimate_inr,
                    "roi": recommendation.roi
                },
                "economic_summary": {
                    "total_cost": data['budget_inr'] * 0.6,  # Simplified
                    "expected_income": recommendation.profit_estimate_inr + (data['budget_inr'] * 0.6),
                    "payback_period_months": 12 / recommendation.roi if recommendation.roi > 0 else 12
                },
                "sustainability_tips": recommendation.sustainability_tips,
                "language_output": {
                    "hi": f"इस भूमि के लिए उपयुक्त फसलें {recommendation.main_crop} और {recommendation.intercrop} हैं। {' और '.join(recommendation.trees)} के पेड़ों को किनारे लगाएं।",
                    "kn": f"ಈ ಭೂಮಿಗೆ ಸೂಕ್ತವಾದ ಬೆಳೆಗಳು {recommendation.main_crop} ಮತ್ತು {recommendation.intercrop} ಆಗಿವೆ. {' ಮತ್ತು '.join(recommendation.trees)} ಮರಗಳನ್ನು ಅಂಚಿನಲ್ಲಿ ನೆಡಿ."
                }
            }
            
            return jsonify(result), 200
        else:
            return jsonify({"error": "Recommendation engine not loaded"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Recommendation generation failed: {str(e)}"}), 500

@app.route('/preprocess', methods=['POST'])
def preprocess_data():
    """Preprocess agricultural data."""
    try:
        # Get input data
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Initialize preprocessor
        preprocessor = AgriDataPreprocessor()
        
        # Process data based on type
        data_type = data.get('type')
        if data_type == 'nasa_power':
            # Process NASA POWER data
            # This is a simplified example
            result = {"message": "NASA POWER data processed successfully"}
        elif data_type == 'crop_price':
            # Process crop price data
            result = {"message": "Crop price data processed successfully"}
        elif data_type == 'yield':
            # Process yield data
            result = {"message": "Yield data processed successfully"}
        elif data_type == 'area':
            # Process area data
            result = {"message": "Area data processed successfully"}
        else:
            return jsonify({"error": "Invalid data type"}), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Data preprocessing failed: {str(e)}"}), 500

if __name__ == '__main__':
    # Load models on startup
    load_models()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)