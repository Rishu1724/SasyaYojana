"""
API endpoints for land layout map visualization in Sasya-Mitra.
"""

import sys
import os
import json
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from map_visualization.land_layout_mapper import LandLayoutMapper
from recommendation.engine import SoilData, WeatherData, EconomicData

# Initialize Firebase availability flag
FIREBASE_AVAILABLE = False
db = None
bucket = None
maps_collection = None

# Try to import Firebase Admin SDK
try:
    import firebase_admin
    from firebase_admin import credentials, firestore, storage
    from datetime import datetime
    FIREBASE_AVAILABLE = True
except ImportError:
    print("Firebase Admin SDK not available.")

app = Flask(__name__)
CORS(app)

# Initialize the land layout mapper
mapper = LandLayoutMapper()

# Initialize Firebase if available
if FIREBASE_AVAILABLE:
    try:
        # Initialize Firebase Admin SDK if not already initialized
        if not firebase_admin._apps:
            # Try to initialize with default credentials (for development)
            try:
                firebase_admin.initialize_app()
            except Exception as e:
                print(f"Could not initialize Firebase with default credentials: {e}")
                # Try to initialize with environment variable (for production)
                try:
                    cred = credentials.ApplicationDefault()
                    firebase_admin.initialize_app(cred, {
                        'projectId': 'sasyayojana-79840',
                    })
                except Exception as e2:
                    print(f"Could not initialize Firebase with Application Default: {e2}")
                    # Try to initialize with service account key (if available)
                    try:
                        # This would be the path to your service account key file
                        # For development, you might need to set the GOOGLE_APPLICATION_CREDENTIALS environment variable
                        cred = credentials.ApplicationDefault()
                        firebase_admin.initialize_app(cred)
                    except Exception as e3:
                        print(f"Could not initialize Firebase: {e3}")
                        FIREBASE_AVAILABLE = False
        
        if FIREBASE_AVAILABLE:
            # Initialize Firestore and Storage
            try:
                db = firestore.client()
                bucket = storage.bucket('sasyayojana-79840.firebasestorage.app')
                maps_collection = db.collection('land_layout_maps')
            except Exception as e:
                print(f"Could not initialize Firestore/Storage: {e}")
                FIREBASE_AVAILABLE = False
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        FIREBASE_AVAILABLE = False

def store_map_in_firebase(map_data, map_html, filename):
    """
    Store map data and HTML file in Firebase.
    
    Parameters:
    map_data (dict): Map metadata
    map_html (str): HTML content of the map
    filename (str): Name of the map file
    
    Returns:
    dict: Storage result with IDs and URLs
    """
    global FIREBASE_AVAILABLE, db, bucket
    if not FIREBASE_AVAILABLE or db is None or bucket is None:
        # Firebase not available, return mock result
        return {
            'success': True,
            'message': 'Firebase not available, map stored locally',
            'map_id': 'local_' + filename.replace('.html', ''),
            'map_url': f'/api/get-map/{filename}'
        }
    
    try:
        # Store map metadata in Firestore
        map_doc_ref = maps_collection.document()
        map_data_with_timestamp = {
            **map_data,
            'created_at': firestore.SERVER_TIMESTAMP,
            'filename': filename
        }
        map_doc_ref.set(map_data_with_timestamp)
        map_id = map_doc_ref.id
        
        # Upload HTML file to Firebase Storage
        blob = bucket.blob(f'land-layout-maps/{filename}')
        blob.upload_from_string(map_html, content_type='text/html')
        
        # Make the file publicly readable
        blob.make_public()
        map_url = blob.public_url
        
        return {
            'success': True,
            'message': 'Map successfully stored in Firebase',
            'map_id': map_id,
            'map_url': map_url
        }
    except Exception as e:
        print(f"Error storing map in Firebase: {e}")
        # Return fallback result
        return {
            'success': False,
            'message': f'Failed to store map in Firebase: {str(e)}',
            'map_id': None,
            'map_url': None
        }

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
        
        # Get the filename from the filepath
        filename = os.path.basename(map_filepath)
        
        # Read the HTML content
        with open(map_filepath, 'r', encoding='utf-8') as f:
            map_html = f.read()
        
        # Prepare map data for storage
        map_data = {
            'center_lat': center_lat,
            'center_lon': center_lon,
            'land_area_acres': land_area_acres,
            'location': location,
            'soil_data': soil_data_dict,
            'weather_data': weather_data_dict,
            'economic_data': economic_data_dict,
            'recommendation': recommendation,
            'created_at': datetime.now().isoformat() if FIREBASE_AVAILABLE else None
        }
        
        # Store map in Firebase
        storage_result = store_map_in_firebase(map_data, map_html, filename)
        
        # Return success response
        return jsonify({
            'success': True,
            'map_file_path': map_filepath,
            'map_url': storage_result.get('map_url', f'/api/get-map/{filename}'),
            'map_id': storage_result.get('map_id', 'local'),
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