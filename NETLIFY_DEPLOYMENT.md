# Netlify Deployment Guide for Sasya-Yojana

This guide explains how to deploy the Sasya-Yojana application to Netlify.

## Prerequisites

1. A Netlify account (free at [netlify.com](https://netlify.com))
2. A GitHub, GitLab, or Bitbucket account
3. The Sasya-Yojana repository

## Deployment Options

### Option 1: Deploy with Git (Recommended)

1. Push your Sasya-Yojana code to a Git repository (GitHub, GitLab, or Bitbucket)
2. Log in to your Netlify account
3. Click "New site from Git"
4. Select your Git provider and repository
5. Configure the deployment settings:
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
6. Click "Deploy site"

### Option 2: Deploy Manually

1. Build the project locally:
   ```bash
   npm run build
   ```
2. Log in to your Netlify account
3. Drag and drop the `dist` folder to the Netlify deployment area

## Environment Variables

After deployment, you need to set the environment variables in Netlify:

1. Go to your site settings in Netlify
2. Navigate to "Build & deploy" → "Environment"
3. Add the following environment variables:

```
VITE_WEATHER_API_KEY=your_openweathermap_api_key
REACT_APP_FIREBASE_API_KEY=your_firebase_api_key
REACT_APP_FIREBASE_AUTH_DOMAIN=your_firebase_auth_domain
REACT_APP_FIREBASE_PROJECT_ID=your_firebase_project_id
REACT_APP_FIREBASE_STORAGE_BUCKET=your_firebase_storage_bucket
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your_firebase_messaging_sender_id
REACT_APP_FIREBASE_APP_ID=your_firebase_app_id
REACT_APP_FIREBASE_MEASUREMENT_ID=your_firebase_measurement_id
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

## Backend API Configuration

The frontend application makes API calls to backend services. For Netlify deployment, you have two options:

### Option 1: Use Netlify Functions (Proxy)

The project includes a Netlify function (`functions/api-proxy.js`) that can proxy API calls to your backend.

1. Update the `functions/api-proxy.js` file with your actual backend URL:
   ```javascript
   const backendUrl = 'https://your-actual-backend-url.com' + apiPath;
   ```

2. Deploy the functions by including them in your Git repository

### Option 2: Direct API Calls

If you have a publicly accessible backend, you can configure the frontend to call it directly by:

1. Updating the `src/utils/api.js` file to use your backend URL
2. Setting the appropriate CORS headers on your backend

## Custom Domain

To use a custom domain:

1. Go to your site settings in Netlify
2. Navigate to "Domain management"
3. Add your custom domain
4. Follow the DNS configuration instructions

## Redirects and Headers

The project includes:

- `_redirects` file for SPA routing
- `_headers` file for security and caching headers

These files are automatically copied to the `dist` directory during build.

## Continuous Deployment

With Git-based deployment, Netlify will automatically rebuild and deploy your site whenever you push changes to your repository.

## Troubleshooting

### Common Issues

1. **API calls failing**: Make sure your backend URL is correctly configured
2. **Environment variables not loading**: Check that they are properly set in Netlify
3. **Map not displaying**: Verify Google Maps API key and billing setup
4. **Firebase errors**: Ensure Firebase configuration is correct

### Checking Build Logs

You can view build logs in the Netlify dashboard under "Deploys" → "Deploy details"

## Local Development with Netlify Dev

You can use Netlify Dev for local development with functions:

```bash
npm install -g netlify-cli
netlify dev
```

This will start the development server with Netlify functions emulation.

## Support

For issues with deployment, check:
- Netlify documentation: https://docs.netlify.com/
- Sasya-Yojana documentation in the repository