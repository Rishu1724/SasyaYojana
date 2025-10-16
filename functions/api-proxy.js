// Netlify function to proxy API calls
import fetch from 'node-fetch';

exports.handler = async (event, context) => {
  const { httpMethod, path, queryStringParameters, body, headers } = event;
  
  // Extract the API path
  const apiPath = path.replace('/.netlify/functions/api-proxy', '');
  
  // Your backend API URL - replace with your actual backend URL
  const backendUrl = 'https://your-backend-url.com' + apiPath;
  
  try {
    // Forward the request to your backend
    const response = await fetch(backendUrl, {
      method: httpMethod,
      headers: {
        'Content-Type': 'application/json',
        ...headers
      },
      body: httpMethod !== 'GET' && body ? body : undefined
    });
    
    const data = await response.json();
    
    return {
      statusCode: response.status,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
      body: JSON.stringify(data)
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ 
        error: 'Failed to fetch from backend API',
        message: error.message 
      })
    };
  }
};