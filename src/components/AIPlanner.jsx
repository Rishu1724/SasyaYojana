import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import agroIntelService from '../services/agroIntelService';

const AIPlanner = () => {
  const { t, i18n } = useTranslation();
  const [farmData, setFarmData] = useState({
    latitude: '',
    longitude: '',
    land_area: '',
    investment_capacity: 'medium'
  });
  const [soilData, setSoilData] = useState(null);
  const [weatherData, setWeatherData] = useState(null);
  const [agroPlan, setAgroPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFarmData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Fetch data and generate plan
  const generatePlan = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      // Validate inputs
      if (!farmData.latitude || !farmData.longitude) {
        throw new Error('Please enter valid coordinates');
      }
      
      const lat = parseFloat(farmData.latitude);
      const lon = parseFloat(farmData.longitude);
      
      if (isNaN(lat) || isNaN(lon)) {
        throw new Error('Please enter valid numeric coordinates');
      }
      
      // Fetch soil data
      const soil = await agroIntelService.fetchSoilData(lat, lon);
      setSoilData(soil);
      
      // Fetch weather data
      const weather = await agroIntelService.fetchWeatherData(lat, lon);
      setWeatherData(weather);
      
      // Generate agroforestry plan
      const inputs = {
        latitude: lat,
        longitude: lon,
        soil_pH: soil.ph,
        organic_carbon: soil.organic_carbon,
        nitrogen: soil.nitrogen,
        cec: soil.cec,
        sand: soil.sand,
        silt: soil.silt,
        clay: soil.clay,
        avg_rainfall_mm: weather.avg_rainfall_mm,
        avg_temperature_c: weather.avg_temperature_c,
        solar_radiation: weather.solar_radiation,
        land_area: farmData.land_area,
        investment_capacity: farmData.investment_capacity
      };
      
      const plan = await agroIntelService.generateAgroforestryPlan(inputs);
      setAgroPlan(plan);
    } catch (err) {
      console.error('Error generating plan:', err);
      setError(err.message || 'Failed to generate plan. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Reset form
  const resetForm = () => {
    setFarmData({
      latitude: '',
      longitude: '',
      land_area: '',
      investment_capacity: 'medium'
    });
    setSoilData(null);
    setWeatherData(null);
    setAgroPlan(null);
    setError(null);
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">
        🌱 {t('aiDrivenAgroforestryPlanner')}
      </h2>
      
      {!agroPlan ? (
        <form onSubmit={generatePlan} className="space-y-6">
          {error && (
            <div className="bg-red-50 text-red-700 p-3 rounded-lg">
              {error}
            </div>
          )}
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-gray-700 mb-2 font-medium">
                {t('latitude')}
              </label>
              <input
                type="text"
                name="latitude"
                value={farmData.latitude}
                onChange={handleInputChange}
                placeholder="e.g., 15.8221"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-gray-700 mb-2 font-medium">
                {t('longitude')}
              </label>
              <input
                type="text"
                name="longitude"
                value={farmData.longitude}
                onChange={handleInputChange}
                placeholder="e.g., 75.0302"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-gray-700 mb-2 font-medium">
                {t('landAreaInAcres')}
              </label>
              <input
                type="number"
                name="land_area"
                value={farmData.land_area}
                onChange={handleInputChange}
                placeholder="e.g., 2.5"
                step="0.1"
                min="0.1"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-gray-700 mb-2 font-medium">
                {t('investmentCapacity')}
              </label>
              <select
                name="investment_capacity"
                value={farmData.investment_capacity}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
              >
                <option value="low">{t('lowBudget')}</option>
                <option value="medium">{t('mediumBudget')}</option>
                <option value="high">{t('highBudget')}</option>
              </select>
            </div>
          </div>
          
          <div className="flex flex-wrap gap-3">
            <button
              type="submit"
              disabled={loading}
              className={`bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-lg transition duration-300 ${loading ? 'opacity-75 cursor-not-allowed' : ''}`}
            >
              {loading ? t('generatingPlan') : t('generateAgroforestryPlan')}
            </button>
            
            <button
              type="button"
              onClick={resetForm}
              className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-3 px-6 rounded-lg transition duration-300"
            >
              {t('reset')}
            </button>
          </div>
        </form>
      ) : (
        <div className="space-y-6">
          {/* Farm Location */}
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="text-lg font-medium text-gray-800 mb-3">📍 {t('farmLocation')}</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
              <div>
                <span className="text-gray-600">{t('latitude')}:</span>
                <span className="ml-2 font-medium">{agroPlan.farm_location.latitude}</span>
              </div>
              <div>
                <span className="text-gray-600">{t('longitude')}:</span>
                <span className="ml-2 font-medium">{agroPlan.farm_location.longitude}</span>
              </div>
              <div>
                <span className="text-gray-600">{t('region')}:</span>
                <span className="ml-2 font-medium">{agroPlan.farm_location.region}</span>
              </div>
              <div>
                <span className="text-gray-600">{t('elevation')}:</span>
                <span className="ml-2 font-medium">{agroPlan.farm_location.elevation} m</span>
              </div>
            </div>
          </div>
          
          {/* Soil Summary */}
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="text-lg font-medium text-gray-800 mb-3">🌍 {t('soilSummary')}</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p><span className="text-gray-600">{t('phLevel')}:</span> <span className="font-medium">{agroPlan.soil_summary.ph}</span></p>
                <p><span className="text-gray-600">{t('organicCarbon')}:</span> <span className="font-medium">{agroPlan.soil_summary.organic_carbon}</span></p>
                <p><span className="text-gray-600">{t('nitrogen')}:</span> <span className="font-medium">{agroPlan.soil_summary.nitrogen}</span></p>
                <p><span className="text-gray-600">{t('cec')}:</span> <span className="font-medium">{agroPlan.soil_summary.cec}</span></p>
                <p><span className="text-gray-600">{t('texture')}:</span> <span className="font-medium">{agroPlan.soil_summary.texture}</span></p>
                <p><span className="text-gray-600">{t('drainage')}:</span> <span className="font-medium">{agroPlan.soil_summary.drainage}</span></p>
              </div>
              <div>
                <p className="text-gray-700">{agroPlan.soil_summary.recommendation}</p>
              </div>
            </div>
          </div>
          
          {/* Climate Summary */}
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="text-lg font-medium text-gray-800 mb-3">☀️ {t('climateSummary')}</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p><span className="text-gray-600">{t('averageRainfall')}:</span> <span className="font-medium">{agroPlan.climate_summary.avg_rainfall_mm} mm</span></p>
                <p><span className="text-gray-600">{t('averageTemperature')}:</span> <span className="font-medium">{agroPlan.climate_summary.avg_temperature_c}°C</span></p>
                <p><span className="text-gray-600">{t('solarRadiation')}:</span> <span className="font-medium">{agroPlan.climate_summary.solar_radiation}</span></p>
              </div>
              <div>
                <p className="text-gray-700">{agroPlan.climate_summary.recommendation}</p>
              </div>
            </div>
          </div>
          
          {/* Soil Improvement Tips */}
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="text-lg font-medium text-gray-800 mb-3">🌱 {t('soilImprovementTips')}</h3>
            <ul className="list-disc list-inside space-y-2">
              {agroPlan.soil_improvement_tips.map((tip, index) => (
                <li key={index} className="text-gray-700">{tip}</li>
              ))}
            </ul>
          </div>
          
          {/* Recommended Agroforestry System */}
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="text-lg font-medium text-gray-800 mb-3">🌳 {t('recommendedAgroforestrySystem')}</h3>
            
            <div className="mb-4">
              <h4 className="font-medium text-gray-800 mb-2">{t('trees')}</h4>
              <ul className="space-y-2">
                {agroPlan.recommended_agroforestry_system.trees.map((tree, index) => (
                  <li key={index} className="flex flex-wrap items-center gap-2 border-b border-gray-100 pb-2 last:border-0 last:pb-0">
                    <span className="font-medium text-green-700">{tree.name}</span>
                    <span>({tree.spacing_m}m spacing, matures in {tree.maturity_years} years)</span>
                    <span>Yield: {tree.yield_kg_per_tree} kg/tree</span>
                    <span className="text-sm text-gray-600">{tree.benefit}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="mb-4">
              <h4 className="font-medium text-gray-800 mb-2">{t('mainCrops')}</h4>
              <ul className="space-y-2">
                {agroPlan.recommended_agroforestry_system.main_crops.map((crop, index) => (
                  <li key={index} className="flex flex-wrap items-center gap-2 border-b border-gray-100 pb-2 last:border-0 last:pb-0">
                    <span className="font-medium text-blue-700">{crop.name}</span>
                    <span>{crop.planting_density}</span>
                    <span>{crop.spacing}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="mb-4">
              <h4 className="font-medium text-gray-800 mb-2">{t('intercrops')}</h4>
              <ul className="space-y-2">
                {agroPlan.recommended_agroforestry_system.intercrops.map((crop, index) => (
                  <li key={index} className="flex flex-wrap items-center gap-2 border-b border-gray-100 pb-2 last:border-0 last:pb-0">
                    <span className="font-medium text-purple-700">{crop.name}</span>
                    <span>{crop.planting_density}</span>
                    <span>{crop.benefit}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-800 mb-2">{t('herbs')}</h4>
              <ul className="space-y-2">
                {agroPlan.recommended_agroforestry_system.herbs.map((herb, index) => (
                  <li key={index} className="flex flex-wrap items-center gap-2 border-b border-gray-100 pb-2 last:border-0 last:pb-0">
                    <span className="font-medium text-orange-700">{herb.name}</span>
                    <span>{herb.planting_density}</span>
                    <span>{herb.benefit}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          
          {/* Layout Plan */}
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="text-lg font-medium text-gray-800 mb-3">📐 {t('layoutPlan')}</h3>
            <p><span className="font-medium">{agroPlan.layout_plan.pattern}</span> - {agroPlan.layout_plan.description}</p>
            <p className="mt-2"><span className="text-gray-600">{t('treeSpacing')}:</span> {agroPlan.layout_plan.tree_spacing}</p>
            <p><span className="text-gray-600">{t('cropSpacing')}:</span> {agroPlan.layout_plan.crop_spacing}</p>
          </div>
          
          {/* Economic Projection */}
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="text-lg font-medium text-gray-800 mb-3">💰 {t('economicProjection')}</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
              <div className="bg-green-50 rounded-lg p-3 text-center">
                <p className="text-gray-600">{t('estimatedInvestment')}</p>
                <p className="text-xl font-bold text-green-700">₹{agroPlan.economic_projection.estimated_investment.toLocaleString()}</p>
              </div>
              <div className="bg-blue-50 rounded-lg p-3 text-center">
                <p className="text-gray-600">{t('expectedIncome')}</p>
                <p className="text-xl font-bold text-blue-700">₹{agroPlan.economic_projection.expected_income.toLocaleString()}</p>
              </div>
              <div className="bg-purple-50 rounded-lg p-3 text-center">
                <p className="text-gray-600">{t('roi')}</p>
                <p className="text-xl font-bold text-purple-700">{agroPlan.economic_projection.roi}</p>
              </div>
              <div className="bg-yellow-50 rounded-lg p-3 text-center">
                <p className="text-gray-600">{t('paybackPeriod')}</p>
                <p className="text-xl font-bold text-yellow-700">{agroPlan.economic_projection.payback_period_months} {t('months')}</p>
              </div>
            </div>
            
            {/* Crop Income Breakdown */}
            <div className="mt-4">
              <h4 className="font-medium text-gray-800 mb-2">{t('incomeBreakdown')}</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <h5 className="font-medium text-gray-700 mb-2">{t('cropIncome')}</h5>
                  <ul className="space-y-1">
                    {Object.entries(agroPlan.economic_projection.crop_income).map(([crop, income]) => (
                      <li key={crop} className="flex justify-between text-sm">
                        <span>{crop}:</span>
                        <span className="font-medium">₹{income.toLocaleString()}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h5 className="font-medium text-gray-700 mb-2">{t('treeIncome')}</h5>
                  <ul className="space-y-1">
                    {Object.entries(agroPlan.economic_projection.tree_income).map(([tree, income]) => (
                      <li key={tree} className="flex justify-between text-sm">
                        <span>{tree}:</span>
                        <span className="font-medium">₹{income.toLocaleString()}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
          
          {/* Sustainability Metrics */}
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="text-lg font-medium text-gray-800 mb-3">♻️ {t('sustainabilityMetrics')}</h3>
            <ul className="space-y-2">
              <li className="flex justify-between">
                <span className="text-gray-600">{t('soilHealthIncrease')}:</span>
                <span className="font-medium">{agroPlan.sustainability_metrics.soil_health_increase}</span>
              </li>
              <li className="flex justify-between">
                <span className="text-gray-600">{t('waterSavings')}:</span>
                <span className="font-medium">{agroPlan.sustainability_metrics.water_savings}</span>
              </li>
              <li className="flex justify-between">
                <span className="text-gray-600">{t('carbonSequestration')}:</span>
                <span className="font-medium">{agroPlan.sustainability_metrics.carbon_sequestration_potential}</span>
              </li>
              <li className="flex justify-between">
                <span className="text-gray-600">{t('biodiversityScore')}:</span>
                <span className="font-medium">{agroPlan.sustainability_metrics.biodiversity_score}</span>
              </li>
              <li className="flex justify-between">
                <span className="text-gray-600">{t('climateResilience')}:</span>
                <span className="font-medium">{agroPlan.sustainability_metrics.climate_resilience}</span>
              </li>
            </ul>
          </div>
          
          {/* Next Steps */}
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="text-lg font-medium text-gray-800 mb-3">✅ {t('nextSteps')}</h3>
            <ol className="list-decimal list-inside space-y-2">
              {agroPlan.next_steps.map((step, index) => (
                <li key={index} className="text-gray-700">{step}</li>
              ))}
            </ol>
          </div>
          
          {/* Action Buttons */}
          <div className="flex flex-wrap gap-3 pt-4">
            <button
              onClick={resetForm}
              className="bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-lg transition duration-300"
            >
              {t('generateNewPlan')}
            </button>
            
            <button
              onClick={() => window.print()}
              className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-3 px-6 rounded-lg transition duration-300"
            >
              {t('printPlan')}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIPlanner;