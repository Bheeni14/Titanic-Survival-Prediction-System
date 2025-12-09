import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import PredictionForm from './components/PredictionForm';
import Dashboard from './components/Dashboard';
import ModelInfo from './components/ModelInfo';
import { FaShip, FaMoon, FaSun, FaGithub } from 'react-icons/fa';
import { motion } from 'framer-motion';

function App() {
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode');
    return saved === 'true';
  });
  const [activeTab, setActiveTab] = useState('predict');

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const toggleDarkMode = () => {
    const newMode = !darkMode;
    setDarkMode(newMode);
    localStorage.setItem('darkMode', newMode);
    if (newMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  return (
    <Router>
      <div className="min-h-screen">
        <Toaster position="top-right" />
        
        {/* Header */}
        <header className="glass-effect shadow-lg sticky top-0 z-50">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              {/* Logo */}
              <motion.div 
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                className="flex items-center space-x-3"
              >
                <FaShip className="text-4xl text-blue-600 dark:text-blue-400" />
                <div>
                  <h1 className="text-2xl font-bold gradient-text">
                    Titanic Survival Predictor
                  </h1>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    Advanced ML Prediction System
                  </p>
                </div>
              </motion.div>

              {/* Navigation */}
              <nav className="hidden md:flex items-center space-x-6">
                {[
                  { id: 'predict', label: 'Predict' },
                  { id: 'dashboard', label: 'Dashboard' },
                  { id: 'model', label: 'Model Info' }
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`px-4 py-2 rounded-lg font-semibold transition-all duration-300 ${
                      activeTab === tab.id
                        ? 'bg-blue-600 text-white shadow-lg'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </nav>

              {/* Controls */}
              <div className="flex items-center space-x-4">
                <button
                  onClick={toggleDarkMode}
                  className="p-3 rounded-full glass-effect hover:bg-gray-200 dark:hover:bg-gray-700 transition-all duration-300"
                  aria-label="Toggle dark mode"
                >
                  {darkMode ? (
                    <FaSun className="text-xl text-yellow-500" />
                  ) : (
                    <FaMoon className="text-xl text-blue-600" />
                  )}
                </button>
                <a
                  href="https://github.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-3 rounded-full glass-effect hover:bg-gray-200 dark:hover:bg-gray-700 transition-all duration-300"
                  aria-label="View on GitHub"
                >
                  <FaGithub className="text-xl text-gray-800 dark:text-white" />
                </a>
              </div>
            </div>

            {/* Mobile Navigation */}
            <div className="md:hidden mt-4 flex space-x-2">
              {[
                { id: 'predict', label: 'Predict' },
                { id: 'dashboard', label: 'Dashboard' },
                { id: 'model', label: 'Model' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 px-3 py-2 rounded-lg text-sm font-semibold transition-all duration-300 ${
                    activeTab === tab.id
                      ? 'bg-blue-600 text-white shadow-lg'
                      : 'text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-800'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="container mx-auto px-4 py-8">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            {activeTab === 'predict' && <PredictionForm />}
            {activeTab === 'dashboard' && <Dashboard />}
            {activeTab === 'model' && <ModelInfo />}
          </motion.div>
        </main>

        {/* Footer */}
        <footer className="mt-16 py-8 glass-effect">
          <div className="container mx-auto px-4 text-center">
            <p className="text-gray-600 dark:text-gray-400">
              Built with ❤️ using React, FastAPI, and Advanced ML
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
              © 2024 Titanic Survival Predictor. Achieving 82%+ accuracy with state-of-the-art models.
            </p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
