// frontend/src/window/components/ui/card.jsx
import React from 'react';

export const Card = ({ children, className = '', ...props }) => {
  return (
    <div className={`rounded-lg border border-gray-700 bg-gray-800 shadow-md ${className}`} {...props}>
      {children}
    </div>
  );
};

export const CardContent = ({ children, className = '', ...props }) => {
  return (
    <div className={`p-4 ${className}`} {...props}>
      {children}
    </div>
  );
};
