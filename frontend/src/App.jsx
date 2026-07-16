import { Navigate, Route, Routes } from 'react-router-dom';
import OrgLayout from './components/OrgLayout';
import RequireAuth from './components/RequireAuth';
import { AuthProvider } from './context/AuthContext';
import { OrgProvider } from './context/OrgContext';
import BillingPage from './pages/BillingPage';
import LoginPage from './pages/LoginPage';
import OrgListPage from './pages/OrgListPage';
import ProjectDetailPage from './pages/ProjectDetailPage';
import ProjectListPage from './pages/ProjectListPage';
import RegisterPage from './pages/RegisterPage';

export default function App() {
  return (
    <AuthProvider>
      <OrgProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          <Route
            path="/orgs"
            element={
              <RequireAuth>
                <OrgListPage />
              </RequireAuth>
            }
          />

          <Route
            path="/orgs/:orgSlug"
            element={
              <RequireAuth>
                <OrgLayout />
              </RequireAuth>
            }
          >
            <Route path="projects" element={<ProjectListPage />} />
            <Route path="projects/:projectId" element={<ProjectDetailPage />} />
            <Route path="billing" element={<BillingPage />} />
          </Route>

          <Route path="/" element={<Navigate to="/orgs" replace />} />
          <Route path="*" element={<Navigate to="/orgs" replace />} />
        </Routes>
      </OrgProvider>
    </AuthProvider>
  );
}
