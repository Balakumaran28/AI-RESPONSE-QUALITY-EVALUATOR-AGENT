import React from 'react';
import RagSearchConsole from './components/RagSearchConsole';
import EvaluationPanel from './components/EvaluationPanel';
import DocumentUploader from './components/DocumentUploader';

function App() {
  return (
    <div style={{ backgroundColor: '#f8f9fa', minHeight: '100vh', padding: '50px 20px', fontFamily: '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif' }}>
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        <header style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1 style={{ color: '#1e293b', margin: '0 0 12px 0', fontSize: '2.5rem', fontWeight: '700', lineHeight: '1.2' }}>
            LLM Metrics Evaluation Framework
          </h1>
          <p style={{ color: '#64748b', margin: 0, fontSize: '1.1rem', fontWeight: '500' }}>
            System UI Portal Gate Client Dashboard
          </p>
        </header>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
          <RagSearchConsole />
          <EvaluationPanel />
          <DocumentUploader />
        </div>
      </div>
    </div>
  );
}

export default App;