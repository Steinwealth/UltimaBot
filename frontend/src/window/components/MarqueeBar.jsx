import React, { useEffect, useState } from 'react';

const MarqueeBar = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8080/ws/marquee'); // Replace with actual backend socket
    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const text = data.text || data.message || JSON.stringify(data);
        setMessages((prev) => [...prev.slice(-9), { text }]);
      } catch (err) {
        console.error('WebSocket message parse error:', err);
      }
    };
    return () => socket.close();
  }, []);

  return (
    <div className="w-full overflow-hidden text-gray-800 bg-gray-200 dark:bg-gray-700 dark:text-gray-100">
      <div className="flex whitespace-nowrap animate-marquee">
        {messages.map((msg, index) => (
          <span key={index} className="mx-4">{msg.text}</span>
        ))}
      </div>
    </div>
  );
};

export default MarqueeBar;
