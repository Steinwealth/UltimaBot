// frontend/src/window/components/ui/badge.jsx
import React from 'react';
import clsx from 'clsx';

export const Badge = ({ children, variant = 'solid', className = '', ...props }) => {
  const base = 'inline-flex items-center px-3 py-1 text-sm font-medium rounded-full';
  const variants = {
    solid: 'bg-green-600 text-white',
    outline: 'border border-green-600 text-green-600 bg-transparent',
    subtle: 'bg-green-100 text-green-700'
  };

  return (
    <span
      className={clsx(base, variants[variant], className)}
      {...props}
    >
      {children}
    </span>
  );
};
