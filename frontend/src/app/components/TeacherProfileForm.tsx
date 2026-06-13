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
  schools: { id: number; name: string }[];
}

export function TeacherProfileForm({ onSubmit, initialData, schools }: TeacherProfileFormProps) {
  const [formData, setFormData] = useState<TeacherProfile>(
    initialData ?? {
      name: '',
      schoolId: null,
      schoolName: '',
      yearsExperience: '',
      specializations: [],
      teachingStyle: '',
    }
  );

  const specializationOptions = [
    'Erken okuryazarlık',
    'Matematik ve sayı farkındalığı',
    'Sanat ve yaratıcılık',
    'STEM eğitimi',
    'Müzik ve hareket',
    'Sosyal-duygusal öğrenme',
    'Özel eğitim',
    'Çift dilli eğitim',
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
          <CardTitle>Öğretmen Profili</CardTitle>
        </div>
        <CardDescription>
          Kişiselleştirilmiş etkinlik önerileri sunabilmemiz için öğretmen bilgilerinizi girin
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6 pb-16">
          <div className="space-y-2">
            <Label htmlFor="name">Ad Soyad *</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="Ayşe Yılmaz"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="school">Okul *</Label>
            <select
              id="school"
              className="w-full border rounded-md px-3 py-2"
              value={formData.schoolId ?? ''}
              onChange={(e) => {
                const selectedId = e.target.value ? Number(e.target.value) : null;
                const selectedSchool = schools.find((school) => school.id === selectedId);

                setFormData({
                  ...formData,
                  schoolId: selectedId,
                  schoolName: selectedSchool?.name || '',
                });
              }}
              required
            >
              <option value="">Okul seçin</option>
              {schools.map((school) => (
                <option key={school.id} value={school.id}>
                  {school.name}
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <Label>Deneyim yılı *</Label>
            <RadioGroup
              value={String(formData.yearsExperience ?? '')}
              onValueChange={(value) =>
                setFormData({ ...formData, yearsExperience: Number(value) })
              }
              required
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="1" id="exp1" />
                <Label htmlFor="exp1">0-2 yıl</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="4" id="exp2" />
                <Label htmlFor="exp2">3-5 yıl</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="8" id="exp3" />
                <Label htmlFor="exp3">6-10 yıl</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="10" id="exp4" />
                <Label htmlFor="exp4">10+ yıl</Label>
              </div>
            </RadioGroup>
          </div>

          <div className="space-y-2">
            <Label>Uzmanlık Alanları *</Label>
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
            <Label>Öğretim Stili *</Label>
            <RadioGroup
              value={formData.teachingStyle}
              onValueChange={(value) => setFormData({ ...formData, teachingStyle: value })}
              required
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="structured" id="style1" />
                <Label htmlFor="style1">Yapılandırılmış ve Rehberli</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="balanced" id="style2" />
                <Label htmlFor="style2">Dengeli Karışım</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="exploratory" id="style3" />
                <Label htmlFor="style3">Keşfetme ve Çocuk-Merkezli</Label>
              </div>
            </RadioGroup>
          </div>

          <Button type="submit" className="w-full" size="lg">
            Sınıf Profiline Geç
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}