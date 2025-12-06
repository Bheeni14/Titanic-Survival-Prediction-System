import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const predictSurvival = async (passengerData) => {
  try {
    const response = await api.post('/api/v1/predict', passengerData);
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || 'Failed to make prediction';
  }
};

export const batchPredict = async (passengers) => {
  try {
    const response = await api.post('/api/v1/predict/batch', { passengers });
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || 'Failed to make batch prediction';
  }
};

export const getModelInfo = async () => {
  try {
    const response = await api.get('/api/v1/model/info');
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || 'Failed to fetch model info';
  }
};

export const getModelMetrics = async () => {
  try {
    const response = await api.get('/api/v1/model/metrics');
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || 'Failed to fetch model metrics';
  }
};

export const getFeatureImportance = async () => {
  try {
    const response = await api.get('/api/v1/visualizations/feature-importance');
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || 'Failed to fetch feature importance';
  }
};

export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || 'Health check failed';
  }
};

export default api;
