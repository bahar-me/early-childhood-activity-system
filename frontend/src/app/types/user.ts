export type UserRole = 'teacher' | 'school_admin' | 'system_admin';

export interface User {
  id: string;
  email: string;
  role: UserRole;

  // backend alanları 
  school_id?: number | null;
  created_at?: string;

  // frontend alanları
  name?: string;
  schoolId?: string;
  createdAt?: string;
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