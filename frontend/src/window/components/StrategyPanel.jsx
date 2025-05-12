import React from 'react';
import { Card, CardContent } from "@/window/components/ui/card";
import { Slider } from "@/window/components/ui/slider";
import { Badge } from "@/window/components/ui/badge";

const StrategyPanel = ({
  model = "N/A",
  strategy = "N/A",
  confidenceThreshold = 0.95,
  setConfidenceThreshold = () => {},
  tpForecast = 0,
  slForecast = 0,
  isDeFiWallet = false,
  swapDefaults = {
    baseCurrency: 'USDC',
    slippage: '0.5%',
    gasLimit: '300,000'
  }
}) => {
  return (
    <Card className="w-full p-5 bg-white dark:bg-gray-900 rounded-2xl shadow-lg transition-all">
      <CardContent className="space-y-5">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
          Strategy Panel
        </h2>

        {/* Model */}
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Model:</span>
          <Badge className="text-sm px-3 py-1 bg-green-500 text-white rounded-full">
            {model}
          </Badge>
        </div>

        {/* Strategy */}
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Strategy:</span>
          <Badge variant="outline" className="text-sm border-green-400 text-green-500 px-3 py-1 rounded-full">
            {strategy}
          </Badge>
        </div>

        {/* Confidence Threshold Slider */}
        <div className="space-y-1">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Confidence Threshold: {confidenceThreshold.toFixed(3)}
          </span>
          <Slider
            min={0.90}
            max={1.0}
            step={0.001}
            value={[confidenceThreshold]}
            onValueChange={(val) => setConfidenceThreshold(val[0])}
            className="accent-blue-500 dark:accent-blue-300"
          />
        </div>

        {/* Forecast TP/SL */}
        <div className="grid grid-cols-2 gap-4 pt-2">
          <div>
            <span className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              TP Forecast
            </span>
            <span className="text-lg font-semibold text-green-600 dark:text-green-400">
              {tpForecast}%
            </span>
          </div>
          <div>
            <span className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              SL Forecast
            </span>
            <span className="text-lg font-semibold text-red-500 dark:text-red-400">
              {slForecast}%
            </span>
          </div>
        </div>

        {/* DeFi Swap Defaults */}
        {isDeFiWallet && (
          <div className="pt-4 space-y-2">
            <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">DeFi Swap Settings</h3>
            <div className="flex justify-between text-sm">
              <span>Base Currency:</span>
              <span className="font-semibold text-blue-500">{swapDefaults.baseCurrency}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Slippage Tolerance:</span>
              <span className="font-semibold text-yellow-500">{swapDefaults.slippage}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Gas Limit:</span>
              <span className="font-semibold text-pink-500">{swapDefaults.gasLimit}</span>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default StrategyPanel;
