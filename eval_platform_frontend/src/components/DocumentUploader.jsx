import React, { useState } from 'react';

function DocumentUploader() {
  const [file, setFile] = useState(null);
  const [statusText, setStatusText] = useState('');

  const uploadFile = async (e) => {
    e.preventDefault();
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/evaluate/upload-context', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (response.ok) setStatusText(`Uploaded: ${data.filename} (${data.character_count} chars parsed)`);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: '25px', backgroundColor: '#ffffff', borderRadius: '12px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}>
      <h3 style={{ color: '#16a34a', margin: '0 0 15px 0', fontSize: '1.3rem', fontWeight: '600' }}>Reference Grounding Upload</h3>
      <form onSubmit={uploadFile} style={{ display: 'flex', itemsAlign: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '15px' }}>
        <input 
          type="file" 
          accept=".txt" 
          onChange={e => setFile(e.target.files[0])} 
          style={{ padding: '8px 0', color: '#475569', fontSize: '0.95rem' }} 
        />
        <button type="submit" style={{ padding: '12px 24px', backgroundColor: '#16a34a', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600', fontSize: '1rem' }}>
          Upload Source Document
        </button>
      </form>
      {statusText && <p style={{ color: '#16a34a', margin: '15px 0 0 0', fontWeight: '500' }}>{statusText}</p>}
    </div>
  );
}

export default DocumentUploader;