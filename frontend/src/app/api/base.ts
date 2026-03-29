import { Capacitor } from '@capacitor/core';

export const API_BASE_URL = Capacitor.isNativePlatform()
  ? 'http://10.0.2.2:5000'
  : 'http://127.0.0.1:5000';

export function getAuthHeaders() {
  const token = localStorage.getItem('access-token');

  if (!token) {
    throw new Error('No access token found. Please log in.');
  }

  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  };
}