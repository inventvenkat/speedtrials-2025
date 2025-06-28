import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './auth/AuthContext';
import { ProtectedRoute } from './auth/ProtectedRoute';
import { LoginPage } from './pages/LoginPage';
import HomePage from './pages/HomePage';
import WaterSystemReport from './pages/WaterSystemReport';
import { OperatorDashboard } from './pages/OperatorDashboard';
import { RegulatorMap } from './pages/RegulatorMap';
import Layout from './components/layout/Layout';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Layout>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<HomePage />} />
            <Route path="/report/:pwsid" element={<WaterSystemReport />} />

            <Route element={<ProtectedRoute allowedRoles={['Operator']} />}>
              <Route path="/dashboard" element={<OperatorDashboard />} />
            </Route>

            <Route element={<ProtectedRoute allowedRoles={['Regulator']} />}>
              <Route path="/map" element={<RegulatorMap />} />
            </Route>
          </Routes>
        </Layout>
      </Router>
    </AuthProvider>
  );
}

export default App
