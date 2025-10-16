"""
Land Layout Mapper for Sasya-Mitra agricultural advisory system.
Generates interactive maps showing crop layout recommendations from AI engine.
"""

import sys
import os
import folium
import geopandas as gpd
from shapely.geometry import Polygon, Point
import numpy as np
import json
from typing import Dict, List, Tuple

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recommendation.engine import AgriRecommendationEngine, SoilData, WeatherData, EconomicData

# Initialize Firebase availability flag
FIREBASE_AVAILABLE = False
db = None
bucket = None

# Try to import Firebase Admin SDK
try:
    import firebase_admin
    from firebase_admin import credentials, firestore, storage
    from datetime import datetime
    FIREBASE_AVAILABLE = True
except ImportError:
    print("Firebase Admin SDK not available. Map data will not be stored in Firebase.")

class LandLayoutMapper:
    """
    Generates interactive land layout maps based on AI recommendations.
    """
    
    def __init__(self):
        self.engine = AgriRecommendationEngine()
        self.output_dir = "models/map_visualization/generated_maps"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize Firebase if available
        global FIREBASE_AVAILABLE, db, bucket
        if FIREBASE_AVAILABLE:
            try:
                # Initialize Firebase Admin SDK if not already initialized
                if not firebase_admin._apps:
                    # Try to initialize with default credentials
                    try:
                        firebase_admin.initialize_app()
                    except Exception as e:
                        print(f"Could not initialize Firebase with default credentials: {e}")
                        FIREBASE_AVAILABLE = False
                
                if FIREBASE_AVAILABLE:
                    # Initialize Firestore and Storage
                    try:
                        db = firestore.client()
                        bucket = storage.bucket('sasyayojana-79840.firebasestorage.app')
                    except Exception as e:
                        print(f"Could not initialize Firestore/Storage: {e}")
                        FIREBASE_AVAILABLE = False
            except Exception as e:
                print(f"Error initializing Firebase: {e}")
                FIREBASE_AVAILABLE = False
    
    def generate_land_polygon(self, center_lat: float, center_lon: float, area_acres: float) -> Polygon:
        """
        Generate a polygon representing the farm land based on center coordinates and area.
        
        Parameters:
        center_lat (float): Latitude of farm center
        center_lon (float): Longitude of farm center
        area_acres (float): Area of farm in acres
        
        Returns:
        Polygon: Shapely polygon representing the farm boundary
        """
        # Convert acres to approximate square meters
        area_sq_m = area_acres * 4046.86
        
        # Assuming a roughly square/rectangular plot for visualization
        # Calculate side length (approximate)
        side_length = np.sqrt(area_sq_m)
        
        # Convert to approximate degrees (rough approximation)
        lat_offset = side_length / 111320  # meters per degree latitude
        lon_offset = side_length / (111320 * np.cos(np.radians(center_lat)))  # meters per degree longitude
        
        # Create polygon coordinates
        coords = [
            (center_lon - lon_offset/2, center_lat - lat_offset/2),
            (center_lon + lon_offset/2, center_lat - lat_offset/2),
            (center_lon + lon_offset/2, center_lat + lat_offset/2),
            (center_lon - lon_offset/2, center_lat + lat_offset/2),
            (center_lon - lon_offset/2, center_lat - lat_offset/2)  # Close the polygon
        ]
        
        return Polygon(coords)
    
    def calculate_layout_ratios(self, recommendation) -> Dict[str, float]:
        """
        Calculate the area ratios for main crops, intercrops, and trees based on recommendation.
        
        Parameters:
        recommendation: Recommendation object from AI engine
        
        Returns:
        Dict[str, float]: Dictionary with area ratios
        """
        # These ratios would typically come from the AI recommendation
        # For now, we'll use sample values that can be overridden by the recommendation
        ratios = {
            'main_crop_ratio': 0.6,  # 60% for main crop
            'intercrop_ratio': 0.25,  # 25% for intercrops
            'tree_ratio': 0.15   # 15% for trees
        }
        
        # Override with recommendation values if available
        # This would depend on how your recommendation engine structures its output
        # For example, if the recommendation includes specific layout ratios:
        # if hasattr(recommendation, 'layout_ratios'):
        #     ratios.update(recommendation.layout_ratios)
            
        return ratios
    
    def create_land_use_polygons(self, land_poly: Polygon, ratios: Dict[str, float]) -> gpd.GeoDataFrame:
        """
        Create sub-polygons for different land use types based on ratios.
        
        Parameters:
        land_poly (Polygon): The main land polygon
        ratios (Dict[str, float]): Area ratios for different land use types
        
        Returns:
        gpd.GeoDataFrame: GeoDataFrame with land use polygons
        """
        # Get bounds of the land polygon
        minx, miny, maxx, maxy = land_poly.bounds
        width = maxx - minx
        height = maxy - miny
        
        # Calculate vertical divisions based on ratios
        main_crop_limit = miny + height * ratios['main_crop_ratio']
        intercrop_limit = main_crop_limit + height * ratios['intercrop_ratio']
        
        # Create sub-polygons
        main_crop_poly = Polygon([
            (minx, miny), 
            (maxx, miny), 
            (maxx, main_crop_limit), 
            (minx, main_crop_limit),
            (minx, miny)
        ])
        
        intercrop_poly = Polygon([
            (minx, main_crop_limit), 
            (maxx, main_crop_limit), 
            (maxx, intercrop_limit), 
            (minx, intercrop_limit),
            (minx, main_crop_limit)
        ])
        
        tree_poly = Polygon([
            (minx, intercrop_limit), 
            (maxx, intercrop_limit), 
            (maxx, maxy), 
            (minx, maxy),
            (minx, intercrop_limit)
        ])
        
        # Create GeoDataFrame
        land_use = gpd.GeoDataFrame({
            'geometry': [main_crop_poly, intercrop_poly, tree_poly],
            'land_use_type': ['Main Crop', 'Intercrop', 'Trees'],
            'color': ['green', 'yellow', 'darkgreen']
        })
        
        return land_use
    
    def generate_interactive_map(self, land_use_gdf: gpd.GeoDataFrame, center_lat: float, 
                                center_lon: float, recommendation) -> folium.Map:
        """
        Generate an interactive Folium map with land use polygons and satellite imagery.
        
        Parameters:
        land_use_gdf (gpd.GeoDataFrame): GeoDataFrame with land use polygons
        center_lat (float): Latitude of farm center
        center_lon (float): Longitude of farm center
        recommendation: Recommendation object from AI engine
        
        Returns:
        folium.Map: Interactive map object
        """
        # Create the map with satellite imagery
        m = folium.Map(
            location=[center_lat, center_lon], 
            zoom_start=16,
            tiles=None  # We'll add our own tile layers
        )
        
        # Add satellite imagery layer
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            name='Satellite',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Add OpenStreetMap as an alternative
        folium.TileLayer(
            tiles='OpenStreetMap',
            name='Street Map',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Add land use polygons to the map
        for _, row in land_use_gdf.iterrows():
            # Determine color based on land use type
            color_map = {
                'Main Crop': 'green',
                'Intercrop': 'yellow',
                'Trees': 'darkgreen'
            }
            color = color_map.get(row['land_use_type'], 'blue')
            
            # Add polygon to map
            folium.GeoJson(
                row['geometry'].__geo_interface__,
                name=row['land_use_type'],
                style_function=lambda feature, color=color: {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 2,
                    'fillOpacity': 0.6
                },
                tooltip=f"{row['land_use_type']}: {getattr(recommendation, row['land_use_type'].lower().replace(' ', '_'), 'N/A')}"
            ).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Add title
        title_html = '''
                     <h3 align="center" style="font-size:16px"><b>AI-Generated Land Use Layout</b></h3>
                     '''
        m.get_root().html.add_child(folium.Element(title_html))
        
        # Add a legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 150px; height: 90px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        &nbsp; Land Use Legend <br>
        &nbsp; <i class="fa fa-square" style="color:green"></i> Main Crop (60%)<br>
        &nbsp; <i class="fa fa-square" style="color:yellow"></i> Intercrop (25%)<br>
        &nbsp; <i class="fa fa-square" style="color:darkgreen"></i> Trees (15%)
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        return m
    
    def save_map(self, map_obj: folium.Map, filename: str = "sasyayojana_live_map.html") -> str:
        """
        Save the map to an HTML file.
        
        Parameters:
        map_obj (folium.Map): The Folium map object
        filename (str): Name of the output file
        
        Returns:
        str: Path to the saved file
        """
        filepath = os.path.join(self.output_dir, filename)
        map_obj.save(filepath)
        return filepath
    
    def generate_layout_from_recommendation(self, recommendation, center_lat: float, 
                                          center_lon: float, area_acres: float) -> str:
        """
        Generate a complete land layout map from an AI recommendation.
        
        Parameters:
        recommendation: Recommendation object from AI engine
        center_lat (float): Latitude of farm center
        center_lon (float): Longitude of farm center
        area_acres (float): Area of farm in acres
        
        Returns:
        str: Path to the generated HTML map file
        """
        # Generate land polygon
        land_poly = self.generate_land_polygon(center_lat, center_lon, area_acres)
        
        # Calculate layout ratios
        ratios = self.calculate_layout_ratios(recommendation)
        
        # Create land use polygons
        land_use_gdf = self.create_land_use_polygons(land_poly, ratios)
        
        # Generate interactive map
        map_obj = self.generate_interactive_map(land_use_gdf, center_lat, center_lon, recommendation)
        
        # Save map
        filepath = self.save_map(map_obj, f"sasyayojana_live_map_{int(center_lat*1000)}_{int(center_lon*1000)}.html")
        
        return filepath
    
    def get_real_time_recommendation_and_map(self, soil_data: SoilData, weather_data: WeatherData, 
                                           economic_data: EconomicData, land_area_acres: float,
                                           center_lat: float, center_lon: float, location: str) -> Tuple[str, Dict]:
        """
        Get real-time recommendation from AI engine and generate corresponding map.
        
        Parameters:
        soil_data (SoilData): Soil data
        weather_data (WeatherData): Weather data
        economic_data (EconomicData): Economic data
        land_area_acres (float): Land area in acres
        center_lat (float): Latitude of farm center
        center_lon (float): Longitude of farm center
        location (str): Location name
        
        Returns:
        Tuple[str, Dict]: (map_file_path, recommendation_dict)
        """
        # Generate recommendation from AI engine
        recommendation = self.engine.generate_recommendation(
            soil_data, weather_data, economic_data, land_area_acres, location
        )
        
        # Convert recommendation to dictionary for JSON serialization
        recommendation_dict = {
            'main_crop': recommendation.main_crop,
            'intercrop': recommendation.intercrop,
            'trees': recommendation.trees,
            'layout': recommendation.layout,
            'expected_yield_kg': recommendation.expected_yield_kg,
            'profit_estimate_inr': recommendation.profit_estimate_inr,
            'roi': recommendation.roi,
            'sustainability_tips': recommendation.sustainability_tips
        }
        
        # Generate map
        map_filepath = self.generate_layout_from_recommendation(
            recommendation, center_lat, center_lon, land_area_acres
        )
        
        # Store map data in Firebase if available
        global FIREBASE_AVAILABLE, db, bucket
        if FIREBASE_AVAILABLE and db is not None and bucket is not None:
            try:
                # Read the HTML content
                with open(map_filepath, 'r', encoding='utf-8') as f:
                    map_html = f.read()
                
                # Prepare map data for storage
                map_data = {
                    'center_lat': center_lat,
                    'center_lon': center_lon,
                    'land_area_acres': land_area_acres,
                    'location': location,
                    'recommendation': recommendation_dict,
                    'created_at': datetime.now().isoformat()
                }
                
                # Get filename from filepath
                filename = os.path.basename(map_filepath)
                
                # Upload HTML file to Firebase Storage
                blob = bucket.blob(f'land-layout-maps/{filename}')
                blob.upload_from_string(map_html, content_type='text/html')
                blob.make_public()
                
                # Store metadata in Firestore
                doc_ref = db.collection('land_layout_maps').document()
                doc_ref.set({
                    **map_data,
                    'filename': filename,
                    'map_url': blob.public_url,
                    'created_at': firestore.SERVER_TIMESTAMP
                })
                
                print(f"Map data stored in Firebase with ID: {doc_ref.id}")
            except Exception as e:
                print(f"Error storing map data in Firebase: {e}")
        
        return map_filepath, recommendation_dict