"""
Test script for the map API in Sasya-Mitra.
"""

import requests
import json

def test_map_api():
    """Test the land layout map generation API."""
    url = "http://localhost:5001/api/generate-land-layout-map"
    
    # Test data
    data = {
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
    
    try:
        # Send POST request
        response = requests.post(url, json=data)
        
        # Print response
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing map API: {e}")
        return False

if __name__ == "__main__":
    print("Testing map API...")
    success = test_map_api()
    if success:
        print("\n🎉 Map API test completed successfully!")
    else:
        print("\n💥 Map API test failed!")