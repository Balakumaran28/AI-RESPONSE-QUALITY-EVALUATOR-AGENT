import React, { useState } from 'react';

function EvaluationPanel() {
  const [question, setQuestion] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [msg, setMsg] = useState('');

  const submitEval = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/evaluate/single', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question_text: question, ai_response_text: aiResponse }),
      });
      const data = await response.json();
      if (response.ok) setMsg(data.message);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: '25px', backgroundColor: '#ffffff', borderRadius: '12px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}>
      <h3 style={{ color: '#1e3a8a', margin: '0 0 15px 0', fontSize: '1.3rem', fontWeight: '600' }}>Evaluation Target Submission</h3>
      <form onSubmit={submitEval} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <input 
          type="text" 
          placeholder="Enter Question Text..." 
          value={question} 
          onChange={e => setQuestion(e.target.value)} 
          style={{ padding: '12px 16px', borderRadius: '8px', border: '1px solid #cbd5e1', backgroundColor: '#f8fafc', color: '#334155', fontSize: '1rem' }} 
        />
        <textarea 
          placeholder="Enter AI Generated Output..." 
          value={aiResponse} 
          onChange={e => setAiResponse(e.target.value)} 
          style={{ padding: '12px 16px', borderRadius: '8px', border: '1px solid #cbd5e1', backgroundColor: '#f8fafc', color: '#334155', fontSize: '1rem', minHeight: '100px', resize: 'vertical', fontFamily: 'inherit' }} 
        />
        <button type="submit" style={{ padding: '14px', backgroundColor: '#1e3a8a', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600', fontSize: '1rem' }}>
          Process Target Metrics
        </button>
      </form>
      {msg && <p style={{ color: '#16a34a', margin: '15px 0 0 0', fontWeight: '500' }}>{msg}</p>}
    </div>
  );
}

export default EvaluationPanel;