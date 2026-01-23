// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBsxokS9iRLeqTVJrwwgplwohQA3JO8zow",
  authDomain: "quiz-system-78263.firebaseapp.com",
  projectId: "quiz-system-78263",
  storageBucket: "quiz-system-78263.firebasestorage.app",
  messagingSenderId: "392714808244",
  appId: "1:392714808244:web:079173a3da098b120120e1",
  measurementId: "G-XC3SHZNTE1"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
export const auth = getAuth(app);

export default app;
