import { useState } from 'react';
import { ClassProfile } from '../types/profile';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Button } from './ui/button';
import { Checkbox } from './ui/checkbox';
import { RadioGroup, RadioGroupItem } from './ui/radio-group';
import { Slider } from './ui/slider';
import { Users } from 'lucide-react';

interface ClassProfileFormProps {
  onSubmit: (profile: ClassProfile) => void;
  onBack: () => void;
  initialData?: ClassProfile;
}

export function ClassProfileForm({ onSubmit, onBack, initialData }: ClassProfileFormProps) {
  const [formData, setFormData] = useState<ClassProfile>(
    initialData ?? {
      className: '',
      ageGroup: '',
      classSize: 20,
      specialNeeds: [],
      learningFocus: [],
      availableResources: [],
      dailySchedule: {
        morningActivities: 45,
        afternoonActivities: 30,
      },
    }
  );

  const specialNeedsOptions = [
    'Dil desteği ihtiyacı',
    'Dikkat ve odaklanma desteği',
    'Otizm spektrum desteği',
    'Üstün yetenekli çocuklar',
    'Motor beceri desteği',
    'Konuşma ve dil desteği',
  ];

  const learningFocusOptions = [
    'Okuma yazmaya hazırlık',
    'Matematik temelleri',
    'Sosyal beceriler',
    'Yaratıcı ifade',
    'Fiziksel gelişim',
    'Fen ve doğa keşfi',
  ];

  const resourceOptions = [
    'Tablet/Teknoloji',
    'Sanat malzemeleri',
    'Müzik aletleri',
    'Açık alan',
    'Kitaplık / kitaplar',
    'Eğitici manipülatif materyaller',
    'Fen materyalleri',
  ];

  const handleArrayChange = (
    field: 'specialNeeds' | 'learningFocus' | 'availableResources',
    value: string
  ) => {
    setFormData((prev) => ({
      ...prev,
      [field]: prev[field].includes(value)
        ? prev[field].filter((item) => item !== value)
        : [...prev[field], value],
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <div className="flex items-center gap-2">
          <Users className="h-6 w-6 text-purple-600" />
          <CardTitle>Sınıf Profili</CardTitle>
        </div>
        <CardDescription>
          Sınıfınız hakkında bize bilgi verin, böylece kişiselleştirilmiş etkinlik önerileri sunabilelim
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="className">Sınıf Adı *</Label>
            <Input
              id="className"
              value={formData.className}
              onChange={(e) => setFormData({ ...formData, className: e.target.value })}
              placeholder="Güneş Anaokulu Sınıf A"
              required
            />
          </div>

          <div className="space-y-2">
            <Label>Yaş Grubu *</Label>
            <RadioGroup
              value={formData.ageGroup}
              onValueChange={(value) => setFormData({ ...formData, ageGroup: value })}
              required
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="4-5" id="age1" />
                <Label htmlFor="age1">4-5 yaş (Okul Öncesi)</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="5-6" id="age2" />
                <Label htmlFor="age2">5-6 yaş (Anaokulu)</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="6-7" id="age3" />
                <Label htmlFor="age3">6-7 yaş (Geçiş K/1. Sınıf)</Label>
              </div>
            </RadioGroup>
          </div>

          <div className="space-y-2">
            <Label htmlFor="classSize">Sınıf Mevcudu: {formData.classSize} öğrenci</Label>
            <Slider
              id="classSize"
              min={5}
              max={35}
              step={1}
              value={[formData.classSize]}
              onValueChange={(value) => setFormData({ ...formData, classSize: value[0] ?? formData.classSize })}
            />
          </div>

          <div className="space-y-2">
            <Label>Özel İhtiyaçlar veya Dikkat Edilmesi Gerekenler</Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {specialNeedsOptions.map((need) => (
                <div key={need} className="flex items-center gap-2">
                  <Checkbox
                    id={`need-${need}`}
                    checked={formData.specialNeeds.includes(need)}
                    onCheckedChange={() => handleArrayChange('specialNeeds', need)}
                  />
                  <label htmlFor={`need-${need}`} className="text-sm cursor-pointer">
                    {need}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>Öğrenme Odak Noktaları</Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {learningFocusOptions.map((focus) => (
                <div key={focus} className="flex items-center gap-2">
                  <Checkbox
                    id={`focus-${focus}`}
                    checked={formData.learningFocus.includes(focus)}
                    onCheckedChange={() => handleArrayChange('learningFocus', focus)}
                  />
                  <label htmlFor={`focus-${focus}`} className="text-sm cursor-pointer">
                    {focus}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>Mevcut Kaynaklar</Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {resourceOptions.map((resource) => (
                <div key={resource} className="flex items-center gap-2">
                  <Checkbox
                    id={`resource-${resource}`}
                    checked={formData.availableResources.includes(resource)}
                    onCheckedChange={() => handleArrayChange('availableResources', resource)}
                  />
                  <label htmlFor={`resource-${resource}`} className="text-sm cursor-pointer">
                    {resource}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-4">
            <Label>Günlük Etkinlik Programı</Label>
            <div className="space-y-2">
              <Label htmlFor="morning">
                Sabah Etkinlikleri: {formData.dailySchedule.morningActivities} dakika
              </Label>
              <Slider
                id="morning"
                min={15}
                max={120}
                step={15}
                value={[formData.dailySchedule.morningActivities]}
                onValueChange={(value) =>
                  setFormData({
                    ...formData,
                    dailySchedule: { ...formData.dailySchedule, morningActivities: value[0] ?? formData.dailySchedule.morningActivities },
                  })
                }
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="afternoon">
                Öğleden Sonra Etkinlikleri: {formData.dailySchedule.afternoonActivities} dakika
              </Label>
              <Slider
                id="afternoon"
                min={15}
                max={120}
                step={15}
                value={[formData.dailySchedule.afternoonActivities]}
                onValueChange={(value) =>
                  setFormData({
                    ...formData,
                    dailySchedule: { ...formData.dailySchedule, afternoonActivities: value[0] ?? formData.dailySchedule.afternoonActivities },
                  })
                }
              />
            </div>
          </div>

          <div className="flex gap-3">
            <Button type="button" variant="outline" onClick={onBack} className="flex-1">
              Geri
            </Button>
            <Button type="submit" className="flex-1" size="lg">
              Uygulamayı Kullanmaya Başla
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
