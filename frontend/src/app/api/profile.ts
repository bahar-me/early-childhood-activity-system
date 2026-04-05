import { API_BASE_URL, getAuthHeaders } from './base';
import { clearAuthStorage } from './authStorage';

export async function saveTeacherProfile(payload: {
  name: string;
  years_experience: number;
  specializations: string[];
  teaching_style: string;
}) {
  const response = await fetch(`${API_BASE_URL}/api/profile/teacher`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Your session has expired. Please log in again.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Failed to save teacher profile');
  }

  return data.profile;
}

export async function getTeacherProfile() {
  const response = await fetch(`${API_BASE_URL}/api/profile/teacher`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Your session has expired. Please log in again.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Failed to load teacher profile');
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
}) {
  const response = await fetch(`${API_BASE_URL}/api/profile/class`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Your session has expired. Please log in again.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Failed to save class profile');
  }

  return data.class_profile;
}

export async function getClassProfile() {
  const response = await fetch(`${API_BASE_URL}/api/profile/class`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Your session has expired. Please log in again.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Failed to load class profile');
  }

  return data.class_profile;
}