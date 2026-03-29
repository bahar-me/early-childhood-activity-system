import { API_BASE_URL, getAuthHeaders } from './base';

export async function createActivityPlan(payload: {
  activity_ids: string[];
  notes?: string;
}) {
  const response = await fetch(`${API_BASE_URL}/api/activity-plans/`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Failed to create activity plan');
  }

  return data.plan;
}