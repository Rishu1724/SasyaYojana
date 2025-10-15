"""
Recommendation engine for Sasya-Mitra agricultural advisory system.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum

@dataclass
class SoilData:
    """Soil data structure."""
    ph: float
    organic_carbon: float
    nitrogen: float
    phosphorus: float
    potassium: float
    texture: str
    drainage: str

@dataclass
class WeatherData:
    """Weather data structure."""
    rainfall_mm: float
    temperature_c: float
    humidity: float
    solar_radiation: float

@dataclass
class EconomicData:
    """Economic data structure."""
    budget_inr: float
    labor_availability: str
    input_cost_type: str

@dataclass
class Recommendation:
    """Recommendation structure."""
    main_crop: str
    intercrop: str
    trees: List[str]
    layout: str
    expected_yield_kg: float
    profit_estimate_inr: float
    roi: float
    sustainability_tips: List[str]

class CropType(Enum):
    """Crop type enumeration."""
    CEREAL = "cereal"
    PULSE = "pulse"
    OILSEED = "oilseed"
    FIBER = "fiber"
    FRUIT = "fruit"
    VEGETABLE = "vegetable"
    SPICE = "spice"

class AgriRecommendationEngine:
    """
    Agricultural recommendation engine that combines ML models with expert rules.
    """
    
    def __init__(self):
        # Crop suitability rules (simplified)
        self.crop_suitability = {
            'Maize': {
                'ph_min': 5.5, 'ph_max': 7.5,
                'temp_min': 15, 'temp_max': 35,
                'rainfall_min': 500, 'rainfall_max': 1500,
                'soil_types': ['Loam', 'Sandy Loam'],
                'crop_type': CropType.CEREAL
            },
            'Cowpea': {
                'ph_min': 5.5, 'ph_max': 7.0,
                'temp_min': 20, 'temp_max': 35,
                'rainfall_min': 400, 'rainfall_max': 1200,
                'soil_types': ['Loam', 'Sandy Loam', 'Clay Loam'],
                'crop_type': CropType.PULSE
            },
            'Mango': {
                'ph_min': 5.5, 'ph_max': 7.5,
                'temp_min': 20, 'temp_max': 40,
                'rainfall_min': 600, 'rainfall_max': 2500,
                'soil_types': ['Loam', 'Sandy Loam', 'Clay Loam'],
                'crop_type': CropType.FRUIT
            },
            'Gliricidia': {
                'ph_min': 5.0, 'ph_max': 8.0,
                'temp_min': 15, 'temp_max': 35,
                'rainfall_min': 500, 'rainfall_max': 2500,
                'soil_types': ['Loam', 'Sandy Loam', 'Clay Loam', 'Sandy'],
                'crop_type': CropType.FIBER
            },
            'Turmeric': {
                'ph_min': 4.5, 'ph_max': 7.5,
                'temp_min': 20, 'temp_max': 35,
                'rainfall_min': 1000, 'rainfall_max': 2500,
                'soil_types': ['Loam', 'Clay Loam'],
                'crop_type': CropType.SPICE
            },
            'Sorghum': {
                'ph_min': 5.5, 'ph_max': 7.5,
                'temp_min': 15, 'temp_max': 35,
                'rainfall_min': 300, 'rainfall_max': 1000,
                'soil_types': ['Loam', 'Sandy Loam', 'Clay Loam', 'Sandy'],
                'crop_type': CropType.CEREAL
            }
        }
        
        # Tree suitability rules
        self.tree_suitability = {
            'Mango': {
                'spacing': '10x10m',
                'maturity_years': 4,
                'yield_per_tree_kg': 200
            },
            'Gliricidia': {
                'spacing': '2x2m',
                'maturity_years': 2,
                'yield_per_tree_kg': 15
            }
        }
        
        # Layout patterns
        self.layout_patterns = {
            'Alley Cropping': {
                'description': 'Alternate rows of trees and crops',
                'spacing': '5-10m between tree rows'
            },
            'Boundary Planting': {
                'description': 'Trees planted along field boundaries',
                'spacing': 'Along perimeter'
            },
            'Mixed System': {
                'description': 'Trees scattered throughout the field',
                'spacing': 'Variable based on species'
            }
        }
        
        # Sustainability tips
        self.sustainability_tips_base = [
            "Apply compost from residues and cow dung",
            "Use drip irrigation to optimize water",
            "Rotate crops every two seasons",
            "Plant nitrogen-fixing legumes to improve soil fertility",
            "Use organic mulch to retain moisture and suppress weeds",
            "Practice intercropping to maximize land use efficiency"
        ]
        
    def assess_soil_suitability(self, soil_data: SoilData, crop_name: str) -> float:
        """
        Assess soil suitability for a specific crop.
        
        Parameters:
        soil_data (SoilData): Soil data
        crop_name (str): Name of the crop
        
        Returns:
        float: Suitability score (0-1)
        """
        if crop_name not in self.crop_suitability:
            return 0.0
            
        crop_rules = self.crop_suitability[crop_name]
        
        # Check pH suitability
        ph_score = 1.0 if (crop_rules['ph_min'] <= soil_data.ph <= crop_rules['ph_max']) else 0.5
        
        # Check soil type suitability
        soil_type_score = 1.0 if soil_data.texture in crop_rules['soil_types'] else 0.7
        
        # Check organic carbon (higher is better, but with diminishing returns)
        oc_score = min(1.0, soil_data.organic_carbon / 2.0)  # Optimal at 2%
        
        # Combine scores (weighted average)
        suitability = (ph_score * 0.3 + soil_type_score * 0.3 + oc_score * 0.4)
        
        return suitability
    
    def assess_weather_suitability(self, weather_data: WeatherData, crop_name: str) -> float:
        """
        Assess weather suitability for a specific crop.
        
        Parameters:
        weather_data (WeatherData): Weather data
        crop_name (str): Name of the crop
        
        Returns:
        float: Suitability score (0-1)
        """
        if crop_name not in self.crop_suitability:
            return 0.0
            
        crop_rules = self.crop_suitability[crop_name]
        
        # Check temperature suitability
        temp_score = 1.0 if (crop_rules['temp_min'] <= weather_data.temperature_c <= crop_rules['temp_max']) else 0.5
        
        # Check rainfall suitability
        if weather_data.rainfall_mm < crop_rules['rainfall_min']:
            rainfall_score = weather_data.rainfall_mm / crop_rules['rainfall_min']
        elif weather_data.rainfall_mm > crop_rules['rainfall_max']:
            rainfall_score = crop_rules['rainfall_max'] / weather_data.rainfall_mm
        else:
            rainfall_score = 1.0
            
        # Combine scores
        suitability = (temp_score * 0.6 + rainfall_score * 0.4)
        
        return suitability
    
    def recommend_crops(self, soil_data: SoilData, weather_data: WeatherData) -> List[Tuple[str, float]]:
        """
        Recommend suitable crops based on soil and weather conditions.
        
        Parameters:
        soil_data (SoilData): Soil data
        weather_data (WeatherData): Weather data
        
        Returns:
        List[Tuple[str, float]]: List of (crop_name, suitability_score)
        """
        crop_scores = []
        
        for crop_name in self.crop_suitability:
            soil_suitability = self.assess_soil_suitability(soil_data, crop_name)
            weather_suitability = self.assess_weather_suitability(weather_data, crop_name)
            
            # Combined suitability score
            combined_score = (soil_suitability + weather_suitability) / 2
            
            crop_scores.append((crop_name, combined_score))
        
        # Sort by suitability score (descending)
        crop_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return top 5 crops with suitability > 0.5
        return [(crop, score) for crop, score in crop_scores if score > 0.5][:5]
    
    def recommend_trees(self, soil_data: SoilData, weather_data: WeatherData) -> List[Tuple[str, Dict]]:
        """
        Recommend suitable trees based on soil and weather conditions.
        
        Parameters:
        soil_data (SoilData): Soil data
        weather_data (WeatherData): Weather data
        
        Returns:
        List[Tuple[str, Dict]]: List of (tree_name, tree_info)
        """
        tree_recommendations = []
        
        for tree_name in self.tree_suitability:
            # For simplicity, we'll assume all trees in our database are suitable
            # In a real implementation, you would check soil and weather suitability
            tree_info = self.tree_suitability[tree_name]
            tree_recommendations.append((tree_name, tree_info))
        
        return tree_recommendations
    
    def determine_layout(self, soil_data: SoilData, weather_data: WeatherData) -> Tuple[str, str]:
        """
        Determine the optimal layout pattern.
        
        Parameters:
        soil_data (SoilData): Soil data
        weather_data (WeatherData): Weather data
        
        Returns:
        Tuple[str, str]: (layout_name, description)
        """
        # Simple rule-based approach
        if soil_data.texture == 'Sandy' and weather_data.rainfall_mm < 600:
            return ('Boundary Planting', self.layout_patterns['Boundary Planting']['description'])
        elif weather_data.rainfall_mm > 1200:
            return ('Mixed System', self.layout_patterns['Mixed System']['description'])
        else:
            return ('Alley Cropping', self.layout_patterns['Alley Cropping']['description'])
    
    def estimate_yield(self, main_crop: str, land_area_acres: float) -> float:
        """
        Estimate yield based on crop and land area.
        
        Parameters:
        main_crop (str): Main crop name
        land_area_acres (float): Land area in acres
        
        Returns:
        float: Estimated yield in kg
        """
        # Simplified yield estimation
        # In a real implementation, this would use your trained ML model
        base_yields = {
            'Maize': 4000,      # kg/acre
            'Sorghum': 3000,    # kg/acre
            'Cowpea': 1000,     # kg/acre
            'Turmeric': 2000    # kg/acre
        }
        
        base_yield = base_yields.get(main_crop, 2500)  # Default yield
        return base_yield * land_area_acres
    
    def estimate_profit(self, main_crop: str, intercrop: str, trees: List[str], 
                       land_area_acres: float, budget_inr: float) -> Tuple[float, float]:
        """
        Estimate profit and ROI.
        
        Parameters:
        main_crop (str): Main crop name
        intercrop (str): Intercrop name
        trees (List[str]): List of tree names
        land_area_acres (float): Land area in acres
        budget_inr (float): Budget in INR
        
        Returns:
        Tuple[float, float]: (profit_estimate, roi)
        """
        # Simplified pricing (INR per kg)
        crop_prices = {
            'Maize': 20,
            'Sorghum': 25,
            'Cowpea': 50,
            'Turmeric': 100,
            'Mango': 60
        }
        
        # Estimate yields
        main_crop_yield = self.estimate_yield(main_crop, land_area_acres)
        intercrop_yield = self.estimate_yield(intercrop, land_area_acres * 0.3)  # 30% of area
        
        # Estimate tree yield (simplified - only for mango)
        tree_yield = 0
        if 'Mango' in trees:
            # Assume 20 mango trees per acre
            num_trees = int(land_area_acres * 20)
            tree_yield = num_trees * 200  # 200 kg per tree (mature)
        
        # Calculate income
        main_crop_income = main_crop_yield * crop_prices.get(main_crop, 25)
        intercrop_income = intercrop_yield * crop_prices.get(intercrop, 30)
        tree_income = tree_yield * crop_prices.get('Mango', 60)
        
        total_income = main_crop_income + intercrop_income + tree_income
        
        # Estimate costs (simplified)
        # Assume 60% of budget is used for cultivation
        total_cost = budget_inr * 0.6
        
        # Calculate profit and ROI
        profit = total_income - total_cost
        roi = profit / total_cost if total_cost > 0 else 0
        
        return profit, roi
    
    def generate_sustainability_tips(self, soil_data: SoilData, weather_data: WeatherData) -> List[str]:
        """
        Generate sustainability tips based on conditions.
        
        Parameters:
        soil_data (SoilData): Soil data
        weather_data (WeatherData): Weather data
        
        Returns:
        List[str]: List of sustainability tips
        """
        tips = self.sustainability_tips_base.copy()
        
        # Add condition-specific tips
        if soil_data.organic_carbon < 1.0:
            tips.append("Soil organic carbon is low. Increase compost application.")
            
        if soil_data.ph < 5.5:
            tips.append("Soil is acidic. Consider liming to raise pH.")
        elif soil_data.ph > 8.0:
            tips.append("Soil is alkaline. Add organic matter to lower pH.")
            
        if weather_data.rainfall_mm < 500:
            tips.append("Low rainfall area. Focus on drought-resistant crops and water conservation.")
        elif weather_data.rainfall_mm > 1500:
            tips.append("High rainfall area. Ensure proper drainage to prevent waterlogging.")
            
        return tips
    
    def generate_recommendation(self, soil_data: SoilData, weather_data: WeatherData, 
                              economic_data: EconomicData, land_area_acres: float,
                              location: str) -> Recommendation:
        """
        Generate a complete recommendation.
        
        Parameters:
        soil_data (SoilData): Soil data
        weather_data (WeatherData): Weather data
        economic_data (EconomicData): Economic data
        land_area_acres (float): Land area in acres
        location (str): Location name
        
        Returns:
        Recommendation: Complete recommendation
        """
        # Get crop recommendations
        crop_recommendations = self.recommend_crops(soil_data, weather_data)
        
        if not crop_recommendations:
            # Fallback recommendation
            main_crop = 'Maize'
            intercrop = 'Cowpea'
        else:
            # Select main crop (highest suitability)
            main_crop = crop_recommendations[0][0]
            
            # Select intercrop (different type, good suitability)
            main_crop_type = self.crop_suitability[main_crop]['crop_type']
            intercrop = 'Cowpea'  # Default fallback
            
            for crop, score in crop_recommendations[1:]:
                crop_type = self.crop_suitability[crop]['crop_type']
                if crop_type != main_crop_type:
                    intercrop = crop
                    break
        
        # Get tree recommendations
        tree_recommendations = self.recommend_trees(soil_data, weather_data)
        trees = [tree[0] for tree in tree_recommendations[:2]]  # Top 2 trees
        
        # Determine layout
        layout, _ = self.determine_layout(soil_data, weather_data)
        
        # Estimate yield
        expected_yield_kg = self.estimate_yield(main_crop, land_area_acres)
        
        # Estimate profit and ROI
        profit_estimate_inr, roi = self.estimate_profit(
            main_crop, intercrop, trees, land_area_acres, economic_data.budget_inr
        )
        
        # Generate sustainability tips
        sustainability_tips = self.generate_sustainability_tips(soil_data, weather_data)
        
        return Recommendation(
            main_crop=main_crop,
            intercrop=intercrop,
            trees=trees,
            layout=layout,
            expected_yield_kg=expected_yield_kg,
            profit_estimate_inr=profit_estimate_inr,
            roi=roi,
            sustainability_tips=sustainability_tips
        )

# Example usage
if __name__ == "__main__":
    # Example of how to use the recommendation engine
    engine = AgriRecommendationEngine()
    
    # Sample data
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
    
    # Generate recommendation
    recommendation = engine.generate_recommendation(
        soil_data, weather_data, economic_data, 5.0, "Belagavi, Karnataka"
    )
    
    print("Recommendation:")
    print(f"  Main Crop: {recommendation.main_crop}")
    print(f"  Intercrop: {recommendation.intercrop}")
    print(f"  Trees: {', '.join(recommendation.trees)}")
    print(f"  Layout: {recommendation.layout}")
    print(f"  Expected Yield: {recommendation.expected_yield_kg:.0f} kg")
    print(f"  Profit Estimate: ₹{recommendation.profit_estimate_inr:.0f}")
    print(f"  ROI: {recommendation.roi:.1f}x")
    print("  Sustainability Tips:")
    for tip in recommendation.sustainability_tips:
        print(f"    - {tip}")