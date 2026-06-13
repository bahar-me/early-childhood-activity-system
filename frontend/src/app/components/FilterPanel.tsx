import { Subject, Duration, GroupSize } from '../types/activity';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Label } from './ui/label';
import { Checkbox } from './ui/checkbox';
import { Button } from './ui/button';

interface FilterPanelProps {
  selectedSubjects: Subject[];
  selectedDurations: Duration[];
  selectedGroupSizes: GroupSize[];
  onSubjectChange: (subject: Subject) => void;
  onDurationChange: (duration: Duration) => void;
  onGroupSizeChange: (groupSize: GroupSize) => void;
  onClearFilters: () => void;
}

export function FilterPanel({
  selectedSubjects,
  selectedDurations,
  selectedGroupSizes,
  onSubjectChange,
  onDurationChange,
  onGroupSizeChange,
  onClearFilters,
}: FilterPanelProps) {
  const subjects: Subject[] = ['Math', 'Language', 'Art', 'Science', 'Music', 'Physical', 'Social-Emotional'];
  const durations: Duration[] = ['5-15min', '15-30min', '30-45min', '45-60min'];
  const groupSizes: GroupSize[] = ['Individual', 'Small Group', 'Whole Class'];

  const hasActiveFilters = 
    selectedSubjects.length > 0 || 
    selectedDurations.length > 0 || 
    selectedGroupSizes.length > 0;

  const translateSubject = (subject: string) => {
    const map: Record<string, string> = {
      Math: 'Matematik',
      Language: 'Dil Gelişimi',
      Art: 'Sanat',
      Science: 'Fen ve Doğa',
      Music: 'Müzik',
      Physical: 'Fiziksel Gelişim',
      'Social-Emotional': 'Sosyal-Duygusal Gelişim',
    };
    return map[subject] || subject;
  };

  const translateGroupSize = (groupSize: string) => {
    const map: Record<string, string> = {
      Individual: 'Bireysel',
      'Small Group': 'Küçük Grup',
      'Whole Class': 'Tüm Sınıf',
    };
    return map[groupSize] || groupSize;
  };

  const translateDuration = (duration: string) => {
    const map: Record<string, string> = {
      '5-15min': '5-15 dakika',
      '15-30min': '15-30 dakika',
      '30-45min': '30-45 dakika',
      '45-60min': '45-60 dakika',
    };
    return map[duration] || duration;
  };

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Filtreler</CardTitle>
        {hasActiveFilters && (
          <Button variant="ghost" size="sm" onClick={onClearFilters}>
            Filtreleri Temizle
          </Button>
        )}
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <Label className="mb-3 block">Gelişim Alanları</Label>
          <div className="space-y-2">
            {subjects.map((subject) => (
              <div key={subject} className="flex items-center gap-2">
                <Checkbox
                  id={`subject-${subject}`}
                  checked={selectedSubjects.includes(subject)}
                  onCheckedChange={() => onSubjectChange(subject)}
                />
                <label
                  htmlFor={`subject-${subject}`}
                  className="text-sm cursor-pointer"
                >
                  {translateSubject(subject)}
                </label>
              </div>
            ))}
          </div>
        </div>

        <div>
          <Label className="mb-3 block">Süre</Label>
          <div className="space-y-2">
            {durations.map((duration) => (
              <div key={duration} className="flex items-center gap-2">
                <Checkbox
                  id={`duration-${duration}`}
                  checked={selectedDurations.includes(duration)}
                  onCheckedChange={() => onDurationChange(duration)}
                />
                <label
                  htmlFor={`duration-${duration}`}
                  className="text-sm cursor-pointer"
                >
                  {translateDuration(duration)}
                </label>
              </div>
            ))}
          </div>
        </div>

        <div>
          <Label className="mb-3 block">Grup Yapısı</Label>
          <div className="space-y-2">
            {groupSizes.map((size) => (
              <div key={size} className="flex items-center gap-2">
                <Checkbox
                  id={`group-${size}`}
                  checked={selectedGroupSizes.includes(size)}
                  onCheckedChange={() => onGroupSizeChange(size)}
                />
                <label
                  htmlFor={`group-${size}`}
                  className="text-sm cursor-pointer"
                >
                  {translateGroupSize(size)}
                </label>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
