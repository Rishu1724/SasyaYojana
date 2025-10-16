"""
Test script to verify Firebase storage integration
"""

import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import Firebase Admin SDK
try:
    import firebase_admin
    from firebase_admin import credentials, firestore, storage
    FIREBASE_AVAILABLE = True
    print("✅ Firebase Admin SDK available")
except ImportError:
    FIREBASE_AVAILABLE = False
    print("❌ Firebase Admin SDK not available")

def test_firebase_initialization():
    """Test Firebase initialization"""
    if not FIREBASE_AVAILABLE:
        print("❌ Firebase not available, skipping tests")
        return False
    
    try:
        # Initialize Firebase Admin SDK if not already initialized
        if not firebase_admin._apps:
            # Try to initialize with default credentials
            try:
                firebase_admin.initialize_app()
                print("✅ Firebase initialized with default credentials")
            except Exception as e:
                print(f"❌ Could not initialize Firebase with default credentials: {e}")
                return False
        
        # Test Firestore connection
        db = firestore.client()
        print("✅ Firestore client initialized")
        
        # Test Storage connection
        bucket = storage.bucket('sasyayojana-79840.firebasestorage.app')
        print("✅ Firebase Storage bucket connected")
        
        return True
    except Exception as e:
        print(f"❌ Error testing Firebase: {e}")
        return False

def test_firestore_write():
    """Test writing data to Firestore"""
    if not FIREBASE_AVAILABLE:
        return False
    
    try:
        db = firestore.client()
        
        # Create test document
        test_data = {
            'test_name': 'Firebase Storage Test',
            'timestamp': datetime.now().isoformat(),
            'test_data': {
                'value1': 'test',
                'value2': 123
            }
        }
        
        # Write to Firestore
        doc_ref = db.collection('test_collection').document()
        doc_ref.set(test_data)
        print(f"✅ Test document written to Firestore with ID: {doc_ref.id}")
        
        # Read back the document
        doc = doc_ref.get()
        if doc.exists:
            print("✅ Test document read back successfully")
            print(f"   Document data: {doc.to_dict()}")
            return True
        else:
            print("❌ Test document not found after writing")
            return False
    except Exception as e:
        print(f"❌ Error testing Firestore write: {e}")
        return False

def test_storage_upload():
    """Test uploading file to Firebase Storage"""
    if not FIREBASE_AVAILABLE:
        return False
    
    try:
        bucket = storage.bucket('sasyayojana-79840.firebasestorage.app')
        
        # Create test content
        test_content = "<html><body><h1>Test Map File</h1><p>This is a test file for Firebase Storage.</p></body></html>"
        test_filename = f"test_map_{int(datetime.now().timestamp())}.html"
        
        # Upload to Firebase Storage
        blob = bucket.blob(f'test-files/{test_filename}')
        blob.upload_from_string(test_content, content_type='text/html')
        blob.make_public()
        
        print(f"✅ Test file uploaded to Firebase Storage: {test_filename}")
        print(f"   Public URL: {blob.public_url}")
        
        # Verify file exists
        if blob.exists():
            print("✅ Test file verified in Firebase Storage")
            return True
        else:
            print("❌ Test file not found in Firebase Storage")
            return False
    except Exception as e:
        print(f"❌ Error testing Firebase Storage upload: {e}")
        return False

def main():
    """Main test function"""
    print("Testing Firebase Storage Integration...")
    print("=" * 50)
    
    # Test Firebase initialization
    if not test_firebase_initialization():
        print("❌ Firebase initialization failed")
        return
    
    # Test Firestore write
    if not test_firestore_write():
        print("❌ Firestore write test failed")
        return
    
    # Test Storage upload
    if not test_storage_upload():
        print("❌ Firebase Storage upload test failed")
        return
    
    print("=" * 50)
    print("🎉 All Firebase integration tests passed!")
    print("✅ Firebase is properly configured for storing all application data")

if __name__ == "__main__":
    main()