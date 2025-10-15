import React from 'react';
import { useTranslation } from 'react-i18next';

const LanguageSelector = () => {
  const { t, i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <div className="mb-8 w-full max-w-md">
      <h2 className="text-xl font-semibold text-gray-800 mb-4 text-center">
        {t('selectLanguage')}
      </h2>
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        <button
          onClick={() => changeLanguage('en')}
          className={`py-3 px-4 rounded-lg transition duration-300 ${
            i18n.language === 'en'
              ? 'bg-green-600 text-white'
              : 'bg-white border border-green-600 text-green-600 hover:bg-green-50'
          }`}
        >
          {t('english')}
        </button>
        <button
          onClick={() => changeLanguage('hi')}
          className={`py-3 px-4 rounded-lg transition duration-300 ${
            i18n.language === 'hi'
              ? 'bg-green-600 text-white'
              : 'bg-white border border-green-600 text-green-600 hover:bg-green-50'
          }`}
        >
          {t('hindi')}
        </button>
        <button
          onClick={() => changeLanguage('mr')}
          className={`py-3 px-4 rounded-lg transition duration-300 ${
            i18n.language === 'mr'
              ? 'bg-green-600 text-white'
              : 'bg-white border border-green-600 text-green-600 hover:bg-green-50'
          }`}
        >
          {t('marathi')}
        </button>
        <button
          onClick={() => changeLanguage('te')}
          className={`py-3 px-4 rounded-lg transition duration-300 ${
            i18n.language === 'te'
              ? 'bg-green-600 text-white'
              : 'bg-white border border-green-600 text-green-600 hover:bg-green-50'
          }`}
        >
          {t('telugu')}
        </button>
        <button
          onClick={() => changeLanguage('kn')}
          className={`py-3 px-4 rounded-lg transition duration-300 col-span-2 sm:col-span-1 ${
            i18n.language === 'kn'
              ? 'bg-green-600 text-white'
              : 'bg-white border border-green-600 text-green-600 hover:bg-green-50'
          }`}
        >
          {t('kannada')}
        </button>
      </div>
    </div>
  );
};

export default LanguageSelector;