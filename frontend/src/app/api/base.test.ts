import { describe, expect, it, beforeEach } from 'vitest';
import { API_BASE_URL, getAuthHeaders } from './base';

describe('API base configuration', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('should define an API base URL', () => {
    expect(API_BASE_URL).toBeDefined();
    expect(typeof API_BASE_URL).toBe('string');
    expect(API_BASE_URL.length).toBeGreaterThan(0);
  });

  it('should return auth headers when access token exists', () => {
    localStorage.setItem('access-token', 'test-token');

    const headers = getAuthHeaders();

    expect(headers).toEqual({
      'Content-Type': 'application/json',
      Authorization: 'Bearer test-token',
    });
  });

  it('should throw an error when access token is missing', () => {
    expect(() => getAuthHeaders()).toThrow(
      'Access token bulunamadı. Lütfen tekrar giriş yapın.'
    );
  });
});