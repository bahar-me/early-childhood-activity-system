const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000';

function getAuthHeaders() {
  const token = localStorage.getItem('access-token');

  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  };
}

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

  if (!response.ok) {
    throw new Error(data.error || 'Failed to load class profile');
  }

  return data.class_profile;
}