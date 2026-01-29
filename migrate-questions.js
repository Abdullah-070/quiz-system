/**
 * Questions Migration Script
 * Migrates questions from Django API to Firestore
 * 
 * Usage: node migrate-questions.js
 */

const admin = require('firebase-admin');
const axios = require('axios');

// Initialize Firebase Admin SDK
const serviceAccountKey = require('./serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccountKey),
  projectId: 'quiz-system-e9cfb',
});

const db = admin.firestore();

// Django API endpoint
const API_BASE_URL = 'https://quiz-system-backend-oiq0.onrender.com/api';

async function getQuestionsFromAPI() {
  try {
    console.log('Fetching questions from Django API...');
    const response = await axios.get(`${API_BASE_URL}/questions/?page_size=2000`);
    const questions = response.data.results || response.data;
    console.log(`Found ${questions.length} questions`);
    return questions;
  } catch (error) {
    console.error('Error fetching questions from API:', error.message);
    throw error;
  }
}

async function migrateQuestionsToFirestore(questions) {
  const batch = db.batch();
  let count = 0;

  for (const question of questions) {
    const questionRef = db.collection('questions').doc(String(question.id || count));

    batch.set(questionRef, {
      id: question.id || count,
      title: question.title || '',
      description: question.description || '',
      difficulty: question.difficulty || 'medium',
      category: question.category || 'general',
      topic: question.topic || 'general',
      options: question.options || [
        { text: 'Option A', isCorrect: false },
        { text: 'Option B', isCorrect: false },
        { text: 'Option C', isCorrect: true },
        { text: 'Option D', isCorrect: false },
      ],
      correctAnswer: question.correct_answer || question.correctAnswer || '',
      explanation: question.explanation || '',
      createdAt: new Date(),
      updatedAt: new Date(),
    });

    count++;

    // Firestore batch has 500 limit
    if (count % 500 === 0) {
      console.log(`Committing batch of 500 (total: ${count})...`);
      await batch.commit();
    }
  }

  // Commit remaining
  if (count % 500 !== 0) {
    console.log(`Committing final batch (total: ${count})...`);
    await batch.commit();
  }

  console.log(`✅ Successfully migrated ${count} questions to Firestore`);
}

async function main() {
  try {
    console.log('Starting question migration...\n');

    // Step 1: Fetch questions from API
    const questions = await getQuestionsFromAPI();

    // Step 2: Migrate to Firestore
    await migrateQuestionsToFirestore(questions);

    console.log('\n✅ Migration complete!');
    process.exit(0);
  } catch (error) {
    console.error('\n❌ Migration failed:', error);
    process.exit(1);
  }
}

main();
