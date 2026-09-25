import { useEffect, useState } from 'react';
  import { useParams, Link } from 'react-router-dom';
  import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from
  'recharts';
  import { getMachine, getPredictions, getSensorReadings } from '../services/api';
  import type { Machine, Prediction, SensorReading } from '../types';

  export default function MachineDetails() {
    const { id } = useParams<{ id: string }>();
    const machineId = parseInt(id || '0', 10);

    const [machine, setMachine] = useState<Machine | null>(null);
    const [predictions, setPredictions] = useState<Prediction[]>([]);
    const [sensorReadings, setSensorReadings] = useState<SensorReading[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
      loadData();
    }, [machineId]);

    const loadData = async () => {
      try {
        setLoading(true);
        const [machineData, predictionsData, readingsData] = await Promise.all([
          getMachine(machineId),
          getPredictions(machineId, 0, 50),
          getSensorReadings(machineId, 0, 50),
        ]);
        setMachine(machineData);
        setPredictions(predictionsData);
        setSensorReadings(readingsData);
      } catch (err) {
        setError('Failed to load machine details');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (loading) {
      return (
        <div className="flex items-center justify-center h-64">
          <div className="spinner"></div>
        </div>
      );
    }

    if (error || !machine) {
      return (
        <div className="flex items-center justify-center h-64">
          <div className="text-[#DC2626]">{error || 'Machine not found'}</div>
        </div>
      );
    }

    const latestPrediction = predictions[0];

    const rulChartData = predictions
      .slice(0, 20)
      .reverse()
      .map((p) => ({
        time: new Date(p.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        RUL: p.predicted_rul,
        'Effective RUL': p.effective_rul,
      }));

    const healthChartData = predictions
      .slice(0, 20)
      .reverse()
      .map((p) => ({
        time: new Date(p.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        'Health Score': p.health_score,
      }));

    const sensorChartData = sensorReadings
      .slice(0, 20)
      .reverse()
      .map((r) => ({
        cycle: r.cycle,
        'Sensor 2': r.sensor_2,
        'Sensor 3': r.sensor_3,
        'Sensor 4': r.sensor_4,
        'Sensor 14': r.sensor_14,
      }));

    const getStatusBadgeClass = (status: string) => {
      switch (status) {
        case 'NORMAL': return 'status-normal';
        case 'MONITOR': return 'status-monitor';
        case 'MAINTENANCE_RECOMMENDED': return 'status-maintenance';
        case 'CRITICAL': return 'status-critical';
        default: return 'status-normal';
      }
    };

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <Link to="/machines" className="text-[#2563EB] hover:text-[#1D4ED8] font-medium mb-2
  inline-block">
              ← Back to Machines
            </Link>
            <h2 className="text-3xl font-bold text-[#1E293B]">{machine.name}</h2>
            <p className="text-[#64748B] mt-1">{machine.description}</p>
          </div>
        </div>

        {/* Machine Info */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="scada-card p-6">
            <h3 className="text-sm font-semibold text-[#64748B] uppercase tracking-wide mb-2">Machine ID</h3>
            <p className="text-2xl font-bold text-[#1E293B] font-mono-data">{machine.id}</p>
          </div>
          <div className="scada-card p-6">
            <h3 className="text-sm font-semibold text-[#64748B] uppercase tracking-wide mb-2">Location</h3>
            <p className="text-2xl font-bold text-[#1E293B]">{machine.location || 'N/A'}</p>
          </div>
          <div className="scada-card p-6">
            <h3 className="text-sm font-semibold text-[#64748B] uppercase tracking-wide mb-2">Model</h3>
            <p className="text-2xl font-bold text-[#1E293B]">{machine.model || 'N/A'}</p>
          </div>
        </div>

        {/* AI Prediction */}
        {latestPrediction && (
          <div className="scada-card p-6 border-l-4 border-l-[#6366F1]">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-3xl">🤖</span>
              <h3 className="text-xl font-bold text-[#1E293B]">AI Prediction</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <h4 className="text-sm font-semibold text-[#64748B] uppercase tracking-wide mb-2">Remaining
  Useful Life</h4>
                <p className="text-3xl font-bold text-[#1E293B] font-mono-data">
                  {latestPrediction.effective_rul.toFixed(1)}
                </p>
                <p className="text-sm text-[#64748B] mt-1">cycles remaining</p>
              </div>
              <div>
                <h4 className="text-sm font-semibold text-[#64748B] uppercase tracking-wide mb-2">Health
  Score</h4>
                <p className="text-3xl font-bold text-[#1E293B] font-mono-data">
                  {latestPrediction.health_score.toFixed(1)}
                </p>
                <p className="text-sm text-[#64748B] mt-1">out of 100</p>
              </div>
              <div>
                <h4 className="text-sm font-semibold text-[#64748B] uppercase tracking-wide mb-2">Maintenance
  Status</h4>
                <span className={`status-badge ${getStatusBadgeClass(latestPrediction.maintenance_status)}`}>
                  {latestPrediction.maintenance_status}
                </span>
                <p className="text-sm text-[#64748B] mt-2">
                  {new Date(latestPrediction.timestamp).toLocaleString()}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* RUL Chart */}
          <div className="scada-card p-6">
            <h3 className="text-lg font-semibold text-[#1E293B] mb-4">Remaining Useful Life Trend</h3>
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={rulChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis dataKey="time" tick={{ fontSize: 11 }} stroke="#64748B" />
                <YAxis tick={{ fontSize: 11 }} stroke="#64748B" />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="RUL" stroke="#6366F1" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="Effective RUL" stroke="#8B5CF6" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Health Score Chart */}
          <div className="scada-card p-6">
            <h3 className="text-lg font-semibold text-[#1E293B] mb-4">Health Score Trend</h3>
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={healthChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis dataKey="time" tick={{ fontSize: 11 }} stroke="#64748B" />
                <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} stroke="#64748B" />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="Health Score" stroke="#10B981" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Sensor Readings Chart */}
        <div className="scada-card p-6">
          <h3 className="text-lg font-semibold text-[#1E293B] mb-4">Recent Sensor Readings</h3>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={sensorChartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
              <XAxis dataKey="cycle" tick={{ fontSize: 11 }} stroke="#64748B" label={{ value: 'Cycle',
  position: 'insideBottom', offset: -5 }} />
              <YAxis tick={{ fontSize: 11 }} stroke="#64748B" />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="Sensor 2" stroke="#3B82F6" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="Sensor 3" stroke="#F59E0B" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="Sensor 4" stroke="#10B981" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="Sensor 14" stroke="#8B5CF6" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  }