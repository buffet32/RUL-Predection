
  import { useEffect, useState, useMemo } from 'react';
  import { Link } from 'react-router-dom';
  import { getPredictions, getMachines } from '../services/api';
  import type { Prediction, Machine } from '../types';
  import Sparkline from '../components/Sparkline';

  export default function Maintenance() {
    const [predictions, setPredictions] = useState<Prediction[]>([]);
    const [machines, setMachines] = useState<Machine[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
      loadData();
    }, []);

    const loadData = async () => {
      try {
        setLoading(true);
        const [predictionsData, machinesData] = await Promise.all([
          getPredictions(undefined, 0, 1000),
          getMachines(0, 1000),
        ]);
        setPredictions(predictionsData);
        setMachines(machinesData);
      } catch (err) {
        setError('Failed to load maintenance data');
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

    const criticalMachines = machinePredictions.filter(
      (m) => m.latestPrediction?.maintenance_status === 'CRITICAL'
    );
    const maintenanceRecommendedMachines = machinePredictions.filter(
      (m) => m.latestPrediction?.maintenance_status === 'MAINTENANCE_RECOMMENDED'
    );
    const monitorMachines = machinePredictions.filter(
      (m) => m.latestPrediction?.maintenance_status === 'MONITOR'
    );

    const getSparklineColor = (status: string) => {
      switch (status) {
        case 'NORMAL': return '#10B981';
        case 'MONITOR': return '#F59E0B';
        case 'MAINTENANCE_RECOMMENDED': return '#EA580C';
        case 'CRITICAL': return '#EF4444';
        default: return '#10B981';
      }
    };

    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-[#1E293B]">Maintenance Recommendations</h2>
          <p className="text-[#64748B] mt-1">Prioritized list of machines requiring attention</p>
        </div>

        {/* Critical Machines */}
        {criticalMachines.length > 0 && (
          <div className="scada-card overflow-hidden border-l-4 border-l-[#EF4444]">
            <div className="bg-gradient-to-r from-[#FEE2E2] to-white px-6 py-4 border-b border-[#E2E8F0]">
              <h3 className="text-lg font-bold text-[#DC2626] flex items-center gap-2">
                <span className="text-2xl">🚨</span> Critical - Immediate Attention Required
              </h3>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-[#E2E8F0]">
                <thead className="bg-[#FEF2F2]">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#7F1D1D] uppercase
  tracking-wider">Machine ID</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#7F1D1D] uppercase
  tracking-wider">Name</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#7F1D1D] uppercase
  tracking-wider">Effective RUL</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#7F1D1D] uppercase
  tracking-wider">Health Score</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#7F1D1D] uppercase
  tracking-wider">Trend</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#7F1D1D] uppercase
  tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-[#E2E8F0]">
                  {criticalMachines.map((machine) => (
                    <tr key={machine.id} className="hover:bg-[#FEF2F2] transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B] font-mono-data
  font-semibold">
                        {machine.id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-[#1E293B]">
                        {machine.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B] font-mono-data">
                        {machine.latestPrediction?.effective_rul.toFixed(1) || '-'} cycles
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B] font-mono-data">
                        {machine.latestPrediction?.health_score.toFixed(1) || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        {machine.recentHealthScores.length > 1 ? (
                          <Sparkline data={machine.recentHealthScores} color={getSparklineColor('CRITICAL')}
  />
                        ) : (
                          <span className="text-[#94A3B8] text-xs">N/A</span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <Link to={`/machines/${machine.id}`} className="text-[#EF4444] hover:text-[#DC2626]
  font-semibold">
                          View Details →
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Maintenance Recommended */}
        {maintenanceRecommendedMachines.length > 0 && (
          <div className="scada-card overflow-hidden border-l-4 border-l-[#EA580C]">
            <div className="bg-gradient-to-r from-[#FFEDD5] to-white px-6 py-4 border-b border-[#E2E8F0]">
              <h3 className="text-lg font-bold text-[#EA580C] flex items-center gap-2">
                <span className="text-2xl">⚠️ </span> Maintenance Recommended - Schedule Soon
              </h3>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-[#E2E8F0]">
                <thead className="bg-[#FFF7ED]">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#7C2D12] uppercase
  tracking-wider">Machine ID</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#7C2D12] uppercase
  tracking-wider">Name</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#7C2D12] uppercase
  tracking-wider">Effective RUL</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#7C2D12] uppercase
  tracking-wider">Health Score</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#7C2D12] uppercase
  tracking-wider">Trend</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#7C2D12] uppercase
  tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-[#E2E8F0]">
                  {maintenanceRecommendedMachines.map((machine) => (
                    <tr key={machine.id} className="hover:bg-[#FFF7ED] transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B] font-mono-data
  font-semibold">
                        {machine.id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-[#1E293B]">
                        {machine.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B] font-mono-data">
                        {machine.latestPrediction?.effective_rul.toFixed(1) || '-'} cycles
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B] font-mono-data">
                        {machine.latestPrediction?.health_score.toFixed(1) || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        {machine.recentHealthScores.length > 1 ? (
                          <Sparkline data={machine.recentHealthScores} 
  color={getSparklineColor('MAINTENANCE_RECOMMENDED')} />
                        ) : (
                          <span className="text-[#94A3B8] text-xs">N/A</span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <Link to={`/machines/${machine.id}`} className="text-[#EA580C] hover:text-[#C2410C]
  font-semibold">
                          View Details →
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Monitor */}
        {monitorMachines.length > 0 && (
          <div className="scada-card overflow-hidden border-l-4 border-l-[#F59E0B]">
            <div className="bg-gradient-to-r from-[#FEF3C7] to-white px-6 py-4 border-b border-[#E2E8F0]">
              <h3 className="text-lg font-bold text-[#D97706] flex items-center gap-2">
                <span className="text-2xl">👁️ </span> Monitor - Watch Closely
              </h3>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-[#E2E8F0]">
                <thead className="bg-[#FFFBEB]">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#78350F] uppercase
  tracking-wider">Machine ID</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#78350F] uppercase
  tracking-wider">Name</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#78350F] uppercase
  tracking-wider">Effective RUL</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#78350F] uppercase
  tracking-wider">Health Score</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#78350F] uppercase
  tracking-wider">Trend</th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-[#78350F] uppercase
  tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-[#E2E8F0]">
                  {monitorMachines.map((machine) => (
                    <tr key={machine.id} className="hover:bg-[#FFFBEB] transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B] font-mono-data
  font-semibold">
                        {machine.id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-[#1E293B]">
                        {machine.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B] font-mono-data">
                        {machine.latestPrediction?.effective_rul.toFixed(1) || '-'} cycles
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-[#1E293B] font-mono-data">
                        {machine.latestPrediction?.health_score.toFixed(1) || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        {machine.recentHealthScores.length > 1 ? (
                          <Sparkline data={machine.recentHealthScores} color={getSparklineColor('MONITOR')}
  />
                        ) : (
                          <span className="text-[#94A3B8] text-xs">N/A</span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <Link to={`/machines/${machine.id}`} className="text-[#F59E0B] hover:text-[#D97706]
  font-semibold">
                          View Details →
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* All Normal */}
        {criticalMachines.length === 0 && maintenanceRecommendedMachines.length === 0 &&
  monitorMachines.length === 0 && (
          <div className="scada-card p-12 border-l-4 border-l-[#10B981]">
            <div className="text-center">
              <span className="text-6xl mb-4 block">✅</span>
              <h3 className="text-2xl font-bold text-[#10B981] mt-2">All Systems Normal</h3>
              <p className="text-[#059669] mt-2 text-lg">No machines require immediate attention</p>
            </div>
          </div>
        )}
      </div>
    );
  }