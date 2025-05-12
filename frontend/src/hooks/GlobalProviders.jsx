// src/hooks/GlobalProviders.jsx
import React from 'react';
import { ThemeProvider } from './useTheme';
import { ModeSettingsProvider } from './ModeSettingsContext';
import { SoundSettingsProvider } from './SoundSettingsContext';

const GlobalProviders = ({ children }) => {
  return (
    <ThemeProvider>
      <ModeSettingsProvider>
        <SoundSettingsProvider>
          {children}
        </SoundSettingsProvider>
      </ModeSettingsProvider>
    </ThemeProvider>
  );
};

export default GlobalProviders;
