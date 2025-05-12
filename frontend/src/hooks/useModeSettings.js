import { useState, useEffect } from 'react';

const useModeSettings = () => {
  const [mode, setMode] = useState(() => {
    if (typeof window !== 'undefined') {
      const savedMode = localStorage.getItem('mode');
      if (['easy', 'hard', 'hero'].includes(savedMode)) {
        return savedMode;
      }
    }
    return 'easy'; // Default to Easy Mode
  });

  useEffect(() => {
    localStorage.setItem('mode', mode);
  }, [mode]);

  const toggleMode = () => {
    const modes = ['easy', 'hard', 'hero'];
    const currentIndex = modes.indexOf(mode);
    setMode(modes[(currentIndex + 1) % modes.length]);
  };

  return { mode, setMode, toggleMode };
};

export default useModeSettings;
