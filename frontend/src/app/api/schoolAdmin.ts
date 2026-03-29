import { Capacitor } from '@capacitor/core';

const API_BASE_URL = Capacitor.isNativePlatform()
  ? 'http://10.0.2.2:5000'
  : 'http://127.0.0.1:5000';
  
function getAuthHeaders() {
  const token = localStorage.getItem('access-token');

  if (!token) {
    throw new Error('No access token found. Please log in.');
  }
  
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  };
}

export async function getSchoolAdminOverview() {
  const response = await fetch(`${API_BASE_URL}/api/school-admin/overview`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Failed to load school admin overview');
  }

  return data;
}