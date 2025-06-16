//const handleLogin = async (email, password) => {
//    const { user, session, error } = await supabase.auth.signInWithPassword({ email, password })
//    if (error) alert(error.message)
    // Save user ID to context or pass with backend requests
//  }

// Login.jsx
import React, { useState } from 'react';
import { supabase } from '../supabase_client';

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    const { error } = await supabase.auth.signInWithOtp({ email });
    if (error) alert(error.message);
    else alert("Check your email for the login link!");
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="email"
        placeholder="Enter your email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        required
      />
      <button type="submit">Login</button>
    </form>
  );
};

export default Login;