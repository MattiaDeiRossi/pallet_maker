let socket: WebSocket | null = null;
let listeners: ((data: any) => void)[] = [];

export const connectWebSocket = (url: string) => {
  socket = new WebSocket(url);

  socket.onopen = () => {
    console.log('[WS] Connected');
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      listeners.forEach((cb) => cb(data));
    } catch (err) {
      console.error('[WS] Invalid message:', err);
    }
  };

  socket.onclose = () => {
    console.log('[WS] Disconnected');
  };

  socket.onerror = (err) => {
    console.error('[WS] Error:', err);
  };
};

export const onMessage = (callback: (data: any) => void) => {
  listeners.push(callback);
};

export const disconnectWebSocket = () => {
  if (socket) {
    socket.close();
    socket = null;
  }
};

export const sendMessage = (message: any) => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(message));
  }
};
