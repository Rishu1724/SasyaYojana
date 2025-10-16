"""
Test script to verify the API endpoints are working.
"""

import requests

def test_api():
    """Test the API endpoints."""
    try:
        # Test health endpoint
        response = requests.get('http://localhost:5000/health')
        print(f"Health endpoint status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test map endpoint
        response = requests.get('http://localhost:5000/sasyayojana_live_map.html')
        print(f"Map endpoint status: {response.status_code}")
        print(f"Content length: {len(response.text)}")
        
        return True
    except Exception as e:
        print(f"Error testing API: {e}")
        return False

if __name__ == "__main__":
    print("Testing API endpoints...")
    success = test_api()
    if success:
        print("\n✅ API tests completed successfully!")
    else:
        print("\n❌ API tests failed!")