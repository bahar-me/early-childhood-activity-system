export interface TeacherProfile {
  name: string;
  schoolName: string;
  yearsExperience: string;
  specializations: string[];
  teachingStyle: string;
}

export interface ClassProfile {
  className: string;
  ageGroup: string;
  classSize: number;
  specialNeeds: string[];
  learningFocus: string[];
  availableResources: string[];
  dailySchedule: {
    morningActivities: number; // minutes
    afternoonActivities: number; // minutes
  };
}
