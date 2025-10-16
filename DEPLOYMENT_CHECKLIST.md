# Sasya-Yojana Netlify Deployment Checklist

This checklist ensures that all necessary steps are completed for a successful Netlify deployment.

## Pre-deployment Checklist

### 1. Code Preparation
- [ ] All code is committed and pushed to the repository
- [ ] `package.json` has correct build scripts
- [ ] Environment variables are documented
- [ ] API endpoints are properly configured
- [ ] All dependencies are listed in `package.json`

### 2. Configuration Files
- [ ] `netlify.toml` is configured with build settings
- [ ] `vite.config.js` is properly configured for production
- [ ] `_headers` file exists in `public/` directory
- [ ] `_redirects` file exists in `public/` directory
- [ ] `404.html` exists for custom error pages
- [ ] `robots.txt` exists for SEO

### 3. Environment Variables
- [ ] `VITE_WEATHER_API_KEY` - OpenWeatherMap API key
- [ ] `REACT_APP_FIREBASE_API_KEY` - Firebase API key
- [ ] `REACT_APP_FIREBASE_AUTH_DOMAIN` - Firebase auth domain
- [ ] `REACT_APP_FIREBASE_PROJECT_ID` - Firebase project ID
- [ ] `REACT_APP_FIREBASE_STORAGE_BUCKET` - Firebase storage bucket
- [ ] `REACT_APP_FIREBASE_MESSAGING_SENDER_ID` - Firebase messaging sender ID
- [ ] `REACT_APP_FIREBASE_APP_ID` - Firebase app ID
- [ ] `REACT_APP_FIREBASE_MEASUREMENT_ID` - Firebase measurement ID
- [ ] `REACT_APP_GOOGLE_MAPS_API_KEY` - Google Maps API key

## Deployment Steps

### 1. Netlify Setup
- [ ] Create Netlify account if needed
- [ ] Connect Git repository (GitHub, GitLab, or Bitbucket)
- [ ] Configure build settings:
  - Build command: `npm run build`
  - Publish directory: `dist`
- [ ] Set environment variables in Netlify dashboard

### 2. Backend Configuration
- [ ] Update `functions/api-proxy.js` with actual backend URL
- [ ] OR configure direct API calls in `src/utils/api.js`
- [ ] Ensure backend has proper CORS configuration
- [ ] Test API endpoints are accessible

### 3. Domain and SSL
- [ ] Configure custom domain (if needed)
- [ ] Verify SSL certificate is active
- [ ] Update DNS records as needed

### 4. Testing
- [ ] Test build locally: `npm run build`
- [ ] Test locally with Netlify CLI: `netlify dev`
- [ ] Verify all pages load correctly
- [ ] Test API functionality
- [ ] Check mobile responsiveness
- [ ] Verify Firebase integration
- [ ] Test Google Maps integration

## Post-deployment Checklist

### 1. Monitoring
- [ ] Set up Netlify analytics
- [ ] Configure error tracking
- [ ] Set up performance monitoring
- [ ] Configure uptime monitoring

### 2. SEO and Performance
- [ ] Submit sitemap to search engines
- [ ] Verify robots.txt is working
- [ ] Test page load speeds
- [ ] Optimize images if needed
- [ ] Check accessibility compliance

### 3. Security
- [ ] Verify HTTPS is working
- [ ] Check security headers
- [ ] Review Firebase security rules
- [ ] Verify API keys are properly secured

## Troubleshooting Common Issues

### 1. Build Failures
- Check Node.js version compatibility
- Verify all dependencies are installed
- Check for syntax errors in configuration files

### 2. Runtime Errors
- Check browser console for JavaScript errors
- Verify environment variables are set correctly
- Check network tab for failed API requests
- Verify Firebase configuration

### 3. Performance Issues
- Analyze bundle sizes
- Optimize images and assets
- Implement code splitting
- Use Netlify's performance features

## Maintenance

### 1. Updates
- Regular dependency updates
- Security patches
- Content updates
- Feature enhancements

### 2. Backups
- Regular database backups
- Code repository backups
- Configuration backups

## Support Resources

- Netlify Documentation: https://docs.netlify.com/
- Vite Documentation: https://vitejs.dev/
- Firebase Documentation: https://firebase.google.com/docs/
- React Documentation: https://reactjs.org/

## Contact Information

For deployment issues, contact:
- Development Team: [team email]
- Netlify Support: support@netlify.com