import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from './firebase';
import LanguageSelector from './components/LanguageSelector';
import Login from './components/Login';
import Signup from './components/Signup';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const { t, i18n } = useTranslation();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authMode, setAuthMode] = useState('login'); // 'login' or 'signup'
  const [showLanguageSelection, setShowLanguageSelection] = useState(true);

  // Check auth state on app load
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });

    // Cleanup subscription on unmount
    return () => unsubscribe();
  }, []);

  const switchToLogin = () => setAuthMode('login');
  const switchToSignup = () => setAuthMode('signup');
  const handleLanguageSelected = () => setShowLanguageSelection(false);

  if (loading) {
    return (
      <div className="min-h-screen bg-green-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // If user is authenticated, show dashboard
  if (user) {
    return <Dashboard />;
  }

  // Show language selection first
  if (showLanguageSelection) {
    return <LanguageSelector onLanguageSelected={handleLanguageSelected} />;
  }

  return (
    <div className="min-h-screen bg-green-50 flex flex-col items-center justify-center p-4">
      <header className="w-full max-w-4xl mb-8 text-center">
        <h1 className="text-3xl md:text-4xl font-bold text-green-800 mb-2">
          Sasya-Mitra (सस्य-मित्र)
        </h1>
        <p className="text-lg text-green-600">
          {t('tagline')}
        </p>
        {/* Notification about dataset integration */}
        <div className="mt-4 p-3 bg-blue-100 rounded-lg text-blue-800 text-sm">
          <p>ℹ️ {t('datasetsIntegrated')}</p>
          <p className="mt-1">{t('aiModelsPersonalized')}</p>
        </div>
      </header>
      
      <main className="w-full max-w-2xl">
        {authMode === 'login' ? (
          <Login onSwitchToSignup={switchToSignup} />
        ) : (
          <Signup onSwitchToLogin={switchToLogin} />
        )}
        
        <div className="bg-white rounded-xl shadow-md p-6 md:p-8 mt-6">
          <div className="border-t border-gray-200 pt-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-3">
              {t('features')}
            </h3>
            <ul className="grid grid-cols-1 md:grid-cols-2 gap-3 text-gray-600">
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>{t('multilingualSupport')}</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>{t('aiPlanning')}</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>{t('secureData')}</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>{t('blockchain')}</span>
              </li>
            </ul>
          </div>
        </div>
      </main>
      
      <footer className="mt-8 text-center text-gray-500 text-sm">
        <p>{t('footer')}</p>
      </footer>
    </div>
  );
}

export default App;