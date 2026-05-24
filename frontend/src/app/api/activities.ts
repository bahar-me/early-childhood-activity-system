import { API_BASE_URL, getAuthHeaders } from './base';
import { clearAuthStorage } from './authStorage';
import { Activity } from '../types/activity';

export type CreateActivityPayload = Omit<Activity, 'id'> & {
  sourceType?: 'seed' | 'manual_edit' | 'llm_generated';
  parentActivityId?: string | null;
  createdByUserId?: string | null;
};

export async function getActivities(): Promise<Activity[]> {
  const response = await fetch(`${API_BASE_URL}/api/activities/`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Oturum süresi doldu. Lütfen tekrar giriş yapın.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Etkinlikler yüklenemedi.');
  }

  return data.activities;
}

export async function createActivity(payload: CreateActivityPayload): Promise<Activity> {
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
        throw new Error('Oturum süresi doldu. Lütfen tekrar giriş yapın.');
    }

    if (!response.ok) {
        throw new Error(data.error || 'Etkinlik oluşturulamadı');
    }

    return data.activity;
}