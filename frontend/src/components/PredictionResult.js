import React from 'react';
import { motion } from 'framer-motion';
import { FaCheckCircle, FaTimesCircle, FaExclamationTriangle } from 'react-icons/fa';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const PredictionResult = ({ prediction }) => {
  const survived = prediction.survived === 1;
  const survivalProb = (prediction.survival_probability * 100).toFixed(1);
  const deathProb = (prediction.death_probability * 100).toFixed(1);
  const confidence = (prediction.confidence * 100).toFixed(1);

  const chartData = [
    { name: 'Survival', value: prediction.survival_probability * 100 },
    { name: 'Death', value: prediction.death_probability * 100 }
  ];

  const COLORS = ['#10b981', '#ef4444'];

  const getRiskColor = () => {
    if (prediction.risk_level === 'Low Risk') return 'text-green-600 dark:text-green-400';
    if (prediction.risk_level === 'Medium Risk') return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getRiskIcon = () => {
    if (prediction.risk_level === 'Low Risk') return FaCheckCircle;
    if (prediction.risk_level === 'Medium Risk') return FaExclamationTriangle;
    return FaTimesCircle;
  };

  const RiskIcon = getRiskIcon();

  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className="glass-effect rounded-2xl shadow-xl p-8 space-y-6"
    >
      {/* Main Result */}
      <div className={`text-center p-6 rounded-xl ${
        survived 
          ? 'bg-green-50 dark:bg-green-900/20 border-2 border-green-500'
          : 'bg-red-50 dark:bg-red-900/20 border-2 border-red-500'
      }`}>
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
        >
          {survived ? (
            <FaCheckCircle className="text-6xl text-green-600 dark:text-green-400 mx-auto mb-4" />
          ) : (
            <FaTimesCircle className="text-6xl text-red-600 dark:text-red-400 mx-auto mb-4" />
          )}
        </motion.div>
        
        <h3 className={`text-3xl font-bold mb-2 ${
          survived ? 'text-green-800 dark:text-green-300' : 'text-red-800 dark:text-red-300'
        }`}>
          {survived ? 'Would Likely Survive' : 'Would Likely Not Survive'}
        </h3>
        
        <p className="text-gray-700 dark:text-gray-300 text-lg">
          Survival Probability: <span className="font-bold">{survivalProb}%</span>
        </p>
      </div>

      {/* Probability Chart */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6">
        <h4 className="text-xl font-semibold text-gray-800 dark:text-white mb-4 text-center">
          Probability Distribution
        </h4>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, value }) => `${name}: ${value.toFixed(1)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
              animationBegin={0}
              animationDuration={800}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `${value.toFixed(1)}%`} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Detailed Stats */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 rounded-xl p-4">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Confidence</p>
          <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">{confidence}%</p>
        </div>
        
        <div className={`bg-gradient-to-br rounded-xl p-4 ${
          prediction.risk_level === 'Low Risk' 
            ? 'from-green-50 to-green-100 dark:from-green-900/30 dark:to-green-800/30'
            : prediction.risk_level === 'Medium Risk'
            ? 'from-yellow-50 to-yellow-100 dark:from-yellow-900/30 dark:to-yellow-800/30'
            : 'from-red-50 to-red-100 dark:from-red-900/30 dark:to-red-800/30'
        }`}>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Risk Level</p>
          <p className={`text-xl font-bold flex items-center space-x-2 ${getRiskColor()}`}>
            <RiskIcon />
            <span>{prediction.risk_level}</span>
          </p>
        </div>
      </div>

      {/* Feature Contributions */}
      {prediction.feature_contributions && (
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6">
          <h4 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">
            Top Influencing Factors
          </h4>
          <div className="space-y-3">
            {Object.entries(prediction.feature_contributions).slice(0, 5).map(([feature, importance], index) => (
              <motion.div
                key={feature}
                initial={{ width: 0 }}
                animate={{ width: '100%' }}
                transition={{ delay: 0.1 * index, duration: 0.5 }}
              >
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium text-gray-700 dark:text-gray-300">{feature}</span>
                  <span className="text-gray-600 dark:text-gray-400">{(importance * 100).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${importance * 100}%` }}
                    transition={{ delay: 0.1 * index, duration: 0.8 }}
                    className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                  />
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Info Note */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-4">
        <p className="text-sm text-gray-700 dark:text-gray-300">
          <strong>Note:</strong> This prediction is based on historical Titanic data and advanced machine learning models 
          achieving 82%+ accuracy. Results are probabilistic and for educational purposes.
        </p>
      </div>
    </motion.div>
  );
};

export default PredictionResult;
