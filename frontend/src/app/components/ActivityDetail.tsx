import { Activity } from '../types/activity';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from './ui/dialog';
import { Badge } from './ui/badge';
import { Clock, Users } from 'lucide-react';
import { ScrollArea } from './ui/scroll-area';
import { Button } from './ui/button';

interface ActivityDetailProps {
  activity: Activity | null;
  open: boolean;
  onClose: () => void;
  onEdit?: (activity: Activity) => void;
  onAdapt?: (activity: Activity) => void;
}

export function ActivityDetail({ activity, open, onClose, onEdit, onAdapt }: ActivityDetailProps) {
  if (!activity) return null;

  const getSubjectColor = (subject: string) => {
    const colors: Record<string, string> = {
      Math: 'bg-blue-100 text-blue-800 border-blue-300',
      Language: 'bg-purple-100 text-purple-800 border-purple-300',
      Art: 'bg-pink-100 text-pink-800 border-pink-300',
      Science: 'bg-green-100 text-green-800 border-green-300',
      Music: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      Physical: 'bg-orange-100 text-orange-800 border-orange-300',
      'Social-Emotional': 'bg-teal-100 text-teal-800 border-teal-300',
    };
    return colors[subject] || 'bg-gray-100 text-gray-800 border-gray-300';
  };

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
    <Dialog open={open} onOpenChange={(nextOpen) => {
      if (!nextOpen) onClose();
    }}>
      <DialogContent className="max-w-2xl max-h-[90vh]">
        <DialogHeader>
          <DialogTitle>{activity.title}</DialogTitle>
          <DialogDescription className="flex flex-wrap gap-2 mt-2">
            <Badge className={getSubjectColor(activity.subject)}>
              {translateSubject(activity.subject)}
            </Badge>
            <Badge variant="outline" className="flex items-center gap-1">
              <Clock className="h-3 w-3" />
              {translateDuration(activity.duration)}
            </Badge>
            <Badge variant="outline" className="flex items-center gap-1">
              <Users className="h-3 w-3" />
              {translateGroupSize(activity.groupSize)}
            </Badge>
          </DialogDescription>
        </DialogHeader>

        <ScrollArea className="max-h-[calc(90vh-120px)] pr-4">
          <div className="space-y-6">
            <div>
              <h3 className="font-semibold mb-2">Açıklama</h3>
              <p className="text-gray-600">{activity.description}</p>
            </div>

            <div>
              <h3 className="font-semibold mb-2">Gerekli Materyaller</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-600">
                {activity.materials.map((material, index) => (
                  <li key={index}>{material}</li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-2">Uygulama Adımları</h3>
              <ol className="list-decimal list-inside space-y-2 text-gray-600">
                {activity.instructions.map((instruction, index) => (
                  <li key={index} className="pl-2">{instruction}</li>
                ))}
              </ol>
            </div>

            <div>
              <h3 className="font-semibold mb-2">Öğrenme Hedefleri</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-600">
                {activity.learningGoals.map((goal, index) => (
                  <li key={index}>{goal}</li>
                ))}
              </ul>
            </div>

            {activity.learningOutcomesSummary && (
              <div>
                <h3 className="font-semibold mb-2">Öğrenme Çıktısı Özeti</h3>
                <p className="text-gray-600">{activity.learningOutcomesSummary}</p>
              </div>
            )}

            {activity.assessmentQuestions && activity.assessmentQuestions.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2">Değerlendirme Soruları</h3>
                <ul className="list-disc list-inside space-y-1 text-gray-600">
                  {activity.assessmentQuestions.map((question, index) => (
                    <li key={index}>{question}</li>
                  ))}
                </ul>
              </div>
            )}

            {activity.differentiationNotes && (
              <div>
                <h3 className="font-semibold mb-2">Farklılaştırma</h3>
                <p className="text-gray-600">{activity.differentiationNotes}</p>
              </div>
            )}

            {activity.familyCommunityNotes && (
              <div>
                <h3 className="font-semibold mb-2">Aile / Toplum Katılımı</h3>
                <p className="text-gray-600">{activity.familyCommunityNotes}</p>
              </div>
            )}

          </div>
        </ScrollArea>

        <div className="flex justify-end gap-2 pt-4 border-t mt-4">
          {onEdit && (
            <Button
              variant="outline"
              onClick={() => {
                onClose();
                onEdit(activity)
              }}
            >
              Düzenle
            </Button>
          )}
          {onAdapt && (
            <Button
              variant="outline"
              onClick={() => {
                onClose();
                onAdapt(activity)
              }}
            >
              YZ ile Uyarlat
            </Button>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
