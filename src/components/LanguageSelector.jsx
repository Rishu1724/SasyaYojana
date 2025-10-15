import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { FaGlobe, FaLeaf, FaSeedling } from 'react-icons/fa';

const LanguageSelector = ({ onLanguageSelected }) => {
  const { t, i18n } = useTranslation();
  const [hoveredLang, setHoveredLang] = useState(null);

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    // Notify the parent component that language has been selected
    if (onLanguageSelected) {
      setTimeout(onLanguageSelected, 300); // Small delay for better UX
    }
  };

  const languages = [
    { code: 'en', label: 'English', native: 'English' },
    { code: 'hi', label: 'हिंदी', native: 'Hindi' },
    { code: 'mr', label: 'मराठी', native: 'Marathi' },
    { code: 'te', label: 'తెలుగు', native: 'Telugu' },
    { code: 'kn', label: 'ಕನ್ನಡ', native: 'Kannada' },
  ];

  return (
    <div className="min-h-screen relative overflow-hidden bg-gradient-to-br from-emerald-50 via-green-50 to-lime-50">
      {/* Decorative background elements */}
      <div className="absolute top-10 left-10 opacity-10">
        <FaLeaf className="text-green-600 text-9xl transform -rotate-12" />
      </div>
      <div className="absolute bottom-20 right-10 opacity-10">
        <FaSeedling className="text-green-600 text-9xl transform rotate-12" />
      </div>
      
      <div className="relative z-10 flex flex-col justify-center items-center min-h-screen p-6">
        {/* Logo and Brand */}
        <div className="mb-8 text-center">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-green-400 to-emerald-600 shadow-2xl mb-4 animate-pulse">
            <FaGlobe className="text-white text-4xl" />
          </div>
          <h1 className="text-5xl sm:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-green-600 via-emerald-600 to-green-700 mb-2">
            {t('appName') || 'SasyaYojana'}
          </h1>
          <div className="flex items-center justify-center space-x-2 text-green-700">
            <div className="h-px w-12 bg-green-400"></div>
            <FaSeedling className="text-green-500 text-sm" />
            <div className="h-px w-12 bg-green-400"></div>
          </div>
        </div>

        {/* Main Card */}
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-2xl p-8 sm:p-12 max-w-2xl w-full border border-green-100">
          <h2 className="text-2xl sm:text-3xl font-bold text-green-800 text-center mb-3">
            {t('selectLanguage') || 'Choose Your Language'}
          </h2>
          <p className="text-green-600 text-center text-base mb-8">
            {t('experienceAIforSmartFarming') || 'Experience AI-powered smart farming'}
          </p>

          {/* Language Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
            {languages.map((lang) => {
              const isActive = i18n.language === lang.code;
              const isHovered = hoveredLang === lang.code;
              
              return (
                <button
                  key={lang.code}
                  onClick={() => changeLanguage(lang.code)}
                  onMouseEnter={() => setHoveredLang(lang.code)}
                  onMouseLeave={() => setHoveredLang(null)}
                  className={`relative group py-5 px-6 rounded-2xl font-semibold text-lg transition-all duration-300 transform ${
                    isActive
                      ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-xl scale-105 -translate-y-1'
                      : 'bg-white border-2 border-green-200 text-green-700 hover:border-green-400 hover:shadow-lg hover:scale-102 hover:-translate-y-0.5'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex flex-col items-start">
                      <span className="text-2xl mb-1">{lang.label}</span>
                      <span className={`text-xs ${isActive ? 'text-green-100' : 'text-green-500'}`}>
                        {lang.native}
                      </span>
                    </div>
                    {isActive && (
                      <div className="flex items-center justify-center w-8 h-8 rounded-full bg-white/20">
                        <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </div>
                    )}
                  </div>
                  
                  {/* Hover effect overlay */}
                  {!isActive && isHovered && (
                    <div className="absolute inset-0 bg-gradient-to-r from-green-400/10 to-emerald-400/10 rounded-2xl"></div>
                  )}
                </button>
              );
            })}
          </div>

          {/* Features */}
          <div className="grid grid-cols-3 gap-4 pt-6 border-t border-green-100">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-green-100 mb-2">
                <FaLeaf className="text-green-600 text-xl" />
              </div>
              <p className="text-xs text-green-700 font-medium">
                {t('sustainableFarming') || 'Sustainable'}
              </p>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-emerald-100 mb-2">
                <svg className="w-6 h-6 text-emerald-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M13 7H7v6h6V7z" />
                  <path fillRule="evenodd" d="M7 2a1 1 0 012 0v1h2V2a1 1 0 112 0v1h2a2 2 0 012 2v2h1a1 1 0 110 2h-1v2h1a1 1 0 110 2h-1v2a2 2 0 01-2 2h-2v1a1 1 0 11-2 0v-1H9v1a1 1 0 11-2 0v-1H5a2 2 0 01-2-2v-2H2a1 1 0 110-2h1V9H2a1 1 0 010-2h1V5a2 2 0 012-2h2V2zM5 5h10v10H5V5z" clipRule="evenodd" />
                </svg>
              </div>
              <p className="text-xs text-green-700 font-medium">
                {t('poweredByAI') || 'AI Powered'}
              </p>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-lime-100 mb-2">
                <FaGlobe className="text-lime-600 text-xl" />
              </div>
              <p className="text-xs text-green-700 font-medium">
                {t('multilingual') || 'Multi-lingual'}
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <p className="mt-8 text-green-600 text-sm text-center max-w-md">
          {t('empoweringFarmers') || 'Empowering farmers with intelligent solutions for a sustainable future 🌾'}
        </p>
      </div>
    </div>
  );
};

export default LanguageSelector;