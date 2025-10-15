"""
Test script to demonstrate the real-time prediction workflow.
"""

import requests
import json

def test_realtime_prediction():
    """
    Test the real-time prediction API endpoint.
    """
    # Farmer input data
    farmer_data = {
        "location": {
            "lat": 18.5204,  # Pune, India
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
    
    # API endpoint
    url = "http://localhost:5000/predict/realtime"
    
    try:
        # Make API request
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(farmer_data)
        )
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            print("✅ Real-time prediction successful!")
            print("\nPredictions:")
            print(f"  Yield: {result['predictions']['yield_kg_per_acre']} kg/acre")
            print(f"  ROI: {result['predictions']['roi']}x")
            print(f"  Confidence: {result['predictions']['confidence']}")
            
            print("\nWeather Data:")
            weather = result['weather_data']
            print(f"  Temperature: {weather['avg_temperature_c']}°C")
            print(f"  Humidity: {weather['avg_humidity']}%")
            print(f"  Rainfall: {weather['avg_rainfall_mm']} mm/year")
            print(f"  Solar Radiation: {weather['solar_radiation']} kWh/m²/day")
            
            print("\nRecommendations:")
            rec = result['recommendations']
            print(f"  Best Crop: {rec['best_crop']}")
            print(f"  Planting Time: {rec['planting_time']}")
            print(f"  Irrigation Needs: {rec['irrigation_needs']}")
            
        else:
            print(f"❌ API request failed with status code: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running.")
        print("Start the server with: python models/api/app.py")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")

def test_health_check():
    """
    Test the health check endpoint.
    """
    url = "http://localhost:5000/health"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            print("✅ Health check successful!")
            print(f"Service: {result['service']}")
            print(f"Status: {result['status']}")
        else:
            print(f"❌ Health check failed with status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running.")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")

if __name__ == "__main__":
    print("SASYA-MITRA REAL-TIME PREDICTION TEST")
    print("=" * 50)
    
    # Test health check first
    print("\n1. Testing Health Check Endpoint:")
    test_health_check()
    
    # Test real-time prediction
    print("\n2. Testing Real-Time Prediction Endpoint:")
    test_realtime_prediction()
    
    print("\n" + "=" * 50)
    print("TEST COMPLETE")