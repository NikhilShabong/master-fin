import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import OnboardingForm from './components/OnboardingForm';
import KpiSelection from './components/KpiSelection';
import Chat from './components/Chat';

function App() {
  // 🟢 Put your useState hooks here:
  const [currentVector, setCurrentVector] = useState(null);
  const [selectedKpis, setSelectedKpis] = useState([]);
  const [futureVector, setFutureVector] = useState(null);

  return (
    <Router>
      <Routes>
        {/* Onboarding page */}
        <Route
          path="/"
          element={
            <OnboardingForm onSubmit={responses => setCurrentVector(responses)} />
          }
        />
        {/* KPI Selection page */}
        <Route
          path="/select-kpi"
          element={
            <KpiSelection
              currentVector={currentVector}
              setSelectedKpis={setSelectedKpis}
              setFutureVector={setFutureVector}
              onSubmit={() => {/* TODO: Navigate to chat page */}}
            />
          }
        />
        {/* Add Chat page route here next */}
        <Route
          path="/chat"
          element={
            <Chat
              currentVector={currentVector}
              futureVector={futureVector}
              selectedKpis={selectedKpis}
            />
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
