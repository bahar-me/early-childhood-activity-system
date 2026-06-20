import { CreateActivityPayload } from '../api/activities';
import { useEffect, useState } from 'react';
import { Activity, Subject, Duration, GroupSize } from '../types/activity';
import { Button } from './ui/button';
import { toast } from 'sonner';

interface ActivityEditModalProps {
  open: boolean;
  activity: Activity | null;
  onClose: () => void;
  onSaveAsNew: (payload: Omit<CreateActivityPayload, 'sourceType' | 'parentActivityId' | 'createdByUserId'>) => Promise<void> | void;
  onUpdate: (payload: Omit<CreateActivityPayload, 'sourceType' | 'parentActivityId' | 'createdByUserId'>) => Promise<void> | void;
  isSaving?: boolean;
}

export function ActivityEditModal({
  open,
  activity,
  onClose,
  onSaveAsNew,
  onUpdate,
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
  const [assessmentQuestionsText, setAssessmentQuestionsText] = useState('');
  const [differentiationNotes, setDifferentiationNotes] = useState('');
  const [familyCommunityNotes, setFamilyCommunityNotes] = useState('');
  const [learningOutcomesSummary, setLearningOutcomesSummary] = useState('');

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
      setAssessmentQuestionsText((activity.assessmentQuestions || []).join('\n'));
      setDifferentiationNotes(activity.differentiationNotes || '');
      setFamilyCommunityNotes(activity.familyCommunityNotes || '');
      setLearningOutcomesSummary(activity.learningOutcomesSummary || '');
    }

    if (!open) {
      setTitle('');
      setSubject('Math');
      setDuration('15-30min');
      setGroupSize('Small Group');
      setDescription('');
      setMaterialsText('');
      setInstructionsText('');
      setLearningGoalsText('');
      setAssessmentQuestionsText('');
      setDifferentiationNotes('');
      setFamilyCommunityNotes('');
      setLearningOutcomesSummary('');
    }
  }, [open, activity]);

  useEffect(() => {
    if (open) {
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.body.style.overflow = '';
    };
  }, [open]);

  if (!open || !activity) return null;

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

  const translateDuration = (duration: string) => {
    const map: Record<string, string> = {
        '5-15min': '5-15 dakika',
        '15-30min': '15-30 dakika',
        '30-45min': '30-45 dakika',
        '45-60min': '45-60 dakika',
    };
    return map[duration] || duration;
  };

  const translateGroupSize = (groupSize: string) => {
    const map: Record<string, string> = {
        Individual: 'Bireysel',
        'Small Group': 'Küçük Grup',
        'Whole Class': 'Tüm Sınıf',
    };
    return map[groupSize] || groupSize;
  };

  const buildPayload = () => {
    if (!title.trim()) {
      toast.error('Başlık zorunludur.');
      return null;
    }

    if (!description.trim()) {
      toast.error('Açıklama zorunludur.');
      return null;
    }
    
    const payload: Omit<CreateActivityPayload, 'sourceType' | 'parentActivityId' | 'createdByUserId'> = {
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
      assessmentQuestions: assessmentQuestionsText
        .split('\n')
        .map((item) => item.trim())
        .filter(Boolean),
      differentiationNotes: differentiationNotes.trim(),
      familyCommunityNotes: familyCommunityNotes.trim(),
      learningOutcomesSummary: learningOutcomesSummary.trim(),
    };

    return payload;
  };

  const handleUpdate = async () => {
    const payload = buildPayload();
    if (!payload) return;

    await onUpdate(payload);
  };

  const handleSaveAsNew = async () => {
    const payload = buildPayload();
    if (!payload) return;

    await onSaveAsNew(payload);
  };

  return (
    <div className="fixed inset-0 z-[60] bg-black/50 flex items-center justify-center p-4">
      <div className="bg-white w-full max-w-3xl max-h-[90vh] overflow-y-auto rounded-lg shadow-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Etkinliği Düzenle / Yeni Kayıt Oluştur</h2>
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
                <option value="Math">{translateSubject('Math')}</option>
                <option value="Language">{translateSubject('Language')}</option>
                <option value="Art">{translateSubject('Art')}</option>
                <option value="Science">{translateSubject('Science')}</option>
                <option value="Music">{translateSubject('Music')}</option>
                <option value="Physical">{translateSubject('Physical')}</option>
                <option value="Social-Emotional">{translateSubject('Social-Emotional')}</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Süre</label>
              <select
                className="w-full border rounded-md px-3 py-2"
                value={duration}
                onChange={(e) => setDuration(e.target.value as Duration)}
              >
                <option value="5-15min">{translateDuration('5-15min')}</option>
                <option value="15-30min">{translateDuration('15-30min')}</option>
                <option value="30-45min">{translateDuration('30-45min')}</option>
                <option value="45-60min">{translateDuration('45-60min')}</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Grup Yapısı</label>
              <select
                className="w-full border rounded-md px-3 py-2"
                value={groupSize}
                onChange={(e) => setGroupSize(e.target.value as GroupSize)}
              >
                <option value="Individual">{translateGroupSize('Individual')}</option>
                <option value="Small Group">{translateGroupSize('Small Group')}</option>
                <option value="Whole Class">{translateGroupSize('Whole Class')}</option>
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
          <div>
            <label className="block text-sm font-medium mb-1">
              Değerlendirme Soruları (her satıra bir soru)
            </label>
            <textarea
              className="w-full border rounded-md px-3 py-2 min-h-[120px]"
              value={assessmentQuestionsText}
              onChange={(e) => setAssessmentQuestionsText(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Farklılaştırma</label>
            <textarea
              className="w-full border rounded-md px-3 py-2 min-h-[100px]"
              value={differentiationNotes}
              onChange={(e) => setDifferentiationNotes(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Aile / Toplum Katılımı</label>
            <textarea
              className="w-full border rounded-md px-3 py-2 min-h-[100px]"
              value={familyCommunityNotes}
              onChange={(e) => setFamilyCommunityNotes(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Öğrenme Çıktısı Özeti</label>
            <textarea
              className="w-full border rounded-md px-3 py-2 min-h-[100px]"
              value={learningOutcomesSummary}
              onChange={(e) => setLearningOutcomesSummary(e.target.value)}
            />
          </div>
        </div>

        <div className="flex justify-end gap-2 mt-6">
          <Button variant="outline" onClick={onClose}>
            İptal
          </Button>
          
          <Button variant="outline" onClick={handleUpdate} disabled={isSaving}>
            {isSaving ? 'Kaydediliyor...' : 'Güncelle'}
          </Button>

          <Button onClick={handleSaveAsNew} disabled={isSaving}>
            {isSaving ? 'Kaydediliyor...' : 'Yeni Etkinlik Olarak Kaydet'}
          </Button>

        </div>
      </div>
    </div>
  );
}