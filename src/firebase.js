// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyC_afRd0Ss4wk85D-940qtbSQPH_DUtMcU",
  authDomain: "sasyayojana-79840.firebaseapp.com",
  projectId: "sasyayojana-79840",
  storageBucket: "sasyayojana-79840.firebasestorage.app",
  messagingSenderId: "722672208125",
  appId: "1:722672208125:web:856be97e10465e89eb9694",
  measurementId: "G-71RGGWLD25"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Initialize Firebase services
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);

export default app;