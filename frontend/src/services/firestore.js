import { db, auth } from '../firebaseConfig';
import {
  collection,
  doc,
  setDoc,
  getDoc,
  getDocs,
  updateDoc,
  deleteDoc,
  query,
  where,
  orderBy,
  limit,
  addDoc,
  increment,
  serverTimestamp,
} from 'firebase/firestore';

// ============ USER PROFILE ============
export const createUserProfile = async (userId, userData) => {
  try {
    await setDoc(doc(db, 'users', userId), {
      email: userData.email,
      username: userData.username || userData.email.split('@')[0],
      firstName: userData.firstName || '',
      lastName: userData.lastName || '',
      createdAt: serverTimestamp(),
      updatedAt: serverTimestamp(),
      totalQuizzes: 0,
      bestScore: 0,
      averageScore: 0,
    });
  } catch (error) {
    console.error('Error creating user profile:', error);
    throw error;
  }
};

export const getUserProfile = async (userId) => {
  try {
    const userDoc = await getDoc(doc(db, 'users', userId));
    if (userDoc.exists()) {
      return { id: userDoc.id, ...userDoc.data() };
    }
    return null;
  } catch (error) {
    console.error('Error getting user profile:', error);
    throw error;
  }
};

export const updateUserProfile = async (userId, data) => {
  try {
    await updateDoc(doc(db, 'users', userId), {
      ...data,
      updatedAt: serverTimestamp(),
    });
  } catch (error) {
    console.error('Error updating user profile:', error);
    throw error;
  }
};

// ============ QUIZZES ============
export const getQuestions = async (filters = {}) => {
  try {
    let q = collection(db, 'questions');
    const constraints = [];

    if (filters.difficulty) {
      constraints.push(where('difficulty', '==', filters.difficulty));
    }
    if (filters.category) {
      constraints.push(where('category', '==', filters.category));
    }
    if (filters.topic) {
      constraints.push(where('topic', '==', filters.topic));
    }

    const querySnapshot = await getDocs(
      constraints.length > 0 ? query(q, ...constraints) : q
    );

    return querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data(),
    }));
  } catch (error) {
    console.error('Error fetching questions:', error);
    throw error;
  }
};

export const getQuestionById = async (questionId) => {
  try {
    const docSnap = await getDoc(doc(db, 'questions', questionId));
    if (docSnap.exists()) {
      return { id: docSnap.id, ...docSnap.data() };
    }
    return null;
  } catch (error) {
    console.error('Error getting question:', error);
    throw error;
  }
};

export const createQuiz = async (userId, quizData) => {
  try {
    const docRef = await addDoc(collection(db, 'quizzes'), {
      userId,
      title: quizData.title,
      description: quizData.description || '',
      quizType: quizData.quizType || 'practice',
      questionIds: quizData.questionIds || [],
      timeLimit: quizData.timeLimit || 0,
      isActive: true,
      createdAt: serverTimestamp(),
      updatedAt: serverTimestamp(),
    });
    return docRef.id;
  } catch (error) {
    console.error('Error creating quiz:', error);
    throw error;
  }
};

// ============ QUIZ SESSIONS ============
export const createQuizSession = async (userId, sessionData) => {
  try {
    const docRef = await addDoc(collection(db, 'sessions'), {
      userId,
      quizId: sessionData.quizId || '',
      quizType: sessionData.quizType || 'practice',
      title: sessionData.title || 'Quiz Session',
      totalQuestions: sessionData.totalQuestions || 0,
      questionsAnswered: 0,
      score: 0,
      correctAnswers: 0,
      wrongAnswers: 0,
      answers: [], // Array of { questionId, answer, correct }
      startedAt: serverTimestamp(),
      completedAt: null,
      isCompleted: false,
      timeSpent: 0,
    });
    return docRef.id;
  } catch (error) {
    console.error('Error creating session:', error);
    throw error;
  }
};

export const getQuizSession = async (sessionId) => {
  try {
    const docSnap = await getDoc(doc(db, 'sessions', sessionId));
    if (docSnap.exists()) {
      return { id: docSnap.id, ...docSnap.data() };
    }
    return null;
  } catch (error) {
    console.error('Error getting session:', error);
    throw error;
  }
};

export const submitAnswer = async (sessionId, questionId, answer, correct) => {
  try {
    const sessionRef = doc(db, 'sessions', sessionId);
    const sessionDoc = await getDoc(sessionRef);
    const answers = sessionDoc.data().answers || [];

    const newAnswers = answers.filter(a => a.questionId !== questionId);
    newAnswers.push({
      questionId,
      answer,
      correct,
      timestamp: new Date(),
    });

    const scoreIncrement = correct ? 1 : 0;
    const correctIncrement = correct ? 1 : 0;
    const wrongIncrement = correct ? 0 : 1;

    await updateDoc(sessionRef, {
      answers: newAnswers,
      questionsAnswered: newAnswers.length,
      score: increment(scoreIncrement),
      correctAnswers: increment(correctIncrement),
      wrongAnswers: increment(wrongIncrement),
      updatedAt: serverTimestamp(),
    });
  } catch (error) {
    console.error('Error submitting answer:', error);
    throw error;
  }
};

export const completeQuizSession = async (sessionId) => {
  try {
    const sessionRef = doc(db, 'sessions', sessionId);
    const sessionDoc = await getDoc(sessionRef);
    const sessionData = sessionDoc.data();

    // Update session as completed
    await updateDoc(sessionRef, {
      isCompleted: true,
      completedAt: serverTimestamp(),
    });

    // Update user stats
    const userId = sessionData.userId;
    const userRef = doc(db, 'users', userId);
    const userDoc = await getDoc(userRef);
    const userData = userDoc.data();

    const newTotalQuizzes = (userData.totalQuizzes || 0) + 1;
    const newAverageScore =
      (userData.averageScore * (newTotalQuizzes - 1) + sessionData.score) /
      newTotalQuizzes;

    await updateDoc(userRef, {
      totalQuizzes: newTotalQuizzes,
      bestScore: Math.max(userData.bestScore || 0, sessionData.score),
      averageScore: newAverageScore,
    });

    return sessionData;
  } catch (error) {
    console.error('Error completing session:', error);
    throw error;
  }
};

export const getUserSessions = async (userId) => {
  try {
    const q = query(
      collection(db, 'sessions'),
      where('userId', '==', userId),
      orderBy('startedAt', 'desc')
    );
    const querySnapshot = await getDocs(q);
    return querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data(),
    }));
  } catch (error) {
    console.error('Error getting user sessions:', error);
    throw error;
  }
};

// ============ LEADERBOARD ============
export const getLeaderboard = async (limitCount = 50) => {
  try {
    const q = query(
      collection(db, 'users'),
      orderBy('bestScore', 'desc'),
      limit(limitCount)
    );
    const querySnapshot = await getDocs(q);
    return querySnapshot.docs.map((doc, index) => ({
      id: doc.id,
      rank: index + 1,
      ...doc.data(),
    }));
  } catch (error) {
    console.error('Error getting leaderboard:', error);
    throw error;
  }
};

// ============ BOOKMARKS ============
export const bookmarkQuestion = async (userId, questionId) => {
  try {
    const bookmarkId = `${userId}_${questionId}`;
    await setDoc(doc(db, 'bookmarks', bookmarkId), {
      userId,
      questionId,
      createdAt: serverTimestamp(),
    });
  } catch (error) {
    console.error('Error bookmarking question:', error);
    throw error;
  }
};

export const unbookmarkQuestion = async (userId, questionId) => {
  try {
    const bookmarkId = `${userId}_${questionId}`;
    await deleteDoc(doc(db, 'bookmarks', bookmarkId));
  } catch (error) {
    console.error('Error unbookmarking question:', error);
    throw error;
  }
};

export const getUserBookmarks = async (userId) => {
  try {
    const q = query(
      collection(db, 'bookmarks'),
      where('userId', '==', userId)
    );
    const querySnapshot = await getDocs(q);
    const bookmarkedQuestionIds = querySnapshot.docs.map(
      doc => doc.data().questionId
    );

    // Fetch the actual questions
    const questions = await Promise.all(
      bookmarkedQuestionIds.map(id => getQuestionById(id))
    );
    return questions.filter(q => q !== null);
  } catch (error) {
    console.error('Error getting bookmarks:', error);
    throw error;
  }
};

export const isQuestionBookmarked = async (userId, questionId) => {
  try {
    const bookmarkId = `${userId}_${questionId}`;
    const docSnap = await getDoc(doc(db, 'bookmarks', bookmarkId));
    return docSnap.exists();
  } catch (error) {
    console.error('Error checking bookmark:', error);
    return false;
  }
};
