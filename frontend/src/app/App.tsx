import { useEffect, useState } from 'react';
import { User } from './types/user';
import { LoginPage } from './components/LoginPage';
import { TeacherApp } from './TeacherApp';
import { SchoolAdminDashboard } from './components/SchoolAdminDashboard';
import { SystemAdminDashboard } from './components/SystemAdminDashboard';
import { Toaster } from './components/ui/sonner';
import { logoutRequest } from './api/auth';

export default function App() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  useEffect(() => {
    const savedUser = localStorage.getItem('current-user');
    if (savedUser) {
      setCurrentUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLogin = (user: User, accessToken: string, refreshToken: string) => {
    setCurrentUser(user);

    localStorage.setItem('current-user', JSON.stringify(user));
    localStorage.setItem('access-token', accessToken);
    localStorage.setItem('refresh-token', refreshToken);
  };

  const handleLogout = async () => {
    const refreshToken = localStorage.getItem('refresh-token');

    try {
      if (refreshToken) {
        await logoutRequest(refreshToken);
      }
    } catch (error) {
      console.error('Logout request failed:', error);
    } finally {
      setCurrentUser(null);
      localStorage.removeItem('current-user');
      localStorage.removeItem('access-token');
      localStorage.removeItem('refresh-token');
    }
  };

  if (!currentUser) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <>
      <Toaster />

      {currentUser.role === 'teacher' && (
        <TeacherApp user={currentUser} onLogout={handleLogout} />
      )}

      {currentUser.role === 'school_admin' && (
        <SchoolAdminDashboard user={currentUser} onLogout={handleLogout} />
      )}

      {currentUser.role === 'system_admin' && (
        <SystemAdminDashboard user={currentUser} onLogout={handleLogout} />
      )}
    </>
  );
}