export function clearAuthStorage() {
  localStorage.removeItem('current-user');
  localStorage.removeItem('access-token');
  localStorage.removeItem('refresh-token');
}