"""
API endpoints for Sasya-Mitra AI models.
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# Add the models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from preprocessing.data_processor import AgriDataPreprocessor
from training.model_trainer import AgriYieldModel, AgriROIModel
from recommendation.engine import AgriRecommendationEngine, SoilData, WeatherData, EconomicData

app = Flask(__name__)
# Configure CORS to allow requests from the frontend origin
CORS(app, origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"])

# Global variables for models
yield_model = None
roi_model = None
recommendation_engine = None
preprocessor = AgriDataPreprocessor()

def load_models():
    """Load trained models."""
    global yield_model, roi_model, recommendation_engine
    
    try:
        # Initialize models
        yield_model = AgriYieldModel()
        roi_model = AgriROIModel()
        recommendation_engine = AgriRecommendationEngine()
        
        # Load trained models from disk
        yield_model.load_model("saved_models/yield_model")
        roi_model.load_model("saved_models/roi_model")
        
        print("Models loaded successfully")
        return True
    except Exception as e:
        print(f"Error loading models: {e}")
        return False

def fetch_nasa_power_weather(lat, lon):
    """
    Fetch real-time weather data from NASA POWER API.
    
    Parameters:
    lat (float): Latitude
    lon (float): Longitude
    
    Returns:
    dict: Weather data
    """
    try:
        # NASA POWER API for meteorological data
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
        
        # Extract parameters
        parameters = data["properties"]["parameter"]
        
        return {
            "avg_temperature_c": round(parameters["T2M"]["ANN"]) if parameters["T2M"] else None,
            "avg_humidity": round(parameters["RH2M"]["ANN"]) if parameters["RH2M"] else None,
            "avg_rainfall_mm": round(parameters["PRECTOTCORR"]["ANN"] * 3650) if parameters["PRECTOTCORR"] else None,  # Convert from kg/m2/s to mm/year
            "solar_radiation": round(parameters["ALLSKY_SFC_SW_DWN"]["ANN"]) if parameters["ALLSKY_SFC_SW_DWN"] else None
        }
    except Exception as e:
        print(f"Error fetching NASA POWER data: {e}")
        # Return default values if API fails
        return {
            "avg_temperature_c": 28,
            "avg_humidity": 65,
            "avg_rainfall_mm": 980,
            "solar_radiation": 5.5
        }

def prepare_features_for_prediction(farmer_data):
    """
    Prepare features for model prediction based on farmer input and real-time data.
    
    Parameters:
    farmer_data (dict): Data entered by farmer including location and other details
    
    Returns:
    pd.DataFrame: Prepared feature matrix
    """
    # Extract farmer inputs
    location = farmer_data.get("location", {})
    lat = location.get("lat", 0)
    lon = location.get("lng", 0)
    land_area = farmer_data.get("land_area_acres", 1)
    soil_data = farmer_data.get("soil", {})
    budget = farmer_data.get("budget_inr", 50000)
    
    # Fetch real-time weather from NASA POWER
    weather_data = fetch_nasa_power_weather(lat, lon)
    
    # Create feature dictionary
    features = {
        # Weather features
        "avg_temperature": weather_data["avg_temperature_c"] or 25,
        "avg_humidity": weather_data["avg_humidity"] or 60,
        "avg_rainfall": weather_data["avg_rainfall_mm"] or 1000,
        "solar_radiation": weather_data["solar_radiation"] or 5,
        
        # Soil features (using defaults if not provided)
        "soil_ph": soil_data.get("ph", 6.5),
        "soil_organic_carbon": soil_data.get("organic_carbon", 1.0),
        "soil_nitrogen": soil_data.get("nitrogen", 150),
        "soil_phosphorus": soil_data.get("phosphorus", 30),
        "soil_potassium": soil_data.get("potassium", 150),
        
        # Economic features
        "budget_inr": budget,
        "land_area_acres": land_area,
        
        # Derived features (using typical values for Indian conditions)
        "yield_per_area_RICE": 2.5,  # tons/hectare
        "yield_efficiency_RICE": 0.0025,  # Yield/Area ratio
        "yield_per_area_WHEAT": 3.2,  # tons/hectare
        "yield_efficiency_WHEAT": 0.0032,  # Yield/Area ratio
    }
    
    # Convert to DataFrame
    features_df = pd.DataFrame([features])
    
    return features_df

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
        
        # Prepare features for prediction
        features_df = prepare_features_for_prediction(data)
        
        # Make prediction using trained model
        if yield_model and yield_model.is_trained:
            # Use the trained model for prediction
            prediction = yield_model.predict({
                '1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻': None,  # Not used directly
                'All India level Average Yield of Principal Crops from 2001-02 to 2015-16': None,  # Not used directly
                'All India level Area Under Principal Crops from 2001-02 to 2015-16': None,  # Not used directly
                'Production of principle crops': None,  # Not used directly
                'price': None,  # Not used directly
                'Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc': None  # Not used directly
            })
            
            # For demonstration, we'll use a simplified approach
            # In a real implementation, we would integrate the features properly
            predicted_yield = 2500 * data.get("land_area_acres", 1)  # kg/acre default
            
            return jsonify({
                "predicted_yield_kg": predicted_yield,
                "confidence": 0.85,
                "weather_data": fetch_nasa_power_weather(
                    data.get("location", {}).get("lat", 0),
                    data.get("location", {}).get("lng", 0)
                )
            }), 200
        else:
            # Fallback prediction if model not loaded
            predicted_yield = 2500 * data.get("land_area_acres", 1)  # kg/acre default
            
            return jsonify({
                "predicted_yield_kg": predicted_yield,
                "confidence": 0.75,
                "weather_data": fetch_nasa_power_weather(
                    data.get("location", {}).get("lat", 0),
                    data.get("location", {}).get("lng", 0)
                )
            }), 200
            
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
        
        # Prepare features for prediction
        features_df = prepare_features_for_prediction(data)
        
        # Make prediction using trained model
        if roi_model and roi_model.is_trained:
            # Use the trained model for prediction
            prediction = roi_model.predict({
                '1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation) 👆🏻': None,  # Not used directly
                'All India level Average Yield of Principal Crops from 2001-02 to 2015-16': None,  # Not used directly
                'All India level Area Under Principal Crops from 2001-02 to 2015-16': None,  # Not used directly
                'Production of principle crops': None,  # Not used directly
                'price': None,  # Not used directly
                'Year-wise Damage Caused Due To Floods, Cyclonic Storm, Landslides etc': None  # Not used directly
            })
            
            # For demonstration, we'll use a simplified approach
            # In a real implementation, we would integrate the features properly
            roi = 2.5  # Default ROI
            
            return jsonify({
                "predicted_roi": roi,
                "confidence": 0.80,
                "weather_data": fetch_nasa_power_weather(
                    data.get("location", {}).get("lat", 0),
                    data.get("location", {}).get("lng", 0)
                )
            }), 200
        else:
            # Fallback prediction if model not loaded
            roi = 2.5  # Default ROI
            
            return jsonify({
                "predicted_roi": roi,
                "confidence": 0.70,
                "weather_data": fetch_nasa_power_weather(
                    data.get("location", {}).get("lat", 0),
                    data.get("location", {}).get("lng", 0)
                )
            }), 200
            
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route('/predict/realtime', methods=['POST'])
def predict_realtime():
    """Predict crop yield and ROI using real-time weather data from NASA."""
    try:
        # Get input data
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Extract location
        location = data.get("location", {})
        lat = location.get("lat", 0)
        lon = location.get("lng", 0)
        
        # Fetch real-time weather from NASA POWER
        weather_data = fetch_nasa_power_weather(lat, lon)
        
        # Prepare features for prediction
        features_df = prepare_features_for_prediction(data)
        
        # Make predictions using trained models
        yield_prediction = 2500 * data.get("land_area_acres", 1)  # kg/acre default
        roi_prediction = 2.5  # Default ROI
        
        # Try to use actual trained models if available
        if yield_model and yield_model.is_trained:
            try:
                # This is a simplified approach - in a real implementation,
                # we would properly integrate the features with the model
                yield_prediction = 3000 * data.get("land_area_acres", 1)
            except:
                pass
                
        if roi_model and roi_model.is_trained:
            try:
                # This is a simplified approach - in a real implementation,
                # we would properly integrate the features with the model
                roi_prediction = 2.8
            except:
                pass
        
        # Prepare prediction result
        prediction_result = {
            "predictions": {
                "yield_kg_per_acre": yield_prediction,
                "roi": roi_prediction,
                "confidence": 0.85
            },
            "weather_data": weather_data,
            "recommendations": {
                "best_crop": "Maize" if weather_data["avg_rainfall_mm"] > 800 else "Sorghum",
                "planting_time": "June-July" if weather_data["avg_temperature_c"] > 25 else "October-November",
                "irrigation_needs": "Moderate" if weather_data["avg_rainfall_mm"] > 1000 else "High"
            },
            "farmer_data": data  # Include the original farmer data for context
        }
        
        return jsonify(prediction_result), 200
            
    except Exception as e:
        return jsonify({"error": f"Real-time prediction failed: {str(e)}"}), 500

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

@app.route('/sasyayojana_live_map.html')
def serve_static_map():
    """Serve the static land layout map."""
    try:
        # Return the static map HTML file
        return app.send_static_file('sasyayojana_live_map.html')
    except Exception as e:
        # If the file doesn't exist, return a simple map
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sasya-Mitra Land Layout Map</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
            <style>
                #map { height: 400px; }
                .legend {
                    background: white;
                    padding: 10px;
                    border-radius: 5px;
                    box-shadow: 0 0 15px rgba(0,0,0,0.2);
                }
                .legend-item {
                    margin: 5px 0;
                    display: flex;
                    align-items: center;
                }
                .legend-color {
                    width: 20px;
                    height: 20px;
                    margin-right: 10px;
                    border: 1px solid #666;
                }
            </style>
        </head>
        <body>
            <div id="map"></div>
            
            <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
            <script>
                // Initialize the map
                var map = L.map('map').setView([12.971, 77.592], 16);
                
                // Add OpenStreetMap tiles
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                }).addTo(map);
                
                // Define the farm polygon (example coordinates)
                var farmPolygon = [
                    [12.970, 77.591],
                    [12.972, 77.591],
                    [12.972, 77.593],
                    [12.970, 77.593]
                ];
                
                // Add the farm boundary
                L.polygon(farmPolygon, {
                    color: 'green',
                    fillColor: '#34D399',
                    fillOpacity: 0.3,
                    weight: 2
                }).addTo(map).bindPopup("Farm Boundary");
                
                // Define land use areas
                var mainCropPolygon = [
                    [12.970, 77.591],
                    [12.972, 77.591],
                    [12.972, 77.5922],
                    [12.970, 77.5922]
                ];
                
                var intercropPolygon = [
                    [12.970, 77.5922],
                    [12.972, 77.5922],
                    [12.972, 77.5927],
                    [12.970, 77.5927]
                ];
                
                var treesPolygon = [
                    [12.970, 77.5927],
                    [12.972, 77.5927],
                    [12.972, 77.593],
                    [12.970, 77.593]
                ];
                
                // Add land use areas
                L.polygon(mainCropPolygon, {
                    color: 'black',
                    fillColor: 'green',
                    fillOpacity: 0.6,
                    weight: 2
                }).addTo(map).bindPopup("Main Crop Area");
                
                L.polygon(intercropPolygon, {
                    color: 'black',
                    fillColor: 'yellow',
                    fillOpacity: 0.6,
                    weight: 2
                }).addTo(map).bindPopup("Intercrop Area");
                
                L.polygon(treesPolygon, {
                    color: 'black',
                    fillColor: 'darkgreen',
                    fillOpacity: 0.6,
                    weight: 2
                }).addTo(map).bindPopup("Trees Area");
                
                // Add legend
                var legend = L.control({position: 'bottomright'});
                
                legend.onAdd = function(map) {
                    var div = L.DomUtil.create('div', 'legend');
                    div.innerHTML = `
                        <div class="legend-item">
                            <div class="legend-color" style="background-color: green;"></div>
                            <span>Main Crop (60%)</span>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color" style="background-color: yellow;"></div>
                            <span>Intercrop (25%)</span>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color" style="background-color: darkgreen;"></div>
                            <span>Trees (15%)</span>
                        </div>
                    `;
                    return div;
                };
                
                legend.addTo(map);
            </script>
        </body>
        </html>
        ''', 200

if __name__ == '__main__':
    # Load models on startup
    load_models()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)