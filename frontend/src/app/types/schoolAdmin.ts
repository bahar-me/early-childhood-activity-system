export type TeacherOverview = {
  id: string | number;
  name: string;
  years_experience?: number;
  specializations?: string[];
  teaching_style?: string;
  created_at?: string;
  school_id?: string | number;
};

export type ClassOverview = {
  id: string | number;
  class_name: string;
  age_group?: string;
  class_size?: number;
  learning_focus?: string[];
  updated_at?: string;
  school_id?: string | number;
};

export type PlanOverview = {
  id: string | number;
  teacher_id: string | number;
  class_id: string | number;
  activity_ids?: string[];
  created_at?: string;
  notes?: string;
  school_id?: string | number;
};

export type SchoolOverviewResponse = {
  success: boolean;
  school: {
    id: string | number;
    name: string;
    address?: string | null;
    contactEmail?: string;
    createdAt?: string;
    created_at?: string;
  };
  stats?: {
    teachers: number;
    classes: number;
    students: number;
    activity_plans: number;
  };
  teachers_list?: TeacherOverview[];
  classes_list?: ClassOverview[];
  plans_list?: PlanOverview[];
};