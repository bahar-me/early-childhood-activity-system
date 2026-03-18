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
  id: string | number;
  email?: string;
  schoolId?: string;
  school_id?: number | string;
  createdAt?: string;
  created_at?: string;
  lastActive?: string;
  years_experience?: number;
  teaching_style?: string;
}

export interface ClassRecord extends ClassProfile {
  id: string | number;
  teacherId?: string | number;
  teacher_id?: string | number;
  teacherName?: string;
  schoolId?: string;
  school_id?: number | string;
  createdAt?: string;
  created_at?: string;
  updatedAt?: string;
  updated_at?: string;
  class_name?: string;
  age_group?: string;
  class_size?: number;
  learning_focus?: string[];
}

export interface ActivityPlan {
  id: string | number;

  // eski mock alanları
  teacherId?: string;
  teacherName?: string;
  classId?: string;
  className?: string;
  schoolId?: string;
  activityIds?: string[];
  createdAt?: string;

  // backend alanları
  teacher_id?: string | number;
  class_id?: string | number;
  school_id?: string | number;
  activity_ids?: string[];
  created_at?: string;

  notes?: string;
}