// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCmpD9yB1d3uF83HP4RTDKwA7bs8eRT4i4",
  authDomain: "quiz-system-e9cfb.firebaseapp.com",
  projectId: "quiz-system-e9cfb",
  storageBucket: "quiz-system-e9cfb.firebasestorage.app",
  messagingSenderId: "292267390936",
  appId: "1:292267390936:web:f2544e974d08dafcc7e4ad",
  measurementId: "G-X28MB1VJ70"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
export const auth = getAuth(app);
export const db = getFirestore(app);

export default app;
