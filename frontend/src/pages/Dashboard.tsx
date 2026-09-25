 import { useEffect, useState } from 'react';
  import { Link } from 'react-router-dom';
  import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, LineChart,
  Line } from 'recharts';
  import { getMachines, getPredictions, getMaintenanceSummary } from '../services/api';
  import type { Machine, Prediction, MaintenanceSummary } from '../types';

  export default function Dashboard() {
    const [machines, setMachines] = useState<Machine[]>([]);
    const [predictions, setPredictions] = useState<Prediction[]>([]);
    const [summary, setSummary] = useState<MaintenanceSummary | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

    useEffect(() => {
      loadData();
      // Auto-refresh every 30 seconds
      const interval = setInterval(loadData, 30000);
      return () => clearInterval(interval);
    }, []);

    const loadData = async () => {
      try {
        setLoading(true);
        const [machinesData, predictionsData, summaryData] = await Promise.all([
          getMachines(0, 1000),
          getPredictions(undefined, 0, 100),
          getMaintenanceSummary(),
        ]);
        setMachines(machinesData);
        setPredictions(predictionsData);
        setSummary(summaryData);
        setLastUpdate(new Date());
        setError(null);
      } catch (err) {
        setError('Failed to load dashboard data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (loading && !summary) {
      return (
        <div className="flex items-center justify-center h-64">
          <div className="spinner"></div>
        </div>
      );
    }

    if (error && !summary) {
      return (
        <div className="flex items-center justify-center h-64">
          <div className="text-[#DC2626]">{error}</div>
        </div>
      );
    }

    const statusColors = {
      NORMAL: '#10B981',
      MONITOR: '#F59E0B',
      MAINTENANCE_RECOMMENDED: '#EA580C',
      CRITICAL: '#EF4444',
    };

    const pieData = summary ? [
      { name: 'Normal', value: summary.normal_count, color: statusColors.NORMAL },
      { name: 'Monitor', value: summary.monitor_count, color: statusColors.MONITOR },
      { name: 'Maintenance', value: summary.maintenance_count, color: statusColors.MAINTENANCE_RECOMMENDED },
      { name: 'Critical', value: summary.critical_count, color: statusColors.CRITICAL },
    ].filter(item => item.value > 0) : [];

    const barData = summary ? [
      { status: 'Normal', count: summary.normal_count, fill: statusColors.NORMAL },
      { status: 'Monitor', count: summary.monitor_count, fill: statusColors.MONITOR },
      { status: 'Maintenance', count: summary.maintenance_count, fill: statusColors.MAINTENANCE_RECOMMENDED
  },
      { status: 'Critical', count: summary.critical_count, fill: statusColors.CRITICAL },
    ] : [];

    // Calculate average health score from recent predictions
    const avgHealthScore = predictions.length > 0
      ? predictions.reduce((sum, p) => sum + p.health_score, 0) / predictions.length
      : 0;

    // Group predictions by timestamp for trend
    const healthTrend = predictions.slice(0, 20).reverse().map((p, idx) => ({
      index: idx + 1,
      health: p.health_score,
      rul: p.predicted_rul,
    }));

    const recentPredictions = predictions.slice(0, 10);

    return (
      <div className="space-y-6">
        {/* Header with Refresh */}
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-semibold text-[#1E293B]">System Overview</h2>
            <p className="text-[#64748B] mt-1">
              Last updated: {lastUpdate.toLocaleTimeString()}
            </p>
          </div>
          <button
            onClick={loadData}
            disabled={loading}
            className="px-5 py-2.5 bg-gradient-to-r from-[#667EEA] to-[#764BA2] text-white rounded-lg
  hover:shadow-lg transition-all font-medium disabled:opacity-50 flex items-center gap-2"
          >
            <span className={loading ? 'animate-spin' : ''}>🔄</span>
            Refresh Data
          </button>
        </div>

        {/* Metric Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="metric-card info">
            <div className="flex items-center justify-between mb-2">
              <span className="text-3xl">🏭</span>
              <span className="text-3xl font-bold text-[#1E293B] font-mono-data">
                {machines.length}
              </span>
            </div>
            <h3 className="text-sm font-semibold text-[#64748B] uppercase tracking-wide">Total Machines</h3>
          </div>

          <div className="metric-card success">
            <div className="flex items-center justify-between mb-2">
              <span className="text-3xl">✅</span>
              <span className="text-3xl font-bold text-[#1E293B] font-mono-data">
                {summary?.normal_count || 0}
              </span>
            </div>
            <h3 className="text-sm font-semibold text-[#64748B] uppercase tracking-wide">Normal Status</h3>
          </div>

          <div className="metric-card warning">
            <div className="flex items-center justify-between mb-2">
              <span className="text-3xl">⚠️ </span>
              <span className="text-3xl font-bold text-[#1E293B] font-mono-data">
                {(summary?.monitor_count || 0) + (summary?.maintenance_count || 0)}
              </span>
            </div>
            <h3 className="text-sm font-semibold text-[#64748B] uppercase tracking-wide">Needs Attention</h3>
          </div>

          <div className="metric-card danger">
            <div className="flex items-center justify-between mb-2">
              <span className="text-3xl">🔴</span>
              <span className="text-3xl font-bold text-[#1E293B] font-mono-data">
                {summary?.critical_count || 0}
              </span>
            </div>
            <h3 className="text-sm font-semibold text-[#64748B] uppercase tracking-wide">Critical</h3>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link to="/maintenance" className="scada-card p-4 hover:shadow-lg transition-all group">
            <div className="flex items-center gap-3">
              <span className="text-3xl group-hover:scale-110 transition-transform">🔧</span>
              <div>
                <h4 className="font-semibold text-[#1E293B]">View Maintenance Schedule</h4>
                <p className="text-xs text-[#64748B]">Check priority recommendations</p>
              </div>
            </div>
          </Link>

          <Link to="/test-prediction" className="scada-card p-4 hover:shadow-lg transition-all group">
            <div className="flex items-center gap-3">
              <span className="text-3xl group-hover:scale-110 transition-transform">🧪</span>
              <div>
                <h4 className="font-semibold text-[#1E293B]">Run Test Prediction</h4>
                <p className="text-xs text-[#64748B]">Test with custom sensor data</p>
              </div>
            </div>
          </Link>

          <Link to="/reports" className="scada-card p-4 hover:shadow-lg transition-all group">
            <div className="flex items-center gap-3">
              <span className="text-3xl group-hover:scale-110 transition-transform">📈</span>
              <div>
                <h4 className="font-semibold text-[#1E293B]">Weekly Reports</h4>
                <p className="text-xs text-[#64748B]">View performance analytics</p>
              </div>
            </div>
          </Link>
        </div>

        {/* Charts Row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="scada-card p-6">
            <h3 className="text-lg font-semibold text-[#1E293B] mb-4">Status Distribution</h3>
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${((percent ?? 0) * 100).toFixed(0)}%`}
                  outerRadius={90}
                  fill="#8884d8"
                  dataKey="value"
                  animationBegin={0}
                  animationDuration={800}
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="scada-card p-6">
            <h3 className="text-lg font-semibold text-[#1E293B] mb-4">Machines by Status</h3>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={barData}>
                <XAxis dataKey="status" tick={{ fontSize: 12 }} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" radius={[8, 8, 0, 0]} animationDuration={800}>
                  {barData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Fleet Health Trend */}
        {healthTrend.length > 0 && (
          <div className="scada-card p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-[#1E293B]">Fleet Health Trend</h3>
                <p className="text-sm text-[#64748B]">Recent 20 predictions</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-semibold text-[#64748B]">Avg Health Score</p>
                <p className="text-2xl font-bold text-[#1E293B]
  font-mono-data">{avgHealthScore.toFixed(1)}</p>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={healthTrend}>
                <XAxis dataKey="index" label={{ value: 'Recent Predictions', position: 'insideBottom',
  offset: -5 }} />
                <YAxis domain={[0, 100]} label={{ value: 'Health Score', angle: -90, position: 'insideLeft'
  }} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="health" stroke="#6366F1" strokeWidth={2} dot={{ r: 4 }}
  name="Health Score" animationDuration={800} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Recent Predictions */}
        <div className="scada-card overflow-hidden">
          <div className="px-6 py-4 border-b border-[#E2E8F0] flex items-center justify-between">
            <h3 className="text-lg font-semibold text-[#1E293B]">Recent Predictions</h3>
            <Link to="/machines" className="text-sm font-medium text-[#6366F1] hover:text-[#4F46E5]">
              View All Machines →
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-[#E2E8F0]">
              <thead className="bg-[#F8FAFC]">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-[#64748B] uppercase
  tracking-wider">Machine ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-[#64748B] uppercase
  tracking-wider">Predicted RUL</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-[#64748B] uppercase
  tracking-wider">Health Score</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-[#64748B] uppercase
  tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-[#64748B] uppercase
  tracking-wider">Timestamp</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-[#64748B] uppercase
  tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-[#E2E8F0]">
                {recentPredictions.map((prediction) => (
                  <tr key={prediction.id} className="hover:bg-[#F8FAFC] transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B]
  font-mono-data">{prediction.machine_id}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B]
  font-mono-data">{prediction.predicted_rul.toFixed(1)} cycles</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B]
  font-mono-data">{prediction.health_score.toFixed(1)}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span className={`status-badge status-${prediction.maintenance_status.toLowerCase()}`}>
                        {prediction.maintenance_status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-[#64748B] font-mono-data">{new
  Date(prediction.timestamp).toLocaleString()}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <Link to={`/machines/${prediction.machine_id}`} className="text-[#2563EB]
  hover:text-[#1D4ED8] font-medium">
                        View Details
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }