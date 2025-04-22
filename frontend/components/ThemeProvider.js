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
      <div className={theme + ' transition-colors duration-300 relative'}>
        {isTransitioning && (
          <div className="fixed inset-0 z-50 bg-black opacity-20 pointer-events-none transition-opacity duration-500" />
        )}
        {children}
      </div>
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
