import { useEffect, useState } from 'react';
import { Activity } from '../types/activity';
import { TeacherProfile, ClassProfile } from '../types/profile';
import { adaptActivity, AdaptActivityDraft } from '../api/ai';
import { Button } from './ui/button';
import { toast } from 'sonner';

interface ActivityAdaptModalProps {
  open: boolean;
  activity: Activity | null;
  teacherProfile: TeacherProfile | null;
  classProfile: ClassProfile | null;
  onClose: () => void;
  onSaveDraft: (draft: AdaptActivityDraft) => Promise<void> | void;
  isSaving?: boolean;
}

export function ActivityAdaptModal({
  open,
  activity,
  teacherProfile,
  classProfile,
  onClose,
  onSaveDraft,
  isSaving = false,
}: ActivityAdaptModalProps) {
  const [adaptationPrompt, setAdaptationPrompt] = useState('');
  const [isAdapting, setIsAdapting] = useState(false);
  const [draft, setDraft] = useState<AdaptActivityDraft | null>(null);

  useEffect(() => {
    if (!open) {
        setAdaptationPrompt('');
        setDraft(null);
    }
  }, [open]);  

  if (!open || !activity) return null;

  const handleAdapt = async () => {
    if (!adaptationPrompt.trim()) {
      toast.error('Lütfen bir uyarlama isteği yaz.');
      return;
    }

    try {
      setIsAdapting(true);

      const result = await adaptActivity({
        activity: {
          title: activity.title,
          subject: activity.subject,
          duration: activity.duration,
          groupSize: activity.groupSize,
          description: activity.description,
          materials: activity.materials,
          instructions: activity.instructions,
          learningGoals: activity.learningGoals,
        },
        teacher_profile: teacherProfile
          ? {
              name: teacherProfile.name,
              years_experience: teacherProfile.yearsExperience,
              specializations: teacherProfile.specializations,
              teaching_style: teacherProfile.teachingStyle,
            }
          : undefined,
        class_profile: classProfile
          ? {
              class_name: classProfile.className,
              age_group: classProfile.ageGroup,
              class_size: classProfile.classSize,
              learning_focus: classProfile.learningFocus,
              available_resources: classProfile.availableResources,
              special_needs: classProfile.specialNeeds,
            }
          : undefined,
        adaptation_prompt: adaptationPrompt,
      });

      setDraft(result.activity_draft);
      toast.success('YZ etkinlik taslağı oluşturdu.');
    } catch (error) {
      const message =
        error instanceof Error ? error.message : 'Etkinlik uyarlanamadı.';
      toast.error(message);
    } finally {
      setIsAdapting(false);
    }
  };

  const handleSave = async () => {
    if (!draft) return;

    try {
      await onSaveDraft(draft);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : 'Taslak kaydedilemedi.';
      toast.error(message);
    }
  };

  return (
    <div className="fixed inset-0 z-[70] bg-black/50 flex items-center justify-center p-4">
      <div className="bg-white w-full max-w-4xl max-h-[90vh] overflow-y-auto rounded-lg shadow-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">YZ ile Etkinlik Uyarlat</h2>
          <Button variant="outline" onClick={onClose}>
            Kapat
          </Button>
        </div>

        <div className="space-y-4">
          <div className="rounded-lg border p-4 bg-gray-50">
            <h3 className="font-medium mb-2">Seçili Etkinlik</h3>
            <p className="font-semibold">{activity.title}</p>
            <p className="text-sm text-gray-600 mt-1">{activity.description}</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Uyarlama isteği
            </label>
            <textarea
              className="w-full border rounded-md px-3 py-2 min-h-[120px]"
              placeholder="Örn: Bu etkinliği 4 yaş için sadeleştir, materyalsiz hale getir ve süreyi kısalt."
              value={adaptationPrompt}
              onChange={(e) => setAdaptationPrompt(e.target.value)}
            />
          </div>

          <div className="flex gap-2">
            <Button onClick={handleAdapt} disabled={isAdapting || isSaving}>
              {isAdapting ? 'YZ Uyarlıyor...' : 'YZ ile Uyarlat'}
            </Button>
          </div>

          {draft && (
            <div className="rounded-lg border p-4 space-y-4">
              <h3 className="text-lg font-semibold">Oluşturulan Taslak</h3>

              <div>
                <p className="text-sm font-medium">Başlık</p>
                <p>{draft.title}</p>
              </div>

              <div>
                <p className="text-sm font-medium">Açıklama</p>
                <p>{draft.description}</p>
              </div>

              <div>
                <p className="text-sm font-medium">Materyaller</p>
                <ul className="list-disc list-inside">
                  {draft.materials.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </div>

              <div>
                <p className="text-sm font-medium">Uygulama Adımları</p>
                <ol className="list-decimal list-inside">
                  {draft.instructions.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ol>
              </div>

              <div>
                <p className="text-sm font-medium">Öğrenme Hedefleri</p>
                <ul className="list-disc list-inside">
                  {draft.learningGoals.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <Button 
                    variant="outline" 
                    onClick={() => setDraft(null)}
                    disabled={isSaving}>
                  Taslağı Temizle
                </Button>
                <Button onClick={handleSave} disabled={isSaving}>
                    {isSaving ? 'Kaydediliyor...' : 'Yeni Etkinlik Olarak Kaydet'}
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}