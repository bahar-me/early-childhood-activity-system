import { API_BASE_URL, getAuthHeaders} from './base';
import { clearAuthStorage } from './authStorage';

async function parseJSONSafely(response: Response) {
  const text = await response.text();
  return text ? JSON.parse(text) : {};
}

export async function getSchoolAdminOverview() {
  
  const response = await fetch(`${API_BASE_URL}/api/school-admin/overview`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  const data = await parseJSONSafely(response);
  
  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Oturum süresi doldu. Lütfen tekrar giriş yapın.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Okul yöneticisi genel bakışı yüklenemedi.');
  }

  return data;
}