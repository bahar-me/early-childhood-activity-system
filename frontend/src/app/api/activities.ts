import { API_BASE_URL, getAuthHeaders } from './base';
import { clearAuthStorage } from './authStorage';
import { Activity } from '../types/activity';

export async function getActivities(): Promise<Activity[]> {
  const response = await fetch(`${API_BASE_URL}/api/activities/`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Your session has expired. Please log in again.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Failed to load activities');
  }

  return data.activities;
}