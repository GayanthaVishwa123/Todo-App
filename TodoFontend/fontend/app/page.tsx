'use client';

import { useState } from 'react';
import Dashboard from './dashboard/page'; 
import RegistrationForm from './auth/registerPage';
import LoginForm from './auth/loginPage';

export default function Home() {
  const [isRegistrationOpen, setIsRegistrationOpen] = useState(false);
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false); 

  // Handle closing the registration form
  const handleRegistrationClose = () => {
    setIsRegistrationOpen(false);
  };

  // Handle closing the login form
  const handleLoginClose = () => {
    setIsLoginOpen(false);
  };

  // Handle successful login (set loggedIn state to true)
  const handleLogin = (token: string) => {
    console.log('Logged in with token:', token);
    setIsLoggedIn(true);  
    setIsLoginOpen(false); 
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-200">
      {/* Show TodoApp only when logged in */}
      {isLoggedIn && <Dashboard />}

      {/* Registration Form */}
      {isRegistrationOpen && <RegistrationForm onClose={handleRegistrationClose} />}

      {/* Login Form */}
      {isLoginOpen && <LoginForm onLogin={handleLogin} onClose={handleLoginClose} />}

      {/* Buttons to open the forms */}
      {!isLoggedIn && (  // Show these buttons only if the user is not logged in
        <>
          <button
            onClick={() => setIsRegistrationOpen(true)}
            className="bg-blue-500 text-white px-4 py-2 rounded-md"
          >
            Register
          </button>

          <button
            onClick={() => setIsLoginOpen(true)}
            className="bg-green-500 text-white px-4 py-2 rounded-md ml-4"
          >
            Login
          </button>
        </>
      )}
    </div>
  );
}

