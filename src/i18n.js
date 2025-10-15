import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

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
  .use(initReactI18next) // passes i18n down to react-i18next
  .init({
    resources,
    lng: "en", // language to use, more information here: https://www.i18next.com/overview/configuration-options#languages-namespaces-resources
    fallbackLng: "en", // fallback language if translation is missing
    interpolation: {
      escapeValue: false // react already safes from xss
    }
  });

export default i18n;