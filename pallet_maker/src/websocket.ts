// src/websocket.ts
let socket: WebSocket;

type Callback = (data: any) => void;
let listeners: Callback[] = [];

export const connectWebSocket = () => {
  socket = new WebSocket('ws://localhost:8080');

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    listeners.forEach((callback) => callback(data));
  };
};

export const sendMessage = (message: any) => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(message));
  }
};

export const addListener = (callback: Callback) => {
  listeners.push(callback);
};
