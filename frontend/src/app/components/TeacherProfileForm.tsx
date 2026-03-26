import { useState } from 'react';
import { TeacherProfile } from '../types/profile';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Button } from './ui/button';
import { Checkbox } from './ui/checkbox';
import { RadioGroup, RadioGroupItem } from './ui/radio-group';
import { User } from 'lucide-react';

interface TeacherProfileFormProps {
  onSubmit: (profile: TeacherProfile) => void;
  initialData?: TeacherProfile;
}

export function TeacherProfileForm({ onSubmit, initialData }: TeacherProfileFormProps) {
  const [formData, setFormData] = useState<TeacherProfile>(
    initialData || {
      name: '',
      schoolName: '',
      yearsExperience: '',
      specializations: [],
      teachingStyle: '',
    }
  );

  const specializationOptions = [
    'Early Literacy',
    'Math & Numeracy',
    'Art & Creativity',
    'STEM Education',
    'Music & Movement',
    'Social-Emotional Learning',
    'Special Education',
    'Bilingual Education',
  ];

  const handleSpecializationChange = (specialization: string) => {
    setFormData((prev) => ({
      ...prev,
      specializations: prev.specializations.includes(specialization)
        ? prev.specializations.filter((s) => s !== specialization)
        : [...prev.specializations, specialization],
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Card className="max-w-2xl mx-auto w-full mb-24">
      <CardHeader>
        <div className="flex items-center gap-2">
          <User className="h-6 w-6 text-purple-600" />
          <CardTitle>Teacher Profile</CardTitle>
        </div>
        <CardDescription>
          Tell us about yourself to get personalized activity recommendations
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6 pb-16">
          <div className="space-y-2">
            <Label htmlFor="name">Full Name *</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="Ms. Sarah Johnson"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="schoolName">School Name *</Label>
            <Input
              id="schoolName"
              value={formData.schoolName}
              onChange={(e) => setFormData({ ...formData, schoolName: e.target.value })}
              placeholder="Sunshine Elementary School"
              required
            />
          </div>

          <div className="space-y-2">
            <Label>Years of Teaching Experience *</Label>
            <RadioGroup
              value={formData.yearsExperience}
              onValueChange={(value) => setFormData({ ...formData, yearsExperience: value })}
              required
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="0-2" id="exp1" />
                <Label htmlFor="exp1">0-2 years (New Teacher)</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="3-5" id="exp2" />
                <Label htmlFor="exp2">3-5 years</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="6-10" id="exp3" />
                <Label htmlFor="exp3">6-10 years</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="10+" id="exp4" />
                <Label htmlFor="exp4">10+ years (Experienced)</Label>
              </div>
            </RadioGroup>
          </div>

          <div className="space-y-2">
            <Label>Areas of Specialization</Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {specializationOptions.map((spec) => (
                <div key={spec} className="flex items-center gap-2">
                  <Checkbox
                    id={`spec-${spec}`}
                    checked={formData.specializations.includes(spec)}
                    onCheckedChange={() => handleSpecializationChange(spec)}
                  />
                  <label htmlFor={`spec-${spec}`} className="text-sm cursor-pointer">
                    {spec}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>Teaching Style *</Label>
            <RadioGroup
              value={formData.teachingStyle}
              onValueChange={(value) => setFormData({ ...formData, teachingStyle: value })}
              required
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="structured" id="style1" />
                <Label htmlFor="style1">Structured & Guided</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="balanced" id="style2" />
                <Label htmlFor="style2">Balanced Mix</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="exploratory" id="style3" />
                <Label htmlFor="style3">Exploratory & Child-Led</Label>
              </div>
            </RadioGroup>
          </div>

          <Button type="submit" className="w-full" size="lg">
            Continue to Class Profile
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
