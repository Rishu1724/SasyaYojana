# Firebase Setup Instructions for SasyaYojana

This document provides instructions for setting up Firebase integration in the SasyaYojana application.

## Frontend Firebase Setup (Already Configured)

The frontend Firebase integration is already configured in the application:

- **File**: `src/firebase.js`
- **Configuration**: Uses API keys from `.env` file

The frontend can already:
- Authenticate users
- Store map metadata in Firestore
- Upload map files to Firebase Storage

## Backend Firebase Setup (Required for Full Integration)

To enable full Firebase integration in the Python backend, you need to set up Application Default Credentials.

### Option 1: Using Service Account Key (Recommended for Development)

1. **Create a Service Account Key**:
   - Go to the Firebase Console
   - Navigate to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Save the JSON file securely

2. **Set Environment Variable**:
   ```bash
   # On Windows (PowerShell)
   $env:GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
   
   # On macOS/Linux
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
   ```

3. **Verify Setup**:
   Run the test script:
   ```bash
   cd SasyaYojana
   python test_firebase_storage.py
   ```

### Option 2: Using Google Cloud SDK (Recommended for Production)

1. **Install Google Cloud SDK**:
   Download and install from: https://cloud.google.com/sdk/docs/install

2. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth application-default login
   ```

3. **Set Project**:
   ```bash
   gcloud config set project sasyayojana-79840
   ```

### Option 3: Using Firebase Admin SDK Credentials

If you prefer to use explicit credentials in the code:

1. **Modify `models/api/map_api.py`**:
   ```python
   if FIREBASE_AVAILABLE:
       try:
           # Initialize Firebase Admin SDK with service account
           cred = credentials.Certificate("path/to/serviceAccountKey.json")
           firebase_admin.initialize_app(cred)
           
           # Initialize Firestore and Storage
           db = firestore.client()
           bucket = storage.bucket('sasyayojana-79840.firebasestorage.app')
           maps_collection = db.collection('land_layout_maps')
   ```

## Firebase Storage Rules

Ensure your Firebase Storage rules allow read/write access:

```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read, write: if request.auth != null;
    }
    
    // Public read access for map files
    match /land-layout-maps/{mapId} {
      allow read: if true;  // Public read
      allow write: if request.auth != null;  // Authenticated write
    }
  }
}
```

## Firestore Security Rules

Ensure your Firestore rules allow appropriate access:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow authenticated users to read/write their own data
    match /land_layout_maps/{mapId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## Testing Firebase Integration

After setting up credentials, test the integration:

```bash
cd SasyaYojana
python test_firebase_storage.py
```

Expected output:
```
✅ Firebase Admin SDK available
Testing Firebase Storage Integration...
==================================================
✅ Firebase initialized with default credentials
✅ Firestore client initialized
✅ Firebase Storage bucket connected
✅ Test document written to Firestore with ID: xxx
✅ Test document read back successfully
✅ Test file uploaded to Firebase Storage: test_map_xxx.html
✅ Test file verified in Firebase Storage
==================================================
🎉 All Firebase integration tests passed!
✅ Firebase is properly configured for storing all application data
```

## Troubleshooting

### Common Issues

1. **"Your default credentials were not found"**:
   - Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
   - Verify the path to the service account key file is correct

2. **"Permission denied"**:
   - Check Firebase Security Rules
   - Ensure the service account has proper permissions

3. **"Bucket not found"**:
   - Verify the bucket name in the code matches your Firebase Storage bucket

### Verifying Firebase Integration

Once properly configured, the application will:
- Store map metadata in Firestore when maps are generated
- Upload map HTML files to Firebase Storage
- Make map files publicly accessible via URLs
- Associate maps with user accounts when authenticated

All data will be persistently stored in Firebase and accessible from any device.