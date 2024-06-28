import React, { useState, useEffect } from 'react';
import './App.css';

const wsUrl = 'ws://localhost:8080';

function App() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('Connected to WebSocket server');
    };

    ws.onmessage = (event) => {
      console.log(`Received message: ${event.data}`);
      setMessages((prevMessages) => [...prevMessages, event.data]);
    };

    ws.onerror = (error) => {
      console.error(`WebSocket error: ${error.message}`);
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Warning Weather Data</h1>
        <ul>
          {messages.map((message, index) => (
             <li key={index}>{message}</li>
          ))}
        </ul>
      </header>
    </div>
  );
}

export default App;
