import React from 'react';
import clsx from 'clsx';

export default function ModelViewerPanel({ model }) {
  if (!model) {
    return (
      <div className="p-4 bg-neutral-900 text-neutral-400 rounded-xl italic">
        Select a model to view full description and performance.
      </div>
    );
  }

  return (
    <div className="p-4 bg-neutral-900 text-white rounded-xl shadow-inner">
      <h2 className="text-lg font-bold mb-2">{model.name} Overview</h2>

      <div className="text-sm space-y-2">
        <div>
          <span className="text-gray-400 font-semibold">Type:</span>{' '}
          <span className="text-blue-300">{model.type}</span>
        </div>

        {model.description && (
          <div>
            <span className="text-gray-400 font-semibold">Description:</span>
            <p className="text-neutral-200 mt-1">{model.description}</p>
          </div>
        )}

        {model.performance && (
          <div>
            <span className="text-gray-400 font-semibold">Performance:</span>
            <ul className="list-disc list-inside text-neutral-300 mt-1">
              {model.performance.map((line, idx) => (
                <li key={idx}>{line}</li>
              ))}
            </ul>
          </div>
        )}

        {model.roles && model.roles.length > 0 && (
          <div>
            <span className="text-gray-400 font-semibold">Fusion Roles:</span>
            <div className="flex flex-wrap gap-2 mt-1">
              {model.roles.map((role, idx) => (
                <span
                  key={idx}
                  className="px-2 py-0.5 text-xs font-medium rounded-full bg-purple-700 text-white"
                >
                  {role}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
