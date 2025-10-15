import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import { auth } from '../firebase';
import { signOut } from 'firebase/auth';
import { GoogleMap, LoadScript, Marker, Polygon } from '@react-google-maps/api';
import AgroforestryPlanner from './AgroforestryPlanner';
import AIPlanner from './AIPlanner';

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
  const [activeTab, setActiveTab] = useState('overview');

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
        },
        (error) => {
          console.error('Error getting location:', error);
          // Fetch weather for default location if geolocation fails
          fetchWeather(defaultCenter.lat, defaultCenter.lng);
        }
      );
    } else {
      // Fetch weather for default location if geolocation not supported
      fetchWeather(defaultCenter.lat, defaultCenter.lng);
    }
  }, []);

  const fetchWeather = async (lat, lon) => {
    try {
      const response = await axios.get(
        `https://api.openweathermap.org/data/2.5/weather`,
        {
          params: {
            lat: lat,
            lon: lon,
            units: 'metric',
            appid: import.meta.env.VITE_WEATHER_API_KEY
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
    }
  };

  // Mock data for soil, rainfall, and investment capacity
  useEffect(() => {
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

  return (
    <div className="min-h-screen bg-green-50 p-4">
      <header className="w-full max-w-6xl mx-auto mb-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 py-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-green-800">
              Sasya-Mitra Dashboard
            </h1>
            <p className="text-green-600">AI-Powered Agricultural Advisory System</p>
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
            Overview
          </button>
          <button 
            onClick={() => setActiveTab('soil')}
            className={`px-4 py-2 rounded-lg transition duration-300 ${activeTab === 'soil' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-green-100'}`}
          >
            Soil Analysis
          </button>
          <button 
            onClick={() => setActiveTab('weather')}
            className={`px-4 py-2 rounded-lg transition duration-300 ${activeTab === 'weather' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-green-100'}`}
          >
            Weather & Rainfall
          </button>
          <button 
            onClick={() => setActiveTab('ai')}
            className={`px-4 py-2 rounded-lg transition duration-300 ${activeTab === 'ai' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-green-100'}`}
          >
            AI Recommendations
          </button>
          <button 
            onClick={() => setActiveTab('agroforestry')}
            className={`px-4 py-2 rounded-lg transition duration-300 ${activeTab === 'agroforestry' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-green-100'}`}
          >
            Agroforestry
          </button>
          <button 
            onClick={() => setActiveTab('aiplanner')}
            className={`px-4 py-2 rounded-lg transition duration-300 ${activeTab === 'aiplanner' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-green-100'}`}
          >
            AI Planner
          </button>
          <button 
            onClick={() => setActiveTab('map')}
            className={`px-4 py-2 rounded-lg transition duration-300 ${activeTab === 'map' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-green-100'}`}
          >
            Farm Map
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
                    <p className="text-gray-500 text-sm">Farm Area</p>
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
                    <p className="text-gray-500 text-sm">Current Weather</p>
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
                    <p className="text-gray-500 text-sm">Investment Capacity</p>
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
                    <p className="text-gray-500 text-sm">Expected Profit</p>
                    <p className="text-xl font-semibold">
                      {aiRecommendations ? '₹45,000/ha' : 'Loading...'}
                    </p>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 bg-white rounded-xl shadow-md p-6">
                <h2 className="text-xl font-semibold text-gray-800 mb-4">AI-Powered Crop Recommendations</h2>
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
                  <p className="text-gray-500">Loading recommendations...</p>
                )}
              </div>
              
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-xl font-semibold text-gray-800 mb-4">Quick Actions</h2>
                <div className="space-y-3">
                  <button className="w-full text-left p-3 rounded-lg bg-green-50 hover:bg-green-100 transition duration-300">
                    <div className="font-medium text-green-800">Update Farm Profile</div>
                    <div className="text-gray-600 text-sm">Edit your farm details</div>
                  </button>
                  <button className="w-full text-left p-3 rounded-lg bg-blue-50 hover:bg-blue-100 transition duration-300">
                    <div className="font-medium text-blue-800">Generate New Plan</div>
                    <div className="text-gray-600 text-sm">Create AI land-use plan</div>
                  </button>
                  <button className="w-full text-left p-3 rounded-lg bg-purple-50 hover:bg-purple-100 transition duration-300">
                    <div className="font-medium text-purple-800">View Historical Data</div>
                    <div className="text-gray-600 text-sm">Access past recommendations</div>
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {/* Soil Analysis Tab */}
        {activeTab === 'soil' && (
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Soil Analysis Report</h2>
            {soilData ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-medium text-gray-800 mb-4">Soil Properties</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between border-b border-gray-100 pb-2">
                      <span className="text-gray-600">pH Level</span>
                      <span className="font-medium">{soilData.pH}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-100 pb-2">
                      <span className="text-gray-600">Texture</span>
                      <span className="font-medium">{soilData.texture}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-100 pb-2">
                      <span className="text-gray-600">Organic Carbon</span>
                      <span className="font-medium">{soilData.organicCarbon}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-100 pb-2">
                      <span className="text-gray-600">Bulk Density</span>
                      <span className="font-medium">{soilData.bulkDensity}</span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-lg font-medium text-gray-800 mb-4">Nutrient Content</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between border-b border-gray-100 pb-2">
                      <span className="text-gray-600">Nitrogen (N)</span>
                      <span className="font-medium">{soilData.nitrogen}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-100 pb-2">
                      <span className="text-gray-600">Phosphorus (P)</span>
                      <span className="font-medium">{soilData.phosphorus}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-100 pb-2">
                      <span className="text-gray-600">Potassium (K)</span>
                      <span className="font-medium">{soilData.potassium}</span>
                    </div>
                  </div>
                </div>
                
                <div className="md:col-span-2 mt-6">
                  <h3 className="text-lg font-medium text-gray-800 mb-4">AI Soil Management Recommendations</h3>
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
                    <p className="text-gray-500">Loading recommendations...</p>
                  )}
                </div>
              </div>
            ) : (
              <p className="text-gray-500">Loading soil data...</p>
            )}
          </div>
        )}
        
        {/* Weather & Rainfall Tab */}
        {activeTab === 'weather' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-6">Current Weather Conditions</h2>
              {weather ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                  <div className="bg-blue-50 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-blue-800">{weather.temp}°C</div>
                    <div className="text-gray-600">Temperature</div>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-blue-800">{weather.humidity}%</div>
                    <div className="text-gray-600">Humidity</div>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-blue-800">{weather.pressure} hPa</div>
                    <div className="text-gray-600">Pressure</div>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-blue-800">{weather.windSpeed} m/s</div>
                    <div className="text-gray-600">Wind Speed</div>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-blue-800 capitalize">{weather.description}</div>
                    <div className="text-gray-600">Condition</div>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500">Loading weather data...</p>
              )}
            </div>
            
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-6">Rainfall Analysis</h2>
              {rainfallData ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-lg font-medium text-gray-800 mb-4">Annual Rainfall</h3>
                    <div className="text-3xl font-bold text-blue-600 mb-2">{rainfallData.annual}</div>
                    <p className="text-gray-600">Based on historical data for your region</p>
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-medium text-gray-800 mb-4">Seasonal Distribution</h3>
                    <p className="text-gray-700">{rainfallData.seasonal}</p>
                  </div>
                  
                  <div className="md:col-span-2 mt-4">
                    <h3 className="text-lg font-medium text-gray-800 mb-4">Soil Wetness Index</h3>
                    <div className="w-full bg-gray-200 rounded-full h-4">
                      <div className="bg-blue-600 h-4 rounded-full" style={{ width: '60%' }}></div>
                    </div>
                    <div className="flex justify-between mt-2">
                      <span className="text-sm text-gray-600">Dry</span>
                      <span className="text-sm font-medium text-gray-800">{rainfallData.soilWetness}</span>
                      <span className="text-sm text-gray-600">Wet</span>
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500">Loading rainfall data...</p>
              )}
            </div>
            
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-6">AI Irrigation Recommendations</h2>
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
                <p className="text-gray-500">Loading recommendations...</p>
              )}
            </div>
          </div>
        )}
        
        {/* AI Recommendations Tab */}
        {activeTab === 'ai' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-6">Personalized Crop Rotation Plan</h2>
              {aiRecommendations ? (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Season</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Recommended Crop</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reason</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {aiRecommendations.cropRotation.map((recommendation, index) => (
                        <tr key={index}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-gray-900">{recommendation.season}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{recommendation.crop}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {recommendation.reason}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-gray-500">Loading recommendations...</p>
              )}
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-2xl font-semibold text-gray-800 mb-6">Soil Management Practices</h2>
                {aiRecommendations ? (
                  <ul className="space-y-3">
                    {aiRecommendations.soilManagement.map((recommendation, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-green-500 mr-2">✓</span>
                        <span className="text-gray-700">{recommendation}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-gray-500">Loading recommendations...</p>
                )}
              </div>
              
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-2xl font-semibold text-gray-800 mb-6">Economic Forecast</h2>
                {aiRecommendations ? (
                  <div>
                    <div className="mb-4">
                      <h3 className="text-lg font-medium text-gray-800 mb-2">Expected Yield</h3>
                      <p className="text-gray-700">{aiRecommendations.economicForecast.expectedYield}</p>
                    </div>
                    <div className="mb-4">
                      <h3 className="text-lg font-medium text-gray-800 mb-2">Input Cost</h3>
                      <p className="text-gray-700">{aiRecommendations.economicForecast.inputCost}</p>
                    </div>
                    <div>
                      <h3 className="text-lg font-medium text-gray-800 mb-2">Expected Profit</h3>
                      <p className="text-gray-700">{aiRecommendations.economicForecast.expectedProfit}</p>
                    </div>
                  </div>
                ) : (
                  <p className="text-gray-500">Loading forecast...</p>
                )}
              </div>
            </div>
          </div>
        )}
        
        {/* Agroforestry Tab */}
        {activeTab === 'agroforestry' && (
          <AgroforestryPlanner />
        )}
        
        {/* AI Planner Tab */}
        {activeTab === 'aiplanner' && (
          <AIPlanner />
        )}
        
        {/* Farm Map Tab */}
        {activeTab === 'map' && (
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Farm Map</h2>
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
                <h3 className="font-medium text-green-800 mb-2">Farm Area</h3>
                <p className="text-2xl font-bold">2.5 acres</p>
              </div>
              <div className="bg-blue-50 rounded-lg p-4">
                <h3 className="font-medium text-blue-800 mb-2">GPS Coordinates</h3>
                <p className="text-lg font-bold">{center.lat.toFixed(4)}, {center.lng.toFixed(4)}</p>
              </div>
              <div className="bg-purple-50 rounded-lg p-4">
                <h3 className="font-medium text-purple-800 mb-2">Boundary Status</h3>
                <p className="text-lg font-bold text-green-600">Verified</p>
              </div>
            </div>
          </div>
        )}
        
        {/* Recent Activity Section (Visible on all tabs) */}
        <div className="bg-white rounded-xl shadow-md p-6 mt-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Activity</h2>
          <div className="space-y-4">
            <div className="border-b border-gray-100 pb-4">
              <h3 className="font-medium text-gray-800">New AI Plan Generated</h3>
              <p className="text-gray-600 text-sm">2 hours ago</p>
            </div>
            <div className="border-b border-gray-100 pb-4">
              <h3 className="font-medium text-gray-800">Soil Data Updated</h3>
              <p className="text-gray-600 text-sm">1 day ago</p>
            </div>
            <div>
              <h3 className="font-medium text-gray-800">Farm Profile Created</h3>
              <p className="text-gray-600 text-sm">3 days ago</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;