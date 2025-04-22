import React, { createContext, useContext, useEffect, useState } from 'react';

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('dark');
  const [isTransitioning, setIsTransitioning] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem('ultima-theme') || 'dark';
    setTheme(savedTheme);
    document.documentElement.classList.remove('light', 'dark');
    document.documentElement.classList.add(savedTheme);
    document.documentElement.style.transition = 'background-color 0.3s ease, color 0.3s ease';
  }, []);

  const toggleTheme = () => {
    setIsTransitioning(true);
    setTimeout(() => setIsTransitioning(false), 600);

    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    document.documentElement.classList.remove('light', 'dark');
    document.documentElement.classList.add(nextTheme);
    document.documentElement.style.transition = 'background-color 0.3s ease, color 0.3s ease';
    localStorage.setItem('ultima-theme', nextTheme);
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <div className={theme + ' transition-colors duration-300 relative overflow-hidden'}>
        {isTransitioning && (
          <div className="fixed inset-0 z-50 pointer-events-none transition-opacity duration-500 backdrop-blur-md" style={{
            background: 'radial-gradient(circle at center, rgba(255,255,255,0.4), rgba(0,0,0,0.3))',
            opacity: 0.7
          }} />
        )}
        {children}
      </div>
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
