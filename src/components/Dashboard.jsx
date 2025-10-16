import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { auth } from '../firebase';
import { signOut } from 'firebase/auth';
import { GoogleMap, LoadScript, Marker, Polygon } from '@react-google-maps/api';
import AgroforestryPlanner from './AgroforestryPlanner';
import AIPlanner from './AIPlanner';
import agroIntelService from '../services/agroIntelService';
import FeedbackForm from './FeedbackForm';
import mapStorageService from '../services/mapStorageService';
import { generateLandLayoutMap } from '../utils/api';

// Map container style
const mapContainerStyle = {
  width: '100%',
  height: '400px'
};

// Default center (fallback if geolocation fails)
const defaultCenter = { lat: 20.5937, lng: 78.9629 };

// Example farm polygon (replace with dynamic farmer input later)
const farmPolygon = [
  { lat: 20.60, lng: 78.95 },
  { lat: 20.61, lng: 78.95 },
  { lat: 20.61, lng: 78.97 },
  { lat: 20.60, lng: 78.97 }
];

const Dashboard = () => {
  const { t, i18n } = useTranslation();
  const [center, setCenter] = useState(defaultCenter);
  const [weather, setWeather] = useState(null);
  const [soilData, setSoilData] = useState(null);
  const [rainfallData, setRainfallData] = useState(null);
  const [investmentCapacity, setInvestmentCapacity] = useState(null);
  const [aiRecommendations, setAiRecommendations] = useState(null);
  const [realTimePredictions, setRealTimePredictions] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [currentPredictionId, setCurrentPredictionId] = useState(null);
  const [mapId, setMapId] = useState(null);

  // Get user location using browser geolocation
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const userCenter = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          setCenter(userCenter);

          // Fetch weather for user location
          fetchWeather(userCenter.lat, userCenter.lng);
          
          // Fetch real-time predictions
          fetchRealTimePredictions(userCenter.lat, userCenter.lng);
        },
        (error) => {
          console.error('Error getting location:', error);
          // Fetch weather for default location if geolocation fails
          fetchWeather(defaultCenter.lat, defaultCenter.lng);
          fetchRealTimePredictions(defaultCenter.lat, defaultCenter.lng);
        }
      );
    } else {
      // Fetch weather for default location if geolocation not supported
      fetchWeather(defaultCenter.lat, defaultCenter.lng);
      fetchRealTimePredictions(defaultCenter.lat, defaultCenter.lng);
    }
  }, []);

  const fetchWeather = async (lat, lon) => {
    try {
      // Check if API key is available
      const apiKey = import.meta.env.VITE_WEATHER_API_KEY;
      if (!apiKey) {
        console.warn('Weather API key not found');
        // Set mock data if API key is missing
        setWeather({
          temp: 28,
          humidity: 65,
          description: 'Clear Sky',
          pressure: 1013,
          windSpeed: 5
        });
        return;
      }

      const response = await axios.get(
        `https://api.openweathermap.org/data/2.5/weather`,
        {
          params: {
            lat: lat,
            lon: lon,
            units: 'metric',
            appid: apiKey
          }
        }
      );
      const data = response.data;
      setWeather({
        temp: data.main.temp,
        humidity: data.main.humidity,
        description: data.weather[0].description,
        pressure: data.main.pressure,
        windSpeed: data.wind.speed
      });
    } catch (error) {
      console.error('Error fetching weather:', error);
      // Set mock data on error
      setWeather({
        temp: 28,
        humidity: 65,
        description: 'Clear Sky',
        pressure: 1013,
        windSpeed: 5
      });
    }
  };

  const fetchRealTimePredictions = async (lat, lon) => {
    try {
      // Prepare farmer data for prediction
      const farmerData = {
        location: { lat, lng: lon },
        land_area_acres: 2.5, // Default value, would be dynamic in real app
        soil: {
          ph: 6.8,
          organic_carbon: 1.2,
          nitrogen: 150,
          phosphorus: 30,
          potassium: 150
        },
        budget_inr: 50000 // Default value, would be dynamic in real app
      };
      
      // Fetch real-time predictions from our ML models
      const predictions = await agroIntelService.fetchRealTimePredictions(farmerData);
      setRealTimePredictions(predictions);
      
      // Store the prediction ID for feedback
      if (predictions && predictions.prediction_id) {
        setCurrentPredictionId(predictions.prediction_id);
      }
    } catch (error) {
      console.error('Error fetching real-time predictions:', error);
      // Set mock data on error
      setRealTimePredictions({
        prediction_id: 'mock-prediction-id',
        predictions: {
          yield_kg_per_acre: 3000,
          confidence: 0.85,
          roi: 2.8,
          payback_period: 18
        },
        recommendations: {
          best_crop: 'Maize',
          planting_time: 'June-July',
          irrigation_needs: 'Moderate'
        },
        weather_data: {
          avg_temperature_c: 28,
          avg_humidity: 65,
          avg_rainfall_mm: 980,
          solar_radiation: 5.5
        },
        costs: {
          seeds_and_saplings: 8000,
          fertilizers: 12000,
          labor: 15000
        }
      });
    }
  };

  // Mock data for soil, rainfall, and investment capacity
  useEffect(() => {
    try {
      // Mock soil data
      setSoilData({
        pH: 6.8,
        texture: 'Loamy',
        organicCarbon: '1.2%',
        bulkDensity: '1.3 g/cm³',
        nitrogen: '25 kg/ha',
        phosphorus: '15 kg/ha',
        potassium: '30 kg/ha'
      });

      // Mock rainfall data
      setRainfallData({
        annual: '950 mm',
        seasonal: 'Monsoon: 750 mm, Winter: 150 mm, Summer: 50 mm',
        soilWetness: 'Moderate'
      });

      // Mock investment capacity
      setInvestmentCapacity({
        category: 'Medium',
        budget: '₹50,000 - ₹1,00,000',
        riskTolerance: 'Moderate'
      });

      // Mock AI recommendations
      setAiRecommendations({
        cropRotation: [
          { season: 'Kharif', crop: 'Rice', reason: 'High rainfall season' },
          { season: 'Rabi', crop: 'Wheat', reason: 'Cooler temperatures' },
          { season: 'Summer', crop: 'Moong Dal', reason: 'Drought-resistant legume' }
        ],
        soilManagement: [
          'Add organic compost to improve soil fertility',
          'Practice crop rotation to maintain soil health',
          'Use natural pest control methods'
        ],
        irrigation: [
          'Install drip irrigation for water efficiency',
          'Collect rainwater during monsoon season',
          'Schedule irrigation based on soil moisture levels'
        ],
        economicForecast: {
          expectedYield: 'Rice: 4 tons/ha, Wheat: 3.5 tons/ha',
          inputCost: '₹25,000/ha',
          expectedProfit: '₹45,000/ha'
        }
      });
    } catch (error) {
      console.error('Error setting mock data:', error);
    }
  }, []);

  const handleLogout = async () => {
    try {
      await signOut(auth);
      console.log('User logged out successfully');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  const languages = [
    { code: 'en', label: 'English' },
    { code: 'hi', label: 'हिंदी' },
    { code: 'mr', label: 'मराठी' },
    { code: 'te', label: 'తెలుగు' },
    { code: 'kn', label: 'ಕನ್ನಡ' },
  ];

  const generateLandLayoutMap = async () => {
    try {
      // Prepare data for map generation
      const mapData = {
        center_lat: center.lat,
        center_lon: center.lng,
        land_area_acres: 2.5,
        location: "Farmer Location",
        soil_data: {
          ph: soilData ? soilData.pH : 6.8,
          organic_carbon: soilData ? parseFloat(soilData.organicCarbon) : 1.2,
          nitrogen: soilData ? parseFloat(soilData.nitrogen) : 150,
          phosphorus: soilData ? parseFloat(soilData.phosphorus) : 30,
          potassium: soilData ? parseFloat(soilData.potassium) : 150,
          texture: soilData ? soilData.texture : 'Loam',
          drainage: 'Moderate'
        },
        weather_data: {
          rainfall_mm: weather ? weather.rainfall_mm : 980,
          temperature_c: weather ? weather.temp : 28,
          humidity: weather ? weather.humidity : 65,
          solar_radiation: 5.5
        },
        economic_data: {
          budget_inr: 50000,
          labor_availability: 'Medium',
          input_cost_type: 'Organic'
        }
      };

      // Call the map API to generate the layout using the new utility
      const response = await generateLandLayoutMap(mapData);
      
      if (response.success) {
        console.log('Land layout map generated successfully');
        
        // Store map data in Firebase
        try {
          const mapStorageData = {
            center_lat: mapData.center_lat,
            center_lon: mapData.center_lon,
            land_area_acres: mapData.land_area_acres,
            location: mapData.location,
            soil_data: mapData.soil_data,
            weather_data: mapData.weather_data,
            economic_data: mapData.economic_data,
            recommendation: response.recommendation,
            created_at: new Date(),
            user_id: auth.currentUser ? auth.currentUser.uid : null
          };
        
          // Store in Firebase
          const storedMap = await mapStorageService.storeMap(mapStorageData, response.map_file_path);
          setMapId(storedMap.id);
          console.log('Map stored in Firebase with ID:', storedMap.id);
        } catch (storageError) {
          console.error('Error storing map in Firebase:', storageError);
        }
        
        // Refresh the iframe to show the new map
        const iframe = document.querySelector('iframe[title="AI Land Layout Map"]');
        if (iframe) {
          // Use the map URL from the response if available, otherwise refresh the iframe
          if (response.map_url) {
            iframe.src = response.map_url;
          } else {
            // Fallback to local file
            iframe.src = `/api/get-map/${encodeURIComponent(response.map_file_path.split('/').pop())}`;
          }
        }
      } else {
        console.error('Failed to generate land layout map:', response.message);
      }
    } catch (error) {
      console.error('Error generating land layout map:', error);
    }
  };

  return (
    <div className="min-h-screen bg-green-50 p-4">
      <header className="w-full max-w-6xl mx-auto mb-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 py-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-green-800">
              {t('dashboard')}
            </h1>
            <p className="text-green-600">{t('aiDrivenAgriculturalAssistant')}</p>
          </div>
          <div className="flex flex-col sm:flex-row gap-2">
            <div className="flex flex-wrap gap-1">
              {languages.map((lang) => (
                <button
                  key={lang.code}
                  onClick={() => changeLanguage(lang.code)}
                  className={`px-2 py-1 text-xs rounded ${
                    i18n.language === lang.code
                      ? 'bg-green-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {lang.label}
                </button>
              ))}
            </div>
            <button 
              onClick={handleLogout}
              className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition duration-300"
            >
              Logout
            </button>
          </div>
        </div>
      </header>
      
      {/* Tab Navigation */}
      <div className="w-full max-w-6xl mx-auto mb-6">
        <div className="flex flex-wrap gap-2 bg-white rounded-xl shadow-md p-2">
          <button 
            onClick={() => setActiveTab('overview')}
            className={`px-4 py-2 rounded-lg transition duration-300 ${activeTab === 'overview' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-green-100'}`}
          >
            {t('overview')}
          </button>
          <button 
            onClick={() => setActiveTab('aiplanner')}
            className={`px-4 py-2 rounded-lg transition duration-300 ${activeTab === 'aiplanner' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-green-100'}`}
          >
            {t('aiPlanner')}
          </button>
          <button 
            onClick={() => setActiveTab('agroforestry')}
            className={`px-4 py-2 rounded-lg transition duration-300 ${activeTab === 'agroforestry' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-green-100'}`}
          >
            {t('agroforestry')}
          </button>
          <button 
            onClick={() => setActiveTab('soil')}
            className={`px-4 py-2 rounded-lg transition duration-300 ${activeTab === 'soil' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-green-100'}`}
          >
            {t('soilAnalysis')}
          </button>
          <button 
            onClick={() => setActiveTab('weather')}
            className={`px-4 py-2 rounded-lg transition duration-300 ${activeTab === 'weather' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-green-100'}`}
          >
            {t('weatherRainfall')}
          </button>
          <button 
            onClick={() => setActiveTab('map')}
            className={`px-4 py-2 rounded-lg transition duration-300 ${activeTab === 'map' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-green-100'}`}
          >
            {t('farmMap')}
          </button>
          <button 
            onClick={() => setActiveTab('predictions')}
            className={`px-4 py-2 rounded-lg transition duration-300 ${activeTab === 'predictions' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-green-100'}`}
          >
            {t('predictions')}
          </button>
        </div>
      </div>
      
      <main className="w-full max-w-6xl mx-auto">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-xl shadow-md p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-green-100 rounded-lg mr-4">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-gray-500 text-sm">{t('farmArea')}</p>
                    <p className="text-xl font-semibold">2.5 acres</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-xl shadow-md p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-blue-100 rounded-lg mr-4">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4 4 0 003 15z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-gray-500 text-sm">{t('currentWeather')}</p>
                    <p className="text-xl font-semibold">
                      {weather ? `${weather.temp}°C` : 'Loading...'}
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-xl shadow-md p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-yellow-100 rounded-lg mr-4">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-gray-500 text-sm">{t('investmentCapacity')}</p>
                    <p className="text-xl font-semibold">
                      {investmentCapacity ? investmentCapacity.category : 'Loading...'}
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-xl shadow-md p-6">
                <div className="flex items-center">
                  <div className="p-3 bg-purple-100 rounded-lg mr-4">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-gray-500 text-sm">{t('expectedProfit')}</p>
                    <p className="text-xl font-semibold">
                      {aiRecommendations ? '₹45,000/ha' : 'Loading...'}
                    </p>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 bg-white rounded-xl shadow-md p-6">
                <h2 className="text-xl font-semibold text-gray-800 mb-4">{t('aiCropRecommendations')}</h2>
                {aiRecommendations ? (
                  <div className="space-y-4">
                    {aiRecommendations.cropRotation.map((recommendation, index) => (
                      <div key={index} className="flex items-start border-b border-gray-100 pb-4 last:border-0 last:pb-0">
                        <div className="bg-green-100 text-green-800 rounded-full w-8 h-8 flex items-center justify-center mr-3 mt-1 flex-shrink-0">
                          {index + 1}
                        </div>
                        <div>
                          <h3 className="font-medium text-gray-800">{recommendation.season}: {recommendation.crop}</h3>
                          <p className="text-gray-600 text-sm">{recommendation.reason}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">{t('loadingRecommendations')}</p>
                )}
              </div>
              
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-xl font-semibold text-gray-800 mb-4">{t('quickActions')}</h2>
                <div className="space-y-3">
                  <button 
                    onClick={() => setActiveTab('aiplanner')}
                    className="w-full text-left p-3 rounded-lg bg-green-50 hover:bg-green-100 transition duration-300"
                  >
                    <div className="font-medium text-green-800">{t('generateAIPlan')}</div>
                    <div className="text-gray-600 text-sm">{t('createLandUsePlan')}</div>
                  </button>
                  <button 
                    onClick={() => setActiveTab('agroforestry')}
                    className="w-full text-left p-3 rounded-lg bg-blue-50 hover:bg-blue-100 transition duration-300"
                  >
                    <div className="font-medium text-blue-800">{t('exploreAgroforestry')}</div>
                    <div className="text-gray-600 text-sm">{t('multiCroppingSystems')}</div>
                  </button>
                  <button 
                    onClick={() => setActiveTab('predictions')}
                    className="w-full text-left p-3 rounded-lg bg-purple-50 hover:bg-purple-100 transition duration-300"
                  >
                    <div className="font-medium text-purple-800">{t('viewPredictions')}</div>
                    <div className="text-gray-600 text-sm">{t('realTimeCropPredictions')}</div>
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {/* AI Planner Tab */}
        {activeTab === 'aiplanner' && (
          <AIPlanner />
        )}
        
        {/* Agroforestry Tab */}
        {activeTab === 'agroforestry' && (
          <AgroforestryPlanner />
        )}
        
        {/* Soil Analysis Tab */}
        {activeTab === 'soil' && (
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">{t('soilAnalysisReport')}</h2>
            {soilData ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-medium text-gray-800 mb-4">{t('soilProperties')}</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between border-b border-gray-100 pb-2">
                      <span className="text-gray-600">{t('phLevel')}</span>
                      <span className="font-medium">{soilData.pH}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-100 pb-2">
                      <span className="text-gray-600">{t('texture')}</span>
                      <span className="font-medium">{soilData.texture}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-100 pb-2">
                      <span className="text-gray-600">{t('organicCarbon')}</span>
                      <span className="font-medium">{soilData.organicCarbon}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-100 pb-2">
                      <span className="text-gray-600">{t('bulkDensity')}</span>
                      <span className="font-medium">{soilData.bulkDensity}</span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-lg font-medium text-gray-800 mb-4">{t('nutrientContent')}</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between border-b border-gray-100 pb-2">
                      <span className="text-gray-600">{t('nitrogen')}</span>
                      <span className="font-medium">{soilData.nitrogen}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-100 pb-2">
                      <span className="text-gray-600">{t('phosphorus')}</span>
                      <span className="font-medium">{soilData.phosphorus}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-100 pb-2">
                      <span className="text-gray-600">{t('potassium')}</span>
                      <span className="font-medium">{soilData.potassium}</span>
                    </div>
                  </div>
                </div>
                
                <div className="md:col-span-2 mt-6">
                  <h3 className="text-lg font-medium text-gray-800 mb-4">{t('aiSoilManagement')}</h3>
                  {aiRecommendations ? (
                    <ul className="space-y-2">
                      {aiRecommendations.soilManagement.map((recommendation, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-green-500 mr-2">✓</span>
                          <span className="text-gray-700">{recommendation}</span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-gray-500">{t('loadingRecommendations')}</p>
                  )}
                </div>
              </div>
            ) : (
              <p className="text-gray-500">{t('loadingSoilData')}</p>
            )}
          </div>
        )}
        
        {/* Weather & Rainfall Tab */}
        {activeTab === 'weather' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-6">{t('currentWeatherConditions')}</h2>
              {weather ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                  <div className="bg-blue-50 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-blue-800">{weather.temp}°C</div>
                    <div className="text-gray-600">{t('temperature')}</div>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-blue-800">{weather.humidity}%</div>
                    <div className="text-gray-600">{t('humidity')}</div>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-blue-800">{weather.pressure} {t('pressureUnit')}</div>
                    <div className="text-gray-600">{t('pressure')}</div>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-blue-800">{weather.windSpeed} {t('windSpeedUnit')}</div>
                    <div className="text-gray-600">{t('windSpeed')}</div>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-blue-800 capitalize">{t(weather.description) || weather.description}</div>
                    <div className="text-gray-600">{t('condition')}</div>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500">{t('loadingWeatherData')}</p>
              )}
            </div>
            
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-6">{t('rainfallAnalysis')}</h2>
              {rainfallData ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-lg font-medium text-gray-800 mb-4">{t('annualRainfall')}</h3>
                    <div className="text-3xl font-bold text-blue-600 mb-2">{rainfallData.annual}</div>
                    <p className="text-gray-600">{t('basedOnHistoricalData')}</p>
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-medium text-gray-800 mb-4">{t('seasonalDistribution')}</h3>
                    <p className="text-gray-700">{rainfallData.seasonal}</p>
                  </div>
                  
                  <div className="md:col-span-2 mt-4">
                    <h3 className="text-lg font-medium text-gray-800 mb-4">{t('soilWetnessIndex')}</h3>
                    <div className="w-full bg-gray-200 rounded-full h-4">
                      <div className="bg-blue-600 h-4 rounded-full" style={{ width: '60%' }}></div>
                    </div>
                    <div className="flex justify-between mt-2">
                      <span className="text-sm text-gray-600">{t('dry')}</span>
                      <span className="text-sm font-medium text-gray-800">{rainfallData.soilWetness}</span>
                      <span className="text-sm text-gray-600">{t('wet')}</span>
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500">{t('loadingRainfallData')}</p>
              )}
            </div>
            
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-6">{t('aiIrrigationRecommendations')}</h2>
              {aiRecommendations ? (
                <ul className="space-y-3">
                  {aiRecommendations.irrigation.map((recommendation, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-green-500 mr-2">✓</span>
                      <span className="text-gray-700">{recommendation}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500">{t('loadingRecommendations')}</p>
              )}
            </div>
          </div>
        )}
        
        {/* Farm Map Tab */}
        {activeTab === 'map' && (
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">{t('farmMap')}</h2>
            <LoadScript googleMapsApiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
              <GoogleMap mapContainerStyle={mapContainerStyle} center={center} zoom={16}>
                <Polygon
                  paths={farmPolygon}
                  options={{
                    fillColor: '#34D399',
                    fillOpacity: 0.3,
                    strokeColor: '#059669',
                    strokeWeight: 2
                  }}
                />
                <Marker position={center} />
              </GoogleMap>
            </LoadScript>
            
            <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-green-50 rounded-lg p-4">
                <h3 className="font-medium text-green-800 mb-2">{t('farmArea')}</h3>
                <p className="text-2xl font-bold">2.5 acres</p>
              </div>
              <div className="bg-blue-50 rounded-lg p-4">
                <h3 className="font-medium text-blue-800 mb-2">{t('gpsCoordinates')}</h3>
                <p className="text-lg font-bold">{center.lat.toFixed(4)}, {center.lng.toFixed(4)}</p>
              </div>
              <div className="bg-purple-50 rounded-lg p-4">
                <h3 className="font-medium text-purple-800 mb-2">{t('boundaryStatus')}</h3>
                <p className="text-lg font-bold text-green-600">{t('verified')}</p>
              </div>
            </div>
            
            {/* AI-Generated Land Layout Map */}
            <div className="mt-8">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">{t('aiGeneratedLandLayout')}</h3>
              <div className="bg-gray-100 rounded-lg p-4">
                <iframe 
                  src="/api/latest-map" 
                  title="AI Land Layout Map" 
                  className="w-full h-96 rounded-lg border-0"
                  sandbox="allow-scripts allow-same-origin"
                ></iframe>
                <div className="mt-4 flex justify-center">
                  <button 
                    onClick={generateLandLayoutMap}
                    className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-6 rounded-lg transition duration-300 flex items-center"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 110 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
                    </svg>
                    {t('refreshLandLayout')}
                  </button>
                </div>
                
                {/* Legend for land use types */}
                <div className="mt-6 bg-gray-50 rounded-lg p-4 inline-block">
                  <h4 className="font-medium text-gray-800 mb-2">{t('landUseLegend')}</h4>
                  <div className="space-y-2">
                    <div className="flex items-center">
                      <div className="w-4 h-4 bg-green-500 mr-2"></div>
                      <span className="text-sm">{t('mainCropArea')} (60%)</span>
                    </div>
                    <div className="flex items-center">
                      <div className="w-4 h-4 bg-yellow-500 mr-2"></div>
                      <span className="text-sm">{t('intercropArea')} (25%)</span>
                    </div>
                    <div className="flex items-center">
                      <div className="w-4 h-4 bg-green-800 mr-2"></div>
                      <span className="text-sm">{t('treesArea')} (15%)</span>
                    </div>
                  </div>
                </div>
                
                {mapId && (
                  <div className="mt-4 text-center text-sm text-green-600">
                    {t('mapStoredInFirebase')} ID: {mapId}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
        
        {/* Predictions Tab */}
        {activeTab === 'predictions' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-6">🌾 {t('realTimePredictions')}</h2>
              
              {realTimePredictions ? (
                <div className="space-y-6">
                  {/* Recommended Crops */}
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h3 className="text-lg font-medium text-gray-800 mb-3">🌾 {t('recommendedCrops')}</h3>
                    <div className="flex flex-wrap gap-3">
                      <div className="bg-green-100 rounded-lg p-4 text-center flex-1 min-w-[200px]">
                        <div className="text-2xl font-bold text-green-800">
                          {realTimePredictions.recommendations?.best_crop || 'Maize'}
                        </div>
                        <div className="text-gray-600">{t('bestCropForConditions')}</div>
                      </div>
                      <div className="bg-blue-100 rounded-lg p-4 text-center flex-1 min-w-[200px]">
                        <div className="text-2xl font-bold text-blue-800">{t('cowpea')}</div>
                        <div className="text-gray-600">{t('nitrogenFixingCrop')}</div>
                      </div>
                      <div className="bg-purple-100 rounded-lg p-4 text-center flex-1 min-w-[200px]">
                        <div className="text-2xl font-bold text-purple-800">{t('turmeric')}</div>
                        <div className="text-gray-600">{t('highValueCrop')}</div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Predicted Yield */}
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h3 className="text-lg font-medium text-gray-800 mb-3">📊 {t('predictedYield')}</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="bg-blue-50 rounded-lg p-4 text-center">
                        <div className="text-3xl font-bold text-blue-800">
                          {realTimePredictions.predictions?.yield_kg_per_acre?.toLocaleString() || '3,000'} kg/acre
                        </div>
                        <div className="text-gray-600">{t('estimatedYieldPerAcre')}</div>
                        <div className="mt-2 text-sm text-gray-500">
                          {t('confidence')}: {realTimePredictions.predictions?.confidence ? (realTimePredictions.predictions.confidence * 100).toFixed(0) : '85'}%
                        </div>
                      </div>
                      <div className="bg-green-50 rounded-lg p-4 text-center">
                        <div className="text-3xl font-bold text-green-800">₹1,20,000</div>
                        <div className="text-gray-600">{t('estimatedRevenue')}</div>
                        <div className="mt-2 text-sm text-gray-500">{t('basedOnCurrentPrices')}</div>
                      </div>
                      <div className="bg-yellow-50 rounded-lg p-4 text-center">
                        <div className="text-3xl font-bold text-yellow-800">
                          {realTimePredictions.predictions?.yield_kg_per_acre > 3000 ? t('high') : 
                           realTimePredictions.predictions?.yield_kg_per_acre > 2000 ? t('medium') : t('low') || t('medium')}
                        </div>
                        <div className="text-gray-600">{t('yieldPotential')}</div>
                        <div className="mt-2 text-sm text-gray-500">{t('basedOnEnvironmentalConditions')}</div>
                      </div>
                    </div>
                  </div>
                  
                  {/* ROI and Cost-Benefit */}
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h3 className="text-lg font-medium text-gray-800 mb-3">💰 {t('roiAndCostBenefit')}</h3>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                      <div className="bg-green-50 rounded-lg p-4 text-center">
                        <div className="text-2xl font-bold text-green-800">
                          {realTimePredictions.predictions?.roi?.toFixed(1) || '2.8'}x
                        </div>
                        <div className="text-gray-600">{t('returnOnInvestment')}</div>
                      </div>
                      <div className="bg-blue-50 rounded-lg p-4 text-center">
                        <div className="text-2xl font-bold text-blue-800">₹50,000</div>
                        <div className="text-gray-600">{t('estimatedInvestment')}</div>
                      </div>
                      <div className="bg-purple-50 rounded-lg p-4 text-center">
                        <div className="text-2xl font-bold text-purple-800">₹1,20,000</div>
                        <div className="text-gray-600">{t('estimatedIncome')}</div>
                      </div>
                      <div className="bg-yellow-50 rounded-lg p-4 text-center">
                        <div className="text-2xl font-bold text-yellow-800">{realTimePredictions.predictions?.payback_period || '18'} {t('months')}</div>
                        <div className="text-gray-600">{t('paybackPeriod')}</div>
                      </div>
                    </div>
                    
                    {/* Cost-Benefit Analysis */}
                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <h4 className="font-medium text-gray-800 mb-2">{t('costBreakdown')}</h4>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                        <div className="bg-white border border-gray-200 rounded p-3">
                          <div className="font-medium text-gray-800">{t('seedsAndSaplings')}</div>
                          <div className="text-green-700 font-bold">{t('currencySymbol')}{realTimePredictions.costs?.seeds_and_saplings?.toLocaleString() || '8,000'}</div>
                        </div>
                        <div className="bg-white border border-gray-200 rounded p-3">
                          <div className="font-medium text-gray-800">{t('fertilizers')}</div>
                          <div className="text-green-700 font-bold">{t('currencySymbol')}{realTimePredictions.costs?.fertilizers?.toLocaleString() || '12,000'}</div>
                        </div>
                        <div className="bg-white border border-gray-200 rounded p-3">
                          <div className="font-medium text-gray-800">{t('labor')}</div>
                          <div className="text-green-700 font-bold">{t('currencySymbol')}{realTimePredictions.costs?.labor?.toLocaleString() || '15,000'}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Weather Conditions */}
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h3 className="text-lg font-medium text-gray-800 mb-3">🌤️ {t('currentWeatherConditions')}</h3>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                      <div className="bg-blue-50 rounded-lg p-3 text-center">
                        <div className="text-xl font-bold text-blue-800">
                          {realTimePredictions.weather_data?.avg_temperature_c || '28'}°C
                        </div>
                        <div className="text-gray-600">{t('temperature')}</div>
                      </div>
                      <div className="bg-green-50 rounded-lg p-3 text-center">
                        <div className="text-xl font-bold text-green-800">
                          {realTimePredictions.weather_data?.avg_humidity || '65'}%
                        </div>
                        <div className="text-gray-600">{t('humidity')}</div>
                      </div>
                      <div className="bg-yellow-50 rounded-lg p-3 text-center">
                        <div className="text-xl font-bold text-yellow-800">
                          {realTimePredictions.weather_data?.avg_rainfall_mm?.toLocaleString() || '980'} mm
                        </div>
                        <div className="text-gray-600">{t('annualRainfall')}</div>
                      </div>
                      <div className="bg-purple-50 rounded-lg p-3 text-center">
                        <div className="text-xl font-bold text-purple-800">
                          {realTimePredictions.weather_data?.solar_radiation || '5.5'} kWh/m²
                        </div>
                        <div className="text-gray-600">{t('solarRadiation')}</div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Recommendations */}
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h3 className="text-lg font-medium text-gray-800 mb-3">✅ {t('recommendations')}</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-medium text-gray-800 mb-2">{t('plantingRecommendations')}</h4>
                        <ul className="space-y-2">
                          <li className="flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            <span className="text-gray-700">{t('plantingTime')}: {realTimePredictions.recommendations?.planting_time || 'June-July'}</span>
                          </li>
                          <li className="flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            <span className="text-gray-700">{t('irrigationNeeds')}: {realTimePredictions.recommendations?.irrigation_needs || 'Moderate'}</span>
                          </li>
                          <li className="flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            <span className="text-gray-700">{t('soilPreparation')}: {t('addOrganicCompost')}</span>
                          </li>
                        </ul>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-800 mb-2">{t('harvestingTips')}</h4>
                        <ul className="space-y-2">
                          <li className="flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            <span className="text-gray-700">{t('monitorCropHealth')}: {t('checkPestsDiseases')}</span>
                          </li>
                          <li className="flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            <span className="text-gray-700">{t('optimalHarvestTime')}: {t('harvestWhenMature')}</span>
                          </li>
                          <li className="flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            <span className="text-gray-700">{t('postHarvestHandling')}: {t('dryGrainsProperly')}</span>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-green-600 mb-4"></div>
                  <p className="text-gray-600">{t('loadingPredictions')}</p>
                </div>
              )}
            </div>
          </div>
        )}
        
        {/* Real-time Predictions Section */}
        {realTimePredictions && (
          <div className="bg-white rounded-xl shadow-md p-6 mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-800">
                📊 {t('realTimePredictions')}
              </h2>
              {currentPredictionId && (
                <button
                  onClick={() => setShowFeedbackForm(true)}
                  className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-2 px-4 rounded-lg transition duration-300"
                >
                  {t('provideFeedback')}
                </button>
              )}
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="bg-green-50 rounded-lg p-4 text-center">
                <p className="text-gray-600">{t('predictedYield')}</p>
                <p className="text-2xl font-bold text-green-700">
                  {realTimePredictions.predictions?.yield_kg_per_acre || 'N/A'} kg/acre
                </p>
                <p className="text-sm text-gray-500">
                  {t('confidence')}: {realTimePredictions.predictions?.confidence ? (realTimePredictions.predictions.confidence * 100).toFixed(0) : 'N/A'}%
                </p>
              </div>
              
              <div className="bg-blue-50 rounded-lg p-4 text-center">
                <p className="text-gray-600">{t('predictedROI')}</p>
                <p className="text-2xl font-bold text-blue-700">
                  {realTimePredictions.predictions?.roi ? `${realTimePredictions.predictions.roi}x` : 'N/A'}
                </p>
                <p className="text-sm text-gray-500">
                  {t('returnOnInvestment')}
                </p>
              </div>
              
              <div className="bg-purple-50 rounded-lg p-4 text-center">
                <p className="text-gray-600">{t('recommendedCrop')}</p>
                <p className="text-2xl font-bold text-purple-700">
                  {realTimePredictions.recommendations?.best_crop || 'N/A'}
                </p>
                <p className="text-sm text-gray-500">
                  {realTimePredictions.recommendations?.planting_time || 'N/A'}
                </p>
              </div>
            </div>
            
            <div className="border-t border-gray-200 pt-4">
              <h3 className="font-medium text-gray-800 mb-2">{t('recommendations')}</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-700">
                <li>{t('bestCrop')}: {realTimePredictions.recommendations?.best_crop || 'N/A'}</li>
                <li>{t('plantingTime')}: {realTimePredictions.recommendations?.planting_time || 'N/A'}</li>
                <li>{t('irrigationNeeds')}: {realTimePredictions.recommendations?.irrigation_needs || 'N/A'}</li>
              </ul>
            </div>
          </div>
        )}
        
        {/* Feedback Form Modal */}
        {showFeedbackForm && currentPredictionId && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-xl shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
              <div className="sticky top-0 bg-white border-b border-gray-200 p-4 flex justify-between items-center rounded-t-xl">
                <h3 className="text-lg font-semibold text-gray-800">
                  {t('provideFeedback')}
                </h3>
                <button
                  onClick={() => setShowFeedbackForm(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div className="p-6">
                <FeedbackForm 
                  predictionId={currentPredictionId} 
                  onClose={() => setShowFeedbackForm(false)} 
                />
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;