import { API_BASE_URL, getAuthHeaders} from './base';

export async function getSchoolAdminOverview() {
  const response = await fetch(`${API_BASE_URL}/api/school-admin/overview`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Failed to load school admin overview');
  }

  return data;
}