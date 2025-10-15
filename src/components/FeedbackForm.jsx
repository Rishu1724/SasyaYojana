import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import agroIntelService from '../services/agroIntelService';

const FeedbackForm = ({ predictionId, onClose }) => {
  const { t } = useTranslation();
  const [feedback, setFeedback] = useState({
    accuracy_rating: 3,
    yield_actual: '',
    roi_actual: '',
    comments: '',
    would_recommend: true
  });
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFeedback(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    
    try {
      // Prepare feedback data
      const feedbackData = {
        ...feedback,
        yield_actual: feedback.yield_actual ? parseFloat(feedback.yield_actual) : null,
        roi_actual: feedback.roi_actual ? parseFloat(feedback.roi_actual) : null,
        timestamp: new Date().toISOString()
      };
      
      // Submit feedback
      await agroIntelService.submitFeedback(predictionId, feedbackData);
      setSubmitted(true);
      
      // Close the form after a delay
      setTimeout(() => {
        onClose();
      }, 2000);
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert(t('feedbackSubmissionError'));
    } finally {
      setSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-center">
          <svg className="h-5 w-5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
          </svg>
          <h3 className="ml-2 text-green-800 font-medium">{t('feedbackSubmitted')}</h3>
        </div>
        <p className="mt-1 text-green-700">{t('thankYouForFeedback')}</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">
        📝 {t('provideFeedback')}
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Accuracy Rating */}
        <div>
          <label className="block text-gray-700 mb-2 font-medium">
            {t('accuracyRating')}
          </label>
          <div className="flex items-center space-x-2">
            {[1, 2, 3, 4, 5].map((rating) => (
              <button
                key={rating}
                type="button"
                onClick={() => setFeedback(prev => ({ ...prev, accuracy_rating: rating }))}
                className={`text-2xl ${feedback.accuracy_rating >= rating ? 'text-yellow-400' : 'text-gray-300'}`}
              >
                ★
              </button>
            ))}
            <span className="ml-2 text-gray-600">
              {feedback.accuracy_rating} {t('outOf5')}
            </span>
          </div>
        </div>
        
        {/* Actual Yield */}
        <div>
          <label className="block text-gray-700 mb-2 font-medium">
            {t('actualYield')} (kg/acre)
          </label>
          <input
            type="number"
            name="yield_actual"
            value={feedback.yield_actual}
            onChange={handleInputChange}
            placeholder={t('enterActualYield')}
            step="0.1"
            min="0"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>
        
        {/* Actual ROI */}
        <div>
          <label className="block text-gray-700 mb-2 font-medium">
            {t('actualROI')}
          </label>
          <input
            type="number"
            name="roi_actual"
            value={feedback.roi_actual}
            onChange={handleInputChange}
            placeholder={t('enterActualROI')}
            step="0.1"
            min="0"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>
        
        {/* Comments */}
        <div>
          <label className="block text-gray-700 mb-2 font-medium">
            {t('additionalComments')}
          </label>
          <textarea
            name="comments"
            value={feedback.comments}
            onChange={handleInputChange}
            placeholder={t('enterComments')}
            rows="3"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>
        
        {/* Would Recommend */}
        <div className="flex items-center">
          <input
            type="checkbox"
            name="would_recommend"
            checked={feedback.would_recommend}
            onChange={handleInputChange}
            className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
          />
          <label className="ml-2 block text-gray-700">
            {t('wouldRecommend')}
          </label>
        </div>
        
        {/* Action Buttons */}
        <div className="flex flex-wrap gap-3 pt-4">
          <button
            type="submit"
            disabled={submitting}
            className={`bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-lg transition duration-300 ${submitting ? 'opacity-75 cursor-not-allowed' : ''}`}
          >
            {submitting ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {t('submitting')}
              </span>
            ) : (
              t('submitFeedback')
            )}
          </button>
          
          <button
            type="button"
            onClick={onClose}
            className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-3 px-6 rounded-lg transition duration-300"
          >
            {t('cancel')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default FeedbackForm;