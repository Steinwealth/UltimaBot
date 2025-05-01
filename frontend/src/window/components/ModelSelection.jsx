import React from 'react';
import { Card } from '@/components/ui/card';

const ModelSelection = ({ models = [], selectedModel, onSelectModel }) => {
  return (
    <div className="grid grid-cols-2 gap-4">
      {Array.isArray(models) && models.length > 0 ? (
        models.map((model) => (
          <Card
            key={model.name}
            className={`p-4 rounded-2xl shadow-soft cursor-pointer transition-transform transform hover:scale-105 ${
              selectedModel === model.name ? 'border-2 border-blue-500' : ''
            }`}
            onClick={() => onSelectModel(model.name)}
          >
            <div className="flex flex-col items-center">
              <span className="text-lg font-semibold mb-1">{model.name}</span>
              <span className="text-sm text-gray-500">{model.type}</span>
              <span className="text-xs text-green-600 mt-2">Accuracy: {model.accuracy}%</span>
            </div>
          </Card>
        ))
      ) : (
        <div className="col-span-2 text-center text-gray-500">No models available</div>
      )}
    </div>
  );
};

export default ModelSelection;
