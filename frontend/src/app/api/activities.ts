import { API_BASE_URL, getAuthHeaders } from './base';
import { clearAuthStorage } from './authStorage';
import { Activity } from '../types/activity';

async function parseJsonSafely(response: Response) {
  const text = await response.text();
  return text ? JSON.parse(text) : {};
}

export type ActivitiesPage = {
  activities: Activity[];
  total: number;
  limit: number;
  offset: number;
};

export type CreateActivityPayload = Omit<Activity, 'id'> & {
  sourceType?: 'seed' | 'manual_edit' | 'llm_generated';
  parentActivityId?: string | null;
  createdByUserId?: string | null;
};

export async function getActivities(limit = 30, offset = 0): Promise<ActivitiesPage> {
  const response = await fetch(`${API_BASE_URL}/api/activities/?limit=${limit}&offset=${offset}`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  const data = await parseJsonSafely(response);

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Oturum süresi doldu. Lütfen tekrar giriş yapın.');
  }

  if (!response.ok) {
    throw new Error(data.error || data.msg || 'Etkinlikler yüklenemedi.');
  }

  return {
    activities: data.activities || [],
    total: data.total ?? data.activities?.length ?? 0,
    limit: data.limit ?? limit,
    offset: data.offset ?? offset,
  };
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

    const data = await parseJsonSafely(response);

    if (response.status === 401) {
        clearAuthStorage();
        throw new Error('Oturum süresi doldu. Lütfen tekrar giriş yapın.');
    }

    if (!response.ok) {
        throw new Error(data.error || 'Etkinlik oluşturulamadı');
    }

    return data.activity;
}

export async function updateActivity(
  activityId: string,
  payload: Omit<CreateActivityPayload, 'sourceType' | 'parentActivityId' | 'createdByUserId'>
): Promise<Activity> {
  const response = await fetch(`${API_BASE_URL}/api/activities/${activityId}`, {
    method: 'PUT',
    headers: {
      ...getAuthHeaders(),
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  const data = await parseJsonSafely(response);

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Oturum süresi doldu. Lütfen tekrar giriş yapın.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Etkinlik güncellenemedi.');
  }

  return data.activity;
}