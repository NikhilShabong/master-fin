import React, { useEffect ,useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { supabase } from './supabase_client';
import OnboardingForm from './components/OnboardingForm';
import KpiSelection from './components/KpiSelection';
import Chat from './components/Chat';
import Login from './components/Login'; 

function App() {
  // 🟢 Put your useState hooks here:
  const [currentVector, setCurrentVector] = useState(null);
  const [selectedKpis, setSelectedKpis] = useState([]);
  const [futureVector, setFutureVector] = useState(null);
  const [session, setSession] = useState(null);

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => setSession(data.session));
    supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });
  }, []);

  return (
    <Router>
      {session ? (
        <Routes>
          <Route
            path="/"
            element={<OnboardingForm onSubmit={responses => setCurrentVector(responses)} />}
          />
          <Route
            path="/select-kpi"
            element={
              <KpiSelection
                currentVector={currentVector}
                setSelectedKpis={setSelectedKpis}
                setFutureVector={setFutureVector}
                onSubmit={() => {/* Optional: Navigate to chat */}}
              />
            }
          />
          <Route
            path="/chat"
            element={
              <Chat
                currentVector={currentVector}
                futureVector={futureVector}
                selectedKpis={selectedKpis}
                userId={session.user.id}  // ✅ passed into session tracking
              />
            }
          />
        </Routes>
      ) : (
        <Login />
      )}
    </Router>
  );
}

export default App;
