export interface Machine {
  id: number;
  name: string;
  description?: string;
  location?: string;
  created_at: string;
  updated_at: string;
}

export interface MachineCreate {
  name: string;
  description?: string;
  location?: string;
}

export interface MachineUpdate {
  description?: string;
  location?: string;
}

export interface SensorReading {
  id: number;
  machine_id: number;
  cycle: number;
  timestamp: string;
  setting_1: number;
  setting_2: number;
  setting_3: number;
  sensor_2: number;
  sensor_3: number;
  sensor_4: number;
  sensor_6: number;
  sensor_7: number;
  sensor_8: number;
  sensor_9: number;
  sensor_11: number;
  sensor_12: number;
  sensor_13: number;
  sensor_14: number;
  sensor_15: number;
  sensor_17: number;
  sensor_20: number;
  sensor_21: number;
}

export interface SensorReadingCreate {
  machine_id: number;
  cycle: number;
  setting_1: number;
  setting_2: number;
  setting_3: number;
  sensor_2: number;
  sensor_3: number;
  sensor_4: number;
  sensor_6: number;
  sensor_7: number;
  sensor_8: number;
  sensor_9: number;
  sensor_11: number;
  sensor_12: number;
  sensor_13: number;
  sensor_14: number;
  sensor_15: number;
  sensor_17: number;
  sensor_20: number;
  sensor_21: number;
}

export interface Prediction {
  id: number;
  machine_id: number;
  timestamp: string;
  predicted_rul: number;
  effective_rul: number;
  health_score: number;
  maintenance_status: string;
  safety_margin_applied: number;
}

export interface PredictionRequest {
  machine_id: number;
  cycle: number;
  setting_1: number;
  setting_2: number;
  setting_3: number;
  sensor_2: number;
  sensor_3: number;
  sensor_4: number;
  sensor_6: number;
  sensor_7: number;
  sensor_8: number;
  sensor_9: number;
  sensor_11: number;
  sensor_12: number;
  sensor_13: number;
  sensor_14: number;
  sensor_15: number;
  sensor_17: number;
  sensor_20: number;
  sensor_21: number;
}

export interface MaintenanceStatus {
  machine_id: number;
  status: string;
  predicted_rul: number;
  effective_rul: number;
  health_score: number;
  last_prediction_timestamp: string;
}

export interface MaintenanceSummary {
  normal_count: any;
  monitor_count: any;
  maintenance_count: any;
  critical_count: any;
  total_machines: number;
  status_breakdown: Record<string, number>;
}

export interface HealthCheck {
  status: string;
  app_name: string;
  app_version: string;
  database_connected: boolean;
  model_loaded: boolean;
}

export type MaintenanceStatusType = 'NORMAL' | 'MONITOR' | 'MAINTENANCE_RECOMMENDED' | 'CRITICAL' | 'NO_DATA';
