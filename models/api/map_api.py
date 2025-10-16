"""
API endpoints for land layout map visualization in Sasya-Mitra.
"""

import sys
import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from map_visualization.land_layout_mapper import LandLayoutMapper
from recommendation.engine import SoilData, WeatherData, EconomicData

app = Flask(__name__)
CORS(app)

# Initialize the land layout mapper
mapper = LandLayoutMapper()

@app.route('/api/generate-land-layout-map', methods=['POST'])
def generate_land_layout_map():
    """
    Generate a land layout map based on AI recommendations.
    
    Expected JSON payload:
    {
        "center_lat": 12.971,
        "center_lon": 77.592,
        "land_area_acres": 5.0,
        "location": "Bangalore, India",
        "soil_data": {
            "ph": 6.7,
            "organic_carbon": 1.2,
            "nitrogen": 150,
            "phosphorus": 40,
            "potassium": 200,
            "texture": "Loam",
            "drainage": "Moderate"
        },
        "weather_data": {
            "rainfall_mm": 850,
            "temperature_c": 28,
            "humidity": 65,
            "solar_radiation": 5.5
        },
        "economic_data": {
            "budget_inr": 60000,
            "labor_availability": "Medium",
            "input_cost_type": "Organic"
        }
    }
    
    Returns:
    JSON response with map file path and recommendation details
    """
    try:
        # Parse request data
        data = request.get_json()
        
        # Extract required parameters
        center_lat = data.get('center_lat', 12.971)
        center_lon = data.get('center_lon', 77.592)
        land_area_acres = data.get('land_area_acres', 5.0)
        location = data.get('location', 'Unknown')
        
        # Extract soil data
        soil_data_dict = data.get('soil_data', {})
        soil_data = SoilData(
            ph=soil_data_dict.get('ph', 6.7),
            organic_carbon=soil_data_dict.get('organic_carbon', 1.2),
            nitrogen=soil_data_dict.get('nitrogen', 150),
            phosphorus=soil_data_dict.get('phosphorus', 40),
            potassium=soil_data_dict.get('potassium', 200),
            texture=soil_data_dict.get('texture', 'Loam'),
            drainage=soil_data_dict.get('drainage', 'Moderate')
        )
        
        # Extract weather data
        weather_data_dict = data.get('weather_data', {})
        weather_data = WeatherData(
            rainfall_mm=weather_data_dict.get('rainfall_mm', 850),
            temperature_c=weather_data_dict.get('temperature_c', 28),
            humidity=weather_data_dict.get('humidity', 65),
            solar_radiation=weather_data_dict.get('solar_radiation', 5.5)
        )
        
        # Extract economic data
        economic_data_dict = data.get('economic_data', {})
        economic_data = EconomicData(
            budget_inr=economic_data_dict.get('budget_inr', 60000),
            labor_availability=economic_data_dict.get('labor_availability', 'Medium'),
            input_cost_type=economic_data_dict.get('input_cost_type', 'Organic')
        )
        
        # Generate recommendation and map
        map_filepath, recommendation = mapper.get_real_time_recommendation_and_map(
            soil_data, weather_data, economic_data, land_area_acres, center_lat, center_lon, location
        )
        
        # Return success response
        return jsonify({
            'success': True,
            'map_file_path': map_filepath,
            'recommendation': recommendation,
            'message': 'Land layout map generated successfully'
        }), 200
        
    except Exception as e:
        # Return error response
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate land layout map'
        }), 500

@app.route('/api/get-map/<path:filename>', methods=['GET'])
def get_map(filename):
    """
    Serve generated map files.
    
    Parameters:
    filename (str): Name of the map file to serve
    
    Returns:
    HTML file of the map
    """
    try:
        # Construct full file path
        file_path = os.path.join(mapper.output_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'message': 'Map file not found'
            }), 404
        
        # Serve the file
        return send_file(file_path)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to serve map file'
        }), 500

@app.route('/api/latest-map', methods=['GET'])
def get_latest_map():
    """
    Get the most recently generated map file.
    
    Returns:
    HTML file of the latest map
    """
    try:
        # List all HTML files in the output directory
        html_files = [f for f in os.listdir(mapper.output_dir) if f.endswith('.html')]
        
        # If no files exist, return error
        if not html_files:
            return jsonify({
                'success': False,
                'message': 'No map files available'
            }), 404
        
        # Sort files by modification time to get the latest
        html_files.sort(key=lambda x: os.path.getmtime(os.path.join(mapper.output_dir, x)), reverse=True)
        latest_file = html_files[0]
        
        # Construct full file path
        file_path = os.path.join(mapper.output_dir, latest_file)
        
        # Serve the file
        return send_file(file_path)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to serve latest map file'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)