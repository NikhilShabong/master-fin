import React from 'react';

const Question = ({ id, text, scale, type, options, onAnswer }) => {
  const handleMainChange = (e) => {
    const value = type === 'number' ? parseFloat(e.target.value) : e.target.value;
    onAnswer(id, value);
  };

  const handleDescriptionChange = (e) => {
    onAnswer(`${id}_description`, e.target.value);
  };

  const handleChangeIntent = (e) => {
    onAnswer(`${id}_change`, e.target.checked);
  };

  return (
    <div style={{ marginBottom: '2rem', padding: '1rem', border: '1px solid #ddd', borderRadius: '8px' }}>
      <label style={{ fontWeight: 'bold', display: 'block', marginBottom: '0.5rem' }}>{text}</label>

      {/* Trait score input */}
      {scale ? (
        <input
          type="range"
          min={scale[0]}
          max={scale[1]}
          defaultValue={(scale[0] + scale[1]) / 2}
          onChange={(e) => onAnswer(id, Number(e.target.value))}
          style={{ width: '100%' }}
        />
      ) : type === 'select' ? (
        <select onChange={handleMainChange}>
          <option value="">Select an option</option>
          {options.map((opt, idx) => (
            <option key={idx} value={opt}>{opt}</option>
          ))}
        </select>
      ) : (
        <input
          type={type === 'number' ? 'number' : 'text'}
          onChange={handleMainChange}
        />
      )}

      {/* Change Trait Checkbox */}
      <div style={{ marginTop: '0.5rem' }}>
        <label style={{ fontSize: '0.9rem' }}>
          <input type="checkbox" onChange={handleChangeIntent} style={{ marginRight: '0.5rem' }} />
          I want to change this trait about myself
        </label>
      </div>

      {/* Optional Description Box */}
      <textarea
        placeholder="Add any personal context or nuance to your answer here (optional)..."
        onChange={handleDescriptionChange}
        style={{ width: '100%', marginTop: '0.5rem', padding: '0.5rem', borderRadius: '4px' }}
      />
    </div>
  );
};

export default Question;
