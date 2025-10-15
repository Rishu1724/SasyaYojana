import React from 'react';
import { useTranslation } from 'react-i18next';
import { auth } from '../firebase';
import { signOut } from 'firebase/auth';
import { GoogleMap, LoadScript, Marker, Polygon } from '@react-google-maps/api';

// Map container style
const mapContainerStyle = {
  width: '100%',
  height: '400px'
};

// Example center of map (India)
const center = { lat: 20.5937, lng: 78.9629 };

// Example farm polygon (replace with dynamic farmer input)
const farmPolygon = [
  { lat: 20.60, lng: 78.95 },
  { lat: 20.61, lng: 78.95 },
  { lat: 20.61, lng: 78.97 },
  { lat: 20.60, lng: 78.97 }
];

const Dashboard = () => {
  const { t } = useTranslation();

  const handleLogout = async () => {
    try {
      await signOut(auth);
      console.log('User logged out successfully');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <div className="min-h-screen bg-green-50 p-4">
      <header className="w-full max-w-6xl mx-auto mb-8">
        <div className="flex justify-between items-center py-4">
          <h1 className="text-2xl md:text-3xl font-bold text-green-800">
            Sasya-Mitra Dashboard
          </h1>
          <button 
            onClick={handleLogout}
            className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition duration-300"
          >
            Logout
          </button>
        </div>
      </header>
      
      <main className="w-full max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Farm Profile</h2>
            <p className="text-gray-600 mb-4">Manage your farm details and land information</p>
            <button className="text-green-600 hover:text-green-700 font-medium">
              View Details →
            </button>
          </div>
          
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">AI Planning</h2>
            <p className="text-gray-600 mb-4">Generate land-use plans with AI assistance</p>
            <button className="text-green-600 hover:text-green-700 font-medium">
              Create Plan →
            </button>
          </div>
          
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">My Plans</h2>
            <p className="text-gray-600 mb-4">View and manage your farming plans</p>
            <button className="text-green-600 hover:text-green-700 font-medium">
              View Plans →
            </button>
          </div>
        </div>
        
        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Activity</h2>
          <div className="space-y-4">
            <div className="border-b border-gray-100 pb-4">
              <h3 className="font-medium text-gray-800">New Plan Generated</h3>
              <p className="text-gray-600 text-sm">2 hours ago</p>
            </div>
            <div className="border-b border-gray-100 pb-4">
              <h3 className="font-medium text-gray-800">Farm Profile Updated</h3>
              <p className="text-gray-600 text-sm">1 day ago</p>
            </div>
            <div>
              <h3 className="font-medium text-gray-800">Account Created</h3>
              <p className="text-gray-600 text-sm">3 days ago</p>
            </div>
          </div>
        </div>

        {/* ================= GOOGLE MAP SECTION ================= */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Farm Map</h2>
          <LoadScript googleMapsApiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
  <GoogleMap mapContainerStyle={mapContainerStyle} center={center} zoom={6}>
    <Polygon
      paths={farmPolygon}
      options={{
        fillColor: '#34D399',
        fillOpacity: 0.3,
        strokeColor: '#059669',
        strokeWeight: 2
      }}
    />
    <Marker position={{ lat: 20.605, lng: 78.955 }} />
    <Marker position={{ lat: 20.607, lng: 78.965 }} />
  </GoogleMap>
</LoadScript>     
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
