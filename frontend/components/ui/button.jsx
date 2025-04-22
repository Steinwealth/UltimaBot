import React from 'react';
import clsx from 'clsx';

export function Button({
  children,
  onClick,
  className = '',
  disabled = false,
  type = 'button',
}) {
  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      className={clsx(
        'rounded-xl px-4 py-2 font-semibold transition-all duration-200',
        'bg-blue-600 hover:bg-blue-700 text-white',
        'disabled:bg-gray-400 disabled:cursor-not-allowed',
        className
      )}
    >
      {children}
    </button>
  );
}
