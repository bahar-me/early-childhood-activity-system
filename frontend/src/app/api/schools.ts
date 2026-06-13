import { School } from '../types/school';
import { clearAuthStorage } from './authStorage';
import { API_BASE_URL, getAuthHeaders } from './base';

async function parseJSONSafely(response: Response) {
  const text = await response.text();
  
  if (!text) return {};

  try {
    return JSON.parse(text);
  } catch {
    return {};
  }
}

function handleUnauthorized(response: Response) {
  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Oturum süresi doldu. Lütfen tekrar giriş yapın.');
  }
}

export async function getSchools(): Promise<School[]> {
  const response = await fetch(`${API_BASE_URL}/api/schools/`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  const data = await parseJSONSafely(response);

  handleUnauthorized(response);

  if (!response.ok) {
    throw new Error(data.error || 'Okullar yüklenemedi.');
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

  const data = await parseJSONSafely(response);

  handleUnauthorized(response);

  if (!response.ok) {
    throw new Error(data.error || 'Okul oluşturulamadı.');
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

  const data = await parseJSONSafely(response);

  handleUnauthorized(response);

  if (!response.ok) {
    throw new Error(data.error || 'Okul güncellenemedi.');
  }

  return data.school;
}

export async function deleteSchool(schoolId: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/schools/${schoolId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });

  const data = await parseJSONSafely(response);

  handleUnauthorized(response);

  if (!response.ok) {
    throw new Error(data.error || 'Okul silinemedi.');
  }
}