import { useEffect, useState } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
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
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2border-blue-600"></div>
          <p className="mt-4 text-gray-600">Loading audit data...</p>
        </div>
      </div>
    );
  }

  const healthTrendData = health && history.length > 0 ? history.map((audit, idx) => ({
    date: new Date(audit.completed_at || new Date()).toLocaleDateString(),
    score: audit.data_health_score || 0,
    issues: audit.total_issues,
  })).reverse() : [];

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
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-lg font-medium transition">
          {running ? 'Running Audit...' : 'Run New Audit'}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {!health ? (
        <div className="bg-white rounded-lg shadow-md p-12 border-l-4 border-gray-300 text-center">
          <div className="mb-4">
            <svg className="mx-auto h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No audits completed yet</h3>
          <p className="text-gray-600 mb-6">Start a data quality audit to analyze your dataset for anomalies, data leakage, and consistency issues.</p>
          <button
            onClick={handleRunAudit}
            disabled={running}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-8 py-3 rounded-lg font-medium transition inline-block">
            {running ? 'Running Audit...' : 'Start Audit Now'}
          </button>
        </div>
      ) : (
        <>
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

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[
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
        </>
      )}
    </div>
  );
}