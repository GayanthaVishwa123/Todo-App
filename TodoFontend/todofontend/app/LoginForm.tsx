'use client';

import { useState } from 'react';
import axios from 'axios';

const LoginForm = ({ onLogin, onClose }: { onLogin: (token: string) => void; onClose: () => void }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

    // Handle login form submission
  const handleLogin = async () => {
    setLoading(true);
    try {
      // Send login request to the FastAPI backend
      const response = await axios.post('http://127.0.0.1:8000/user/login', 
        `grant_type=password&username=${username}&password=${password}`,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          }
        }
      );
      
      // On successful login, store token and close the form
      const token = response.data.access_token;
      localStorage.setItem('authToken', token); // Store token
      console.log("Token:", token); // Debugging: Check the token
      onLogin(token); 
      onClose();
    } catch (err) {
      setError('Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex justify-center items-center z-50">
      <div className="bg-white w-full max-w-md p-8 rounded-xl shadow-lg">
        <h2 className="text-3xl font-semibold text-gray-900 mb-6 text-center">Login to Your Account</h2>
        
        {error && <p className="text-red-500 text-center mb-4">{error}</p>}
        
        <div className="space-y-6">
          <input
            className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          
          <input
            className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        
        <div className="flex justify-between mt-6 gap-4">
          <button
            onClick={onClose}
            className="w-1/2 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-all"
          >
            Cancel
          </button>
          <button
            onClick={handleLogin}
            disabled={loading}
            className={`w-1/2 py-3 text-white rounded-lg ${loading ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'} transition-all`}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;

