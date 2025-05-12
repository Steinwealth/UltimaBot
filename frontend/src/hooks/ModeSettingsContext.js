// src/hooks/ModeSettingsContext.js
import React, { createContext, useContext } from 'react';
import useModeSettingsHook from './useModeSettings';

// Create context
const ModeSettingsContext = createContext(null);

// Provider component
export const ModeSettingsProvider = ({ children }) => {
  const modeSettings = useModeSettingsHook(); // Get hook values
  return (
    <ModeSettingsContext.Provider value={modeSettings}>
      {children}
    </ModeSettingsContext.Provider>
  );
};

// Hook to use context safely
export const useModeSettings = () => {
  const context = useContext(ModeSettingsContext);
  if (!context) {
    throw new Error('useModeSettings must be used within a ModeSettingsProvider');
  }
  return context;
};
