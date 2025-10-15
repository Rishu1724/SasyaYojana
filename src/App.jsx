import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import LanguageSelector from './components/LanguageSelector';
import Login from './components/Login';
import Signup from './components/Signup';
import './App.css';

function App() {
  const { t } = useTranslation();
  const [showAuth, setShowAuth] = useState(false);
  const [authMode, setAuthMode] = useState('login'); // 'login' or 'signup'

  const switchToLogin = () => setAuthMode('login');
  const switchToSignup = () => setAuthMode('signup');

  return (
    <div className="min-h-screen bg-green-50 flex flex-col items-center justify-center p-4">
      <header className="w-full max-w-4xl mb-8 text-center">
        <h1 className="text-3xl md:text-4xl font-bold text-green-800 mb-2">
          Sasya-Mitra (सस्य-मित्र)
        </h1>
        <p className="text-lg text-green-600">
          {t('tagline')}
        </p>
      </header>
      
      <main className="w-full max-w-2xl">
        {!showAuth ? (
          <div className="bg-white rounded-xl shadow-md p-6 md:p-8 text-center">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              {t('welcome')}
            </h2>
            <p className="text-gray-600 mb-6">
              Your trusted companion for sustainable farming practices and land-use planning.
            </p>
            
            <LanguageSelector />
            
            <button 
              onClick={() => setShowAuth(true)}
              className="bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-8 rounded-lg transition duration-300"
            >
              {t('continue')}
            </button>
          </div>
        ) : authMode === 'login' ? (
          <Login onSwitchToSignup={switchToSignup} />
        ) : (
          <Signup onSwitchToLogin={switchToLogin} />
        )}
        
        {!showAuth && (
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
        )}
      </main>
      
      <footer className="mt-8 text-center text-gray-500 text-sm">
        <p>{t('footer')}</p>
      </footer>
    </div>
  );
}

export default App;