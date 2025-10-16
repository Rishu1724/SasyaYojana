# Netlify Deployment Troubleshooting Guide

This guide helps resolve common issues when deploying Sasya-Yojana to Netlify.

## Common Build Errors and Solutions

### 1. Missing Dependencies

**Error**: `Cannot find module 'X'` or `Error: Cannot resolve dependency`

**Solution**:
1. Check that all dependencies are listed in `package.json`
2. Run `npm install` locally to ensure all dependencies are installed
3. Verify that the `node_modules` directory is not in `.gitignore` (it should be ignored)
4. For Netlify functions, ensure dependencies are in `functions/package.json`

### 2. ES Module vs CommonJS Issues

**Error**: `require() of ES Module` or `import statement outside a module`

**Solution**:
1. Ensure `type: "module"` is in `package.json` for ES modules
2. Use `import` statements instead of `require()` in ES modules
3. For Netlify functions, use `import` and set `type: "module"` in `functions/package.json`

### 3. Environment Variables Not Set

**Error**: `undefined` values or authentication failures

**Solution**:
1. Set all required environment variables in Netlify dashboard
2. Prefix client-side variables with `VITE_` or `REACT_APP_`
3. Verify variable names match exactly

### 4. Build Command Failures

**Error**: Build script fails or times out

**Solution**:
1. Test build locally with `npm run build`
2. Check for syntax errors in configuration files
3. Increase build timeout if needed
4. Optimize build process to reduce build time

## Specific Fixes Applied

### 1. Netlify Functions ES Module Fix

**Issue**: The Netlify function was using `require()` in an ES module environment.

**Fix**: 
- Changed `require('node-fetch')` to `import fetch from 'node-fetch'`
- Added `type: "module"` to `functions/package.json`
- Updated `node-fetch` to version 3.3.0 which supports ES modules

### 2. API Proxy Configuration

**Issue**: API calls were not properly routed through Netlify functions.

**Fix**:
- Updated `_redirects` file to route all `/api/*` calls to the Netlify function
- Improved the API utility to detect Netlify environment properly
- Added specific routes for map API endpoints

## Testing Your Fix

1. **Local Testing**:
   ```bash
   # Test the build process
   npm run build
   
   # Test with Netlify CLI
   netlify dev
   ```

2. **Dependency Verification**:
   ```bash
   # Check that all dependencies are installed
   npm ls
   
   # For functions
   cd functions && npm ls
   ```

3. **Environment Variables**:
   ```bash
   # Check that environment variables are accessible
   echo $VITE_WEATHER_API_KEY
   ```

## Netlify-Specific Troubleshooting

### 1. Function Deployment Issues

**Check**:
- Functions directory is correctly specified in `netlify.toml`
- Function files are in the correct directory structure
- Dependencies are in `functions/package.json`

**Solution**:
- Verify `functions` directory in `netlify.toml`
- Check function file extensions (`.js` for JavaScript)
- Ensure function exports `handler` function

### 2. Asset Loading Issues

**Check**:
- `_headers` file for proper caching rules
- `_redirects` file for SPA routing
- Asset paths in built files

**Solution**:
- Verify headers and redirects are copied to `dist/`
- Check that asset paths are relative
- Test locally with `npm run preview`

### 3. Environment Variable Issues

**Check**:
- Variables are prefixed correctly (`VITE_` for Vite, `REACT_APP_` for Create React App)
- Variables are set in Netlify dashboard
- Variables are accessed correctly in code

**Solution**:
- Use `import.meta.env.VITE_VARIABLE_NAME` for Vite
- Set variables in Netlify dashboard under "Environment"
- Restart deployment after setting variables

## Deployment Verification

After applying fixes:

1. **Commit and Push Changes**:
   ```bash
   git add .
   git commit -m "Fix Netlify deployment issues"
   git push origin main
   ```

2. **Trigger New Deployment**:
   - Push to repository to trigger automatic deployment
   - Or manually trigger deployment in Netlify dashboard

3. **Monitor Deployment**:
   - Check build logs in Netlify dashboard
   - Verify deployment succeeds
   - Test deployed site functionality

## If Issues Persist

1. **Check Netlify Status**: https://www.netlifystatus.com/
2. **Review Build Logs**: Look for specific error messages
3. **Contact Netlify Support**: https://www.netlify.com/support/
4. **Check Community Forums**: https://answers.netlify.com/

## Prevention for Future Deployments

1. **Regular Testing**:
   - Test build process regularly
   - Verify environment variables
   - Check function deployments

2. **Documentation**:
   - Keep deployment documentation updated
   - Document environment variables
   - Record successful deployment steps

3. **Monitoring**:
   - Set up deployment notifications
   - Monitor site performance
   - Check for broken links

## Support Resources

- Netlify Documentation: https://docs.netlify.com/
- Vite Documentation: https://vitejs.dev/
- Node.js ES Modules: https://nodejs.org/api/esm.html
- Netlify Functions: https://docs.netlify.com/functions/overview/