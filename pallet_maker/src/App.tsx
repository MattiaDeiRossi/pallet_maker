import React, { useEffect, useState } from 'react';
import LedIndicator from './components/states/LedIndicator';
import { connectWebSocket, disconnectWebSocket, onMessage} from './ws/client';

const App: React.FC = () => {
  const [ledColor, setLedColor] = useState<'red' | 'green' | 'blue'>('green');

  useEffect(() => {
    connectWebSocket('ws://localhost:1234');

      onMessage((data) => {
      if (data.ledStatus === 'red' || data.ledStatus === 'green' || data.ledStatus === 'blue') {
        setLedColor(data.ledStatus);
      }
    });

    return () => {
      disconnectWebSocket();
    };
  }, []);

  return (
    <div style={{ padding: 50 }}>
      <h1>WebSocket LED Indicator</h1>
      <LedIndicator color={ledColor} size={40} />
    </div>
  );
};

export default App;
