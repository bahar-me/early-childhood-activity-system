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

interface ActivityDetailProps {
  activity: Activity | null;
  open: boolean;
  onClose: () => void;
}

export function ActivityDetail({ activity, open, onClose }: ActivityDetailProps) {
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

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh]">
        <DialogHeader>
          <DialogTitle>{activity.title}</DialogTitle>
          <DialogDescription className="flex flex-wrap gap-2 mt-2">
            <Badge className={getSubjectColor(activity.subject)}>
              {activity.subject}
            </Badge>
            <Badge variant="outline" className="flex items-center gap-1">
              <Clock className="h-3 w-3" />
              {activity.duration}
            </Badge>
            <Badge variant="outline" className="flex items-center gap-1">
              <Users className="h-3 w-3" />
              {activity.groupSize}
            </Badge>
          </DialogDescription>
        </DialogHeader>

        <ScrollArea className="max-h-[calc(90vh-120px)] pr-4">
          <div className="space-y-6">
            <div>
              <h3 className="font-semibold mb-2">Description</h3>
              <p className="text-gray-600">{activity.description}</p>
            </div>

            <div>
              <h3 className="font-semibold mb-2">Materials Needed</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-600">
                {activity.materials.map((material, index) => (
                  <li key={index}>{material}</li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-2">Instructions</h3>
              <ol className="list-decimal list-inside space-y-2 text-gray-600">
                {activity.instructions.map((instruction, index) => (
                  <li key={index} className="pl-2">{instruction}</li>
                ))}
              </ol>
            </div>

            <div>
              <h3 className="font-semibold mb-2">Learning Goals</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-600">
                {activity.learningGoals.map((goal, index) => (
                  <li key={index}>{goal}</li>
                ))}
              </ul>
            </div>
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}
