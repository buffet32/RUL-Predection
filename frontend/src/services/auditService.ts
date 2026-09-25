import axios from 'axios';

  const API_BASE = 'http://localhost:8000/api/v1/audit';

  export interface AuditStatus {
    audit_id: string;
    status: string;
    data_health_score: number | null;
    total_issues: number;
    critical_issues: number;
    warning_issues: number;
    execution_time_seconds: number | null;
  }

  export interface AuditReport {
    completed_at: Date;
    audit_id: string;
    status: string;
    data_health_score: number | null;
    total_checks: number;
    passed_checks: number;
    failed_checks: number;
    total_issues: number;
    critical_issues: number;
    warning_issues: number;
    info_issues: number;
    issues: Array<{
      category: string;
      check_name: string;
      severity: string;
      description: string;
      affected_items: string[];
      count: number;
      recommendation: string;
    }>;
    recommendations: string[];
    execution_time_seconds: number | null;
  }

  export interface HealthCheck {
    status: string;
    message: string;
    data_health_score: number | null;
    latest_audit: AuditReport | null;
  }

  export const auditService = {
    async getHealth(): Promise<HealthCheck> {
      const response = await axios.get(`${API_BASE}/health`);
      return response.data;
    },

    async triggerAudit(): Promise<{ audit_id: string; status: string; message: string }> {
      const response = await axios.post(`${API_BASE}/run-audit`);
      return response.data;
    },

    async getStatus(auditId: string): Promise<AuditStatus> {
      const response = await axios.get(`${API_BASE}/status/${auditId}`);
      return response.data;
    },

    async getReport(auditId: string): Promise<AuditReport> {
      const response = await axios.get(`${API_BASE}/report/${auditId}`);
      return response.data;
    },

    async getLatest(): Promise<AuditReport> {
      const response = await axios.get(`${API_BASE}/latest`);
      return response.data;
    },

    async getHistory(limit: number = 10): Promise<AuditReport[]> {
      const response = await axios.get(`${API_BASE}/history?limit=${limit}`);
      return response.data;
    },
  };
  