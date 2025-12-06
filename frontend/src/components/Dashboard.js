import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { FaChartBar, FaUsers, FaPercent, FaBrain } from 'react-icons/fa';
import { getFeatureImportance } from '../services/api';

const Dashboard = () => {
  const [featureImportance, setFeatureImportance] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFeatureImportance();
  }, []);

  const loadFeatureImportance = async () => {
    try {
      const data = await getFeatureImportance();
      setFeatureImportance(data.features.slice(0, 10));
    } catch (error) {
      console.error('Failed to load feature importance:', error);
    } finally {
      setLoading(false);
    }
  };

  // Sample survival data by demographics
  const survivalByClass = [
    { name: '1st Class', survived: 62.96, died: 37.04 },
    { name: '2nd Class', survived: 47.28, died: 52.72 },
    { name: '3rd Class', survived: 24.24, died: 75.76 }
  ];

  const survivalByGender = [
    { name: 'Female', value: 74.20, color: '#ec4899' },
    { name: 'Male', value: 18.89, color: '#3b82f6' }
  ];

  const survivalByAge = [
    { name: 'Children (0-12)', survived: 54 },
    { name: 'Teens (13-18)', survived: 42 },
    { name: 'Adults (19-35)', survived: 38 },
    { name: 'Middle (36-60)', survived: 41 },
    { name: 'Seniors (60+)', survived: 22 }
  ];

  const statCards = [
    {
      title: 'Overall Survival Rate',
      value: '38.4%',
      icon: FaUsers,
      color: 'from-blue-500 to-blue-600',
      description: '342 out of 891 passengers survived'
    },
    {
      title: 'Model Accuracy',
      value: '85.2%',
      icon: FaBrain,
      color: 'from-purple-500 to-purple-600',
      description: 'Using ensemble stacked models'
    },
    {
      title: 'Female Survival Rate',
      value: '74.2%',
      icon: FaPercent,
      color: 'from-pink-500 to-pink-600',
      description: 'Significantly higher than males'
    },
    {
      title: '1st Class Survival',
      value: '63.0%',
      icon: FaChartBar,
      color: 'from-green-500 to-green-600',
      description: 'Highest survival by passenger class'
    }
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h2 className="text-4xl font-bold gradient-text mb-4">
          Data Insights Dashboard
        </h2>
        <p className="text-gray-600 dark:text-gray-400 text-lg">
          Explore survival patterns and model performance metrics
        </p>
      </motion.div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="glass-effect rounded-2xl p-6 card-hover"
          >
            <div className={`inline-flex p-3 rounded-xl bg-gradient-to-r ${stat.color} mb-4`}>
              <stat.icon className="text-2xl text-white" />
            </div>
            <h3 className="text-3xl font-bold text-gray-800 dark:text-white mb-2">
              {stat.value}
            </h3>
            <p className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">
              {stat.title}
            </p>
            <p className="text-xs text-gray-600 dark:text-gray-400">
              {stat.description}
            </p>
          </motion.div>
        ))}
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Survival by Class */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="glass-effect rounded-2xl p-6 card-hover"
        >
          <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-6">
            Survival Rate by Passenger Class
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={survivalByClass}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1f2937', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#fff'
                }} 
              />
              <Legend />
              <Bar dataKey="survived" fill="#10b981" name="Survived %" radius={[8, 8, 0, 0]} />
              <Bar dataKey="died" fill="#ef4444" name="Died %" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Survival by Gender */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="glass-effect rounded-2xl p-6 card-hover"
        >
          <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-6">
            Survival Rate by Gender
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={survivalByGender}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {survivalByGender.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `${value}%`} />
            </PieChart>
          </ResponsiveContainer>
          <p className="text-center text-sm text-gray-600 dark:text-gray-400 mt-4">
            Women and children first policy significantly impacted survival
          </p>
        </motion.div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Survival by Age Group */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
          className="glass-effect rounded-2xl p-6 card-hover"
        >
          <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-6">
            Survival Rate by Age Group
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={survivalByAge} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis type="number" stroke="#9ca3af" />
              <YAxis dataKey="name" type="category" stroke="#9ca3af" width={120} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1f2937', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#fff'
                }} 
                formatter={(value) => `${value}%`}
              />
              <Bar dataKey="survived" fill="#8b5cf6" name="Survival %" radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Feature Importance */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.7 }}
          className="glass-effect rounded-2xl p-6 card-hover"
        >
          <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-6">
            Top 10 Feature Importance
          </h3>
          {loading ? (
            <div className="flex items-center justify-center h-[300px]">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={featureImportance} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis type="number" stroke="#9ca3af" />
                <YAxis dataKey="name" type="category" stroke="#9ca3af" width={100} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1f2937', 
                    border: 'none', 
                    borderRadius: '8px',
                    color: '#fff'
                  }} 
                  formatter={(value) => value.toFixed(4)}
                />
                <Bar dataKey="importance" fill="#3b82f6" radius={[0, 8, 8, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </motion.div>
      </div>

      {/* Key Insights */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="glass-effect rounded-2xl p-8"
      >
        <h3 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">
          Key Insights from the Data
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            {
              title: "Gender Impact",
              description: "74% of women survived compared to only 19% of men, reflecting the 'women and children first' protocol."
            },
            {
              title: "Class Matters",
              description: "First-class passengers had a 63% survival rate, while third-class passengers had only 24%."
            },
            {
              title: "Age Factor",
              description: "Children under 12 had a 54% survival rate, higher than most adult age groups."
            },
            {
              title: "Family Size",
              description: "Passengers with 1-3 family members had better survival rates than those alone or in large groups."
            },
            {
              title: "Fare Correlation",
              description: "Higher fares (indicating better accommodations) strongly correlated with survival."
            },
            {
              title: "Embarkation Port",
              description: "Passengers from Cherbourg (mostly first-class) had higher survival rates than other ports."
            }
          ].map((insight, index) => (
            <div
              key={index}
              className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-800 dark:to-gray-700 p-6 rounded-xl"
            >
              <h4 className="font-bold text-gray-800 dark:text-white mb-2">{insight.title}</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">{insight.description}</p>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;
