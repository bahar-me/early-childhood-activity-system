import { useEffect, useState } from 'react';
import { Activity, Subject, Duration, GroupSize } from '../types/activity';
import { Button } from './ui/button';

interface ActivityEditModalProps {
  open: boolean;
  activity: Activity | null;
  onClose: () => void;
  onSave: (payload: Omit<Activity, 'id'>) => void;
  isSaving?: boolean;
}

export function ActivityEditModal({
  open,
  activity,
  onClose,
  onSave,
  isSaving = false,
}: ActivityEditModalProps) {
  const [title, setTitle] = useState('');
  const [subject, setSubject] = useState<Subject>('Math');
  const [duration, setDuration] = useState<Duration>('15-30min');
  const [groupSize, setGroupSize] = useState<GroupSize>('Small Group');
  const [description, setDescription] = useState('');
  const [materialsText, setMaterialsText] = useState('');
  const [instructionsText, setInstructionsText] = useState('');
  const [learningGoalsText, setLearningGoalsText] = useState('');

  useEffect(() => {
    if (activity) {
      setTitle(activity.title);
      setSubject(activity.subject);
      setDuration(activity.duration);
      setGroupSize(activity.groupSize);
      setDescription(activity.description);
      setMaterialsText(activity.materials.join('\n'));
      setInstructionsText(activity.instructions.join('\n'));
      setLearningGoalsText(activity.learningGoals.join('\n'));
    }
  }, [activity]);

  if (!open || !activity) return null;

  const handleSave = () => {
    const payload: Omit<Activity, 'id'> = {
      title: title.trim(),
      subject,
      duration,
      groupSize,
      description: description.trim(),
      materials: materialsText
        .split('\n')
        .map((item) => item.trim())
        .filter(Boolean),
      instructions: instructionsText
        .split('\n')
        .map((item) => item.trim())
        .filter(Boolean),
      learningGoals: learningGoalsText
        .split('\n')
        .map((item) => item.trim())
        .filter(Boolean),
    };

    onSave(payload);
  };

  return (
    <div className="fixed inset-0 z-[60] bg-black/50 flex items-center justify-center p-4">
      <div className="bg-white w-full max-w-3xl max-h-[90vh] overflow-y-auto rounded-lg shadow-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Etkinliği Düzenle</h2>
          <Button variant="outline" onClick={onClose}>
            Kapat
          </Button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Başlık</label>
            <input
              className="w-full border rounded-md px-3 py-2"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Alan</label>
              <select
                className="w-full border rounded-md px-3 py-2"
                value={subject}
                onChange={(e) => setSubject(e.target.value as Subject)}
              >
                <option value="Math">Math</option>
                <option value="Language">Language</option>
                <option value="Art">Art</option>
                <option value="Science">Science</option>
                <option value="Music">Music</option>
                <option value="Physical">Physical</option>
                <option value="Social-Emotional">Social-Emotional</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Süre</label>
              <select
                className="w-full border rounded-md px-3 py-2"
                value={duration}
                onChange={(e) => setDuration(e.target.value as Duration)}
              >
                <option value="5-15min">5-15min</option>
                <option value="15-30min">15-30min</option>
                <option value="30-45min">30-45min</option>
                <option value="45-60min">45-60min</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Grup Yapısı</label>
              <select
                className="w-full border rounded-md px-3 py-2"
                value={groupSize}
                onChange={(e) => setGroupSize(e.target.value as GroupSize)}
              >
                <option value="Individual">Individual</option>
                <option value="Small Group">Small Group</option>
                <option value="Whole Class">Whole Class</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Açıklama</label>
            <textarea
              className="w-full border rounded-md px-3 py-2 min-h-[100px]"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Materyaller (her satıra bir madde)</label>
            <textarea
              className="w-full border rounded-md px-3 py-2 min-h-[120px]"
              value={materialsText}
              onChange={(e) => setMaterialsText(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Uygulama Adımları (her satıra bir madde)</label>
            <textarea
              className="w-full border rounded-md px-3 py-2 min-h-[140px]"
              value={instructionsText}
              onChange={(e) => setInstructionsText(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Öğrenme Hedefleri (her satıra bir madde)</label>
            <textarea
              className="w-full border rounded-md px-3 py-2 min-h-[120px]"
              value={learningGoalsText}
              onChange={(e) => setLearningGoalsText(e.target.value)}
            />
          </div>
        </div>

        <div className="flex justify-end gap-2 mt-6">
          <Button variant="outline" onClick={onClose}>
            İptal
          </Button>
          <Button onClick={handleSave} disabled={isSaving}>
            {isSaving ? 'Kaydediliyor...' : 'Yeni Etkinlik Olarak Kaydet'}
          </Button>
        </div>
      </div>
    </div>
  );
}