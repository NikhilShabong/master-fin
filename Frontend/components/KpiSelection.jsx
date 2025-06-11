import React, { useState } from 'react';
import { KPI_TRAIT_SCORES } from './KpiTraitScores.js'; 
import { useNavigate } from 'react-router-dom';


const KPI_LIST = [
  "KPI 1 (Body Positivity)",
  "KPI 2 (Self-Esteem Enhancement)",
  "KPI 3 (Stress Reduction)",
  "KPI 4 (Mood Improvement)",
  "KPI 5 (Increased Energy Levels)",
  "KPI 6 (Improved Sleep Quality)",
  "KPI 7 (Enhanced Cognitive Function)",
  "KPI 8 (Sense of Accomplishment)",
  "KPI 9 (Autonomy in Health Management)",
  "KPI 10 (Social Connectedness)",
  "KPI 11 (Body Fat Percentage)",
  "KPI 12 (Muscle Mass Gain)",
  "KPI 13 (Weight Management)",
  "KPI 14 (Strength Benchmarks)",
  "KPI 15 (Cardiovascular Endurance)",
  "KPI 16 (Sport Enhancement - Flexibility & Mobility)",
  "KPI 17 (Sport Enhancement – Balance & Coordination)",
  "KPI 18 (Sport Enhancement – Speed & Agility)"
  // ...add the actual 18 KPIs as per your JSON!
];

const KpiSelection = ({ currentVector, setSelectedKpis, setFutureVector, onSubmit }) => {
  const [selected, setSelected] = useState([]);
  const navigate = useNavigate();

  const handleToggle = kpi => {
    setSelected(prev =>
      prev.includes(kpi) ? prev.filter(k => k !== kpi) : [...prev, kpi]
    );
  };

  const handleSubmit = e => {
    e.preventDefault();
    // Placeholder: You need trait mappings for each KPI to compute the actual averages.
    // For now, just forward selected KPIs and currentVector to the next step.
    setSelectedKpis(selected);

    let traitTotals = {};
    let traitCounts = {};

    selected.forEach(kpi => {
      const traitProfile = KPI_TRAIT_SCORES[kpi];
      if (traitProfile) {
        Object.entries(traitProfile).forEach(([trait, score]) => {
          if (!traitTotals[trait]) {
            traitTotals[trait] = 0;
            traitCounts[trait] = 0;
          }
          traitTotals[trait] += score;
          traitCounts[trait] += 1;
        });
      }
    });

    // Compute the average for each trait  
    const allTraits = [
        "Sleep",
        "Nutrition",
        "Lingering Pain",
        "Exercise Enjoyment (Affective Attitude – during workout)",
        "Exercise Enjoyment (Affective Attitude – after workout)",
        "Exercise Intensity Preference",
        "Exercise Intensity Tolerance",
        "Weather Impacts",
        "Chronotype (Morningness–Eveningness)",
        "OCEAN Extraversion",
        "OCEAN Agreeableness",
        "Social Exercise Orientation (Group-oriented vs Independent)",
        "OCEAN Neuroticism (Stress Reactivity)",
        "PERMA Positive Emotion",
        "PERMA Accomplishment",
        "Negative Affectivity (Type D)",
        "Social Inhibition (Type D)",
        "OCEAN Openness (fitness-adapted)",
        "OCEAN Conscientiousness (fitness-adapted)",
        "MBTI Judging/Perceiving",
        "SDT Autonomy",
        "SDT Competence",
        "Mental Toughness (4Cs simplified)",
        "Habit Formation",
        "TTM Stage of Change",
        "Obliger Tendency (Four Tendencies)",
        "Workout adherence",
        "Weight",
        "Diet adherence",
        "Self-confidence"
      ];
    const averagedFutureVector = {};
    
    allTraits.forEach(trait => {
      if (traitTotals[trait]) {
        averagedFutureVector[trait] = Math.round(traitTotals[trait] / traitCounts[trait]);
      } else {
        // Optionally set to a default value, or currentVector[trait]
        averagedFutureVector[trait] = currentVector[trait] || 3;
      }
    });
    

    setFutureVector(averagedFutureVector);

    // Move to chat page
    navigate('/chat');
  };

  return (
    <div style={{
      maxWidth: 1000,
      margin: '40px auto',
      padding: '32px',
      backgroundColor: '#ffffff',
      borderRadius: '16px',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
    }}>
      <h2 style={{
        fontSize: '28px',
        color: '#2c3e50',
        marginBottom: '32px',
        textAlign: 'center',
        fontWeight: '600'
      }}>Select Your Fitness Goals</h2>
      
      <form onSubmit={handleSubmit}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
          gap: '16px',
          marginBottom: '32px'
        }}>
          {KPI_LIST.map(kpi => (
            <label
              key={kpi}
              style={{
                border: selected.includes(kpi) ? '2px solid #007bff' : '1px solid #e0e0e0',
                borderRadius: '12px',
                padding: '16px',
                cursor: 'pointer',
                background: selected.includes(kpi) ? '#e3f0ff' : '#ffffff',
                transition: 'all 0.2s ease',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                boxShadow: selected.includes(kpi) ? '0 2px 4px rgba(0, 123, 255, 0.1)' : 'none',
                ':hover': {
                  borderColor: '#007bff',
                  transform: 'translateY(-2px)'
                }
              }}
            >
              <input
                type="checkbox"
                value={kpi}
                checked={selected.includes(kpi)}
                onChange={() => handleToggle(kpi)}
                style={{
                  width: '20px',
                  height: '20px',
                  margin: 0,
                  cursor: 'pointer'
                }}
              />
              <span style={{
                fontSize: '14px',
                color: '#2c3e50',
                fontWeight: selected.includes(kpi) ? '500' : '400'
              }}>
                {kpi}
              </span>
            </label>
          ))}
        </div>

        <div style={{
          display: 'flex',
          justifyContent: 'center',
          marginTop: '32px'
        }}>
          <button
            type="submit"
            style={{
              padding: '14px 32px',
              borderRadius: '8px',
              background: '#007bff',
              color: '#ffffff',
              border: 'none',
              fontSize: '16px',
              fontWeight: '500',
              cursor: 'pointer',
              transition: 'background-color 0.2s',
              ':hover': {
                background: '#0056b3'
              }
            }}
          >
            Continue to Chat
          </button>
        </div>
      </form>
    </div>
  );
};

export default KpiSelection;
