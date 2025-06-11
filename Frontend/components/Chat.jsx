import React, { useState } from 'react';
import axios from 'axios';

function stripNonScores(vector) {
  const out = {};
  Object.entries(vector).forEach(([k, v]) => {
    if (
      !k.endsWith('_change') &&
      !k.endsWith('_description') &&
      typeof v === 'number'
    ) {
      out[k] = v;
    }
  });
  return out;
}

const Chat = ({ currentVector, futureVector, selectedKpis }) => {
  const [input, setInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [workoutPlan, setWorkoutPlan] = useState(null);

  // Standard message handler
  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setChatHistory(prev => [...prev, { sender: 'user', text: input }]);

    const payload = {
      user_input: input,
      current_vector: stripNonScores(currentVector),
      future_vector: futureVector,
      active_kpis: selectedKpis
    };

    try {
      const res = await axios.post('http://localhost:8000/generate_advice', payload);
      setChatHistory(prev => [
        ...prev,
        {
          sender: 'assistant',
          text: res.data.gpt_advice || "Sorry, no advice returned.",
          raw: res.data.raw_advice
        }
      ]);
    } catch (err) {
      setChatHistory(prev => [
        ...prev,
        { sender: 'assistant', text: 'Sorry, there was an error. Please try again.' }
      ]);
    }
    setInput('');
  };

  // NEW: Generate Workout handler
  const generateWorkout = async () => {
    const payload = {
      currentVector: stripNonScores(currentVector),
      futureVector,
      archetype: "Powerlifting Beginner" // TODO: make this dynamic from user selection if needed
    };

    try {
      const res = await axios.post("http://localhost:8000/generate_workout", payload);
      setWorkoutPlan(res.data.plan);
      setChatHistory(prev => [
        ...prev,
        {
          sender: 'assistant',
          text: "Here's your personalized workout plan:",
          workout: res.data.plan
        }
      ]);
    } catch (err) {
      setChatHistory(prev => [
        ...prev,
        { sender: 'assistant', text: 'Sorry, there was an error generating your workout plan. Please try again.' }
      ]);
    }
  };

  return (
    <div style={{
      maxWidth: 800,
      margin: '40px auto',
      border: '1px solid #e0e0e0',
      borderRadius: 16,
      padding: 32,
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      backgroundColor: '#ffffff'
    }}>
      <h2 style={{
        fontSize: '24px',
        color: '#2c3e50',
        marginBottom: '24px',
        textAlign: 'center',
        fontWeight: '600'
      }}>Chat with your Fitness Coach</h2>
      
      <div style={{
        minHeight: 400,
        background: '#f8f9fa',
        borderRadius: 12,
        padding: 20,
        marginBottom: 20,
        overflowY: 'auto',
        maxHeight: '60vh'
      }}>
        {chatHistory.map((msg, i) => (
          <div key={i} style={{
            textAlign: msg.sender === 'user' ? 'right' : 'left',
            margin: '12px 0',
          }}>
            <div style={{
              display: 'inline-block',
              background: msg.sender === 'user' ? '#007bff' : '#e9ecef',
              color: msg.sender === 'user' ? '#ffffff' : '#212529',
              borderRadius: 20,
              padding: '12px 20px',
              maxWidth: '85%',
              whiteSpace: 'pre-line',
              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
            }}>
              <b style={{ fontSize: '14px', opacity: 0.8 }}>{msg.sender === 'user' ? "You" : "Coach"}:</b>
              <div style={{ marginTop: '4px' }}>{msg.text}</div>
              {msg.workout && (
                <div style={{
                  marginTop: 12,
                  padding: 16,
                  background: '#ffffff',
                  borderRadius: 12,
                  border: '1px solid #dee2e6'
                }}>
                  <pre style={{
                    margin: 0,
                    whiteSpace: 'pre-wrap',
                    fontSize: '14px',
                    lineHeight: '1.5'
                  }}>{msg.workout}</pre>
                </div>
              )}
            </div>
            {msg.raw && (
              <pre style={{
                fontSize: 12,
                color: '#6c757d',
                margin: '4px 0 0 0',
                fontFamily: 'monospace'
              }}>Raw: {msg.raw}</pre>
            )}
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
        <button
          onClick={generateWorkout}
          style={{
            padding: '12px 24px',
            borderRadius: 8,
            background: '#28a745',
            color: '#fff',
            border: 'none',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: '500',
            transition: 'background-color 0.2s',
            ':hover': {
              background: '#218838'
            }
          }}
        >
          Generate Workout Plan
        </button>
      </div>

      <form onSubmit={sendMessage} style={{ display: 'flex', gap: 12 }}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask me anything about fitness, habits, or your goals..."
          style={{
            flex: 1,
            padding: '12px 16px',
            borderRadius: 8,
            border: '1px solid #ced4da',
            fontSize: '14px',
            transition: 'border-color 0.2s',
            ':focus': {
              outline: 'none',
              borderColor: '#007bff'
            }
          }}
        />
        <button
          type="submit"
          style={{
            padding: '12px 24px',
            borderRadius: 8,
            background: '#007bff',
            color: '#fff',
            border: 'none',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: '500',
            transition: 'background-color 0.2s',
            ':hover': {
              background: '#0056b3'
            }
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default Chat;
