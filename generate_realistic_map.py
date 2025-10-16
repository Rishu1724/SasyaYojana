"""
Script to generate a realistic map with satellite imagery for testing
"""

import sys
import os

# Add the models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from map_visualization.land_layout_mapper import LandLayoutMapper
from recommendation.engine import SoilData, WeatherData, EconomicData

def generate_realistic_map():
    """Generate a realistic map with satellite imagery."""
    print("Generating realistic map with satellite imagery...")
    
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
        
        print(f"✅ Realistic map generated successfully: {map_filepath}")
        print(f"Recommendation: {recommendation}")
        
        # Also save a copy to the public directory for easy access
        public_dir = "public"
        if os.path.exists(public_dir):
            import shutil
            shutil.copy(map_filepath, os.path.join(public_dir, "realistic_land_layout_map.html"))
            print(f"✅ Map copied to public directory for web access")
        
        return True
    except Exception as e:
        print(f"❌ Error generating realistic map: {e}")
        return False

if __name__ == "__main__":
    success = generate_realistic_map()
    if success:
        print("\n🎉 Realistic map generation completed successfully!")
        print("You can view the map by opening the generated HTML file in your browser")
    else:
        print("\n💥 Realistic map generation failed!")