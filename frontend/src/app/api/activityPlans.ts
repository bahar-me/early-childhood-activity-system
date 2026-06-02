import { API_BASE_URL, getAuthHeaders } from './base';
import { clearAuthStorage } from './authStorage';

async function parseJsonSafely(response: Response) {
  const text = await response.text();
  return text ? JSON.parse(text) : {};
}

export async function createActivityPlan(payload: {
  activity_ids: string[];
  notes?: string;
}) {
  const response = await fetch(`${API_BASE_URL}/api/activity-plans/`, {
    method: 'POST',
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
    throw new Error(data.error || 'Etkinlik planı oluşturulamadı.');
  }

  return data.plan;
}