import { API_BASE_URL, getAuthHeaders} from './base';
import { clearAuthStorage } from './authStorage';

export async function getSchoolAdminOverview() {
  console.log('A. overview API called');

  const response = await fetch(`${API_BASE_URL}/api/school-admin/overview`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  console.log('B. overview API response received, status:', response.status);

  const data = await response.json();
  console.log('C. overview API data parsed:', data);

  if (response.status === 401) {
    clearAuthStorage();
    throw new Error('Your session has expired. Please log in again.');
  }

  if (!response.ok) {
    throw new Error(data.error || 'Failed to load school admin overview');
  }

  return data;
}