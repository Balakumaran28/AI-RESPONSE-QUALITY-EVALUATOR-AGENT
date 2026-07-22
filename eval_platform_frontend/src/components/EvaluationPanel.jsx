import { useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

function EvaluationPanel() {
  const [question, setQuestion] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const submitEval = async (e) => {
    e.preventDefault();
    if (!question.trim() || !aiResponse.trim()) {
      setError('Enter both the question and the AI response.');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/evaluate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // The API retrieves the grounding chunks from RAG using this question.
        body: JSON.stringify({ question: question.trim(), response: aiResponse.trim() }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'The evaluation request failed.');
      }
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to contact the evaluation service.');
    } finally {
      setLoading(false);
    }
  };

  const cardStyle = { padding: '25px', backgroundColor: '#ffffff', borderRadius: '12px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' };
  const inputStyle = { padding: '12px 16px', borderRadius: '8px', border: '1px solid #cbd5e1', backgroundColor: '#f8fafc', color: '#334155', fontSize: '1rem', fontFamily: 'inherit' };

  return (
    <div style={cardStyle}>
      <h3 style={{ color: '#1e3a8a', margin: '0 0 8px 0', fontSize: '1.3rem', fontWeight: '600' }}>Evaluate an AI Response</h3>
      <p style={{ color: '#64748b', margin: '0 0 15px' }}>Submit a question and its AI answer. The system retrieves RAG context and evaluates the answer against it.</p>
      <form onSubmit={submitEval} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <textarea
          aria-label="Question asked to the AI"
          placeholder="Question asked to the AI..."
          value={question} 
          onChange={e => setQuestion(e.target.value)} 
          style={{ ...inputStyle, minHeight: '72px', resize: 'vertical' }}
        />
        <textarea 
          aria-label="AI response"
          placeholder="AI response..."
          value={aiResponse} 
          onChange={e => setAiResponse(e.target.value)} 
          style={{ ...inputStyle, minHeight: '120px', resize: 'vertical' }}
        />
        <button type="submit" disabled={loading} style={{ padding: '14px', backgroundColor: loading ? '#64748b' : '#1e3a8a', color: '#fff', border: 'none', borderRadius: '8px', cursor: loading ? 'wait' : 'pointer', fontWeight: '600', fontSize: '1rem' }}>
          {loading ? 'Retrieving context and scoring…' : 'Retrieve Context & Score'}
        </button>
      </form>
      {error && <p role="alert" style={{ color: '#dc2626', margin: '15px 0 0', fontWeight: '500' }}>{error}</p>}
      {result && (
        <section aria-live="polite" style={{ marginTop: '24px', textAlign: 'left' }}>
          <h4 style={{ color: '#1e293b', margin: '0 0 12px' }}>Retrieved RAG Context</h4>
          {result.retrieved_contexts?.length ? (
            <ol style={{ paddingLeft: '20px', margin: '0 0 24px', color: '#334155' }}>
              {result.retrieved_contexts.map((context, index) => (
                <li key={`${index}-${context.slice(0, 32)}`} style={{ marginBottom: '10px', lineHeight: 1.5 }}>{context}</li>
              ))}
            </ol>
          ) : <p style={{ color: '#b45309' }}>No RAG context was returned; grounded scores reflect that.</p>}

          <h4 style={{ color: '#1e293b', margin: '0 0 12px' }}>Evaluation Scores</h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' }}>
            <Metric title="Relevance" value={`${result.relevance.relevance_score}/5`} detail={result.relevance.reasoning} color="#1d4ed8" />
            <Metric title="Accuracy" value={`${Math.round(result.accuracy.accuracy_score * 100)}%`} detail={`${result.accuracy.supporting_evidence.length} supporting source(s)`} color="#15803d" />
            <Metric title="Hallucination" value={`${Math.round(result.hallucination.hallucination_score * 100)}%`} detail={result.hallucination.is_hallucinated ? 'Unsupported claims found' : 'No unsupported claims found'} color={result.hallucination.is_hallucinated ? '#b91c1c' : '#15803d'} />
          </div>
          {result.hallucination.flagged_statements?.length > 0 && (
            <div style={{ marginTop: '16px', padding: '14px', backgroundColor: '#fef2f2', borderRadius: '8px', color: '#991b1b' }}>
              <strong>Flagged statements</strong>
              <ul style={{ margin: '8px 0 0', paddingLeft: '20px' }}>
                {result.hallucination.flagged_statements.map((statement, index) => <li key={`${index}-${statement}`}>{statement}</li>)}
              </ul>
            </div>
          )}
        </section>
      )}
    </div>
  );
}

function Metric({ title, value, detail, color }) {
  return (
    <div style={{ border: `1px solid ${color}33`, borderTop: `4px solid ${color}`, borderRadius: '8px', padding: '14px', backgroundColor: '#f8fafc' }}>
      <div style={{ color: '#475569', fontWeight: 600 }}>{title}</div>
      <div style={{ color, fontSize: '1.75rem', fontWeight: 700, margin: '4px 0' }}>{value}</div>
      <div style={{ color: '#64748b', fontSize: '0.85rem', lineHeight: 1.35 }}>{detail}</div>
    </div>
  );
}

export default EvaluationPanel;
