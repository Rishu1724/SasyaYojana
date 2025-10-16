"""
Test script for map visualization in Sasya-Mitra.
"""

import sys
import os

# Add the models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from map_visualization.land_layout_mapper import LandLayoutMapper
from recommendation.engine import SoilData, WeatherData, EconomicData

def test_map_generation():
    """Test the land layout map generation."""
    print("Testing land layout map generation...")
    
    # Initialize the mapper
    mapper = LandLayoutMapper()
    
    # Example data (replace with real sensor/API data)
    soil_data = SoilData(
        ph=6.7,
        organic_carbon=1.2,
        nitrogen=150,
        phosphorus=40,
        potassium=200,
        texture='Loam',
        drainage='Moderate'
    )
    
    weather_data = WeatherData(
        rainfall_mm=850,
        temperature_c=28,
        humidity=65,
        solar_radiation=5.5
    )
    
    economic_data = EconomicData(
        budget_inr=60000,
        labor_availability='Medium',
        input_cost_type='Organic'
    )
    
    # Generate recommendation and map
    try:
        map_filepath, recommendation = mapper.get_real_time_recommendation_and_map(
            soil_data, weather_data, economic_data, 5.0, 12.971, 77.592, "Bangalore, India"
        )
        
        print(f"✅ Map generated successfully: {map_filepath}")
        print(f"Recommendation: {recommendation}")
        return True
    except Exception as e:
        print(f"❌ Error generating map: {e}")
        return False

if __name__ == "__main__":
    success = test_map_generation()
    if success:
        print("\n🎉 Map visualization test completed successfully!")
    else:
        print("\n💥 Map visualization test failed!")