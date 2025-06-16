import React, { useState, useEffect } from 'react';
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

const Chat = ({ currentVector, futureVector, selectedKpis, userId  }) => {
  const [lastArchetype, setLastArchetype] = useState('');
  const [lastTailoringSnippets, setLastTailoringSnippets] = useState([]);
  const [lastTraits, setLastTraits] = useState([]);
  const [lastKpis, setLastKpis] = useState([]);
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
      active_kpis: selectedKpis,
      last_kpis: lastKpis,
      last_traits: lastTraits,
      user_id: userId
    };

    if (input.toLowerCase().includes("habit blueprint")) {
      if (lastTraits.length === 0 || lastKpis.length === 0) {
        setChatHistory(prev => [
          ...prev,
          { sender: 'assistant', text: "Sorry, no context for habit blueprint. Try asking a fitness question first." }
        ]);
        setInput('');
        return;
      }
      payload.last_traits = lastTraits;
      payload.last_kpis = lastKpis;
    }

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
      setLastTraits(res.data.last_traits || []);
      setLastKpis(res.data.last_kpis || []);
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
      active_kpis: selectedKpis
    };

    try {
      const res = await axios.post("http://localhost:8000/generate_workout", payload);
      setWorkoutPlan(res.data.plan);
      setLastArchetype(res.data.archetype || '');
      setLastTailoringSnippets(res.data.tailoring_snippets ? res.data.tailoring_snippets.slice(0, 2) : []);
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
      {chatHistory.length > 0 &&
          chatHistory[chatHistory.length - 1].sender === "assistant" &&
          chatHistory[chatHistory.length - 1].text &&
          chatHistory[chatHistory.length - 1].text.toLowerCase().indexOf("would you like a detailed habit blueprint") !== -1 && (
            <div style={{ marginBottom: 16, color: "#3984b5", fontWeight: 500, textAlign: "center" }}>
              Would you like a detailed habit blueprint? Type <b>habit blueprint</b> to see more.
          </div>
      )}
      {lastArchetype && (
        <div style={{
          margin: '20px 0 0 0',
          padding: '16px',
          background: '#f6fafd',
          border: '1px solid #bee3f8',
          borderRadius: '10px',
          fontSize: '15px'
        }}>
          <b>🏋️‍♂️ Selected Workout Archetype:</b> {lastArchetype}
          {lastTailoringSnippets.length > 0 && (
            <>
              <div style={{ marginTop: '8px' }}><b>🔑 Tailoring Highlights:</b></div>
              <ul style={{ margin: 0, paddingLeft: '18px' }}>
                {lastTailoringSnippets.map((snippet, i) => (
                  <li key={i} style={{ fontSize: '14px', color: '#283040' }}>{snippet}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}




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
