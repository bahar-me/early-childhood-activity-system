import { API_BASE_URL, getAuthHeaders } from './base';
import { clearAuthStorage } from './authStorage';

async function parseJSONSafely(response: Response) {
  const text = await response.text();
  
  if (!text) return {};

  try {
    return JSON.parse(text);
  } catch {
    return {};
  }
}

export async function saveTeacherProfile(payload: {
  name: string;
  years_experience: number;
  specializations: string[];
  teaching_style: string;
  school_id: number | null;
}) {
  const response = await fetch(`${API_BASE_URL}/api/profile/teacher`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });

  const data = await parseJSONSafely(response);

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Oturum süresi doldu. Lütfen tekrar giriş yapın.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Öğretmen profili kaydedilemedi.');
  }

  return data.profile;
}

export async function getTeacherProfile() {
  const response = await fetch(`${API_BASE_URL}/api/profile/teacher`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  const data = await parseJSONSafely(response);

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Oturum süresi doldu. Lütfen tekrar giriş yapın.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Öğretmen profili yüklenemedi.');
  }

  return data.profile;
}

export async function saveClassProfile(payload: {
  class_name: string;
  age_group: string;
  class_size: number;
  learning_focus: string[];
  available_resources: string[];
  special_needs: string[];
  daily_schedule: {
    morning_activities: number;
    afternoon_activities: number;
  };
}) {
  const response = await fetch(`${API_BASE_URL}/api/profile/class`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });

  const data = await parseJSONSafely(response);

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Oturum süresi doldu. Lütfen tekrar giriş yapın.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Sınıf profili kaydedilemedi.');
  }

  return data.class_profile;
}

export async function getClassProfile() {
  const response = await fetch(`${API_BASE_URL}/api/profile/class`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  const data = await parseJSONSafely(response);

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Oturum süresi doldu. Lütfen tekrar giriş yapın.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Sınıf profili yüklenemedi.');
  }

  return data.class_profile;
}