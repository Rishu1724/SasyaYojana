import React from 'react';
import { useTranslation } from 'react-i18next';
import { FaGlobe } from 'react-icons/fa'; // globe icon for theme

const LanguageSelector = () => {
  const { t, i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  const languages = [
    { code: 'en', label: t('english') },
    { code: 'hi', label: t('hindi') },
    { code: 'mr', label: t('marathi') },
    { code: 'te', label: t('telugu') },
    { code: 'kn', label: t('kannada') },
  ];

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-b from-yellow-50 to-orange-50 p-6">
      {/* Header */}
      <div className="flex items-center space-x-3 mb-8">
        <FaGlobe className="text-orange-500 text-4xl animate-spin-slow" />
        <h1 className="text-3xl sm:text-4xl font-extrabold text-orange-700 drop-shadow-lg text-center">
          SasyaYojana
        </h1>
      </div>

      {/* Subtitle */}
      <p className="text-orange-800 text-center text-lg sm:text-xl mb-6 max-w-md">
        {t('selectLanguage')} - {t('experienceAIforSmartFarming')}
      </p>

      {/* Language buttons */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 w-full max-w-md">
        {languages.map((lang) => (
          <button
            key={lang.code}
            onClick={() => changeLanguage(lang.code)}
            className={`py-3 px-5 rounded-2xl font-semibold text-lg flex justify-center items-center transition duration-300
              ${
                i18n.language === lang.code
                  ? 'bg-gradient-to-r from-orange-400 to-yellow-400 text-white shadow-lg scale-105'
                  : 'bg-white border border-orange-400 text-orange-600 hover:bg-gradient-to-r hover:from-orange-100 hover:to-yellow-100 hover:scale-105'
              }`}
          >
            {lang.label}
          </button>
        ))}
      </div>

      {/* Footer */}
      <p className="mt-10 text-orange-700 text-sm sm:text-base text-center max-w-xs italic">
        🌱 {t('poweredByAI')} - {t('sustainableFarming')}
      </p>
    </div>
  );
};

export default LanguageSelector;
