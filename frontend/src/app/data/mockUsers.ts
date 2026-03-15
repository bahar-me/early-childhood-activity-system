import { User } from '../types/user';
import { School, TeacherRecord, ClassRecord, ActivityPlan } from '../types/school';

// Mock users for demo (in real app, this would be in a database)
export const mockUsers: User[] = [
  {
    id: '1',
    email: 'teacher@school.com',
    name: 'Sarah Johnson',
    role: 'teacher',
    schoolId: 'school-1',
    createdAt: '2024-01-15T08:00:00Z',
  },
  {
    id: '2',
    email: 'teacher2@school.com',
    name: 'Michael Chen',
    role: 'teacher',
    schoolId: 'school-1',
    createdAt: '2024-01-20T08:00:00Z',
  },
  {
    id: '3',
    email: 'admin@school.com',
    name: 'Dr. Emily Martinez',
    role: 'school-admin',
    schoolId: 'school-1',
    createdAt: '2024-01-10T08:00:00Z',
  },
  {
    id: '4',
    email: 'sysadmin@kinderactivity.com',
    name: 'David Kim',
    role: 'system-admin',
    createdAt: '2024-01-01T08:00:00Z',
  },
];

export const mockSchools: School[] = [
  {
    id: 'school-1',
    name: 'Sunshine Elementary School',
    address: '123 Education Lane, Learning City, LC 12345',
    contactEmail: 'contact@sunshine-elem.edu',
    createdAt: '2024-01-01T08:00:00Z',
  },
  {
    id: 'school-2',
    name: 'Rainbow Academy',
    address: '456 Knowledge Drive, Smart Town, ST 67890',
    contactEmail: 'info@rainbow-academy.edu',
    createdAt: '2024-01-05T08:00:00Z',
  },
];

export const mockTeacherRecords: TeacherRecord[] = [
  {
    id: '1',
    email: 'teacher@school.com',
    schoolId: 'school-1',
    name: 'Sarah Johnson',
    schoolName: 'Sunshine Elementary School',
    yearsExperience: '3-5',
    specializations: ['Early Literacy', 'Social-Emotional Learning'],
    teachingStyle: 'balanced',
    createdAt: '2024-01-15T08:00:00Z',
    lastActive: '2026-01-04T10:30:00Z',
  },
  {
    id: '2',
    email: 'teacher2@school.com',
    schoolId: 'school-1',
    name: 'Michael Chen',
    schoolName: 'Sunshine Elementary School',
    yearsExperience: '6-10',
    specializations: ['Math & Numeracy', 'STEM Education'],
    teachingStyle: 'structured',
    createdAt: '2024-01-20T08:00:00Z',
    lastActive: '2026-01-03T14:20:00Z',
  },
];

export const mockClassRecords: ClassRecord[] = [
  {
    id: 'class-1',
    teacherId: '1',
    teacherName: 'Sarah Johnson',
    schoolId: 'school-1',
    className: 'Morning Kindergarten Class A',
    ageGroup: '5-6',
    classSize: 18,
    specialNeeds: ['English Language Learners'],
    learningFocus: ['Literacy Development', 'Social Skills'],
    availableResources: ['Art Supplies', 'Library/Books', 'Outdoor Space'],
    dailySchedule: {
      morningActivities: 45,
      afternoonActivities: 30,
    },
    createdAt: '2024-01-15T08:00:00Z',
    updatedAt: '2026-01-02T09:00:00Z',
  },
  {
    id: 'class-2',
    teacherId: '2',
    teacherName: 'Michael Chen',
    schoolId: 'school-1',
    className: 'Afternoon Pre-K',
    ageGroup: '4-5',
    classSize: 15,
    specialNeeds: [],
    learningFocus: ['Math Foundations', 'Physical Development'],
    availableResources: ['Manipulatives', 'Outdoor Space', 'Science Materials'],
    dailySchedule: {
      morningActivities: 30,
      afternoonActivities: 60,
    },
    createdAt: '2024-01-20T08:00:00Z',
    updatedAt: '2026-01-03T11:15:00Z',
  },
];

export const mockActivityPlans: ActivityPlan[] = [
  {
    id: 'plan-1',
    teacherId: '1',
    teacherName: 'Sarah Johnson',
    classId: 'class-1',
    className: 'Morning Kindergarten Class A',
    schoolId: 'school-1',
    activityIds: ['2', '5', '7', '14'],
    createdAt: '2026-01-03T09:30:00Z',
    notes: 'Focus on language development and social skills this week',
  },
  {
    id: 'plan-2',
    teacherId: '2',
    teacherName: 'Michael Chen',
    classId: 'class-2',
    className: 'Afternoon Pre-K',
    schoolId: 'school-1',
    activityIds: ['1', '8', '15', '20'],
    createdAt: '2026-01-02T14:20:00Z',
    notes: 'Math and physical activities for active learners',
  },
];

// Mock password for demo (in real app, this would be hashed and in a database)
export const mockPasswords: Record<string, string> = {
  'teacher@school.com': 'teacher123',
  'teacher2@school.com': 'teacher123',
  'admin@school.com': 'admin123',
  'sysadmin@kinderactivity.com': 'sysadmin123',
};
