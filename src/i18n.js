import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import enTranslation from './locales/en.json';
import hiTranslation from './locales/hi.json';
import mrTranslation from './locales/mr.json';
import teTranslation from './locales/te.json';
import knTranslation from './locales/kn.json';

// The translations
const resources = {
  en: {
    translation: enTranslation
  },
  hi: {
    translation: hiTranslation
  },
  mr: {
    translation: mrTranslation
  },
  te: {
    translation: teTranslation
  },
  kn: {
    translation: knTranslation
  }
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next) // passes i18n down to react-i18next
  .init({
    resources,
    fallbackLng: "en", // fallback language if translation is missing
    interpolation: {
      escapeValue: false // react already safes from xss
    },
    detection: {
      // cache user language
      caches: ['localStorage', 'cookie'],
      // key to store the language in localStorage
      lookupLocalStorage: 'i18nextLng',
      // key to store the language in cookie
      lookupCookie: 'i18nextLng',
      // cookie options
      cookieMinutes: 60 * 24 * 30, // 30 days
      // cookie domain
      // cookieDomain: 'myDomain'
    }
  });

export default i18n;