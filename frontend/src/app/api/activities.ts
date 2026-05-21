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

export async function createActivity(payload: Omit<Activity, 'id'>): Promise<Activity> {
    const response = await fetch(`${API_BASE_URL}/api/activities/`, {
        method: 'POST',
        headers: {
            ...getAuthHeaders(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (response.status === 401) {
        clearAuthStorage();
        throw new Error('Oturum süresi doldu. Lütfen tekrar giriş yap.');
    }

    if (!response.ok) {
        throw new Error(data.error || 'Etkinlik oluşturulamadı');
    }

    return data.activity;
}