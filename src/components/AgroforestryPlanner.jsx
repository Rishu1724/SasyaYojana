import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const AgroforestryPlanner = () => {
  const { t } = useTranslation();
  const [selectedFarmType, setSelectedFarmType] = useState('small');
  const [soilType, setSoilType] = useState('loamy');
  const [rainfall, setRainfall] = useState('moderate');
  const [agroforestryPlan, setAgroforestryPlan] = useState(null);
  const [multiCroppingPlan, setMultiCroppingPlan] = useState(null);

  // Mock agroforestry recommendations based on farm characteristics
  const generateAgroforestryPlan = () => {
    const plans = {
      small: {
        canopy: [
          { name: 'Mango Trees', spacing: '10m x 10m', benefits: 'Fruit production, shade, income diversification' },
          { name: 'Guava Trees', spacing: '8m x 8m', benefits: 'Fruit production, early returns' }
        ],
        understory: [
          { name: 'Leucaena', spacing: '2m x 2m', benefits: 'Nitrogen fixation, fodder, biomass' },
          { name: 'Gliricidia', spacing: '3m x 3m', benefits: 'Nitrogen fixation, live fencing, fodder' }
        ],
        shrubs: [
          { name: 'Turmeric', spacing: 'Interplant with trees', benefits: 'High value spice, shade tolerant' },
          { name: 'Ginger', spacing: 'Interplant with trees', benefits: 'High value spice, moisture retention' }
        ],
        ground: [
          { name: 'Black Gram', spacing: 'Row planting', benefits: 'Nitrogen fixation, short duration' },
          { name: 'Pigeon Pea', spacing: 'Between tree rows', benefits: 'Protein source, drought tolerant' }
        ]
      },
      medium: {
        canopy: [
          { name: 'Tamarind Trees', spacing: '12m x 12m', benefits: 'Fruit production, long-term investment' },
          { name: 'Jackfruit Trees', spacing: '10m x 10m', benefits: 'High value fruit, climate resilience' }
        ],
        understory: [
          { name: 'Acacia nilotica', spacing: '3m x 3m', benefits: 'Nitrogen fixation, gum production' },
          { name: 'Casuarina', spacing: '4m x 4m', benefits: 'Windbreak, timber, nitrogen fixation' }
        ],
        shrubs: [
          { name: 'Coffee', spacing: 'Shaded areas under trees', benefits: 'High value cash crop, shade requirement' },
          { name: 'Pepper', spacing: 'Supported on tree trunks', benefits: 'Climbing vine, high value spice' }
        ],
        ground: [
          { name: 'Maize', spacing: 'Row planting', benefits: 'Staple food crop, good ground cover' },
          { name: 'Cowpea', spacing: 'Interrow planting', benefits: 'Protein source, nitrogen fixation' }
        ]
      },
      large: {
        canopy: [
          { name: 'Teak Trees', spacing: '8m x 8m', benefits: 'High value timber, long-term investment' },
          { name: 'Neem Trees', spacing: '10m x 10m', benefits: 'Timber, medicinal, pest control' }
        ],
        understory: [
          { name: 'Albizia', spacing: '4m x 4m', benefits: 'Nitrogen fixation, timber, shade' },
          { name: 'Sesbania', spacing: '2m x 2m', benefits: 'Green manure, fodder, nitrogen fixation' }
        ],
        shrubs: [
          { name: 'Medicinal Plants', spacing: 'Dedicated plots', benefits: 'Diverse income, traditional medicine' },
          { name: 'Aromatic Herbs', spacing: 'Border plantings', benefits: 'Essential oils, pest repellent' }
        ],
        ground: [
          { name: 'Sorghum', spacing: 'Row planting', benefits: 'Drought tolerant, fodder and grain' },
          { name: 'Groundnut', spacing: 'Interrow planting', benefits: 'Oilseed crop, nitrogen fixation' }
        ]
      }
    };

    return plans[selectedFarmType];
  };

  // Mock multi-cropping recommendations
  const generateMultiCroppingPlan = () => {
    const plans = {
      small: {
        combinations: [
          {
            name: 'Maize + Cowpea',
            benefits: 'Complementary growth, nitrogen fixation, diversified income',
            layout: 'Alternate rows',
            season: 'Kharif'
          },
          {
            name: 'Wheat + Chickpea',
            benefits: 'Different root zones, nitrogen fixation, cool season combination',
            layout: 'Strip intercropping',
            season: 'Rabi'
          }
        ]
      },
      medium: {
        combinations: [
          {
            name: 'Sorghum + Pigeon Pea',
            benefits: 'Drought tolerance, complementary height, protein + carbohydrate',
            layout: 'Row intercropping',
            season: 'Kharif'
          },
          {
            name: 'Mustard + Lentil',
            benefits: 'Oilseed + pulse combination, different nutrient requirements',
            layout: 'Mixed intercropping',
            season: 'Rabi'
          }
        ]
      },
      large: {
        combinations: [
          {
            name: 'Cotton + Soybean',
            benefits: 'Fiber + protein, pest management, mechanization compatible',
            layout: 'Strip intercropping',
            season: 'Kharif'
          },
          {
            name: 'Barley + Field Pea',
            benefits: 'Cereal + pulse, early harvest, soil improvement',
            layout: 'Alternate row',
            season: 'Rabi'
          }
        ]
      }
    };

    return plans[selectedFarmType];
  };

  // Generate plans when farm characteristics change
  useEffect(() => {
    const agroPlan = generateAgroforestryPlan();
    const multiPlan = generateMultiCroppingPlan();
    
    setAgroforestryPlan(agroPlan);
    setMultiCroppingPlan(multiPlan);
  }, [selectedFarmType, soilType, rainfall]);

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">Agroforestry & Multi-Cropping Planner</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div>
          <label className="block text-gray-700 mb-2 font-medium">Farm Size</label>
          <select 
            value={selectedFarmType}
            onChange={(e) => setSelectedFarmType(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="small">Small (0.5-2 acres)</option>
            <option value="medium">Medium (2-5 acres)</option>
            <option value="large">Large (5+ acres)</option>
          </select>
        </div>
        
        <div>
          <label className="block text-gray-700 mb-2 font-medium">Soil Type</label>
          <select 
            value={soilType}
            onChange={(e) => setSoilType(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="sandy">Sandy</option>
            <option value="loamy">Loamy</option>
            <option value="clay">Clay</option>
            <option value="silty">Silty</option>
          </select>
        </div>
        
        <div>
          <label className="block text-gray-700 mb-2 font-medium">Rainfall</label>
          <select 
            value={rainfall}
            onChange={(e) => setRainfall(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="low">Low (&lt;500mm)</option>
            <option value="moderate">Moderate (500-1000mm)</option>
            <option value="high">High (&gt;1000mm)</option>
          </select>
        </div>
      </div>
      
      {agroforestryPlan && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Agroforestry Layer Plan</h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-800 mb-3 flex items-center">
                <span className="w-3 h-3 bg-green-600 rounded-full mr-2"></span>
                Canopy Trees
              </h4>
              <ul className="space-y-3">
                {agroforestryPlan.canopy.map((tree, index) => (
                  <li key={index} className="flex justify-between items-start border-b border-gray-100 pb-2 last:border-0 last:pb-0">
                    <div>
                      <div className="font-medium text-gray-800">{tree.name}</div>
                      <div className="text-sm text-gray-600">{tree.spacing}</div>
                    </div>
                    <div className="text-sm text-gray-600 text-right">{tree.benefits}</div>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-800 mb-3 flex items-center">
                <span className="w-3 h-3 bg-green-500 rounded-full mr-2"></span>
                Understory Trees
              </h4>
              <ul className="space-y-3">
                {agroforestryPlan.understory.map((tree, index) => (
                  <li key={index} className="flex justify-between items-start border-b border-gray-100 pb-2 last:border-0 last:pb-0">
                    <div>
                      <div className="font-medium text-gray-800">{tree.name}</div>
                      <div className="text-sm text-gray-600">{tree.spacing}</div>
                    </div>
                    <div className="text-sm text-gray-600 text-right">{tree.benefits}</div>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-800 mb-3 flex items-center">
                <span className="w-3 h-3 bg-green-400 rounded-full mr-2"></span>
                Shrubs
              </h4>
              <ul className="space-y-3">
                {agroforestryPlan.shrubs.map((shrub, index) => (
                  <li key={index} className="flex justify-between items-start border-b border-gray-100 pb-2 last:border-0 last:pb-0">
                    <div>
                      <div className="font-medium text-gray-800">{shrub.name}</div>
                      <div className="text-sm text-gray-600">{shrub.spacing}</div>
                    </div>
                    <div className="text-sm text-gray-600 text-right">{shrub.benefits}</div>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-800 mb-3 flex items-center">
                <span className="w-3 h-3 bg-green-300 rounded-full mr-2"></span>
                Ground Crops
              </h4>
              <ul className="space-y-3">
                {agroforestryPlan.ground.map((crop, index) => (
                  <li key={index} className="flex justify-between items-start border-b border-gray-100 pb-2 last:border-0 last:pb-0">
                    <div>
                      <div className="font-medium text-gray-800">{crop.name}</div>
                      <div className="text-sm text-gray-600">{crop.spacing}</div>
                    </div>
                    <div className="text-sm text-gray-600 text-right">{crop.benefits}</div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
      
      {multiCroppingPlan && (
        <div>
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Multi-Cropping Combinations</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {multiCroppingPlan.combinations.map((combination, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <h4 className="font-medium text-gray-800 mb-2">{combination.name}</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Benefits:</span>
                    <span className="text-gray-800 text-right">{combination.benefits}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Layout:</span>
                    <span className="text-gray-800">{combination.layout}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Season:</span>
                    <span className="text-gray-800">{combination.season}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      <div className="mt-8 p-4 bg-green-50 rounded-lg">
        <h4 className="font-medium text-green-800 mb-2">Benefits of Agroforestry & Multi-Cropping</h4>
        <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-green-700">
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>Improves soil fertility and reduces erosion</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>Provides shade and microclimate regulation</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>Produces diverse fruits, nuts, timber, and crops</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>Enhances biodiversity and beneficial insects</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>Reduces pest risks and increases yield stability</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>Ensures more stable income through diversification</span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default AgroforestryPlanner;