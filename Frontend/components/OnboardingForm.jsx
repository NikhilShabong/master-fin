import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Question from "./Question";
 // your trait input component

const questions = [
    {
      compartment: 'Physical',
      questions: [
        { id: 'Sleep', text: 'Rate your average sleep quality over the past week (1 = poor, 5 = excellent).', scale: [1, 5] },
        { id: 'Nutrition', text: 'Rate how balanced your diet was over the past week (1 = poor, 5 = excellent).', scale: [1, 5] },
        { id: 'Lingering Pain', text: 'How often have you experienced lingering pain this week? (1 = never, 5 = frequently)', scale: [1, 5] },
        { id: 'Exercise Enjoyment (Affective Attitude – during workout)', text: 'How much do you enjoy the feeling of working out (whilst working out)?', scale: [1, 5] },
        { id: 'Exercise Enjoyment (Affective Attitude – after workout)', text: 'How much do you enjoy the feeling of working out – post workout?', scale: [1, 5] },
        { id: 'Exercise Intensity Preference', text: 'Do you prefer easier workouts (for quick wins) or challenging workouts (for pushing through challenges)? (1 = easier, 5 = challenging)', scale: [1, 5] },
        { id: 'Exercise Intensity Tolerance', text: 'Do you stop exercising when it becomes uncomfortable, or do you tend to push through? (1 = always stop, 5 = always push through)', scale: [1, 5] }
      ]
    },
    {
      compartment: 'Environmental',
      questions: [
        { id: 'Weather Impacts', text: 'Does weather significantly affect your mood or willingness to exercise? (1 = no impact, 5 = major impact)', scale: [1, 5] },
        { id: 'Chronotype (Morningness–Eveningness)', text: 'What time of day do you feel most energetic?', type: 'select', options: ['Morning', 'Afternoon', 'Evening'] }
      ]
    },
    {
      compartment: 'Social',
      questions: [
        { id: 'OCEAN Extraversion', text: 'I get motivated to exercise when connected socially with others. (1 = disagree strongly, 5 = agree strongly)', scale: [1, 5] },
        { id: 'OCEAN Agreeableness', text: "I find it easy to cooperate and get along with others (I'm empathetic). (1 = disagree strongly, 5 = agree strongly)", scale: [1, 5] },
        { id: 'Social Exercise Orientation (Group-oriented vs Independent)', text: 'When exercising, do you prefer group settings or exercising alone? (1 = prefer alone, 5 = prefer group)', scale: [1, 5] }
      ]
    },
    {
      compartment: 'Mental',
      questions: [
        { id: 'OCEAN Neuroticism (Stress Reactivity)', text: 'I react strongly (feel anxious/worried, stressed, or irritated) to negative stimulus. (1 = rarely, 5 = frequently)', scale: [1, 5] },
        { id: 'PERMA Positive Emotion', text: 'On an average day, how often do you experience positive feelings daily? (hope, interest, joy, love, compassion, pride, amusement, and gratitude) (1 = never, 5 = always)', scale: [1, 5] },
        { id: 'PERMA Accomplishment', text: 'In your day-to-day do you feel like you accomplish a lot/ regularly feel accomplished after your daily activities?', scale: [1, 5] },
        { id: 'Negative Affectivity (Type D)', text: 'In general I sometimes feel unhappy or worried.', scale: [1, 5] },
        { id: 'Social Inhibition (Type D)', text: 'I feel uncomfortable interacting with strangers. (1 = strongly disagree, 5 = strongly agree)', scale: [1, 5] }
      ]
    },
    {
      compartment: 'Psychological',
      questions: [
        { id: 'OCEAN Openness (fitness-adapted)', text: 'When I exercise I prefer to try out different workout routines frequently, rather than stick to just one. (1 = strongly disagree, 5 = strongly agree)', scale: [1, 5] },
        { id: 'OCEAN Conscientiousness (fitness-adapted)', text: "I responsibly and consistently stick to my workout/diet routine when I can, even when I'm less motivated. (1 = rarely, 5 = always)", scale: [1, 5] },
        { id: 'MBTI Judging/Perceiving', text: 'Do you prefer clearly organised/structured/planned fitness routines or more flexible and spontaneous workout plans?', scale: [1, 5] },
        { id: 'SDT Autonomy', text: 'I prefer choosing my own workouts rather than following a prescribed routine. (1 = disagree strongly, 5 = agree strongly)', scale: [1, 5] },
        { id: 'SDT Competence', text: 'I feel confident in my ability to successfully complete workouts. (1 = disagree strongly, 5 = agree strongly)', scale: [1, 5] },
        { id: 'Mental Toughness (4Cs simplified)', text: 'I get energised by setbacks/view them as an opportunity for growth. (1 = rarely, 5 = always)', scale: [1, 5] },
        { id: 'Habit Formation', text: 'Once I form a habit, I find it easy to maintain. (1 = disagree strongly, 5 = agree strongly)', scale: [1, 5] },
        { id: 'TTM Stage of Change', text: 'Describe your current exercise status.', type: 'select', options: ['Not considering', 'Considering', 'Preparing', 'Started recently', 'Exercising regularly'] },
        { id: 'Obliger Tendency (Four Tendencies)', text: 'I want external accountability when I try to achieve my personal fitness goals. (1 = disagree strongly, 5 = agree strongly)', scale: [1, 5] }
      ]
    },
    {
      compartment: 'Learning Usability',
      questions: [
        { id: 'Learning styles', text: 'When learning new exercises, do you prefer:', type: 'select', options: ['Reading instructions', 'Interactive graphics', 'Short key points', 'Quick scan summaries', 'Video demonstrations'] },
        { id: 'MBTI Introversion/Extraversion', text: 'Do you learn better by talking things through with others, or by deeply reflecting alone?', scale: [1, 5] },
        { id: 'VARK Learning styles', text: 'Choose your preferred learning method for new exercises:', type: 'select', options: ['Visual demonstrations', 'Listening to explanations', 'Reading detailed instructions', 'Hands-on practice'] }
      ]
    },
    {
      compartment: 'Thinking Style',
      questions: [
        { id: 'Thinking styles', text: 'Choose two styles that best describe your thinking approach:', type: 'select', options: ['Divergent', 'Systemic', 'Systematic', 'Logical', 'Analogical', 'Convergent'] },
        { id: 'MBTI Sensing/Intuition', text: 'When approaching grey areas in fitness, do you prefer specific details and instructions (Sensing), or understanding the general idea/patterns and adapting from there (Intuition)?', type: 'select', options: ['Sensing', 'Intuition'] }
      ]
    },
    {
      compartment: 'Fitness Specific',
      questions: [
        { id: 'Workout adherence', text: 'How long have you been working out for?', type: 'text' },
        { id: 'Weight', text: 'How much do you weigh?', type: 'number' },
        { id: 'Diet adherence', text: 'How many meals do you eat per day, and how much carbs and protein do you get daily?', type: 'text' },
        { id: 'Self-confidence', text: 'I believe I can succeed in my fitness goals, even if others doubt me. (1 = strongly disagree, 5 = strongly agree)', scale: [1, 5] }
      ]
    }
  ];

const OnboardingForm = ({ onSubmit }) => {
  const navigate = useNavigate();
  const [activeSection, setActiveSection] = useState(0);

  // Initialize ALL fields (score, change, description) for each question
  const initialValues = {};
  questions.forEach(section =>
    section.questions.forEach(q => {
      initialValues[q.id] = 3; // default value, or "" for text/select if you prefer
      initialValues[`${q.id}_change`] = false;
      initialValues[`${q.id}_description`] = "";
    })
  );
  const [responses, setResponses] = useState(initialValues);

  const handleResponse = (id, value) => {
    setResponses(prev => ({ ...prev, [id]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // 1. Save trait responses as current_vector (object)
    onSubmit(responses); // This will trigger setCurrentVector in App.jsx
    // 2. Go to KPI selection page
    navigate('/select-kpi');
  };

  return (
    <div style={{
      maxWidth: 800,
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
      }}>Let's Get to Know You</h2>

      <div style={{
        display: 'flex',
        gap: '24px',
        marginBottom: '32px',
        overflowX: 'auto',
        padding: '8px 0'
      }}>
        {questions.map((section, idx) => (
          <button
            key={idx}
            onClick={() => setActiveSection(idx)}
            style={{
              padding: '12px 24px',
              borderRadius: '8px',
              background: activeSection === idx ? '#007bff' : '#f8f9fa',
              color: activeSection === idx ? '#ffffff' : '#2c3e50',
              border: 'none',
              cursor: 'pointer',
              whiteSpace: 'nowrap',
              transition: 'all 0.2s ease',
              fontWeight: activeSection === idx ? '500' : '400'
            }}
          >
            {section.compartment}
          </button>
        ))}
      </div>

      <form className="onboarding-container" onSubmit={handleSubmit}>
        <div style={{
          background: '#f8f9fa',
          borderRadius: '12px',
          padding: '24px',
          marginBottom: '32px'
        }}>
          <h3 style={{
            fontSize: '20px',
            color: '#2c3e50',
            marginBottom: '24px',
            fontWeight: '500'
          }}>
            {questions[activeSection].compartment}
          </h3>
          
          {questions[activeSection].questions.map(q => (
            <div key={q.id} style={{ marginBottom: '24px' }}>
              <Question
                id={q.id}
                text={q.text}
                scale={q.scale}
                type={q.type}
                options={q.options}
                onAnswer={handleResponse}
              />
            </div>
          ))}
        </div>

        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <button
            type="button"
            onClick={() => setActiveSection(prev => Math.max(0, prev - 1))}
            style={{
              padding: '12px 24px',
              borderRadius: '8px',
              background: '#f8f9fa',
              color: '#2c3e50',
              border: '1px solid #dee2e6',
              cursor: 'pointer',
              display: activeSection === 0 ? 'none' : 'block'
            }}
          >
            Previous
          </button>

          {activeSection < questions.length - 1 ? (
            <button
              type="button"
              onClick={() => setActiveSection(prev => Math.min(questions.length - 1, prev + 1))}
              style={{
                padding: '12px 24px',
                borderRadius: '8px',
                background: '#007bff',
                color: '#ffffff',
                border: 'none',
                cursor: 'pointer'
              }}
            >
              Next Section
            </button>
          ) : (
            <button
              type="submit"
              style={{
                padding: '12px 24px',
                borderRadius: '8px',
                background: '#28a745',
                color: '#ffffff',
                border: 'none',
                cursor: 'pointer'
              }}
            >
              Complete & Continue
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default OnboardingForm;
