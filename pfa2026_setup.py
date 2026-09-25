  #!/usr/bin/env python3
if True:
  """
  Complete Data Quality Audit Agent Setup Script
  Runs all necessary setup steps for the system
  """

  import os
  import sys
  from pathlib import Path

  def create_file(path, content):
      """Create a file with content"""
      path = Path(path)
      path.parent.mkdir(parents=True, exist_ok=True)
      with open(path, 'w') as f:
          f.write(content)
      print(f"✓ Created {path}")

  def main():
      base_path = Path(__file__).parent

      print("="*80)
      print("DATA QUALITY AUDIT AGENT - COMPLETE SETUP")
      print("="*80)

      # ============ STEP 1: Frontend Audit Service ============
      print("\n[STEP 1] Creating Frontend Audit Service...")

      audit_service = '''import axios from 'axios';

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
  '''
      create_file(base_path / "frontend" / "src" / "services" / "auditService.ts", audit_service)

      # ============ STEP 2: Data Quality Dashboard ============
      print("\n[STEP 2] Creating Data Quality Dashboard Component...")

      dashboard = '''import { useEffect, useState } from 'react';
  import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
  import { auditService, AuditReport, AuditStatus } from '../services/auditService';

  export default function DataQuality() {
    const [health, setHealth] = useState<AuditReport | null>(null);
    const [history, setHistory] = useState<AuditReport[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [running, setRunning] = useState(false);
    const [selectedAudit, setSelectedAudit] = useState<AuditReport | null>(null);
    const [activeTab, setActiveTab] = useState<'overview' | 'issues' | 'history'>('overview');

    useEffect(() => {
      loadData();
    }, []);

    const loadData = async () => {
      try {
        setLoading(true);
        const latestReport = await auditService.getLatest().catch(() => null);
        const historyData = await auditService.getHistory(10).catch(() => []);

        setHealth(latestReport);
        setHistory(historyData);
        setSelectedAudit(latestReport);
        setError(null);
      } catch (err) {
        setError('Failed to load audit data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    const handleRunAudit = async () => {
      try {
        setRunning(true);
        const result = await auditService.triggerAudit();
        alert(`Audit started: ${result.audit_id}`);
   
        const pollInterval = setInterval(async () => {
          try {
            const status = await auditService.getStatus(result.audit_id);
            if (status.status === 'completed') {
              clearInterval(pollInterval);
              loadData();
              setRunning(false);
            }
          } catch (err) {
            console.log('Still waiting...');
          }
        }, 2000);

        setTimeout(() => clearInterval(pollInterval), 300000);
      } catch (err) {
        alert('Failed to start audit');
        setRunning(false);
      }
    };

    const getHealthColor = (score: number | null): string => {
      if (score === null) return '#9CA3AF';
      if (score >= 90) return '#10B981';
      if (score >= 75) return '#3B82F6';
      if (score >= 60) return '#F59E0B';
      if (score >= 45) return '#EF4444';
      return '#7F1D1D';
    };

    const getHealthStatus = (score: number | null): string => {
      if (score === null) return 'Unknown';
      if (score >= 90) return 'Excellent';
      if (score >= 75) return 'Good';
      if (score >= 60) return 'Fair';
      if (score >= 45) return 'Poor';
      return 'Critical';
    };

    const getSeverityColor = (severity: string): string => {
      switch (severity) {
        case 'critical': return '#EF4444';
        case 'warning': return '#F59E0B';
        case 'info': return '#3B82F6';
        default: return '#6B7280';
      }
    };

    if (loading && !health) {
      return (
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading audit data...</p>
          </div>
        </div>
      );
    }

    const healthTrendData = history.map((audit, idx) => ({
      date: new Date(audit.completed_at || new Date()).toLocaleDateString(),
      score: audit.data_health_score || 0,
      issues: audit.total_issues,
    })).reverse();

    const issuesBreakdown = selectedAudit ? [
      { name: 'Critical', value: selectedAudit.critical_issues, fill: '#EF4444' },
      { name: 'Warnings', value: selectedAudit.warning_issues, fill: '#F59E0B' },
      { name: 'Info', value: selectedAudit.info_issues, fill: '#3B82F6' },
    ].filter(item => item.value > 0) : [];

    const checkBreakdown = selectedAudit ? [
      { name: 'Passed', value: selectedAudit.passed_checks, fill: '#10B981' },
      { name: 'Failed', value: selectedAudit.failed_checks, fill: '#EF4444' },
    ] : [];

    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Data Quality Audit</h1>
            <p className="text-gray-600 mt-1">Monitor data health and detect quality issues</p>
          </div>
          <button
            onClick={handleRunAudit}
            disabled={running}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-lg font-medium transition"
          >
            {running ? 'Running Audit...' : 'Run New Audit'}
          </button>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {health && (
          <div className="bg-white rounded-lg shadow-md p-6 border-l-4" style={{ borderLeftColor: getHealthColor(health.data_health_score) }}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Overall Data Health</p>
                <div className="flex items-baseline gap-2 mt-2">
                  <span className="text-4xl font-bold" style={{ color: getHealthColor(health.data_health_score) }}>
                    {health.data_health_score?.toFixed(1) || 'N/A'}
                  </span>
                  <span className="text-gray-600">/100</span>
                </div>
                <p className="text-sm text-gray-500 mt-2">{getHealthStatus(health.data_health_score)}</p>
              </div>

              <div className="flex flex-col items-center">
                <div className="relative h-32 w-32">
                  <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="45" fill="none" stroke="#E5E7EB" strokeWidth="8" />
                    <circle
                      cx="50"
                      cy="50"
                      r="45"
                      fill="none"
                      stroke={getHealthColor(health.data_health_score)}
                      strokeWidth="8"
                      strokeDasharray={`${2 * Math.PI * 45 * (health.data_health_score || 0) / 100} ${2 * Math.PI * 45}`}
                      strokeLinecap="round"
                    />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-lg font-bold text-gray-900">{(health.data_health_score || 0).toFixed(0)}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {health && [
            { label: 'Total Checks', value: health.total_checks, color: '#3B82F6' },
            { label: 'Passed', value: health.passed_checks, color: '#10B981' },
            { label: 'Critical Issues', value: health.critical_issues, color: '#EF4444' },
            { label: 'Warnings', value: health.warning_issues, color: '#F59E0B' },
          ].map((metric, idx) => (
            <div key={idx} className="bg-white rounded-lg shadow p-4">
              <p className="text-gray-600 text-sm">{metric.label}</p>
              <p className="text-2xl font-bold mt-2" style={{ color: metric.color }}>
                {metric.value}
              </p>
            </div>
          ))}
        </div>

        <div className="border-b border-gray-200">
          <div className="flex gap-4">
            {(['overview', 'issues', 'history'] as const).map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 font-medium text-sm border-b-2 transition ${
                  activeTab === tab
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>
        </div>

        <div>
          {activeTab === 'overview' && selectedAudit && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Issues by Severity</h3>
                {issuesBreakdown.length > 0 ? (
                  <ResponsiveContainer width="100%" height={250}>
                    <PieChart>
                      <Pie
                        data={issuesBreakdown}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, value }) => `${name}: ${value}`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {issuesBreakdown.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.fill} />
                        ))}
                      </Pie>
                    </PieChart>
                  </ResponsiveContainer>
                ) : (
                  <p className="text-gray-600 text-center py-8">No issues found</p>
                )}
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Checks Status</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={checkBreakdown}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#3B82F6">
                      {checkBreakdown.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.fill} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {activeTab === 'issues' && selectedAudit && (
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 border-b border-gray-200">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Check</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Category</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Severity</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Description</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Count</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedAudit.issues && selectedAudit.issues.length > 0 ? (
                      selectedAudit.issues.map((issue, idx) => (
                        <tr key={idx} className="border-b border-gray-200 hover:bg-gray-50">
                          <td className="px-6 py-4 text-sm font-medium text-gray-900">{issue.check_name}</td>
                          <td className="px-6 py-4 text-sm text-gray-600">{issue.category}</td>
                          <td className="px-6 py-4 text-sm">
                            <span
                              className="px-2 py-1 rounded-full text-xs font-medium text-white"
                              style={{ backgroundColor: getSeverityColor(issue.severity) }}
                            >
                              {issue.severity}
                            </span>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-600">{issue.description}</td>
                          <td className="px-6 py-4 text-sm font-medium text-gray-900">{issue.count}</td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={5} className="px-6 py-8 text-center text-gray-600">
                          No issues found
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'history' && (
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Health Score Trend</h3>
                {healthTrendData.length > 0 ? (
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={healthTrendData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis domain={[0, 100]} />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="score" stroke="#3B82F6" name="Health Score" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                ) : (
                  <p className="text-gray-600 text-center py-8">No history data</p>
                )}
              </div>

              <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-50 border-b border-gray-200">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Date</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Health Score</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Issues</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Status</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {history.map((audit, idx) => (
                        <tr key={idx} className="border-b border-gray-200 hover:bg-gray-50 cursor-pointer" onClick={() => setSelectedAudit(audit)}>
                          <td className="px-6 py-4 text-sm text-gray-900">
                            {new Date(audit.completed_at || new Date()).toLocaleString()}
                          </td>
                          <td className="px-6 py-4 text-sm">
                            <span
                              className="px-2 py-1 rounded-full text-xs font-medium text-white"
                              style={{ backgroundColor: getHealthColor(audit.data_health_score) }}
                            >
                              {audit.data_health_score?.toFixed(1) || 'N/A'}/100
                            </span>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-600">{audit.total_issues}</td>
                          <td className="px-6 py-4 text-sm">
                            <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                              {audit.status}
                            </span>
                          </td>
                          <td className="px-6 py-4 text-sm">
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                setSelectedAudit(audit);
                                setActiveTab('issues');
                              }}
                              className="text-blue-600 hover:text-blue-900 font-medium"
                            >
                              View Details
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>

        {selectedAudit && selectedAudit.recommendations && selectedAudit.recommendations.length > 0 && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-3">Recommendations</h3>
            <ul className="space-y-2">
              {selectedAudit.recommendations.map((rec, idx) => (
                <li key={idx} className="flex items-start gap-3">
                  <span className="text-blue-600 font-bold mt-1">•</span>
                  <span className="text-blue-800">{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  }
  '''
      create_file(base_path / "frontend" / "src" / "pages" / "DataQuality.tsx", dashboard)

      # ============ STEP 3: Backend Models Update ============
      print("\n[STEP 3] Updating Backend Models...")

      models_content = '''from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
  from sqlalchemy.orm import relationship
  from datetime import datetime
  from app.database import Base


  class Machine(Base):
      """Machine model for tracking equipment"""
      __tablename__ = "machines"
   
      id = Column(Integer, primary_key=True, index=True)
      name = Column(String, unique=True, index=True, nullable=False)
      description = Column(String, nullable=True)
      location = Column(String, nullable=True)
      created_at = Column(DateTime, default=datetime.utcnow)
      updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
   
      sensor_readings = relationship("SensorReading", back_populates="machine")
      predictions = relationship("Prediction", back_populates="machine")


  class SensorReading(Base):
      """Sensor reading model for storing sensor data"""
      __tablename__ = "sensor_readings"
   
      id = Column(Integer, primary_key=True, index=True)
      machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)
      cycle = Column(Integer, nullable=False)
      timestamp = Column(DateTime, default=datetime.utcnow)
   
      setting_1 = Column(Float, nullable=False)
      setting_2 = Column(Float, nullable=False)
      setting_3 = Column(Float, nullable=False)
   
      sensor_2 = Column(Float, nullable=False)
      sensor_3 = Column(Float, nullable=False)
      sensor_4 = Column(Float, nullable=False)
      sensor_6 = Column(Float, nullable=False)
      sensor_7 = Column(Float, nullable=False)
      sensor_8 = Column(Float, nullable=False)
      sensor_9 = Column(Float, nullable=False)
      sensor_11 = Column(Float, nullable=False)
      sensor_12 = Column(Float, nullable=False)
      sensor_13 = Column(Float, nullable=False)
      sensor_14 = Column(Float, nullable=False)
      sensor_15 = Column(Float, nullable=False)
      sensor_17 = Column(Float, nullable=False)
      sensor_20 = Column(Float, nullable=False)
      sensor_21 = Column(Float, nullable=False)
   
      machine = relationship("Machine", back_populates="sensor_readings")


  class Prediction(Base):
      """Prediction model for storing RUL predictions"""
      __tablename__ = "predictions"
   
      id = Column(Integer, primary_key=True, index=True)
      machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)
      sensor_reading_id = Column(Integer, ForeignKey("sensor_readings.id"), nullable=True)
      timestamp = Column(DateTime, default=datetime.utcnow)
   
      predicted_rul = Column(Float, nullable=False)
      effective_rul = Column(Float, nullable=False)
      health_score = Column(Float, nullable=False)
      maintenance_status = Column(String, nullable=False)
      safety_margin_applied = Column(Float, nullable=False)
   
      machine = relationship("Machine", back_populates="predictions")


  class AuditLog(Base):
      """Audit log model for tracking data quality audits"""
      __tablename__ = "audit_logs"

      id = Column(Integer, primary_key=True, index=True)
      audit_id = Column(String(36), unique=True, index=True, nullable=False)
      audit_type = Column(String, default="full")
      status = Column(String, nullable=False)

      created_at = Column(DateTime, default=datetime.utcnow, index=True)
      started_at = Column(DateTime, nullable=True)
      completed_at = Column(DateTime, nullable=True)
      execution_time_seconds = Column(Float, nullable=True)

      data_health_score = Column(Float, nullable=True)
      total_checks = Column(Integer, nullable=True)
      passed_checks = Column(Integer, nullable=True)
      failed_checks = Column(Integer, nullable=True)

      total_issues = Column(Integer, nullable=True)
      critical_issues = Column(Integer, nullable=True)
      warning_issues = Column(Integer, nullable=True)
      info_issues = Column(Integer, nullable=True)

      report = Column(JSON, nullable=True)
      issues = Column(JSON, nullable=True)
      sensor_stats = Column(JSON, nullable=True)
      engine_stats = Column(JSON, nullable=True)
      recommendations = Column(JSON, nullable=True)

      error_message = Column(Text, nullable=True)
      data_version = Column(String, nullable=True)
      parameters = Column(JSON, nullable=True)

      def to_dict(self):
          return {
              'id': self.id,
              'audit_id': self.audit_id,
              'audit_type': self.audit_type,
              'status': self.status,
              'created_at': self.created_at.isoformat() if self.created_at else None,
              'started_at': self.started_at.isoformat() if self.started_at else None,
              'completed_at': self.completed_at.isoformat() if self.completed_at else None,
              'execution_time_seconds': self.execution_time_seconds,
              'data_health_score': self.data_health_score,
              'total_checks': self.total_checks,
              'passed_checks': self.passed_checks,
              'failed_checks': self.failed_checks,
              'total_issues': self.total_issues,
              'critical_issues': self.critical_issues,
              'warning_issues': self.warning_issues,
              'info_issues': self.info_issues,
              'issues': self.issues,
              'sensor_stats': self.sensor_stats,
              'engine_stats': self.engine_stats,
              'recommendations': self.recommendations,
              'error_message': self.error_message
          }
  '''
      create_file(base_path / "backend" / "app" / "models" / "__init__.py", models_content)

      # ============ STEP 4: Backend Audit Routes ============
      print("\n[STEP 4] Creating Backend Audit Routes...")

      audit_routes = '''from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
  from sqlalchemy.orm import Session
  from datetime import datetime
  import sys
  from pathlib import Path

  from app.database import get_db
  from app.models import AuditLog
  from app.config import settings
  from pydantic import BaseModel
  from typing import Optional, List, Dict, Any

  ml_path = str(Path(__file__).parent.parent.parent / "ml")
  if ml_path not in sys.path:
      sys.path.insert(0, ml_path)

  try:
      from src.data_quality_audit import DataQualityAudit
      from src.preprocessing import preprocess_training_data, preprocess_test_data
      AUDIT_AVAILABLE = True
  except ImportError as e:
      AUDIT_AVAILABLE = False
      print(f"Warning: Audit not available: {e}")

  router = APIRouter(prefix="/audit", tags=["audit"])


  class AuditStatusResponse(BaseModel):
      audit_id: str
      status: str
      data_health_score: Optional[float]
      total_issues: int
      critical_issues: int

      class Config:
          from_attributes = True


  class AuditReportResponse(BaseModel):
      audit_id: str
      status: str
      data_health_score: Optional[float]
      total_checks: int
      passed_checks: int
      failed_checks: int
      total_issues: int
      critical_issues: int
      warning_issues: int
      issues: Optional[List[Dict]]
      recommendations: Optional[List[str]]
      execution_time_seconds: Optional[float]

      class Config:
          from_attributes = True


  def run_audit_background(db: Session, data_dir: str = None):
      """Run audit in background"""
      try:
          if not AUDIT_AVAILABLE:
              raise Exception("Audit module not available")

          audit = AuditLog(
              audit_id="temp",
              status="running",
              audit_type="full",
              created_at=datetime.utcnow(),
              started_at=datetime.utcnow()
          )
          db.add(audit)
          db.commit()
          db.refresh(audit)

          audit.audit_id = f"audit-{audit.id}"
          db.commit()

          train_df = preprocess_training_data(data_dir or "../../Downloads/archive")
          test_df, rul_df = preprocess_test_data(data_dir or "../../Downloads/archive")

          audit_engine = DataQualityAudit(verbose=False)
          report = audit_engine.audit(train_df, test_df)

          audit.status = "completed"
          audit.completed_at = datetime.utcnow()
          audit.data_health_score = report.data_health_score
          audit.total_checks = report.total_checks
          audit.passed_checks = report.passed_checks
          audit.failed_checks = report.failed_checks
          audit.total_issues = report.total_issues
          audit.critical_issues = report.critical_issues
          audit.warning_issues = report.warning_issues
          audit.info_issues = report.info_issues
          audit.report = report.to_dict()
          audit.issues = report.issues
          audit.sensor_stats = report.sensor_stats
          audit.engine_stats = report.engine_stats
          audit.recommendations = report.recommendations

          delta = datetime.utcnow() - audit.started_at
          audit.execution_time_seconds = delta.total_seconds()

          db.commit()

      except Exception as e:
          audit.status = "failed"
          audit.error_message = str(e)
          audit.completed_at = datetime.utcnow()
          db.commit()


  @router.get("/health")
  def get_audit_health(db: Session = Depends(get_db)):
      """Get current data health status"""
      latest_audit = db.query(AuditLog).filter(
          AuditLog.status == "completed"
      ).order_by(AuditLog.completed_at.desc()).first()

      if not latest_audit:
          return {
              "status": "unknown",
              "message": "No completed audits",
              "data_health_score": None
          }

      return {
          "status": "healthy" if latest_audit.data_health_score >= 75 else "degraded",
          "message": f"Data health: {latest_audit.data_health_score:.1f}/100",
          "data_health_score": latest_audit.data_health_score,
          "latest_audit": latest_audit.to_dict()
      }


  @router.post("/run-audit")
  def trigger_audit(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
      """Trigger a new audit"""
      if not AUDIT_AVAILABLE:
          raise HTTPException(status_code=503, detail="Audit module unavailable")

      audit = AuditLog(
          audit_id="temp",
          status="pending",
          audit_type="full",
          created_at=datetime.utcnow()
      )
      db.add(audit)
      db.commit()
      db.refresh(audit)

      audit.audit_id = f"audit-{audit.id}"
      db.commit()

      background_tasks.add_task(run_audit_background, db, None)

      return {
          "audit_id": audit.audit_id,
          "status": "pending",
          "message": "Audit started"
      }


  @router.get("/report/{audit_id}", response_model=AuditReportResponse)
  def get_audit_report(audit_id: str, db: Session = Depends(get_db)):
      """Retrieve audit report"""
      audit = db.query(AuditLog).filter(AuditLog.audit_id == audit_id).first()
      if not audit:
          raise HTTPException(status_code=404, detail="Audit not found")
      return audit


  @router.get("/latest", response_model=AuditReportResponse)
  def get_latest_audit(db: Session = Depends(get_db)):
      """Get latest audit"""
      audit = db.query(AuditLog).filter(
          AuditLog.status == "completed"
      ).order_by(AuditLog.completed_at.desc()).first()
      if not audit:
          raise HTTPException(status_code=404, detail="No audits found")
      return audit


  @router.get("/history")
  def get_audit_history(limit: int = 10, db: Session = Depends(get_db)):
      """Get audit history"""
      audits = db.query(AuditLog).filter(
          AuditLog.status == "completed"
      ).order_by(AuditLog.completed_at.desc()).limit(limit).all()
      return [audit.to_dict() for audit in audits]


  @router.get("/status/{audit_id}")
  def get_audit_status(audit_id: str, db: Session = Depends(get_db)):
      """Get audit status"""
      audit = db.query(AuditLog).filter(AuditLog.audit_id == audit_id).first()
      if not audit:
          raise HTTPException(status_code=404, detail="Audit not found")
      return {
          "audit_id": audit.audit_id,
          "status": audit.status,
          "data_health_score": audit.data_health_score,
          "total_issues": audit.total_issues,
          "critical_issues": audit.critical_issues,
          "execution_time_seconds": audit.execution_time_seconds
      }
  '''
      create_file(base_path / "backend" / "app" / "routes" / "audit.py", audit_routes)

      # ============ STEP 5: Update main.py ============
      print("\n[STEP 5] Updating Backend Main.py...")

      main_py_path = base_path / "backend" / "app" / "main.py"
      with open(main_py_path, 'r') as f:
          main_content = f.read()

      if 'from app.routes import' in main_content and ', audit' not in main_content:
          main_content = main_content.replace(
              'from app.routes import health, machines, sensor_readings, predictions, maintenance, reports',
              'from app.routes import health, machines, sensor_readings, predictions, maintenance, reports, audit'
          )

      if 'app.include_router(audit.router' not in main_content:
          lines = main_content.split('\n')
          for i, line in enumerate(lines):
              if 'app.include_router(reports.router' in line:
                  lines.insert(i + 1, 'app.include_router(audit.router, prefix=settings.API_PREFIX, tags=["audit"])')
                  break
          main_content = '\n'.join(lines)

      with open(main_py_path, 'w') as f:
          f.write(main_content)
      print("✓ Updated main.py")

      # ============ STEP 6: Update App.tsx ============
      print("\n[STEP 6] Updating Frontend App.tsx...")

      app_tsx_path = base_path / "frontend" / "src" / "App.tsx"
      with open(app_tsx_path, 'r') as f:
          app_content = f.read()

      if "import DataQuality from './pages/DataQuality';" not in app_content:
          import_line = "import Reports from './pages/Reports';"
          new_import = "import Reports from './pages/Reports';\nimport DataQuality from './pages/DataQuality';"
          app_content = app_content.replace(import_line, new_import)

      if '<Route path="/data-quality"' not in app_content:
          route_line = '<Route path="/reports" element={<Reports />} />'
          new_route = '<Route path="/reports" element={<Reports />} />\n            <Route path="/data-quality" element={<DataQuality />} />'
          app_content = app_content.replace(route_line, new_route)

      with open(app_tsx_path, 'w') as f:
          f.write(app_content)
      print("✓ Updated App.tsx")

      # ============ FINAL SUMMARY ============
      print("\n" + "="*80)
      print("✅ SETUP COMPLETE!")
      print("="*80)
      print("\nAll files have been created and updated automatically!")
      print("\nNext Steps:")
      print("\n1️⃣   Install backend dependencies:")
      print("   cd backend")
      print("   python -m venv venv")
      print("   venv\\Scripts\\activate")
      print("   pip install -r requirements.txt")
      print("\n2️⃣   Setup PostgreSQL database:")
      print("   psql -U postgres -c \"CREATE DATABASE predictive_maintenance;\"")
      print("\n3️⃣   Install frontend dependencies:")
      print("   cd frontend")
      print("   npm install")
      print("\n4️⃣   Start backend (Terminal 1):")
      print("   cd backend")
      print("   venv\\Scripts\\activate")
      print("   uvicorn app.main:app --reload --port 8000")
      print("\n5️⃣   Start frontend (Terminal 2):")
      print("   cd frontend")
      print("   npm run dev")
      print("\n6️⃣   Open browser:")
      print("   http://localhost:5173")
      print("   Click '📊 Data Quality' in sidebar")
      print("\n📡 API Endpoints Ready:")
      print("   GET    /api/v1/audit/health")
      print("   POST   /api/v1/audit/run-audit")
      print("   GET    /api/v1/audit/latest")
      print("   GET    /api/v1/audit/history")
      print("   GET    /api/v1/audit/report/{id}")
      print("   GET    /api/v1/audit/status/{id}")

  if __name__ == "__main__":
      main()