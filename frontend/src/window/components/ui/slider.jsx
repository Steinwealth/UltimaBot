// frontend/src/window/components/ui/slider.jsx
import React from 'react';

export const Slider = ({ min, max, step, value, onValueChange, className = '' }) => {
  const handleChange = (e) => {
    const newValue = parseFloat(e.target.value);
    onValueChange([newValue]);
  };

  return (
    <input
      type="range"
      min={min}
      max={max}
      step={step}
      value={value[0]}
      onChange={handleChange}
      className={`w-full h-2 bg-gray-300 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 ${className}`}
    />
  );
};
