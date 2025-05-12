import { useState, useEffect } from 'react';

const useSoundSettings = () => {
  const [soundMuted, setSoundMuted] = useState(false);
  const [customSounds, setCustomSounds] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedMuted = localStorage.getItem('soundMuted') === 'true';
      const storedCustom = localStorage.getItem('customSounds') === 'true';
      setSoundMuted(storedMuted);
      setCustomSounds(storedCustom);
      setIsInitialized(true);
    }
  }, []);

  useEffect(() => {
    if (typeof window !== 'undefined' && isInitialized) {
      localStorage.setItem('soundMuted', soundMuted);
      localStorage.setItem('customSounds', customSounds);
    }
  }, [soundMuted, customSounds, isInitialized]);

  const toggleMute = () => setSoundMuted((prev) => !prev);
  const toggleCustomSounds = () => setCustomSounds((prev) => !prev);

  return { soundMuted, toggleMute, customSounds, toggleCustomSounds };
};

export default useSoundSettings;
