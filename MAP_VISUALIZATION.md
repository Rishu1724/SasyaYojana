# Land Layout Map Visualization in Sasya-Mitra

This document explains how the interactive land layout map visualization works in Sasya-Mitra, showing real-time AI recommendations for crop layouts.

## Overview

The map visualization feature dynamically displays recommended land use layouts based on AI predictions from soil data, weather conditions, and economic factors. It uses Folium and GeoPandas to generate interactive HTML maps showing the optimal distribution of:

- Main crops (60% of area) - 🟩 Green
- Intercrops (25% of area) - 🟨 Yellow
- Trees (15% of area) - 🌲 Dark Green

## Architecture

```
Soil Sensor Data / Weather API / User Inputs
        ↓
AI Recommendation Engine
(generate_recommendation)
        ↓
Layout Ratios or Grid
        ↓
Map Visualization (Folium + GeoPandas)
        ↓
HTML / Web UI or Firebase Dashboard
```

## Components

### 1. Land Layout Mapper (`models/map_visualization/land_layout_mapper.py`)

This Python module generates interactive maps based on AI recommendations:

- **generate_land_polygon()**: Creates a polygon representation of the farm based on GPS coordinates and area
- **calculate_layout_ratios()**: Determines area distribution for different land use types
- **create_land_use_polygons()**: Divides the land into sub-polygons for crops, intercrops, and trees
- **generate_interactive_map()**: Creates an interactive Folium map with color-coded land use areas
- **save_map()**: Exports the map as an HTML file

### 2. Map API (`models/api/map_api.py`)

Flask API endpoints for generating and serving maps:

- **POST /api/generate-land-layout-map**: Generates a new map based on input data
- **GET /api/get-map/<filename>**: Serves a specific map file
- **GET /api/latest-map**: Serves the most recently generated map

### 3. Dashboard Integration (`src/components/Dashboard.jsx`)

The React frontend displays the map in the "Farm Map" tab with an iframe and refresh button.

## How It Works

1. **Data Collection**: Soil, weather, and economic data are collected from sensors, APIs, or user input
2. **AI Processing**: The recommendation engine processes this data to determine optimal crops and layout
3. **Map Generation**: The land layout mapper creates a visual representation of the recommended layout
4. **Display**: The map is served through the API and displayed in the web dashboard

## Real-time Updates

The map automatically updates when AI predictions change due to:
- Soil condition updates
- Weather pattern changes
- Economic data adjustments

## API Usage

### Generate a New Map

```bash
curl -X POST http://localhost:5001/api/generate-land-layout-map \
  -H "Content-Type: application/json" \
  -d '{
    "center_lat": 12.971,
    "center_lon": 77.592,
    "land_area_acres": 5.0,
    "location": "Bangalore, India",
    "soil_data": {
      "ph": 6.7,
      "organic_carbon": 1.2,
      "nitrogen": 150,
      "phosphorus": 40,
      "potassium": 200,
      "texture": "Loam",
      "drainage": "Moderate"
    },
    "weather_data": {
      "rainfall_mm": 850,
      "temperature_c": 28,
      "humidity": 65,
      "solar_radiation": 5.5
    },
    "economic_data": {
      "budget_inr": 60000,
      "labor_availability": "Medium",
      "input_cost_type": "Organic"
    }
  }'
```

### View the Latest Map

Visit `http://localhost:5001/api/latest-map` in your browser to see the most recent map.

## File Structure

```
models/
├── map_visualization/
│   ├── land_layout_mapper.py
│   ├── requirements.txt
│   └── generated_maps/
│       └── sasyayojana_live_map_*.html
├── api/
│   └── map_api.py
└── recommendation/
    └── engine.py
```

## Installation

1. Install required dependencies:
   ```bash
   pip install folium geopandas shapely
   ```

2. Or run the installation script:
   ```bash
   python install_map_dependencies.py
   ```

## Testing

Run the test scripts to verify functionality:
```bash
python test_map_visualization.py
python test_map_api.py
```

## Starting the Services

1. Start the map API server:
   ```bash
   python models/api/map_api.py
   ```

2. Start the main application:
   ```bash
   npm run dev
   ```

The map visualization will be available in the "Farm Map" tab of the dashboard.