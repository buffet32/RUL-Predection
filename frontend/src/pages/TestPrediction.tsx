 import { useState, useEffect } from 'react';
  import { getMachines, createPrediction } from '../services/api';
  import type { Machine, Prediction, PredictionRequest } from '../types';

  const HEALTHY_EXAMPLE = {
    setting_1: -0.0,
    setting_2: 0.0,
    setting_3: 100.0,
    sensor_2: 518.67,
    sensor_3: 642.41,
    sensor_4: 1587.28,
    sensor_6: 14.62,
    sensor_7: 21.61,
    sensor_8: 553.89,
    sensor_9: 2388.06,
    sensor_11: 1.3,
    sensor_12: 47.37,
    sensor_13: 521.86,
    sensor_14: 2388.06,
    sensor_15: 8138.54,
    sensor_17: 0.03,
    sensor_20: 100.0,
    sensor_21: 38.92,
  };

  const CRITICAL_EXAMPLE = {
    setting_1: -0.0014,
    setting_2: -0.0,
    setting_3: 100.0,
    sensor_2: 518.67,
    sensor_3: 643.49,
    sensor_4: 1602.36,
    sensor_6: 14.62,
    sensor_7: 21.61,
    sensor_8: 552.14,
    sensor_9: 2388.15,
    sensor_11: 1.3,
    sensor_12: 48.07,
    sensor_13: 520.48,
    sensor_14: 2388.14,
    sensor_15: 8217.95,
    sensor_17: 0.03,
    sensor_20: 100.0,
    sensor_21: 38.29,
  };

  type SensorValues = typeof HEALTHY_EXAMPLE;

  export default function TestPrediction() {
    const [machines, setMachines] = useState<Machine[]>([]);
    const [selectedMachineId, setSelectedMachineId] = useState<number | ''>('');
    const [sensorValues, setSensorValues] = useState<SensorValues>(HEALTHY_EXAMPLE);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<Prediction | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
      getMachines(0, 100).then(setMachines).catch(console.error);
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      if (!selectedMachineId) {
        setError('Please select a machine');
        return;
      }
      try {
        setLoading(true);
        setError(null);
        setResult(null);
        const request: PredictionRequest = {
          machine_id: selectedMachineId as number,
          cycle: 0,
          ...sensorValues,
        };
        const prediction = await createPrediction(request);
        setResult(prediction);
      } catch (err) {
        setError('Failed to run prediction. Make sure the backend is running.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    const getStatusBadgeClass = (status: string) => {
      switch (status) {
        case 'NORMAL': return 'status-normal';
        case 'MONITOR': return 'status-monitor';
        case 'MAINTENANCE_RECOMMENDED': return 'status-maintenance';
        case 'CRITICAL': return 'status-critical';
        default: return 'status-normal';
      }
    };

    const getStatusExplanation = (status: string) => {
      switch (status) {
        case 'NORMAL': return 'Machine is operating within normal parameters. No action required.';
        case 'MONITOR': return 'Machine shows early signs of degradation. Monitor closely.';
        case 'MAINTENANCE_RECOMMENDED': return 'Machine requires maintenance soon. Schedule within the next operational window.';
        case 'CRITICAL': return 'Machine is in critical condition. Immediate maintenance required to prevent failure.';
        default: return '';
      }
    };

    const sensorFields = Object.keys(HEALTHY_EXAMPLE).filter(k => k !== 'cycle_number') as (keyof
  SensorValues)[];

    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-[#1E293B]">Test Prediction</h2>
          <p className="text-[#64748B] mt-1">Run AI predictions manually with custom sensor inputs</p>
        </div>

        {/* Result */}
        {result && (
          <div className={`scada-card p-6 border-l-4 ${
            result.maintenance_status === 'NORMAL' ? 'border-l-[#10B981]' :
            result.maintenance_status === 'MONITOR' ? 'border-l-[#F59E0B]' :
            result.maintenance_status === 'MAINTENANCE_RECOMMENDED' ? 'border-l-[#EA580C]' :
            'border-l-[#EF4444]'
          }`}>
            <div className="flex items-center gap-3 mb-4">
              <span className="text-3xl">🤖</span>
              <h3 className="text-xl font-bold text-[#1E293B]">Prediction Result</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-4">
              <div>
                <h4 className="text-xs font-bold text-[#64748B] uppercase tracking-wide mb-1">Predicted
  RUL</h4>
                <p className="text-3xl font-bold text-[#1E293B] font-mono-data">
                  {result.predicted_rul.toFixed(1)}
                </p>
                <p className="text-sm text-[#64748B]">cycles</p>
              </div>
              <div>
                <h4 className="text-xs font-bold text-[#64748B] uppercase tracking-wide mb-1">Health
  Score</h4>
                <p className="text-3xl font-bold text-[#1E293B] font-mono-data">
                  {result.health_score.toFixed(1)}
                </p>
                <p className="text-sm text-[#64748B]">out of 100</p>
              </div>
              <div>
                <h4 className="text-xs font-bold text-[#64748B] uppercase tracking-wide mb-1">Status</h4>
                <span className={`status-badge ${getStatusBadgeClass(result.maintenance_status)}`}>
                  {result.maintenance_status}
                </span>
              </div>
            </div>
            <div className="bg-[#F8FAFC] rounded-xl p-4 border border-[#E2E8F0]">
              <p className="text-[#475569] text-sm leading-relaxed">
                💡 {getStatusExplanation(result.maintenance_status)}
              </p>
            </div>
          </div>
        )}

        {error && (
          <div className="scada-card p-4 border-l-4 border-l-[#EF4444] bg-[#FEF2F2]">
            <p className="text-[#DC2626] font-medium">❌ {error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Machine Selection */}
          <div className="scada-card p-6">
            <h3 className="text-lg font-semibold text-[#1E293B] mb-4">Configuration</h3>
            <div>
              <label className="block text-sm font-semibold text-[#64748B] mb-2">
                Machine <span className="text-[#EF4444]">*</span>
              </label>
              <select
                value={selectedMachineId}
                onChange={(e) => setSelectedMachineId(e.target.value ? parseInt(e.target.value) : '')}
                required
                className="w-full px-4 py-2.5 border border-[#E2E8F0] rounded-lg text-[#1E293B]"
              >
                <option value="">Select a machine...</option>
                {machines.map(m => (
                  <option key={m.id} value={m.id}>{m.name} (ID: {m.id})</option>
                ))}
              </select>
            </div>

            {/* Presets */}
            <div className="flex gap-3 mt-4">
              <button
                type="button"
                onClick={() => setSensorValues(HEALTHY_EXAMPLE)}
                className="px-4 py-2 rounded-lg bg-[#D1FAE5] text-[#065F46] font-semibold text-sm
  hover:bg-[#A7F3D0] transition-colors"
              >
                ✅ Load Healthy Example
              </button>
              <button
                type="button"
                onClick={() => setSensorValues(CRITICAL_EXAMPLE)}
                className="px-4 py-2 rounded-lg bg-[#FEE2E2] text-[#991B1B] font-semibold text-sm
  hover:bg-[#FECACA] transition-colors"
              >
                🔴 Load Critical Example
              </button>
            </div>
          </div>

          {/* Sensor Inputs */}
          <div className="scada-card p-6">
            <h3 className="text-lg font-semibold text-[#1E293B] mb-4">Sensor Readings</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
              {sensorFields.map((field) => (
                <div key={field}>
                  <label className="block text-xs font-bold text-[#64748B] uppercase tracking-wide mb-1">
                    {field.replace('_', ' ')}
                  </label>
                  <input
                    type="number"
                    step="any"
                    value={sensorValues[field]}
                    onChange={(e) => setSensorValues(prev => ({ ...prev, [field]: parseFloat(e.target.value)
  }))}
                    className="w-full px-3 py-2 border border-[#E2E8F0] rounded-lg text-sm text-[#1E293B]
  font-mono-data"
                  />
                </div>
              ))}
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 bg-gradient-to-r from-[#667EEA] to-[#764BA2] text-white rounded-xl
  font-bold text-lg hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? '⏳ Running AI Prediction...' : '🚀 Run Prediction'}
          </button>
        </form>
      </div>
    );
  }
