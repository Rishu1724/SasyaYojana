import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { auth } from '../firebase';
import { signInWithEmailAndPassword } from 'firebase/auth';

const Login = ({ onSwitchToSignup }) => {
  const { t } = useTranslation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      await signInWithEmailAndPassword(auth, email, password);
      // Successful login - redirect to dashboard (handled in App.jsx)
      console.log('User logged in successfully');
    } catch (err) {
      console.error('Login error:', err);
      let errorMessage = '';
      
      switch (err.code) {
        case 'auth/invalid-email':
          errorMessage = t('invalidEmail') || 'Invalid email address';
          break;
        case 'auth/user-disabled':
          errorMessage = t('userDisabled') || 'User account has been disabled';
          break;
        case 'auth/user-not-found':
          errorMessage = t('userNotFound') || 'No user found with this email';
          break;
        case 'auth/wrong-password':
          errorMessage = t('wrongPassword') || 'Incorrect password';
          break;
        default:
          errorMessage = t('loginFailed') || 'Failed to login. Please try again.';
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto bg-white rounded-xl shadow-md p-6 md:p-8">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
        {t('login')}
      </h2>
      
      {error && (
        <div className="bg-red-50 text-red-700 p-3 rounded-lg mb-4">
          {error}
        </div>
      )}
      
      <form onSubmit={handleLogin}>
        <div className="mb-4">
          <label htmlFor="email" className="block text-gray-700 mb-2">
            {t('email')}
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
            required
            disabled={loading}
          />
        </div>
        
        <div className="mb-6">
          <label htmlFor="password" className="block text-gray-700 mb-2">
            {t('password')}
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
            required
            disabled={loading}
          />
        </div>
        
        <button
          type="submit"
          className={`w-full bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-4 rounded-lg transition duration-300 ${loading ? 'opacity-75 cursor-not-allowed' : ''}`}
          disabled={loading}
        >
          {loading ? t('loggingIn') || 'Logging in...' : t('login')}
        </button>
      </form>
      
      <div className="mt-6 text-center">
        <p className="text-gray-600">
          {t('noAccount')}{' '}
          <button
            onClick={onSwitchToSignup}
            className="text-green-600 hover:text-green-700 font-medium"
            disabled={loading}
          >
            {t('signup')}
          </button>
        </p>
      </div>
    </div>
  );
};

export default Login;