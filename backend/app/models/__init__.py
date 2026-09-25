
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Machine(Base):
      """Machine model for tracking equipment"""
      __tablename__ = "machines"

      id = Column(Integer, primary_key=True, index=True)
      name = Column(String, unique=True, index=True, nullable=False)
      model = Column(String, nullable=True)
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