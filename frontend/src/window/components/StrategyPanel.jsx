import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';

const StrategyPanel = ({ model, strategy, confidenceThreshold, setConfidenceThreshold, tpForecast, slForecast }) => {
  const safeConfidence = typeof confidenceThreshold === 'number' ? confidenceThreshold : 0.95;
  const safeTP = typeof tpForecast === 'number' ? tpForecast : 0;
  const safeSL = typeof slForecast === 'number' ? slForecast : 0;

  return (
    <Card className="w-full p-4 bg-gray-100 shadow-soft rounded-2xl dark:bg-gray-800">
      <CardContent>
        <h2 className="mb-4 text-xl font-semibold text-gray-900 dark:text-white">Strategy Panel</h2>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="font-medium text-gray-800 dark:text-gray-200">Model:</span>
            <Badge>{model}</Badge>
          </div>
          <div className="flex items-center justify-between">
            <span className="font-medium text-gray-800 dark:text-gray-200">Strategy:</span>
            <Badge variant="outline">{strategy}</Badge>
          </div>
          <div>
            <span className="font-medium text-gray-800 dark:text-gray-200">Confidence Threshold: {safeConfidence.toFixed(3)}</span>
            <Slider
              min={0.90}
              max={1.0}
              step={0.001}
              value={[safeConfidence]}
              onValueChange={(val) => setConfidenceThreshold(val[0])}
              className="mt-2"
            />
          </div>
          <div>
            <span className="font-medium text-gray-800 dark:text-gray-200">TP Forecast: {safeTP}%</span>
          </div>
          <div>
            <span className="font-medium text-gray-800 dark:text-gray-200">SL Forecast: {safeSL}%</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default StrategyPanel;
