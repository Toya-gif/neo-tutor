'use client';

import { useState, useEffect } from 'react';

export default function Home() {
  const [code, setCode] = useState<string>('');
  const [feedback, setFeedback] = useState<string>('AI Feedback will appear here...');
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [submissionStatus, setSubmissionStatus] = useState<string>('');
  const submissionId = 1; // Placeholder for a dynamic ID

  useEffect(() => {
    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/feedback/${submissionId}`);

    ws.onopen = () => console.log('WebSocket connected!');
    ws.onmessage = (event: MessageEvent) => setFeedback(event.data);
    ws.onclose = () => console.log('WebSocket disconnected.');
    
    setSocket(ws);

    return () => {
      ws.close();
    };
  }, [submissionId]);

  const handleCodeChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newCode = event.target.value;
    setCode(newCode);
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(newCode);
    }
  };

  const handleSubmitForReview = async () => {
    setSubmissionStatus('Submitting for final review...');
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/${submissionId}/evaluate`, {
        method: 'POST',
      });

      if (!response.ok) throw new Error('Submission failed');

      const result = await response.json();
      setSubmissionStatus(result.message);
    } catch (error) {
      setSubmissionStatus('Error submitting for review.');
      console.error(error);
    }
  };

  return (
    <main style={{ fontFamily: 'monospace', padding: '2rem', maxWidth: '800px', margin: 'auto' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '2rem' }}>Neo-Tutor Real-Time Editor</h1>
      <textarea
        value={code}
        onChange={handleCodeChange}
        placeholder="Enter your pseudocode here..."
        style={{ 
          width: '100%', 
          height: '300px', 
          fontSize: '16px', 
          border: '1px solid #333', 
          borderRadius: '8px', 
          padding: '10px',
          backgroundColor: '#1e1e1e',
          color: '#d4d4d4',
          resize: 'vertical'
        }}
      />
      
      <div style={{ marginTop: '1rem', display: 'flex', justifyContent: 'flex-end' }}>
        <button onClick={handleSubmitForReview} style={{ padding: '10px 20px', fontWeight: 'bold', cursor: 'pointer' }}>
          Submit for Final Review
        </button>
      </div>

      <div style={{ 
        marginTop: '1.5rem', 
        padding: '1rem', 
        backgroundColor: '#f4f4f4', 
        border: '1px solid #ddd', 
        borderRadius: '8px',
        minHeight: '50px'
      }}>
        <strong style={{ color: '#333' }}>Live Feedback:</strong>
        <p style={{ color: '#555', margin: '0.5rem 0 0 0' }}>{feedback}</p>
      </div>

      {submissionStatus && <p style={{ textAlign: 'center', marginTop: '1rem' }}>{submissionStatus}</p>}
    </main>
  );
}