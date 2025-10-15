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
          { name: t('mangoTrees'), spacing: '10m x 10m', benefits: t('fruitProductionShadeIncome') },
          { name: t('guavaTrees'), spacing: '8m x 8m', benefits: t('fruitProductionEarlyReturns') }
        ],
        understory: [
          { name: t('leucaena'), spacing: '2m x 2m', benefits: t('nitrogenFixationFodderBiomass') },
          { name: t('gliricidia'), spacing: '3m x 3m', benefits: t('nitrogenFixationLiveFencingFodder') }
        ],
        shrubs: [
          { name: t('turmeric'), spacing: t('interplantWithTrees'), benefits: t('highValueSpiceShadeTolerant') },
          { name: t('ginger'), spacing: t('interplantWithTrees'), benefits: t('highValueSpiceMoistureRetention') }
        ],
        ground: [
          { name: t('blackGram'), spacing: t('rowPlanting'), benefits: t('nitrogenFixationShortDuration') },
          { name: t('pigeonPea'), spacing: t('betweenTreeRows'), benefits: t('proteinSourceDroughtTolerant') }
        ]
      },
      medium: {
        canopy: [
          { name: t('tamarindTrees'), spacing: '12m x 12m', benefits: t('fruitProductionLongTermInvestment') },
          { name: t('jackfruitTrees'), spacing: '10m x 10m', benefits: t('highValueFruitClimateResilience') }
        ],
        understory: [
          { name: t('acaciaNilotica'), spacing: '3m x 3m', benefits: t('nitrogenFixationGumProduction') },
          { name: t('casuarina'), spacing: '4m x 4m', benefits: t('windbreakTimberNitrogenFixation') }
        ],
        shrubs: [
          { name: t('coffee'), spacing: t('shadedAreasUnderTrees'), benefits: t('highValueCashCropShadeRequirement') },
          { name: t('pepper'), spacing: t('supportedOnTreeTrunks'), benefits: t('climbingVineHighValueSpice') }
        ],
        ground: [
          { name: t('maize'), spacing: t('rowPlanting'), benefits: t('stapleFoodCropGoodGroundCover') },
          { name: t('cowpea'), spacing: t('interrowPlanting'), benefits: t('proteinSourceNitrogenFixation') }
        ]
      },
      large: {
        canopy: [
          { name: t('teakTrees'), spacing: '8m x 8m', benefits: t('highValueTimberLongTermInvestment') },
          { name: t('neemTrees'), spacing: '10m x 10m', benefits: t('timberMedicinalPestControl') }
        ],
        understory: [
          { name: t('albizia'), spacing: '4m x 4m', benefits: t('nitrogenFixationTimberShade') },
          { name: t('sesbania'), spacing: '2m x 2m', benefits: t('greenManureFodderNitrogenFixation') }
        ],
        shrubs: [
          { name: t('medicinalPlants'), spacing: t('dedicatedPlots'), benefits: t('diverseIncomeTraditionalMedicine') },
          { name: t('aromaticHerbs'), spacing: t('borderPlantings'), benefits: t('essentialOilsPestRepellent') }
        ],
        ground: [
          { name: t('sorghum'), spacing: t('rowPlanting'), benefits: t('droughtTolerantFodderAndGrain') },
          { name: t('groundnut'), spacing: t('interrowPlanting'), benefits: t('oilseedCropNitrogenFixation') }
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
            name: t('maizeCowpea'),
            benefits: t('complementaryGrowthNitrogenFixationDiversifiedIncome'),
            layout: t('alternateRows'),
            season: t('kharif')
          },
          {
            name: t('wheatChickpea'),
            benefits: t('differentRootZonesNitrogenFixationCoolSeasonCombination'),
            layout: t('stripIntercropping'),
            season: t('rabi')
          }
        ]
      },
      medium: {
        combinations: [
          {
            name: t('sorghumPigeonPea'),
            benefits: t('droughtToleranceComplementaryHeightProteinCarbohydrate'),
            layout: t('rowIntercropping'),
            season: t('kharif')
          },
          {
            name: t('mustardLentil'),
            benefits: t('oilseedPulseCombinationDifferentNutrientRequirements'),
            layout: t('mixedIntercropping'),
            season: t('rabi')
          }
        ]
      },
      large: {
        combinations: [
          {
            name: t('cottonSoybean'),
            benefits: t('fiberProteinPestManagementMechanizationCompatible'),
            layout: t('stripIntercropping'),
            season: t('kharif')
          },
          {
            name: t('barleyFieldPea'),
            benefits: t('cerealPulseEarlyHarvestSoilImprovement'),
            layout: t('alternateRow'),
            season: t('rabi')
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
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">{t('agroforestryMultiCroppingPlanner')}</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div>
          <label className="block text-gray-700 mb-2 font-medium">{t('farmSize')}</label>
          <select 
            value={selectedFarmType}
            onChange={(e) => setSelectedFarmType(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="small">{t('small052Acres')}</option>
            <option value="medium">{t('medium25Acres')}</option>
            <option value="large">{t('large5Acres')}</option>
          </select>
        </div>
        
        <div>
          <label className="block text-gray-700 mb-2 font-medium">{t('soilType')}</label>
          <select 
            value={soilType}
            onChange={(e) => setSoilType(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="sandy">{t('sandy')}</option>
            <option value="loamy">{t('loamy')}</option>
            <option value="clay">{t('clay')}</option>
            <option value="silty">{t('silty')}</option>
          </select>
        </div>
        
        <div>
          <label className="block text-gray-700 mb-2 font-medium">{t('rainfall')}</label>
          <select 
            value={rainfall}
            onChange={(e) => setRainfall(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="low">{t('lowRainfall')}</option>
            <option value="moderate">{t('moderateRainfall')}</option>
            <option value="high">{t('highRainfall')}</option>
          </select>
        </div>
      </div>
      
      {agroforestryPlan && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">{t('agroforestryLayerPlan')}</h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-800 mb-3 flex items-center">
                <span className="w-3 h-3 bg-green-600 rounded-full mr-2"></span>
                {t('canopyTrees')}
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
                {t('understoryTrees')}
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
                {t('shrubs')}
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
                {t('groundCrops')}
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
          <h3 className="text-xl font-semibold text-gray-800 mb-4">{t('multiCroppingCombinations')}</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {multiCroppingPlan.combinations.map((combination, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <h4 className="font-medium text-gray-800 mb-2">{combination.name}</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">{t('benefits')}:</span>
                    <span className="text-gray-800 text-right">{combination.benefits}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">{t('layout')}:</span>
                    <span className="text-gray-800">{combination.layout}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">{t('season')}:</span>
                    <span className="text-gray-800">{combination.season}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      <div className="mt-8 p-4 bg-green-50 rounded-lg">
        <h4 className="font-medium text-green-800 mb-2">{t('benefitsOfAgroforestryMultiCropping')}</h4>
        <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-green-700">
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>{t('improvesSoilFertilityReducesErosion')}</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>{t('providesShadeMicroclimateRegulation')}</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>{t('producesDiverseFruitsNutsTimberCrops')}</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>{t('enhancesBiodiversityBeneficialInsects')}</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>{t('reducesPestRisksIncreasesYieldStability')}</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>{t('ensuresStableIncomeThroughDiversification')}</span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default AgroforestryPlanner;