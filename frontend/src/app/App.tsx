import { useEffect, useState } from 'react';
import { User } from './types/user';
import { LoginPage } from './components/LoginPage';
import { TeacherApp } from './TeacherApp';
import { SchoolAdminDashboard } from './components/SchoolAdminDashboard';
import { SystemAdminDashboard } from './components/SystemAdminDashboard';
import { Toaster } from './components/ui/sonner';
import { logoutRequest } from './api/auth';
import { clearAuthStorage } from './api/authStorage';

export default function App() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  useEffect(() => {
    const savedUser = localStorage.getItem('current-user');
    const accessToken = localStorage.getItem('access-token');
    const refreshToken = localStorage.getItem('refresh-token');

    if (savedUser && accessToken && refreshToken) {
      setCurrentUser(JSON.parse(savedUser));
    } else {
      clearAuthStorage();
      setCurrentUser(null);
    }
  }, []);

  const handleLogin = (user: User, accessToken: string, refreshToken: string) => {
    clearAuthStorage();   
    
    localStorage.setItem('current-user', JSON.stringify(user));
    localStorage.setItem('access-token', accessToken);
    localStorage.setItem('refresh-token', refreshToken);

    setCurrentUser(user);
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
      clearAuthStorage();
    }
  };

  if (!currentUser) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <>
      <Toaster />

      {currentUser.role === 'teacher' && (
        <TeacherApp 
        key={`teacher-${currentUser.id}`} 
        user={currentUser} 
        onLogout={handleLogout} 
        />
      )}

      {currentUser.role === 'school_admin' && (
        <SchoolAdminDashboard 
        key={`school-admin-${currentUser.id}`} 
        user={currentUser} 
        onLogout={handleLogout} />
      )}

      {currentUser.role === 'system_admin' && (
        <SystemAdminDashboard 
        key={`system-admin-${currentUser.id}`} 
        user={currentUser} 
        onLogout={handleLogout} />
      )}
    </>
  );
}