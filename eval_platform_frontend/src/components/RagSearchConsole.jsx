import { useState } from 'react';

function RagSearchConsole() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setResult('');

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/rag/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query_text: query }),
      });
      const data = await response.json();
      if (response.ok && data.status === 'success') {
        setResult(data.retrieved_context);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '25px', backgroundColor: '#ffffff', borderRadius: '12px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}>
      <h3 style={{ color: '#c2185b', margin: '0 0 15px 0', fontSize: '1.3rem', fontWeight: '600' }}>Semantic DB Search</h3>
      <form onSubmit={handleSearch} style={{ display: 'flex', gap: '12px' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter concept query (e.g., guitar)..."
          style={{ flexGrow: 1, padding: '12px 16px', borderRadius: '8px', border: '1px solid #cbd5e1', backgroundColor: '#f8fafc', color: '#334155', fontSize: '1rem' }}
        />
        <button type="submit" disabled={loading} style={{ padding: '12px 24px', backgroundColor: '#e91e63', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600', fontSize: '1rem', transition: 'background-color 0.2s' }}>
          {loading ? 'Searching...' : 'Query Engine'}
        </button>
      </form>
      {result && (
        <div style={{ marginTop: '20px', padding: '20px', backgroundColor: '#fff0f5', borderLeft: '4px solid #e91e63', borderRadius: '6px' }}>
          <strong style={{ color: '#c2185b', display: 'block', marginBottom: '6px' }}>Matches Context Found:</strong>
          <p style={{ margin: 0, fontStyle: 'italic', color: '#334155', lineHeight: '1.6' }}>"{result}"</p>
        </div>
      )}
    </div>
  );
}

export default RagSearchConsole;
