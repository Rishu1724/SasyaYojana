import React from 'react';
import { useTranslation } from 'react-i18next';

const Dashboard = () => {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-green-50 p-4">
      <header className="w-full max-w-6xl mx-auto mb-8">
        <div className="flex justify-between items-center py-4">
          <h1 className="text-2xl md:text-3xl font-bold text-green-800">
            Sasya-Mitra Dashboard
          </h1>
          <button className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition duration-300">
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
        
        <div className="bg-white rounded-xl shadow-md p-6">
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
      </main>
    </div>
  );
};

export default Dashboard;