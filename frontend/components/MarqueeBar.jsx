import React, { useEffect, useRef, useState } from 'react';
import { useTheme } from '@/components/ThemeProvider';
import { io } from 'socket.io-client';
import clsx from 'clsx';

const socket = io('http://localhost:8000'); // Update with your backend endpoint if different

export default function MarqueeBar() {
  const { theme } = useTheme();
  const [messages, setMessages] = useState([]);
  const marqueeRef = useRef();

  useEffect(() => {
    // Listen for backend messages
    socket.on('marquee_message', (msg) => {
      setMessages((prev) => [...prev.slice(-10), msg]);
    });

    return () => {
      socket.off('marquee_message');
    };
  }, []);

  // Create scrolling message string
  const marqueeText = messages.join(' • ') || 'Ultima Bot is online. Waiting for trade updates...';

  return (
    <div
      className={clsx(
        'fixed bottom-0 w-full py-1 px-4 z-50 text-sm font-semibold tracking-wide overflow-hidden whitespace-nowrap',
        theme === 'dark' ? 'bg-black text-green-400' : 'bg-white text-yellow-600',
        'border-t border-neutral-700'
      )}
    >
      <div
        ref={marqueeRef}
        className="animate-marquee inline-block"
        style={{ minWidth: '100%' }}
      >
        {marqueeText}
      </div>
    </div>
  );
}
