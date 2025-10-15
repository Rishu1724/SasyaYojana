import axios from 'axios';
import continuousLearningService from './continuousLearningService';

// Service to integrate with free APIs for AgroIntel AI system
class AgroIntelService {
  // Fetch soil data from ISRIC SoilGrids API
  async fetchSoilData(lat, lon) {
    try {
      // SoilGrids API endpoint for soil properties
      const response = await axios.get(
        `https://rest.isric.org/soilgrids/v2.0/properties/query`,
        {
          params: {
            lat: lat,
            lon: lon,
            property: ['phh2o', 'ocd', 'nitrogen', 'cec', 'sand', 'silt', 'clay'],
            depth: '0-5cm',
            value: 'mean'
          }
        }
      );
      
      return {
        ph: response.data.properties.phh2o ? response.data.properties.phh2o.mean / 10 : null,
        organic_carbon: response.data.properties.ocd ? response.data.properties.ocd.mean / 10 : null,
        nitrogen: response.data.properties.nitrogen ? response.data.properties.nitrogen.mean : null,
        cec: response.data.properties.cec ? response.data.properties.cec.mean : null, // Cation Exchange Capacity
        sand: response.data.properties.sand ? response.data.properties.sand.mean : null,
        silt: response.data.properties.silt ? response.data.properties.silt.mean : null,
        clay: response.data.properties.clay ? response.data.properties.clay.mean : null
      };
    } catch (error) {
      console.error('Error fetching soil data:', error);
      // Return mock data if API fails
      return {
        ph: 6.7,
        organic_carbon: 1.2,
        nitrogen: 150,
        cec: 12,
        sand: 45,
        silt: 35,
        clay: 20
      };
    }
  }

  // Fetch weather data from NASA POWER API
  async fetchWeatherData(lat, lon) {
    try {
      // NASA POWER API for meteorological data
      const response = await axios.get(
        `https://power.larc.nasa.gov/api/temporal/climatology/point`,
        {
          params: {
            parameters: 'T2M,RH2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN',
            community: 'AG',
            longitude: lon,
            latitude: lat,
            format: 'JSON',
            start: 2020,
            end: 2022
          }
        }
      );
      
      const data = response.data.properties.parameter;
      
      return {
        avg_temperature_c: data.T2M ? Math.round(data.T2M.ANN) : null,
        avg_humidity: data.RH2M ? Math.round(data.RH2M.ANN) : null,
        avg_rainfall_mm: data.PRECTOTCORR ? Math.round(data.PRECTOTCORR.ANN * 3650) : null, // Convert from kg/m2/s to mm/year
        solar_radiation: data.ALLSKY_SFC_SW_DWN ? Math.round(data.ALLSKY_SFC_SW_DWN.ANN) : null // Solar radiation
      };
    } catch (error) {
      console.error('Error fetching weather data:', error);
      // Return mock data if API fails
      return {
        avg_temperature_c: 28,
        avg_humidity: 65,
        avg_rainfall_mm: 980,
        solar_radiation: 5.5
      };
    }
  }

  // Fetch elevation data from Open Elevation API
  async fetchElevation(lat, lon) {
    try {
      const response = await axios.get(
        `https://api.open-elevation.com/api/v1/lookup`,
        {
          params: {
            locations: `${lat},${lon}`
          }
        }
      );
      
      return response.data.results[0].elevation;
    } catch (error) {
      console.error('Error fetching elevation data:', error);
      return 500; // Default elevation in meters
    }
  }

  // Fetch crop market prices from Agmarknet API (mock implementation)
  async fetchCropPrices(cropList) {
    try {
      // In a real implementation, this would call the Agmarknet API
      // For now, we'll return mock prices
      const prices = {};
      cropList.forEach(crop => {
        // Generate mock prices based on crop type
        switch(crop.toLowerCase()) {
          case 'maize':
            prices[crop] = { min: 1800, max: 2200, avg: 2000 };
            break;
          case 'cowpea':
            prices[crop] = { min: 4500, max: 5500, avg: 5000 };
            break;
          case 'mango':
            prices[crop] = { min: 40, max: 60, avg: 50 };
            break;
          case 'gliricidia':
            prices[crop] = { min: 5, max: 10, avg: 7 };
            break;
          default:
            prices[crop] = { min: 2000, max: 4000, avg: 3000 };
        }
      });
      
      return prices;
    } catch (error) {
      console.error('Error fetching crop prices:', error);
      return {};
    }
  }

  // Call our AI model API to generate recommendations
  async callAIModelAPI(inputs) {
    try {
      // In a production environment, this would call your AI model API
      // For now, we'll return mock data based on the inputs
      console.log('Calling AI Model API with inputs:', inputs);
      
      // This is where you would make an HTTP request to your AI model API
      // const response = await axios.post('http://localhost:5000/recommend', inputs);
      // return response.data;
      
      // For now, return mock data
      return this.generateMockRecommendation(inputs);
    } catch (error) {
      console.error('Error calling AI model API:', error);
      // Fallback to rule-based generation
      return this.generateAgroforestryPlan(inputs);
    }
  }

  // Fetch real-time predictions from our ML models
  async fetchRealTimePredictions(farmerData) {
    try {
      // In a production environment, this would call your AI model API
      console.log('Fetching real-time predictions with farmer data:', farmerData);
      
      // Make API call to our prediction service
      const response = await axios.post('http://localhost:5000/predict/realtime', farmerData);
      
      // Store the prediction in Firebase for continuous learning
      try {
        const predictionId = await continuousLearningService.storePrediction({
          farmer_data: farmerData,
          predictions: response.data.predictions,
          weather_data: response.data.weather_data,
          recommendations: response.data.recommendations,
          timestamp: new Date().toISOString()
        });
        console.log('Prediction stored in Firebase with ID:', predictionId);
        
        // Add the prediction ID to the response for feedback tracking
        response.data.prediction_id = predictionId;
      } catch (storageError) {
        console.error('Error storing prediction in Firebase:', storageError);
      }
      
      return response.data;
    } catch (error) {
      console.error('Error fetching real-time predictions:', error);
      // Return mock data if API fails
      return {
        predictions: {
          yield_kg_per_acre: 3000,
          roi: 2.8,
          confidence: 0.85
        },
        weather_data: {
          avg_temperature_c: 28,
          avg_humidity: 65,
          avg_rainfall_mm: 980,
          solar_radiation: 5.5
        },
        recommendations: {
          best_crop: "Maize",
          planting_time: "June-July",
          irrigation_needs: "Moderate"
        }
      };
    }
  }

  // Generate mock recommendation (to be replaced with actual AI model API call)
  generateMockRecommendation(inputs) {
    const { 
      latitude, 
      longitude, 
      soil_pH, 
      organic_carbon,
      nitrogen,
      cec,
      sand, 
      clay, 
      silt,
      avg_rainfall_mm,
      avg_temperature_c,
      solar_radiation,
      land_area,
      investment_capacity
    } = inputs;
    
    // Determine soil texture based on sand/silt/clay percentages
    const soilTexture = this.determineSoilTexture(sand, silt, clay);
    
    // Determine soil drainage based on texture
    const drainageQuality = this.determineDrainageQuality(soilTexture, clay);
    
    // Determine suitable crops based on soil and climate
    const suitableCrops = this.determineSuitableCrops(soil_pH, avg_rainfall_mm, avg_temperature_c, nitrogen);
    
    // Determine suitable trees based on climate and soil
    const suitableTrees = this.determineSuitableTrees(avg_rainfall_mm, avg_temperature_c, soil_pH, drainageQuality);
    
    // Calculate estimated investment and returns
    const economicProjection = this.calculateEconomicProjection(land_area, investment_capacity, suitableCrops, suitableTrees);
    
    // Generate spatial layout
    const layoutPlan = this.generateLayoutPlan(soilTexture, avg_rainfall_mm);
    
    // Get crop prices for economic analysis
    const cropList = [
      ...suitableCrops.mainCrops.map(c => c.name),
      ...suitableCrops.intercrops.map(c => c.name),
      ...suitableTrees.map(t => t.name)
    ];
    
    // Generate sustainability metrics
    const sustainabilityMetrics = this.calculateSustainabilityMetrics(soilTexture, organic_carbon, avg_rainfall_mm);
    
    // Generate soil improvement recommendations
    const soilImprovementTips = this.generateSoilImprovementTips(soil_pH, organic_carbon, nitrogen, cec);
    
    return {
      farm_location: {
        latitude: latitude,
        longitude: longitude,
        region: this.determineRegion(latitude, longitude),
        elevation: 500 // Mock elevation
      },
      soil_summary: {
        ph: soil_pH,
        organic_carbon: `${organic_carbon}%`,
        nitrogen: `${nitrogen} kg/ha`,
        cec: `${cec} cmol/kg`,
        texture: soilTexture,
        drainage: drainageQuality,
        recommendation: this.getSoilRecommendation(soil_pH, organic_carbon, soilTexture, nitrogen, cec)
      },
      climate_summary: {
        avg_rainfall_mm: avg_rainfall_mm,
        avg_temperature_c: avg_temperature_c,
        solar_radiation: `${solar_radiation} kWh/m²/day`,
        recommendation: this.getClimateRecommendation(avg_rainfall_mm, avg_temperature_c, solar_radiation)
      },
      recommended_agroforestry_system: {
        trees: suitableTrees,
        main_crops: suitableCrops.mainCrops,
        intercrops: suitableCrops.intercrops,
        herbs: suitableCrops.herbs
      },
      layout_plan: layoutPlan,
      economic_projection: economicProjection,
      sustainability_metrics: sustainabilityMetrics,
      soil_improvement_tips: soilImprovementTips,
      next_steps: [
        "Prepare nursery of selected trees",
        "Install drip irrigation (low cost)",
        "Plant nitrogen-fixing crops first",
        "Add organic compost before sowing"
      ]
    };
  }

  // Generate AI-driven agroforestry plan based on inputs
  async generateAgroforestryPlan(inputs) {
    // Call our AI model API
    try {
      const recommendation = await this.callAIModelAPI(inputs);
      return recommendation;
    } catch (error) {
      console.error('Error generating agroforestry plan:', error);
      // Fallback to rule-based generation if AI model fails
      return this.generateRuleBasedPlan(inputs);
    }
  }
  
  // Fallback rule-based plan generation
  generateRuleBasedPlan(inputs) {
    const { 
      latitude, 
      longitude, 
      soil_pH, 
      organic_carbon,
      nitrogen,
      cec,
      sand, 
      clay, 
      silt,
      avg_rainfall_mm,
      avg_temperature_c,
      solar_radiation,
      land_area,
      investment_capacity
    } = inputs;
    
    // Determine soil texture based on sand/silt/clay percentages
    const soilTexture = this.determineSoilTexture(sand, silt, clay);
    
    // Determine soil drainage based on texture
    const drainageQuality = this.determineDrainageQuality(soilTexture, clay);
    
    // Determine suitable crops based on soil and climate
    const suitableCrops = this.determineSuitableCrops(soil_pH, avg_rainfall_mm, avg_temperature_c, nitrogen);
    
    // Determine suitable trees based on climate and soil
    const suitableTrees = this.determineSuitableTrees(avg_rainfall_mm, avg_temperature_c, soil_pH, drainageQuality);
    
    // Calculate estimated investment and returns
    const economicProjection = this.calculateEconomicProjection(land_area, investment_capacity, suitableCrops, suitableTrees);
    
    // Generate spatial layout
    const layoutPlan = this.generateLayoutPlan(soilTexture, avg_rainfall_mm);
    
    // Get crop prices for economic analysis
    const cropList = [
      ...suitableCrops.mainCrops.map(c => c.name),
      ...suitableCrops.intercrops.map(c => c.name),
      ...suitableTrees.map(t => t.name)
    ];
    
    const cropPrices = {}; // Mock crop prices
    
    // Generate sustainability metrics
    const sustainabilityMetrics = this.calculateSustainabilityMetrics(soilTexture, organic_carbon, avg_rainfall_mm);
    
    // Generate soil improvement recommendations
    const soilImprovementTips = this.generateSoilImprovementTips(soil_pH, organic_carbon, nitrogen, cec);
    
    return {
      farm_location: {
        latitude: latitude,
        longitude: longitude,
        region: this.determineRegion(latitude, longitude),
        elevation: 500 // Mock elevation
      },
      soil_summary: {
        ph: soil_pH,
        organic_carbon: `${organic_carbon}%`,
        nitrogen: `${nitrogen} kg/ha`,
        cec: `${cec} cmol/kg`,
        texture: soilTexture,
        drainage: drainageQuality,
        recommendation: this.getSoilRecommendation(soil_pH, organic_carbon, soilTexture, nitrogen, cec)
      },
      climate_summary: {
        avg_rainfall_mm: avg_rainfall_mm,
        avg_temperature_c: avg_temperature_c,
        solar_radiation: `${solar_radiation} kWh/m²/day`,
        recommendation: this.getClimateRecommendation(avg_rainfall_mm, avg_temperature_c, solar_radiation)
      },
      recommended_agroforestry_system: {
        trees: suitableTrees,
        main_crops: suitableCrops.mainCrops,
        intercrops: suitableCrops.intercrops,
        herbs: suitableCrops.herbs
      },
      layout_plan: layoutPlan,
      economic_projection: {
        ...economicProjection,
        crop_prices: cropPrices
      },
      sustainability_metrics: sustainabilityMetrics,
      soil_improvement_tips: soilImprovementTips,
      next_steps: [
        "Prepare nursery of selected trees",
        "Install drip irrigation (low cost)",
        "Plant nitrogen-fixing crops first",
        "Add organic compost before sowing"
      ]
    };
  }
  
  // Helper methods for plan generation
  determineSoilTexture(sand, silt, clay) {
    if (sand && silt && clay) {
      if (sand > 70) return "Sandy";
      if (clay > 40) return "Clay";
      if (silt > 40) return "Silty";
      return "Loamy";
    }
    return "Loamy"; // Default
  }
  
  determineDrainageQuality(texture, clay) {
    if (texture === "Sandy") return "Well Drained";
    if (texture === "Clay" || clay > 40) return "Poorly Drained";
    return "Moderately Drained";
  }
  
  determineSuitableCrops(ph, rainfall, temperature, nitrogen) {
    const mainCrops = [];
    const intercrops = [];
    const herbs = [];
    
    // Main crops based on conditions
    if (ph >= 6.0 && ph <= 7.5 && rainfall >= 600) {
      if (temperature >= 20 && temperature <= 35) {
        mainCrops.push({name: "Maize", planting_density: "50,000 plants/ha", spacing: "75cm rows"});
      }
    }
    
    if (ph >= 5.5 && ph <= 7.0 && rainfall >= 500) {
      if (temperature >= 25 && temperature <= 35) {
        mainCrops.push({name: "Sorghum", planting_density: "60,000 plants/ha", spacing: "45cm rows"});
      }
    }
    
    // Intercrops based on conditions
    if (nitrogen < 200) {
      intercrops.push({name: "Cowpea", planting_density: "40,000 plants/ha", benefit: "Nitrogen fixation"});
    }
    
    if (temperature >= 20 && temperature <= 30) {
      intercrops.push({name: "Black Gram", planting_density: "35,000 plants/ha", benefit: "Protein source"});
    }
    
    // Herbs based on conditions
    if (temperature >= 20 && temperature <= 35) {
      herbs.push({name: "Turmeric", planting_density: "125,000 rhizomes/ha", benefit: "High value spice"});
    }
    
    // Fallback crops if none match
    if (mainCrops.length === 0) {
      mainCrops.push({name: "Finger Millet", planting_density: "55,000 plants/ha", spacing: "30cm rows"});
    }
    
    if (intercrops.length === 0) {
      intercrops.push({name: "Green Gram", planting_density: "40,000 plants/ha", benefit: "Nitrogen fixation"});
    }
    
    if (herbs.length === 0) {
      herbs.push({name: "Ginger", planting_density: "100,000 rhizomes/ha", benefit: "High value spice"});
    }
    
    return { mainCrops, intercrops, herbs };
  }
  
  determineSuitableTrees(rainfall, temperature, ph, drainage) {
    const trees = [];
    
    // Recommend trees based on climate and soil
    if (rainfall > 800 && temperature > 25 && ph >= 5.5 && ph <= 7.5) {
      trees.push({
        name: "Mango", 
        spacing_m: "10x10", 
        yield_kg_per_tree: 200,
        maturity_years: 4,
        benefit: "Fruit production, shade, income diversification"
      });
    }
    
    if (ph >= 5.0 && ph <= 8.0 && drainage !== "Poorly Drained") {
      trees.push({
        name: "Gliricidia", 
        spacing_m: "2x2", 
        yield_kg_per_tree: 15,
        maturity_years: 2,
        benefit: "Nitrogen fixer, soil protector, fodder"
      });
    }
    
    if (rainfall > 600 && temperature >= 20 && temperature <= 35) {
      trees.push({
        name: "Neem", 
        spacing_m: "8x8", 
        yield_kg_per_tree: 5,
        maturity_years: 3,
        benefit: "Multipurpose tree for pest control and shade"
      });
    }
    
    // Fallback trees if none match
    if (trees.length === 0) {
      trees.push({
        name: "Subabul (Leucaena)", 
        spacing_m: "3x3", 
        yield_kg_per_tree: 10,
        maturity_years: 2,
        benefit: "Nitrogen fixer, fodder, biomass"
      });
    }
    
    return trees;
  }
  
  calculateEconomicProjection(land_area, investment_capacity, crops, trees) {
    // Simplified economic calculation
    let estimated_investment = 0;
    let expected_income = 0;
    
    switch(investment_capacity) {
      case 'low':
        estimated_investment = 20000;
        expected_income = 60000;
        break;
      case 'medium':
        estimated_investment = 35000;
        expected_income = 120000;
        break;
      case 'high':
        estimated_investment = 60000;
        expected_income = 200000;
        break;
      default:
        estimated_investment = 35000;
        expected_income = 120000;
    }
    
    const roi = (expected_income / estimated_investment).toFixed(1) + "x";
    const payback_period_months = Math.round(estimated_investment / (expected_income / 12));
    
    // Calculate per crop/tree income (simplified)
    const cropIncome = {};
    crops.mainCrops.forEach(crop => {
      cropIncome[crop.name] = Math.round(expected_income * 0.4);
    });
    
    crops.intercrops.forEach(crop => {
      cropIncome[crop.name] = Math.round(expected_income * 0.2);
    });
    
    const treeIncome = {};
    trees.forEach(tree => {
      treeIncome[tree.name] = Math.round(expected_income * 0.4);
    });
    
    return {
      estimated_investment,
      expected_income,
      roi,
      payback_period_months,
      crop_income: cropIncome,
      tree_income: treeIncome
    };
  }
  
  generateLayoutPlan(soilTexture, rainfall) {
    let pattern = "Alley Cropping";
    let description = "Alternate rows of trees and mixed crops (5m spacing)";
    
    if (soilTexture === "Sandy" && rainfall < 600) {
      pattern = "Boundary Planting";
      description = "Plant trees along boundaries with drought-resistant crops in center";
    } else if (rainfall > 1200) {
      pattern = "Multistorey System";
      description = "Multiple layers of trees, shrubs, and crops for high rainfall areas";
    }
    
    return {
      pattern: pattern,
      description: description,
      tree_spacing: "5-10m depending on species",
      crop_spacing: "As per crop recommendations"
    };
  }
  
  calculateSustainabilityMetrics(soilTexture, organicCarbon, rainfall) {
    // Calculate sustainability metrics based on inputs
    let soilHealthIncrease = "+10-15%";
    let waterSavings = "15-20%";
    let carbonSequestration = "1.0-1.5 tons/ha/year";
    
    // Adjust based on soil quality
    if (organicCarbon > 1.5) {
      soilHealthIncrease = "+15-20%";
      carbonSequestration = "1.5-2.0 tons/ha/year";
    }
    
    // Adjust based on rainfall
    if (rainfall > 1000) {
      waterSavings = "20-25%";
    } else if (rainfall < 500) {
      waterSavings = "10-15%";
    }
    
    return {
      soil_health_increase: soilHealthIncrease,
      water_savings: waterSavings,
      carbon_sequestration_potential: carbonSequestration,
      biodiversity_score: "High",
      climate_resilience: "Improved"
    };
  }
  
  generateSoilImprovementTips(ph, organicCarbon, nitrogen, cec) {
    const tips = [];
    
    if (ph < 6.0) {
      tips.push("Soil is acidic. Add lime (calcium carbonate) to raise pH. Apply 1-2 tons/ha based on current pH.");
    } else if (ph > 7.5) {
      tips.push("Soil is alkaline. Add organic matter like compost to lower pH. Apply 5-10 tons/ha of well-decomposed compost.");
    }
    
    if (organicCarbon < 1.0) {
      tips.push("Low organic matter. Add compost or farmyard manure. Apply 5-10 tons/ha annually.");
    }
    
    if (nitrogen < 150) {
      tips.push("Low nitrogen content. Plant nitrogen-fixing crops like legumes. Apply neem cake @ 100 kg/ha.");
    }
    
    if (cec < 10) {
      tips.push("Low cation exchange capacity. Add organic matter to improve soil structure and nutrient retention.");
    }
    
    tips.push("Practice crop rotation with legumes to maintain soil fertility.");
    tips.push("Use mulching to conserve moisture and add organic matter.");
    
    return tips;
  }
  
  determineRegion(lat, lon) {
    // Simplified region determination for India
    if (lat > 8 && lat < 37 && lon > 68 && lon < 97) {
      return "India";
    }
    return "Global";
  }
  
  getSoilRecommendation(ph, organic_carbon, texture, nitrogen, cec) {
    let recommendation = "";
    
    if (ph < 6.0) {
      recommendation += "Soil is acidic. Add lime to raise pH. ";
    } else if (ph > 7.5) {
      recommendation += "Soil is alkaline. Add organic matter to lower pH. ";
    } else {
      recommendation += "Soil pH is optimal for most crops. ";
    }
    
    if (organic_carbon < 1.0) {
      recommendation += "Low organic matter. Add compost or manure. ";
    } else {
      recommendation += "Good organic matter content. ";
    }
    
    if (nitrogen < 150) {
      recommendation += "Low nitrogen. Include nitrogen-fixing crops. ";
    }
    
    recommendation += `Ideal for ${texture.toLowerCase()} soil crops.`;
    
    return recommendation;
  }
  
  getClimateRecommendation(rainfall, temperature, solar) {
    let recommendation = "";
    
    if (rainfall < 500) {
      recommendation += "Arid conditions. Focus on drought-resistant crops. ";
    } else if (rainfall > 1500) {
      recommendation += "High rainfall area. Ensure good drainage. ";
    } else {
      recommendation += "Moderate rainfall suitable for diverse crops. ";
    }
    
    if (temperature < 20) {
      recommendation += "Cool climate. Suitable for winter crops. ";
    } else if (temperature > 35) {
      recommendation += "Hot climate. Focus on heat-tolerant varieties. ";
    } else {
      recommendation += "Temperature suitable for year-round cultivation. ";
    }
    
    if (solar > 6) {
      recommendation += "High solar radiation - suitable for sun-loving crops. ";
    }
    
    return recommendation.trim();
  }

  // Method to submit farmer feedback
  async submitFeedback(predictionId, feedbackData) {
    try {
      const feedbackId = await continuousLearningService.storeFeedback(predictionId, feedbackData);
      console.log('Feedback submitted successfully with ID:', feedbackId);
      return feedbackId;
    } catch (error) {
      console.error('Error submitting feedback:', error);
      throw error;
    }
  }
}

export default new AgroIntelService();