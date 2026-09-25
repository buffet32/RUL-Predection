 import { useEffect, useState, useMemo } from 'react';
  import { Link, useNavigate } from 'react-router-dom';
  import { getMachines, getPredictions } from '../services/api';
  import type { Machine, Prediction } from '../types';
  import Sparkline from '../components/Sparkline';

  export default function Machines() {
    const navigate = useNavigate();
    const [machines, setMachines] = useState<Machine[]>([]);
    const [predictions, setPredictions] = useState<Prediction[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [statusFilter, setStatusFilter] = useState<string>('ALL');

    useEffect(() => {
      loadData();
    }, []);

    const loadData = async () => {
      try {
        setLoading(true);
        const [machinesData, predictionsData] = await Promise.all([
          getMachines(0, 1000),
          getPredictions(undefined, 0, 1000),
        ]);
        setMachines(machinesData);
        setPredictions(predictionsData);
      } catch (err) {
        setError('Failed to load machines data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    const predictionsByMachine = useMemo(() => {
      const map = new Map<number, Prediction[]>();
      predictions.forEach(pred => {
        const existing = map.get(pred.machine_id) || [];
        map.set(pred.machine_id, [...existing, pred]);
      });
      map.forEach((preds, machineId) => {
        map.set(machineId, preds.sort((a, b) =>
          new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
        ));
      });
      return map;
    }, [predictions]);

    const machinePredictions = useMemo(() => {
      return machines.map((machine) => {
        const machinePreds = predictionsByMachine.get(machine.id) || [];
        return {
          ...machine,
          latestPrediction: machinePreds[0] || null,
          recentHealthScores: machinePreds.slice(0, 10).reverse().map(p => p.health_score),
        };
      });
    }, [machines, predictionsByMachine]);

    const filteredMachines = machinePredictions.filter((machine) => {
      const matchesSearch =
        machine.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        machine.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        machine.location?.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesStatus =
        statusFilter === 'ALL' ||
        (machine.latestPrediction?.maintenance_status === statusFilter);

      return matchesSearch && matchesStatus;
    });

    const getStatusBadgeClass = (status: string) => {
      switch (status) {
        case 'NORMAL': return 'status-normal';
        case 'MONITOR': return 'status-monitor';
        case 'MAINTENANCE_RECOMMENDED': return 'status-maintenance';
        case 'CRITICAL': return 'status-critical';
        default: return 'status-normal';
      }
    };

    const getSparklineColor = (status: string) => {
      switch (status) {
        case 'NORMAL': return '#10B981';
        case 'MONITOR': return '#F59E0B';
        case 'MAINTENANCE_RECOMMENDED': return '#EA580C';
        case 'CRITICAL': return '#EF4444';
        default: return '#10B981';
      }
    };

    if (loading) {
      return (
        <div className="flex items-center justify-center h-64">
          <div className="spinner"></div>
        </div>
      );
    }

    if (error) {
      return (
        <div className="flex items-center justify-center h-64">
          <div className="text-[#DC2626]">{error}</div>
        </div>
      );
    }

    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-semibold text-[#1E293B]">All Machines</h2>
            <p className="text-[#64748B] mt-1">Monitor and manage your factory equipment</p>
          </div>
          <button
            onClick={loadData}
            className="px-5 py-2.5 bg-gradient-to-r from-[#667EEA] to-[#764BA2] text-white rounded-lg
  hover:shadow-lg transition-all font-medium"
          >
            🔄 Refresh
          </button>
        </div>

        {/* Filters */}
        <div className="scada-card p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-[#64748B] mb-2">Search Machines</label>
              <input
                type="text"
                placeholder="Search by name, description, or location..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2.5 border border-[#E2E8F0] rounded-lg focus:ring-2
  focus:ring-[#6366F1] focus:border-transparent text-[#1E293B]"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-[#64748B] mb-2">Filter by Status</label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="w-full px-4 py-2.5 border border-[#E2E8F0] rounded-lg focus:ring-2
  focus:ring-[#6366F1] focus:border-transparent text-[#1E293B]"
              >
                <option value="ALL">All Statuses</option>
                <option value="NORMAL">Normal</option>
                <option value="MONITOR">Monitor</option>
                <option value="MAINTENANCE_RECOMMENDED">Maintenance Recommended</option>
                <option value="CRITICAL">Critical</option>
              </select>
            </div>
          </div>
        </div>

        {/* Machines Table */}
        <div className="scada-card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-[#E2E8F0]">
              <thead className="bg-gradient-to-r from-[#F8FAFC] to-[#F1F5F9] sticky top-0">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-bold text-[#475569] uppercase tracking-wider">
                    Machine ID
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-[#475569] uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-[#475569] uppercase tracking-wider">
                    Location
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-[#475569] uppercase tracking-wider">
                    Predicted RUL
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-[#475569] uppercase tracking-wider">
                    Health Score
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-[#475569] uppercase tracking-wider">
                    Trend
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-[#475569] uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-[#475569] uppercase tracking-wider">
                    Last Update
                  </th>
                  <th className="px-4 py-3 text-right text-xs font-bold text-[#475569] uppercase tracking-wider sticky right-0 bg-[#F1F5F9] shadow-[-4px_0_10px_-3px_rgba(0,0,0,0.05)] z-10">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-[#E2E8F0]">
                {filteredMachines.map((machine) => (
                  <tr key={machine.id} className="hover:bg-[#F8FAFC] transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B] font-mono-data
  font-semibold">
                      {machine.id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-[#1E293B]">
                      {machine.name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-[#64748B]">
                      {machine.location || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B] font-mono-data">
                      {machine.latestPrediction?.predicted_rul.toFixed(1) || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B] font-mono-data">
                      {machine.latestPrediction?.health_score.toFixed(1) || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      {machine.recentHealthScores.length > 1 ? (
                        <Sparkline
                          data={machine.recentHealthScores}
                          color={getSparklineColor(machine.latestPrediction?.maintenance_status || 'NORMAL')}
                        />
                      ) : (
                        <span className="text-[#94A3B8] text-xs">N/A</span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      {machine.latestPrediction ? (
                        <span className={`status-badge 
  ${getStatusBadgeClass(machine.latestPrediction.maintenance_status)}`}>
                          {machine.latestPrediction.maintenance_status}
                        </span>
                      ) : (
                        <span className="status-badge status-normal">NO DATA</span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-[#64748B] font-mono-data">
                      {machine.latestPrediction
                        ? new Date(machine.latestPrediction.timestamp).toLocaleString()
                        : '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <Link
                        to={`/machines/${machine.id}`}
                        className="text-[#6366F1] hover:text-[#4F46E5] font-semibold"
                      >
                        View →
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {filteredMachines.length === 0 && (
            <div className="text-center py-12 text-[#64748B]">
              <span className="text-4xl mb-3 block">🔍</span>
              No machines found matching your criteria
            </div>
          )}
        </div>
      </div>
    );
  }