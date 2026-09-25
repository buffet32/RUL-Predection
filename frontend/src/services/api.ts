import axios from 'axios';
import type {
  Machine,
  MachineCreate,
  MachineUpdate,
  SensorReading,
  SensorReadingCreate,
  Prediction,
  PredictionRequest,
  MaintenanceStatus,
  MaintenanceSummary,
  HealthCheck
} from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health Check
export const getHealthCheck = async (): Promise<HealthCheck> => {
  const response = await api.get('/health');
  return response.data;
};

// Machines
export const getMachines = async (skip = 0, limit = 100): Promise<Machine[]> => {
  const response = await api.get(`/machines/?skip=${skip}&limit=${limit}`);
  return response.data;
};

export const getMachine = async (machineId: number): Promise<Machine> => {
  const response = await api.get(`/machines/${machineId}`);
  return response.data;
};

export const createMachine = async (machine: MachineCreate): Promise<Machine> => {
  const response = await api.post('/machines/', machine);
  return response.data;
};

export const updateMachine = async (machineId: number, machine: MachineUpdate): Promise<Machine> => {
  const response = await api.put(`/machines/${machineId}`, machine);
  return response.data;
};

export const deleteMachine = async (machineId: number): Promise<void> => {
  await api.delete(`/machines/${machineId}`);
};

// Sensor Readings
export const getSensorReadings = async (
  machineId?: number,
  skip = 0,
  limit = 100
): Promise<SensorReading[]> => {
  const params = new URLSearchParams({ skip: skip.toString(), limit: limit.toString() });
  if (machineId) params.append('machine_id', machineId.toString());
  const response = await api.get(`/sensor-readings/?${params.toString()}`);
  return response.data;
};

export const createSensorReading = async (reading: SensorReadingCreate): Promise<SensorReading> => {
  const response = await api.post('/sensor-readings/', reading);
  return response.data;
};

// Predictions
export const getPredictions = async (
  machineId?: number,
  skip = 0,
  limit = 100
): Promise<Prediction[]> => {
  const params = new URLSearchParams({ skip: skip.toString(), limit: limit.toString() });
  if (machineId) params.append('machine_id', machineId.toString());
  const response = await api.get(`/predictions/?${params.toString()}`);
  return response.data;
};

export const getPrediction = async (predictionId: number): Promise<Prediction> => {
  const response = await api.get(`/predictions/${predictionId}`);
  return response.data;
};

export const createPrediction = async (request: PredictionRequest): Promise<Prediction> => {
  const response = await api.post('/predictions/', request);
  return response.data;
};

// Maintenance
export const getMaintenanceStatus = async (machineId: number): Promise<MaintenanceStatus> => {
  const response = await api.get(`/maintenance/status/${machineId}`);
  return response.data;
};

export const getMaintenanceSummary = async (): Promise<MaintenanceSummary> => {
  const response = await api.get('/maintenance/summary');
  return response.data;
};

// Reports
export const getWeeklySummary = async (): Promise<any> => {
  const response = await api.get('/weekly-summary');
  return response.data;
};

export default api;
