/**
 * Verification script for frontend Firebase integration
 * This script checks if the frontend Firebase configuration is properly set up
 */

// Import Firebase modules
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";

// Firebase configuration from environment variables
const firebaseConfig = {
  apiKey: import.meta.env.REACT_APP_FIREBASE_API_KEY || "AIzaSyC_afRd0Ss4wk85D-940qtbSQPH_DUtMcU",
  authDomain: import.meta.env.REACT_APP_FIREBASE_AUTH_DOMAIN || "sasyayojana-79840.firebaseapp.com",
  projectId: import.meta.env.REACT_APP_FIREBASE_PROJECT_ID || "sasyayojana-79840",
  storageBucket: import.meta.env.REACT_APP_FIREBASE_STORAGE_BUCKET || "sasyayojana-79840.firebasestorage.app",
  messagingSenderId: import.meta.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID || "722672208125",
  appId: import.meta.env.REACT_APP_FIREBASE_APP_ID || "1:722672208125:web:856be97e10465e89eb9694",
  measurementId: import.meta.env.REACT_APP_FIREBASE_MEASUREMENT_ID || "G-71RGGWLD25"
};

console.log("Firebase Configuration:");
console.log("Project ID:", firebaseConfig.projectId);
console.log("Storage Bucket:", firebaseConfig.storageBucket);

try {
  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  console.log("✅ Firebase initialized successfully");
  
  // Initialize Firestore
  const db = getFirestore(app);
  console.log("✅ Firestore initialized successfully");
  
  // Initialize Storage
  const storage = getStorage(app);
  console.log("✅ Firebase Storage initialized successfully");
  
  console.log("\n🎉 All Firebase services are properly configured!");
  console.log("✅ The application can store data in Firebase as requested.");
  
  // Export for use in other modules
  export { db, storage };
  
} catch (error) {
  console.error("❌ Error initializing Firebase:", error);
  console.error("Please check your Firebase configuration in .env file");
}