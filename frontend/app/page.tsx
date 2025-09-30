'use client'; // This is a Next.js 13+ directive for client-side components

import { useState, useEffect } from 'react';

export default function Home() {
  const [code, setCode] = useState<string>('');
  const [feedback, setFeedback] = useState<string>('AI Feedback will appear here...');
  // FIX 1: Specify that 'socket' can be a WebSocket object or null
  const [socket, setSocket] = useState<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket('ws://127.0.0.1:8000/ws/feedback/123');

    ws.onopen = () => {
      console.log('WebSocket connected!');
      setSocket(ws);
    };

    ws.onmessage = (event: MessageEvent) => {
      console.log('Received message:', event.data);
      setFeedback(event.data);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected.');
      setSocket(null);
    };

    return () => {
      ws.close();
    };
  }, []);

  // FIX 2: Specify the type for the 'event' parameter
  const handleCodeChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newCode = event.target.value;
    setCode(newCode);
    
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(newCode);
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
    </main>
  );
}