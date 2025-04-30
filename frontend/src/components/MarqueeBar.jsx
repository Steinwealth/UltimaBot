import React, { useEffect, useState } from 'react';

const MarqueeBar = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const socket = new WebSocket('wss://marquee-feed');
    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages((prev) => [...prev.slice(-9), message]); // Keep last 10 messages
    };
    return () => socket.close();
  }, []);

  return (
    <div className="w-full overflow-hidden text-gray-800 bg-gray-200 dark:bg-gray-700 dark:text-gray-100">
      <div className="flex whitespace-nowrap animate-marquee">
        {messages.map((msg, index) => (
          <span key={index} className="mx-4">
            {msg.text}
          </span>
        ))}
      </div>
    </div>
  );
};

export default MarqueeBar;
