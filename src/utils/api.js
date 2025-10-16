import axios from 'axios';

// Determine the base URL based on the environment
const getBaseUrl = () => {
  // For Netlify deployments
  if (typeof process !== 'undefined' && process.env && process.env.NETLIFY === 'true') {
    return '/.netlify/functions/api-proxy';
  }
  
  // For local development with Vite
  if (import.meta.env && import.meta.env.DEV) {
    return '';
  }
  
  // For production deployments
  return '';
};

const API_BASE_URL = getBaseUrl();

// Create an axios instance with the base URL
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions
export const generateLandLayoutMap = async (mapData) => {
  try {
    const response = await apiClient.post('/api/generate-land-layout-map', mapData);
    return response.data;
  } catch (error) {
    console.error('Error generating land layout map:', error);
    throw error;
  }
};

export const getMap = async (filename) => {
  try {
    const response = await apiClient.get(`/api/get-map/${filename}`);
    return response.data;
  } catch (error) {
    console.error('Error getting map:', error);
    throw error;
  }
};

export const getLatestMap = async () => {
  try {
    const response = await apiClient.get('/api/latest-map');
    return response.data;
  } catch (error) {
    console.error('Error getting latest map:', error);
    throw error;
  }
};

// Export the apiClient for direct usage if needed
export default apiClient;