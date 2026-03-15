export type UserRole = 'teacher' | 'school_admin' | 'system_admin';

export interface User {
  id: string;
  email: string;
  role: UserRole;
  school_id?: number | null;
  created_at?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface LoginResponse {
  message: string;
  access_token: string;
  refresh_token: string;
  user: User;
}