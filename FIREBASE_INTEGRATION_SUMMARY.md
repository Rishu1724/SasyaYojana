# Firebase Integration Summary for SasyaYojana

This document outlines how the SasyaYojana application stores all data in Firebase.

## Firebase Services Used

1. **Firebase Authentication** - For user authentication
2. **Cloud Firestore** - For storing structured data
3. **Firebase Storage** - For storing map HTML files

## Data Storage Implementation

### 1. Land Layout Maps

All land layout maps are stored in Firebase with the following structure:

#### Firestore Collection: `land_layout_maps`

Each document contains:
- `center_lat`: Latitude of the farm center
- `center_lon`: Longitude of the farm center
- `land_area_acres`: Size of the farm in acres
- `location`: Location name
- `soil_data`: Soil characteristics
- `weather_data`: Weather conditions
- `economic_data`: Economic factors
- `recommendation`: AI-generated recommendations
- `filename`: Name of the HTML map file
- `map_file_url`: Public URL to the map file in Firebase Storage
- `created_at`: Timestamp when the map was created
- `user_id`: ID of the authenticated user (if available)

#### Firebase Storage: `land-layout-maps/`

Each map is stored as an HTML file with the naming convention:
`{document_id}.html`

### 2. Implementation Details

#### Frontend (React)

- **File**: `src/services/mapStorageService.js`
- **Function**: `storeMap(mapData, mapFilePath)`
  - Reads the HTML file content
  - Stores metadata in Firestore
  - Uploads HTML file to Firebase Storage
  - Updates Firestore document with file URL

#### Backend (Python Flask API)

- **File**: `models/api/map_api.py`
- **Function**: `store_map_in_firebase(map_data, map_html, filename)`
  - Stores metadata in Firestore
  - Uploads HTML file to Firebase Storage
  - Makes file publicly accessible

- **File**: `models/map_visualization/land_layout_mapper.py`
- **Function**: `get_real_time_recommendation_and_map()`
  - Generates map and stores in Firebase when available

### 3. Data Flow

1. User clicks "Generate Land Layout Map" in Dashboard
2. Dashboard sends request to Flask API with farm data
3. API generates AI recommendations and map visualization
4. Map HTML file is saved locally
5. Map metadata and HTML content are stored in Firebase:
   - Metadata → Firestore document
   - HTML file → Firebase Storage
6. Firebase Storage URL is returned to frontend
7. Frontend displays the map from Firebase Storage

## Benefits of Firebase Integration

1. **Persistence**: All maps are permanently stored and accessible
2. **Scalability**: Firebase automatically scales with usage
3. **Real-time**: Data is immediately available across all devices
4. **Security**: Firebase security rules protect user data
5. **Offline Support**: Future implementation can support offline access
6. **Cross-Platform**: Works on web, mobile, and other platforms

## Future Enhancements

1. **User-Specific Maps**: Associate maps with specific user accounts
2. **Map Sharing**: Enable users to share maps with others
3. **Versioning**: Store multiple versions of maps for the same location
4. **Analytics**: Track map usage and user engagement
5. **Search**: Enable searching maps by location, date, or crop type