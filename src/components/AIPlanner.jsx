import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import FarmerInputForm from './FarmerInputForm';

const AIPlanner = () => {
  const { t } = useTranslation();
  const [agroPlan, setAgroPlan] = useState(null);
  const [planInputs, setPlanInputs] = useState(null);

  // Handle plan generation from FarmerInputForm
  const handlePlanGenerated = (plan, inputs) => {
    setAgroPlan(plan);
    setPlanInputs(inputs);
  };

  // Reset form to collect new input
  const resetForm = () => {
    setAgroPlan(null);
    setPlanInputs(null);
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">
        🌱 {t('aiDrivenAgroforestryPlanner')}
      </h2>
      
      {!agroPlan ? (
        <FarmerInputForm onPlanGenerated={handlePlanGenerated} />
      ) : (
        <div className="space-y-6">
          {/* Farm Inputs Summary */}
          <div className="border border-gray-200 rounded-lg p-4 bg-green-50">
            <h3 className="text-lg font-medium text-gray-800 mb-3">📋 {t('farmInputsSummary')}</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
              <div>
                <span className="text-gray-600">{t('latitude')}:</span>
                <span className="ml-2 font-medium">{planInputs.latitude}</span>
              </div>
              <div>
                <span className="text-gray-600">{t('longitude')}:</span>
                <span className="ml-2 font-medium">{planInputs.longitude}</span>
              </div>
              <div>
                <span className="text-gray-600">{t('landAreaInAcres')}:</span>
                <span className="ml-2 font-medium">{planInputs.land_area} acres</span>
              </div>
              <div>
                <span className="text-gray-600">{t('budget')}:</span>
                <span className="ml-2 font-medium">₹{planInputs.investment_capacity === 'low' ? '0-50,000' : planInputs.investment_capacity === 'medium' ? '50,000-1,00,000' : '1,00,000+'}</span>
              </div>
            </div>
          </div>
          
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