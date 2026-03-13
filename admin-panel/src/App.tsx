import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import UsersPage from './pages/UsersPage';
import Layout from './components/Layout';
import './index.css';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

const App: React.FC = () => {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route 
            path="/" 
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<DashboardPage />} />
            <Route path="users" element={<UsersPage />} />
            <Route path="courses" element={
                <div className="flex flex-col items-center justify-center min-h-[50vh] text-slate-500">
                    <h2 className="text-xl font-bold">Khóa học</h2>
                    <p>Tính năng quản lý khóa học đang được xây dựng...</p>
                    <Link to="/" className="mt-4 text-blue-500 hover:underline">Quay lại Dashboard</Link>
                </div>
            } />
            <Route path="settings" element={
                <div className="flex flex-col items-center justify-center min-h-[50vh] text-slate-500">
                    <h2 className="text-xl font-bold">Cài đặt</h2>
                    <p>Tính năng cài đặt hệ thống đang được xây dựng...</p>
                </div>
            } />
          </Route>
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
};

export default App;
