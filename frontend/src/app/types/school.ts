import { TeacherProfile, ClassProfile } from './profile';

export interface School {
  id: string | number;
  name: string;
  address?: string | null;
  contactEmail?: string;
  createdAt?: string;
  created_at?: string;
}

export interface TeacherRecord extends TeacherProfile {
  id: string;
  email: string;
  schoolId: string;
  createdAt: string;
  lastActive: string;
}

export interface ClassRecord extends ClassProfile {
  id: string;
  teacherId: string;
  teacherName: string;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface ActivityPlan {
  id: string;
  teacherId: string;
  teacherName: string;
  classId: string;
  className: string;
  schoolId: string;
  activityIds: string[];
  createdAt: string;
  notes?: string;
}