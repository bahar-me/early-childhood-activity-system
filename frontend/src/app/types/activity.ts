export type Subject = 'Math' | 'Language' | 'Art' | 'Science' | 'Music' | 'Physical' | 'Social-Emotional';
export type Duration = '5-15min' | '15-30min' | '30-45min' | '45-60min';
export type GroupSize = 'Individual' | 'Small Group' | 'Whole Class';

export interface Activity {
  id: string;
  title: string;
  subject: Subject;
  duration: Duration;
  groupSize: GroupSize;
  description: string;
  materials: string[];
  instructions: string[];
  learningGoals: string[];
}
