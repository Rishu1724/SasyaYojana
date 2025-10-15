import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import agroIntelService from '../services/agroIntelService';

const FarmerInputForm = ({ onPlanGenerated }) => {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    location: {
      type: 'gps', // 'gps' or 'village'
      gps: { lat: '', lng: '' },
      village: ''
    },
    land_area: '',
    budget: '',
    crop_preference: '',
    investment_capacity: 'medium'
  });
  const [currentLocation, setCurrentLocation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Get user's current location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setCurrentLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
        },
        (error) => {
          console.log('Geolocation not available or denied');
        }
      );
    }
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    
    if (name === 'location_type') {
      setFormData(prev => ({
        ...prev,
        location: {
          ...prev.location,
          type: value
        }
      }));
    } else if (name === 'lat' || name === 'lng') {
      setFormData(prev => ({
        ...prev,
        location: {
          ...prev.location,
          gps: {
            ...prev.location.gps,
            [name]: value
          }
        }
      }));
    } else if (name === 'village') {
      setFormData(prev => ({
        ...prev,
        location: {
          ...prev.location,
          village: value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleUseCurrentLocation = () => {
    if (currentLocation) {
      setFormData(prev => ({
        ...prev,
        location: {
          ...prev.location,
          gps: {
            lat: currentLocation.lat.toString(),
            lng: currentLocation.lng.toString()
          }
        }
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      // Validate inputs
      if (!formData.land_area || !formData.budget) {
        throw new Error(t('pleaseFillRequiredFields'));
      }
      
      // Parse location data
      let lat, lng;
      if (formData.location.type === 'gps') {
        if (!formData.location.gps.lat || !formData.location.gps.lng) {
          throw new Error(t('pleaseEnterValidCoordinates'));
        }
        lat = parseFloat(formData.location.gps.lat);
        lng = parseFloat(formData.location.gps.lng);
        if (isNaN(lat) || isNaN(lng)) {
          throw new Error(t('pleaseEnterValidCoordinates'));
        }
      } else {
        // For village, we would need to geocode it
        // For now, we'll use a default location
        lat = 20.5937; // Default India coordinates
        lng = 78.9629;
        console.log('Village geocoding not implemented, using default location');
      }
      
      // Parse land area and budget
      const landArea = parseFloat(formData.land_area);
      const budget = parseFloat(formData.budget);
      
      if (isNaN(landArea) || isNaN(budget)) {
        throw new Error(t('pleaseEnterValidNumbers'));
      }
      
      // Determine investment capacity based on budget
      let investmentCapacity = 'low';
      if (budget > 100000) {
        investmentCapacity = 'high';
      } else if (budget > 50000) {
        investmentCapacity = 'medium';
      }
      
      // Fetch soil and weather data
      const soilData = await agroIntelService.fetchSoilData(lat, lng);
      const weatherData = await agroIntelService.fetchWeatherData(lat, lng);
      
      // Prepare inputs for AI model
      const inputs = {
        latitude: lat,
        longitude: lng,
        soil_pH: soilData.ph,
        organic_carbon: soilData.organic_carbon,
        nitrogen: soilData.nitrogen,
        cec: soilData.cec,
        sand: soilData.sand,
        silt: soilData.silt,
        clay: soilData.clay,
        avg_rainfall_mm: weatherData.avg_rainfall_mm,
        avg_temperature_c: weatherData.avg_temperature_c,
        solar_radiation: weatherData.solar_radiation,
        land_area: landArea,
        investment_capacity: investmentCapacity,
        crop_preference: formData.crop_preference || null
      };
      
      // Generate agroforestry plan
      const plan = await agroIntelService.generateAgroforestryPlan(inputs);
      
      // Pass the plan to the parent component
      onPlanGenerated(plan, inputs);
    } catch (err) {
      console.error('Error generating plan:', err);
      setError(err.message || t('failedToGeneratePlan'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">
        🌱 {t('farmerInputForm')}
      </h2>
      
      {error && (
        <div className="bg-red-50 text-red-700 p-3 rounded-lg mb-4">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Location Input */}
        <div className="border border-gray-200 rounded-lg p-4">
          <h3 className="text-lg font-medium text-gray-800 mb-3">
            📍 {t('location')}
          </h3>
          
          <div className="space-y-4">
            <div className="flex space-x-4">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="location_type"
                  value="gps"
                  checked={formData.location.type === 'gps'}
                  onChange={handleInputChange}
                  className="mr-2"
                />
                <span>{t('useGPS')}</span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="location_type"
                  value="village"
                  checked={formData.location.type === 'village'}
                  onChange={handleInputChange}
                  className="mr-2"
                />
                <span>{t('enterVillage')}</span>
              </label>
            </div>
            
            {formData.location.type === 'gps' ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-gray-700 mb-2 font-medium">
                    {t('latitude')}
                  </label>
                  <div className="flex">
                    <input
                      type="text"
                      name="lat"
                      value={formData.location.gps.lat}
                      onChange={handleInputChange}
                      placeholder={t('enterLatitude')}
                      className="flex-1 px-4 py-2 border border-gray-300 rounded-l-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    />
                    {currentLocation && (
                      <button
                        type="button"
                        onClick={handleUseCurrentLocation}
                        className="bg-green-600 hover:bg-green-700 text-white px-3 rounded-r-lg"
                        title={t('useCurrentLocation')}
                      >
                        📍
                      </button>
                    )}
                  </div>
                </div>
                
                <div>
                  <label className="block text-gray-700 mb-2 font-medium">
                    {t('longitude')}
                  </label>
                  <input
                    type="text"
                    name="lng"
                    value={formData.location.gps.lng}
                    onChange={handleInputChange}
                    placeholder={t('enterLongitude')}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  />
                </div>
              </div>
            ) : (
              <div>
                <label className="block text-gray-700 mb-2 font-medium">
                  {t('villageName')}
                </label>
                <input
                  type="text"
                  name="village"
                  value={formData.location.village}
                  onChange={handleInputChange}
                  placeholder={t('enterVillageName')}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                />
                <p className="text-sm text-gray-500 mt-1">
                  {t('noteVillageLocation')}
                </p>
              </div>
            )}
          </div>
        </div>
        
        {/* Farm Details */}
        <div className="border border-gray-200 rounded-lg p-4">
          <h3 className="text-lg font-medium text-gray-800 mb-3">
            🏡 {t('farmDetails')}
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-gray-700 mb-2 font-medium">
                {t('landAreaInAcres')} <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="land_area"
                value={formData.land_area}
                onChange={handleInputChange}
                placeholder={t('enterLandArea')}
                step="0.1"
                min="0.1"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-gray-700 mb-2 font-medium">
                {t('budgetInRupees')} <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="budget"
                value={formData.budget}
                onChange={handleInputChange}
                placeholder={t('enterBudget')}
                min="0"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                required
              />
            </div>
          </div>
        </div>
        
        {/* Preferences */}
        <div className="border border-gray-200 rounded-lg p-4">
          <h3 className="text-lg font-medium text-gray-800 mb-3">
            ⚙️ {t('preferences')}
          </h3>
          
          <div>
            <label className="block text-gray-700 mb-2 font-medium">
              {t('cropPreference')} ({t('optional')})
            </label>
            <input
              type="text"
              name="crop_preference"
              value={formData.crop_preference}
              onChange={handleInputChange}
              placeholder={t('enterCropPreference')}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
            />
            <p className="text-sm text-gray-500 mt-1">
              {t('cropPreferenceNote')}
            </p>
          </div>
        </div>
        
        {/* Action Buttons */}
        <div className="flex flex-wrap gap-3 pt-4">
          <button
            type="submit"
            disabled={loading}
            className={`bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-lg transition duration-300 ${loading ? 'opacity-75 cursor-not-allowed' : ''}`}
          >
            {loading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {t('generatingPlan')}
              </span>
            ) : (
              t('generateAgroforestryPlan')
            )}
          </button>
          
          <button
            type="button"
            onClick={() => setFormData({
              location: {
                type: 'gps',
                gps: { lat: '', lng: '' },
                village: ''
              },
              land_area: '',
              budget: '',
              crop_preference: '',
              investment_capacity: 'medium'
            })}
            className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-3 px-6 rounded-lg transition duration-300"
          >
            {t('reset')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default FarmerInputForm;