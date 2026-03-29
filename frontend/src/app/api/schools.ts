import { School } from '../types/school';

import { API_BASE_URL, getAuthHeaders } from './base';

export async function getSchools(): Promise<School[]> {
  const response = await fetch(`${API_BASE_URL}/api/schools/`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Failed to fetch schools');
  }

  return data.schools || [];
}

export async function createSchool(payload: {
  name: string;
  address?: string;
}): Promise<School> {
  const response = await fetch(`${API_BASE_URL}/api/schools/`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Failed to create school');
  }

  return data.school;
}

export async function updateSchool(
  schoolId: number,
  payload: { name?: string; address?: string }
): Promise<School> {
  const response = await fetch(`${API_BASE_URL}/api/schools/${schoolId}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Failed to update school');
  }

  return data.school;
}

export async function deleteSchool(schoolId: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/schools/${schoolId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Failed to delete school');
  }
}