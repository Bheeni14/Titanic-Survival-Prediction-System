import React, { useState } from 'react';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { predictSurvival } from '../services/api';
import { FaUser, FaVenusMars, FaCalendar, FaUsers, FaMoneyBillWave, FaShip, FaSpinner } from 'react-icons/fa';
import PredictionResult from './PredictionResult';

const PredictionForm = () => {
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [formData, setFormData] = useState({
    pclass: '3',
    sex: 'male',
    age: '30',
    sibsp: '0',
    parch: '0',
    fare: '10',
    embarked: 'S',
    name: '',
    cabin: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPrediction(null);

    try {
      const data = {
        pclass: parseInt(formData.pclass),
        sex: formData.sex,
        age: parseFloat(formData.age),
        sibsp: parseInt(formData.sibsp),
        parch: parseInt(formData.parch),
        fare: parseFloat(formData.fare),
        embarked: formData.embarked,
        name: formData.name || 'Unknown',
        cabin: formData.cabin || null
      };

      const result = await predictSurvival(data);
      setPrediction(result);
      toast.success('Prediction completed successfully!');
    } catch (error) {
      toast.error(error.toString());
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      pclass: '3',
      sex: 'male',
      age: '30',
      sibsp: '0',
      parch: '0',
      fare: '10',
      embarked: 'S',
      name: '',
      cabin: ''
    });
    setPrediction(null);
  };

  const inputFields = [
    {
      name: 'name',
      label: 'Passenger Name',
      type: 'text',
      icon: FaUser,
      placeholder: 'e.g., John Smith (optional)'
    },
    {
      name: 'pclass',
      label: 'Passenger Class',
      type: 'select',
      icon: FaShip,
      options: [
        { value: '1', label: '1st Class (Upper)' },
        { value: '2', label: '2nd Class (Middle)' },
        { value: '3', label: '3rd Class (Lower)' }
      ]
    },
    {
      name: 'sex',
      label: 'Gender',
      type: 'select',
      icon: FaVenusMars,
      options: [
        { value: 'male', label: 'Male' },
        { value: 'female', label: 'Female' }
      ]
    },
    {
      name: 'age',
      label: 'Age',
      type: 'number',
      icon: FaCalendar,
      min: '0',
      max: '100',
      step: '1',
      placeholder: 'e.g., 30'
    },
    {
      name: 'sibsp',
      label: 'Siblings/Spouses Aboard',
      type: 'number',
      icon: FaUsers,
      min: '0',
      max: '10',
      step: '1',
      placeholder: '0'
    },
    {
      name: 'parch',
      label: 'Parents/Children Aboard',
      type: 'number',
      icon: FaUsers,
      min: '0',
      max: '10',
      step: '1',
      placeholder: '0'
    },
    {
      name: 'fare',
      label: 'Fare (£)',
      type: 'number',
      icon: FaMoneyBillWave,
      min: '0',
      step: '0.01',
      placeholder: 'e.g., 10.50'
    },
    {
      name: 'embarked',
      label: 'Port of Embarkation',
      type: 'select',
      icon: FaShip,
      options: [
        { value: 'S', label: 'Southampton (S)' },
        { value: 'C', label: 'Cherbourg (C)' },
        { value: 'Q', label: 'Queenstown (Q)' }
      ]
    },
    {
      name: 'cabin',
      label: 'Cabin',
      type: 'text',
      icon: FaShip,
      placeholder: 'e.g., C85 (optional)'
    }
  ];

  return (
    <div className="max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h2 className="text-4xl font-bold gradient-text mb-4">
          Predict Survival Probability
        </h2>
        <p className="text-gray-600 dark:text-gray-400 text-lg">
          Enter passenger details to predict their survival chances on the Titanic
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Form */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-effect rounded-2xl shadow-xl p-8 card-hover"
        >
          <form onSubmit={handleSubmit} className="space-y-6">
            {inputFields.map((field, index) => (
              <motion.div
                key={field.name}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
              >
                <label className="label-text flex items-center space-x-2">
                  <field.icon className="text-blue-600 dark:text-blue-400" />
                  <span>{field.label}</span>
                </label>
                
                {field.type === 'select' ? (
                  <select
                    name={field.name}
                    value={formData[field.name]}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    {field.options.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    type={field.type}
                    name={field.name}
                    value={formData[field.name]}
                    onChange={handleChange}
                    className="input-field"
                    placeholder={field.placeholder}
                    min={field.min}
                    max={field.max}
                    step={field.step}
                    required={field.name !== 'name' && field.name !== 'cabin'}
                  />
                )}
              </motion.div>
            ))}

            <div className="flex space-x-4 pt-4">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 btn-primary flex items-center justify-center space-x-2"
              >
                {loading ? (
                  <>
                    <FaSpinner className="animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <span>Predict Survival</span>
                )}
              </button>
              <button
                type="button"
                onClick={handleReset}
                className="btn-secondary"
                disabled={loading}
              >
                Reset
              </button>
            </div>
          </form>
        </motion.div>

        {/* Result */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
        >
          {prediction ? (
            <PredictionResult prediction={prediction} />
          ) : (
            <div className="glass-effect rounded-2xl shadow-xl p-8 h-full flex items-center justify-center">
              <div className="text-center">
                <FaShip className="text-6xl text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                <p className="text-gray-500 dark:text-gray-400 text-lg">
                  Fill out the form and click "Predict Survival" to see results
                </p>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default PredictionForm;
