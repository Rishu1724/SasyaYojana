import { db } from '../firebase';
import { collection, addDoc, query, where, getDocs, orderBy, limit, Timestamp } from 'firebase/firestore';

class ContinuousLearningService {
  constructor() {
    this.predictionsCollection = 'predictions';
    this.feedbackCollection = 'feedback';
    this.modelVersionsCollection = 'model_versions';
  }

  /**
   * Store prediction results in Firebase Firestore
   * @param {Object} predictionData - The prediction data to store
   * @returns {Promise<string>} - The document ID of the stored prediction
   */
  async storePrediction(predictionData) {
    try {
      const predictionDoc = {
        ...predictionData,
        timestamp: Timestamp.now(),
        feedback_received: false
      };

      const docRef = await addDoc(collection(db, this.predictionsCollection), predictionDoc);
      console.log('Prediction stored with ID: ', docRef.id);
      return docRef.id;
    } catch (error) {
      console.error('Error storing prediction: ', error);
      throw error;
    }
  }

  /**
   * Store farmer feedback for a prediction
   * @param {string} predictionId - The ID of the prediction
   * @param {Object} feedbackData - The feedback data
   * @returns {Promise<string>} - The document ID of the stored feedback
   */
  async storeFeedback(predictionId, feedbackData) {
    try {
      const feedbackDoc = {
        prediction_id: predictionId,
        ...feedbackData,
        timestamp: Timestamp.now()
      };

      const docRef = await addDoc(collection(db, this.feedbackCollection), feedbackDoc);
      console.log('Feedback stored with ID: ', docRef.id);
      
      // Update the prediction to mark feedback as received
      // This would require updating the prediction document, but for simplicity,
      // we'll just log it here
      console.log(`Feedback linked to prediction ${predictionId}`);
      
      return docRef.id;
    } catch (error) {
      console.error('Error storing feedback: ', error);
      throw error;
    }
  }

  /**
   * Retrieve feedback data for model retraining
   * @param {number} limitCount - Number of feedback records to retrieve
   * @returns {Promise<Array>} - Array of feedback records
   */
  async getFeedbackData(limitCount = 1000) {
    try {
      const feedbackQuery = query(
        collection(db, this.feedbackCollection),
        orderBy('timestamp', 'desc'),
        limit(limitCount)
      );
      
      const querySnapshot = await getDocs(feedbackQuery);
      const feedbackData = [];
      
      querySnapshot.forEach((doc) => {
        feedbackData.push({
          id: doc.id,
          ...doc.data()
        });
      });
      
      return feedbackData;
    } catch (error) {
      console.error('Error retrieving feedback data: ', error);
      throw error;
    }
  }

  /**
   * Store model version information
   * @param {Object} modelInfo - Information about the model version
   * @returns {Promise<string>} - The document ID of the stored model version
   */
  async storeModelVersion(modelInfo) {
    try {
      const modelDoc = {
        ...modelInfo,
        timestamp: Timestamp.now()
      };

      const docRef = await addDoc(collection(db, this.modelVersionsCollection), modelDoc);
      console.log('Model version stored with ID: ', docRef.id);
      return docRef.id;
    } catch (error) {
      console.error('Error storing model version: ', error);
      throw error;
    }
  }

  /**
   * Get recent model versions
   * @param {number} limitCount - Number of model versions to retrieve
   * @returns {Promise<Array>} - Array of model version records
   */
  async getModelVersions(limitCount = 10) {
    try {
      const versionsQuery = query(
        collection(db, this.modelVersionsCollection),
        orderBy('timestamp', 'desc'),
        limit(limitCount)
      );
      
      const querySnapshot = await getDocs(versionsQuery);
      const versionsData = [];
      
      querySnapshot.forEach((doc) => {
        versionsData.push({
          id: doc.id,
          ...doc.data()
        });
      });
      
      return versionsData;
    } catch (error) {
      console.error('Error retrieving model versions: ', error);
      throw error;
    }
  }
}

export default new ContinuousLearningService();