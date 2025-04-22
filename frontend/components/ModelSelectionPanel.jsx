import React, { useState, useEffect } from 'react';
import ModelCard from './ModelCard';
import { Button } from '@/components/ui/button';

export default function ModelSelectionPanel({ models = [], onModelPair }) {
  const [selectedModel, setSelectedModel] = useState(null);

  useEffect(() => {
    if (models.length > 0 && !selectedModel) {
      setSelectedModel(models[0].name);
    }
  }, [models]);

  const handleModelClick = (modelName) => {
    setSelectedModel(modelName);
  };

  const handlePairClick = () => {
    const model = models.find((m) => m.name === selectedModel);
    if (model) onModelPair(model);
  };

  return (
    <div className="p-4 bg-neutral-900 rounded-xl shadow-md">
      <div className="flex justify-between items-center mb-3">
        <h2 className="text-lg font-bold tracking-wide text-white">Select a Model</h2>
        <Button onClick={handlePairClick}>
          Trade Model
        </Button>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 max-h-[300px] overflow-y-auto pr-1">
        {models.map((model) => (
          <ModelCard
            key={model.name}
            name={model.name}
            type={model.type}
            accuracy={model.accuracy}
            isActive={selectedModel === model.name}
            onClick={() => handleModelClick(model.name)}
          />
        ))}
      </div>
    </div>
  );
}
