import React, { createContext, useContext, useState, useEffect } from 'react';

const SoundSettingsContext = createContext();

export const SoundSettingsProvider = ({ children }) => {
  const [soundMuted, setSoundMuted] = useState(false);
  const [customSounds, setCustomSounds] = useState(false);

  useEffect(() => {
    const savedMuted = localStorage.getItem('soundMuted') === 'true';
    const savedCustom = localStorage.getItem('customSounds') === 'true';
    setSoundMuted(savedMuted);
    setCustomSounds(savedCustom);
  }, []);

  const toggleMute = () => {
    setSoundMuted((prev) => {
      localStorage.setItem('soundMuted', !prev);
      return !prev;
    });
  };

  const toggleCustomSounds = () => {
    setCustomSounds((prev) => {
      localStorage.setItem('customSounds', !prev);
      return !prev;
    });
  };

  return (
    <SoundSettingsContext.Provider value={{ soundMuted, toggleMute, customSounds, toggleCustomSounds }}>
      {children}
    </SoundSettingsContext.Provider>
  );
};

export const useSoundSettings = () => useContext(SoundSettingsContext);
