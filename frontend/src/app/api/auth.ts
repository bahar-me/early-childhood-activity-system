import { LoginCredentials, LoginResponse } from '../types/user';
import { API_BASE_URL } from './base';

async function parseJSONSafely(response: Response) {
  const text = await response.text();
  
  if (!text) return {};

  try {
    return JSON.parse(text);
  } catch {
    return {};
  }
}

export async function loginRequest(credentials: LoginCredentials): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  });

  const data = await parseJSONSafely(response);

  if (!response.ok) {
    throw new Error(data.error || 'Giriş başarısız oldu.');
  }

  return data;
}

export async function logoutRequest(refreshToken: string): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/api/auth/logout`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  const data = await parseJSONSafely(response);

  if (!response.ok) {
    throw new Error(data.error || 'Çıkış başarısız oldu.');
  }

  return data;
}