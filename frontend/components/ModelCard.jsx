import React from 'react';
import clsx from 'clsx';

export default function ModelCard({
  name,
  type,
  accuracy,
  isActive,
  onClick,
}) {
  return (
    <div
      onClick={onClick}
      className={clsx(
        'cursor-pointer rounded-2xl px-4 py-3 shadow-md transition-all duration-200 transform',
        'hover:scale-105',
        isActive
          ? 'bg-blue-700 text-white border-2 border-blue-400'
          : 'bg-neutral-800 text-gray-100 border border-neutral-700'
      )}
    >
      <div className="flex justify-between items-center mb-1">
        <div className="text-lg font-bold">{name}</div>
        <div className="text-sm font-semibold text-green-400">
          {accuracy ? `${(accuracy * 100).toFixed(1)}%` : '--'}
        </div>
      </div>
      <div className="text-xs tracking-wide uppercase text-gray-400">{type}</div>
    </div>
  );
}
