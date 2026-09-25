import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ErrorBoundary } from './components/ErrorBoundary';
import Layout from './layouts/Layout';
import Dashboard from './pages/Dashboard';
import Machines from './pages/Machines';
import MachineDetails from './pages/MachineDetails';
import Maintenance from './pages/Maintenance';
import TestPrediction from './pages/TestPrediction';
import Reports from './pages/Reports';
import DataQuality from './pages/DataQuality';

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/machines" element={<Machines />} />
            <Route path="/machines/:id" element={<MachineDetails />} />
            <Route path="/maintenance" element={<Maintenance />} />
            <Route path="/test-prediction" element={<TestPrediction />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/data-quality" element={<DataQuality />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Layout>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
