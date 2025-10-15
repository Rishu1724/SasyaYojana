/**
 * Utility functions for handling agricultural datasets
 */

/**
 * Process NASA POWER dataset
 * @param {Array} data - Raw NASA POWER data
 * @returns {Object} Processed weather data
 */
export const processNASAPowerData = (data) => {
  if (!data || data.length === 0) {
    return null;
  }

  // Assuming data is an array of objects with NASA POWER parameters
  const processed = {
    avg_temperature_c: 0,
    avg_humidity: 0,
    avg_rainfall_mm: 0,
    solar_radiation: 0,
    data_points: data.length
  };

  // Calculate averages
  data.forEach(row => {
    processed.avg_temperature_c += parseFloat(row.T2M) || 0;
    processed.avg_humidity += parseFloat(row.RH2M) || 0;
    // Convert precipitation from kg/m2/s to mm/year
    processed.avg_rainfall_mm += (parseFloat(row.PRECTOTCORR) || 0) * 3650;
    processed.solar_radiation += parseFloat(row.ALLSKY_SFC_SW_DWN) || 0;
  });

  // Calculate averages
  processed.avg_temperature_c = Math.round(processed.avg_temperature_c / data.length);
  processed.avg_humidity = Math.round(processed.avg_humidity / data.length);
  processed.avg_rainfall_mm = Math.round(processed.avg_rainfall_mm / data.length);
  processed.solar_radiation = Math.round(processed.solar_radiation / data.length);

  return processed;
};

/**
 * Process crop price dataset
 * @param {Array} data - Raw crop price data
 * @returns {Object} Processed price data
 */
export const processCropPriceData = (data) => {
  if (!data || data.length === 0) {
    return {};
  }

  const prices = {};

  // Process each row of data
  data.forEach(row => {
    Object.keys(row).forEach(key => {
      // Skip non-price columns (like YEAR, STATE, etc.)
      if (key.toUpperCase().includes('PRICE') || 
          key.toUpperCase().includes('RATE') ||
          (key !== 'YEAR' && key !== 'STATE' && key !== 'DISTRICT' && key !== 'Crop')) {
        const cropName = key.replace('_PRICE', '').replace('_RATE', '').replace('(', '').replace(')', '').toUpperCase();
        const price = parseFloat(row[key]);
        
        if (!isNaN(price)) {
          if (!prices[cropName]) {
            prices[cropName] = { min: price, max: price, sum: 0, count: 0 };
          }
          
          prices[cropName].min = Math.min(prices[cropName].min, price);
          prices[cropName].max = Math.max(prices[cropName].max, price);
          prices[cropName].sum += price;
          prices[cropName].count += 1;
        }
      }
    });
  });

  // Calculate averages
  Object.keys(prices).forEach(crop => {
    prices[crop].avg = Math.round(prices[crop].sum / prices[crop].count);
    delete prices[crop].sum;
    delete prices[crop].count;
  });

  return prices;
};

/**
 * Process crop yield dataset
 * @param {Array} data - Raw crop yield data
 * @returns {Object} Processed yield data
 */
export const processCropYieldData = (data) => {
  if (!data || data.length === 0) {
    return {};
  }

  const yields = {};

  // Process each row of data
  data.forEach(row => {
    Object.keys(row).forEach(key => {
      // Handle the specific column names in your dataset
      if (key.includes('Yield') || key.includes('yield') || 
          (key !== 'YEAR' && key !== 'STATE' && key !== 'DISTRICT' && key !== 'Crop')) {
        // Extract crop name from column header or use row data if structured differently
        const cropName = key.replace('Yield', '').replace('yield', '').trim() || (row['Crop'] || 'UNKNOWN').toUpperCase();
        const yieldValue = parseFloat(row[key]);
        
        if (!isNaN(yieldValue)) {
          if (!yields[cropName]) {
            yields[cropName] = { min: yieldValue, max: yieldValue, sum: 0, count: 0 };
          }
          
          yields[cropName].min = Math.min(yields[cropName].min, yieldValue);
          yields[cropName].max = Math.max(yields[cropName].max, yieldValue);
          yields[cropName].sum += yieldValue;
          yields[cropName].count += 1;
        }
      }
    });
  });

  // Calculate averages
  Object.keys(yields).forEach(crop => {
    yields[crop].avg = Math.round(yields[crop].sum / yields[crop].count);
    delete yields[crop].sum;
    delete yields[crop].count;
  });

  return yields;
};

/**
 * Process crop area dataset
 * @param {Array} data - Raw crop area data
 * @returns {Object} Processed area data
 */
export const processCropAreaData = (data) => {
  if (!data || data.length === 0) {
    return {};
  }

  const areas = {};

  // Process each row of data
  data.forEach(row => {
    Object.keys(row).forEach(key => {
      // Handle the specific column names in your dataset
      if (key.includes('Area') || key.includes('area') || key.includes('AREA') ||
          (key !== 'YEAR' && key !== 'STATE' && key !== 'DISTRICT' && key !== 'Crop')) {
        // Extract crop name from column header or use row data if structured differently
        const cropName = key.replace('Area', '').replace('area', '').replace('AREA', '').trim() || (row['Crop'] || 'UNKNOWN').toUpperCase();
        const areaValue = parseFloat(row[key]);
        
        if (!isNaN(areaValue)) {
          if (!areas[cropName]) {
            areas[cropName] = { min: areaValue, max: areaValue, sum: 0, count: 0 };
          }
          
          areas[cropName].min = Math.min(areas[cropName].min, areaValue);
          areas[cropName].max = Math.max(areas[cropName].max, areaValue);
          areas[cropName].sum += areaValue;
          areas[cropName].count += 1;
        }
      }
    });
  });

  // Calculate averages
  Object.keys(areas).forEach(crop => {
    areas[crop].avg = Math.round(areas[crop].sum / areas[crop].count);
    delete areas[crop].sum;
    delete areas[crop].count;
  });

  return areas;
};

/**
 * Process production dataset
 * @param {Array} data - Raw production data
 * @returns {Object} Processed production data
 */
export const processProductionData = (data) => {
  if (!data || data.length === 0) {
    return {};
  }

  const production = {};

  // Process each row of data
  data.forEach(row => {
    Object.keys(row).forEach(key => {
      // Handle the specific column names in your dataset
      if (key.includes('Production') || key.includes('production') || key.includes('PRODUCTION') ||
          (key !== 'YEAR' && key !== 'STATE' && key !== 'DISTRICT' && key !== 'Crop')) {
        // Extract crop name from column header or use row data if structured differently
        const cropName = key.replace('Production', '').replace('production', '').replace('PRODUCTION', '').trim() || (row['Crop'] || 'UNKNOWN').toUpperCase();
        const productionValue = parseFloat(row[key]);
        
        if (!isNaN(productionValue)) {
          if (!production[cropName]) {
            production[cropName] = { min: productionValue, max: productionValue, sum: 0, count: 0 };
          }
          
          production[cropName].min = Math.min(production[cropName].min, productionValue);
          production[cropName].max = Math.max(production[cropName].max, productionValue);
          production[cropName].sum += productionValue;
          production[cropName].count += 1;
        }
      }
    });
  });

  // Calculate averages
  Object.keys(production).forEach(crop => {
    production[crop].avg = Math.round(production[crop].sum / production[crop].count);
    delete production[crop].sum;
    delete production[crop].count;
  });

  return production;
};

/**
 * Process damage data from natural disasters
 * @param {Array} data - Raw damage data
 * @returns {Object} Processed damage data
 */
export const processDamageData = (data) => {
  if (!data || data.length === 0) {
    return {};
  }

  const damage = {
    total_flood_damage: 0,
    total_cyclone_damage: 0,
    total_landslide_damage: 0,
    years: []
  };

  // Process each row of data
  data.forEach(row => {
    // Add year to tracking
    if (row['Year'] && !damage.years.includes(row['Year'])) {
      damage.years.push(row['Year']);
    }
    
    // Sum up different types of damage
    damage.total_flood_damage += parseFloat(row['Flood']) || 0;
    damage.total_cyclone_damage += parseFloat(row['Cyclone']) || 0;
    damage.total_landslide_damage += parseFloat(row['Landslide']) || 0;
  });

  return damage;
};

/**
 * Combine all datasets into features for ML models
 * @param {Object} nasaData - Processed NASA POWER data
 * @param {Object} priceData - Processed crop price data
 * @param {Object} yieldData - Processed crop yield data
 * @param {Object} areaData - Processed crop area data
 * @param {Object} productionData - Processed production data
 * @param {Object} damageData - Processed damage data
 * @returns {Object} Combined features
 */
export const createFeatures = (nasaData, priceData, yieldData, areaData, productionData, damageData) => {
  const features = {};

  // Add weather features
  if (nasaData) {
    features.avg_temperature = nasaData.avg_temperature_c || 0;
    features.avg_humidity = nasaData.avg_humidity || 0;
    features.rainfall = nasaData.avg_rainfall_mm || 0;
    features.solar_radiation = nasaData.solar_radiation || 0;
  }

  // Add price features (top 5 crops by average price)
  if (priceData) {
    const sortedCrops = Object.keys(priceData)
      .map(crop => ({ name: crop, avg: priceData[crop].avg }))
      .sort((a, b) => b.avg - a.avg)
      .slice(0, 5);

    sortedCrops.forEach((crop, index) => {
      features[`price_${index}_${crop.name}`] = crop.avg;
    });
  }

  // Add yield features (top 5 crops by average yield)
  if (yieldData) {
    const sortedCrops = Object.keys(yieldData)
      .map(crop => ({ name: crop, avg: yieldData[crop].avg }))
      .sort((a, b) => b.avg - a.avg)
      .slice(0, 5);

    sortedCrops.forEach((crop, index) => {
      features[`yield_${index}_${crop.name}`] = crop.avg;
    });
  }

  // Add area features (top 5 crops by average area)
  if (areaData) {
    const sortedCrops = Object.keys(areaData)
      .map(crop => ({ name: crop, avg: areaData[crop].avg }))
      .sort((a, b) => b.avg - a.avg)
      .slice(0, 5);

    sortedCrops.forEach((crop, index) => {
      features[`area_${index}_${crop.name}`] = crop.avg;
    });
  }

  // Add production features (top 5 crops by average production)
  if (productionData) {
    const sortedCrops = Object.keys(productionData)
      .map(crop => ({ name: crop, avg: productionData[crop].avg }))
      .sort((a, b) => b.avg - a.avg)
      .slice(0, 5);

    sortedCrops.forEach((crop, index) => {
      features[`production_${index}_${crop.name}`] = crop.avg;
    });
  }

  // Add damage features
  if (damageData) {
    features.total_flood_damage = damageData.total_flood_damage || 0;
    features.total_cyclone_damage = damageData.total_cyclone_damage || 0;
    features.total_landslide_damage = damageData.total_landslide_damage || 0;
    features.years_of_data = damageData.years ? damageData.years.length : 0;
  }

  return features;
};

export default {
  processNASAPowerData,
  processCropPriceData,
  processCropYieldData,
  processCropAreaData,
  processProductionData,
  processDamageData,
  createFeatures
};