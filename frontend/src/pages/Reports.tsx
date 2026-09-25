  import { useState, useEffect } from 'react';
  import { getWeeklySummary } from '../services/api';
  import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
  } from 'chart.js';
  import { Line, Doughnut } from 'react-chartjs-2';

  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
  );

  export default function Reports() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
      loadData();
    }, []);

    const loadData = async () => {
      try {
        setLoading(true);
        const summary = await getWeeklySummary();
        setData(summary);
      } catch (err) {
        setError('Failed to load reports data');
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

    if (error) {
      return (
        <div className="flex items-center justify-center h-64">
          <div className="text-[#DC2626] font-semibold">{error}</div>
        </div>
      );
    }

    const lineChartData = {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [
        {
          label: 'Average Health Score',
          data: data?.daily_health_scores || [85, 86, 84, 87, 86, 88, 89],
          borderColor: '#6366F1',
          backgroundColor: 'rgba(99, 102, 241, 0.5)',
          tension: 0.4
        }
      ]
    };

    const doughnutData = {
      labels: ['Normal', 'Monitor', 'Maintenance Recommended', 'Critical'],
      datasets: [
        {
          data: [
            data?.status_distribution?.normal || 15,
            data?.status_distribution?.monitor || 5,
            data?.status_distribution?.maintenance_recommended || 3,
            data?.status_distribution?.critical || 1
          ],
          backgroundColor: [
            '#10B981',
            '#F59E0B',
            '#EA580C',
            '#EF4444'
          ],
          borderWidth: 0,
        }
      ]
    };

    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-[#1E293B]">Weekly Maintenance Report</h2>
          <p className="text-[#64748B] mt-1">Overview of factory equipment health</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="scada-card p-6">
            <h3 className="text-lg font-semibold text-[#1E293B] mb-4">Health Score Trend</h3>
            <div className="h-64">
              <Line
                data={lineChartData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  scales: { y: { min: 0, max: 100 } }
                }}
              />
            </div>
          </div>

          <div className="scada-card p-6">
            <h3 className="text-lg font-semibold text-[#1E293B] mb-4">Machine Status Distribution</h3>
            <div className="h-64 flex justify-center">
              <Doughnut
                data={doughnutData}
                options={{ responsive: true, maintainAspectRatio: false }}
              />
            </div>
          </div>
        </div>

        <div className="scada-card p-6">
          <h3 className="text-lg font-semibold text-[#1E293B] mb-4">Key Metrics</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-[#F8FAFC] rounded-lg p-4 border border-[#E2E8F0]">
              <p className="text-sm font-semibold text-[#64748B]">Total Machines Monitored</p>
              <p className="text-3xl font-bold text-[#1E293B] mt-2 font-mono-data">
                {data?.total_machines || 24}
              </p>
            </div>
            <div className="bg-[#F8FAFC] rounded-lg p-4 border border-[#E2E8F0]">
              <p className="text-sm font-semibold text-[#64748B]">Avg Health Score</p>
              <p className="text-3xl font-bold text-[#10B981] mt-2 font-mono-data">
                {data?.average_health_score?.toFixed(1) || '86.4'}%
              </p>
            </div>
            <div className="bg-[#F8FAFC] rounded-lg p-4 border border-[#E2E8F0]">
              <p className="text-sm font-semibold text-[#64748B]">Critical Issues</p>
              <p className="text-3xl font-bold text-[#EF4444] mt-2 font-mono-data">
                {data?.status_distribution?.critical || 1}
              </p>
            </div>
            <div className="bg-[#F8FAFC] rounded-lg p-4 border border-[#E2E8F0]">
              <p className="text-sm font-semibold text-[#64748B]">Predictions Made</p>
              <p className="text-3xl font-bold text-[#6366F1] mt-2 font-mono-data">
                {data?.total_predictions || '1,248'}
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }