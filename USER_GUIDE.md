# Sasya-Mitra User Guide

This guide explains how to use the improved Sasya-Mitra dashboard with enhanced farmer input collection and better organization.

## Getting Started

1. Make sure the development server is running (`npm run dev`)
2. Open your browser and navigate to http://localhost:5174
3. Select your preferred language from the top-right corner
4. Log in or sign up for an account

## Dashboard Overview

The dashboard is organized into several tabs for easy navigation:

### 1. Overview Tab
- View key farm metrics at a glance
- See AI-powered crop recommendations
- Access quick actions for common tasks

### 2. AI Planner Tab
This is the main planning interface where you'll input your farm details:

#### Farmer Input Form:
- **Location**: Choose between GPS coordinates or village name
  - Use the "📍" button to automatically detect your current location
  - Enter specific GPS coordinates if known
  - Enter your village name if preferred
- **Farm Details**:
  - Land area in acres (required)
  - Budget in Rupees (required)
- **Preferences**:
  - Optional crop preferences

#### After Submitting:
- View a comprehensive plan with:
  - Farm inputs summary
  - Location details
  - Soil analysis
  - Climate information
  - Recommended agroforestry system
  - Economic projections
  - Sustainability metrics
  - Implementation steps

### 3. Agroforestry Tab
- Explore different agroforestry systems
- View multi-cropping combinations
- See benefits of integrated farming

### 4. Soil Analysis Tab
- Detailed soil property information
- Nutrient content analysis
- AI soil management recommendations

### 5. Weather & Rainfall Tab
- Current weather conditions
- Rainfall analysis
- AI irrigation recommendations

### 6. Farm Map Tab
- Visual representation of your farm
- GPS coordinates display
- Boundary verification

## How to Generate an AI Plan

1. Navigate to the "AI Planner" tab
2. Fill in your farm details:
   - Select location method (GPS or village)
   - Enter land area in acres
   - Enter your budget in Rupees
   - Optionally specify crop preferences
3. Click "Generate Agroforestry Plan"
4. Review your personalized recommendations:
   - Soil improvement tips
   - Recommended tree and crop combinations
   - Economic projections
   - Sustainability benefits
   - Next steps for implementation

## Key Features

### Multilingual Support
- Available in English, Hindi, Marathi, Telugu, and Kannada
- Change language using the buttons in the header

### Real-time Data Integration
- Soil data from ISRIC SoilGrids
- Weather data from NASA POWER
- Automatic geolocation detection

### Personalized Recommendations
- AI-powered agroforestry planning
- Economic projections based on your budget
- Sustainability metrics for environmental impact
- Step-by-step implementation guide

### Mobile-Friendly Design
- Responsive layout works on phones and tablets
- Touch-friendly interface for field use
- Optimized for rural network conditions

## Troubleshooting

### Common Issues:

1. **Location not detected**:
   - Ensure browser location services are enabled
   - Check browser permissions for the website
   - Manually enter GPS coordinates if needed

2. **Plan generation fails**:
   - Verify all required fields are filled
   - Check internet connection
   - Ensure GPS coordinates are valid numbers

3. **Language not changing**:
   - Refresh the page after changing language
   - Clear browser cache if issues persist

### Error Messages:

- "Please fill all required fields": Make sure land area and budget are entered
- "Please enter valid coordinates": Ensure latitude and longitude are valid numbers
- "Please enter valid numbers": Check that land area and budget are numeric

## Best Practices

1. **For Accurate Recommendations**:
   - Provide as accurate location information as possible
   - Enter realistic budget figures
   - Specify crop preferences if you have them

2. **For Implementation**:
   - Follow the "Next Steps" section of your plan
   - Start with soil improvement recommendations
   - Consider economic projections when making decisions

3. **For Ongoing Use**:
   - Update your farm profile as conditions change
   - Generate new plans seasonally
   - Track your progress using the dashboard

## Technical Information

### Data Sources:
- Soil data: ISRIC SoilGrids API
- Weather data: NASA POWER API
- Geolocation: Browser geolocation services

### AI Model:
- Combines soil, weather, and economic data
- Provides personalized agroforestry recommendations
- Continuously improving with user feedback

### Security:
- All data stored securely on Firebase
- User authentication with email and password
- Optional blockchain verification for premium features

## Support

For technical issues or questions about using Sasya-Mitra:
1. Check this user guide
2. Contact support through the feedback form
3. Refer to the documentation in the GitHub repository

## Feedback

We're constantly improving Sasya-Mitra based on user feedback. If you have suggestions or encounter issues:
1. Use the feedback form in the app
2. Submit issues on GitHub
3. Contact our support team

Thank you for using Sasya-Mitra to improve your farming practices and increase your productivity!