# Sasya-Mitra: AI-Driven Agricultural Assistant

Sasya-Mitra is an advanced agricultural AI system that helps farmers make informed decisions about crop selection, planting schedules, and resource allocation. Built with modern technologies, it provides personalized recommendations based on location, soil conditions, weather data, and economic factors.

## Features

- 🌍 **Location-based Analysis**: Uses GPS coordinates to provide region-specific recommendations
- 🌱 **Soil Analysis**: Integrates with ISRIC SoilGrids API for detailed soil property analysis
- ☀️ **Weather Integration**: Uses NASA POWER API for accurate climate data
- 🤖 **AI-Powered Recommendations**: Machine learning models for crop yield and ROI prediction
- 🌳 **Agroforestry Planning**: Comprehensive agroforestry system design
- 🗺️ **Interactive Land Layout Maps**: Visualizes crop layout recommendations with real-time updates
- 💰 **Economic Projections**: Investment analysis and return on investment calculations
- ♻️ **Sustainability Metrics**: Environmental impact assessment
- 🌐 **Multi-language Support**: Available in English, Hindi, Marathi, Telugu, and Kannada
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🔐 **Secure Authentication**: Firebase Authentication for user accounts
- ☁️ **Cloud Storage**: All maps and data stored in Firebase Cloud Storage
- 🔄 **Continuous Learning**: Improves predictions based on farmer feedback

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- npm or yarn
- Firebase account
- API keys for:
  - NASA POWER API
  - OpenWeatherMap API
  - ISRIC SoilGrids API

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/sasya-mitra.git
   cd sasya-mitra
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up Firebase:
   - Create a Firebase project at https://console.firebase.google.com/
   - Add your Firebase configuration to `src/firebase.js`
   - Enable Authentication (Email/Password and Google)
   - Enable Firestore Database
   - Enable Firebase Storage

5. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your API keys:
     ```
     VITE_WEATHER_API_KEY=your_openweathermap_api_key
     ```

6. Set up Firebase Admin SDK (for backend integration):
   - See [FIREBASE_SETUP_INSTRUCTIONS.md](FIREBASE_SETUP_INSTRUCTIONS.md) for detailed setup instructions

## Dataset Integration

Sasya-Mitra uses several agricultural datasets to power its AI models:

1. NASA POWER Data (Rainfall, Temperature, Humidity, Radiation)
2. All India level Average Yield of Principal Crops (2001-2015)
3. All India level Area Under Principal Crops (2001-2015)
4. Production of principle crops
5. Crop price data (Agmarknet)
6. Natural disaster damage data

See [DATASET_INTEGRATION_SUMMARY.md](DATASET_INTEGRATION_SUMMARY.md) for detailed information on how these datasets are integrated.

## Model Training

To train the AI models with your datasets:

1. Place your datasets in the `data/` directory
2. Run the preprocessing script:
   ```bash
   npm run model:process-data
   ```

3. Train the models:
   ```bash
   npm run model:train
   ```

## Continuous Learning

Sasya-Mitra implements a continuous learning system that improves prediction accuracy over time:

1. **Data Collection**: Prediction results and farmer feedback are stored in Firebase Firestore
2. **Model Retraining**: Models are periodically retrained with collected feedback data
3. **Accuracy Improvement**: Real feedback leads to better predictions

To start the continuous learning scheduler:
```bash
npm run model:schedule-retraining
```

See [CONTINUOUS_LEARNING_IMPLEMENTATION.md](CONTINUOUS_LEARNING_IMPLEMENTATION.md) for detailed implementation information.

## Running the Application

1. Start the AI model API server:
   ```bash
   python models/api/app.py
   ```

2. In a new terminal, start the frontend development server:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:5173`

## Building for Production

To create a production build:

```bash
npm run build
```

To preview the production build locally:

```bash
npm run preview
```

## Project Structure

```
sasya-mitra/
├── data/                 # Agricultural datasets
├── models/               # AI models and training scripts
│   ├── preprocessing/    # Data preprocessing utilities
│   ├── training/         # Model training implementations
│   ├── recommendation/   # Recommendation engine
│   ├── map_visualization/ # Interactive map generation
│   └── api/             # Flask API for model serving
├── src/                  # Frontend source code
│   ├── components/       # React components
│   ├── services/         # Service integrations
│   ├── locales/          # Translation files
│   └── firebase.js       # Firebase configuration
├── public/               # Static assets
├── docs/                 # Documentation
└── tests/                # Test files
```

## Technologies Used

- **Frontend**: React, Tailwind CSS, Firebase SDK
- **Backend**: Python, Flask, Scikit-learn, XGBoost
- **Data Sources**: NASA POWER API, ISRIC SoilGrids API, OpenWeatherMap API
- **Database**: Firebase Firestore
- **Authentication**: Firebase Authentication
- **Mapping**: Folium, GeoPandas for interactive land layout visualization
- **Deployment**: Vite, Firebase Hosting (optional)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue on the GitHub repository or contact the maintainers.