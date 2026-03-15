import { Activity } from '../types/activity';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Heart, Clock, Users } from 'lucide-react';

interface ActivityCardProps {
  activity: Activity;
  isFavorite: boolean;
  onToggleFavorite: (id: string) => void;
  onClick: (activity: Activity) => void;
}

export function ActivityCard({ activity, isFavorite, onToggleFavorite, onClick }: ActivityCardProps) {
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
    <Card className="hover:shadow-lg transition-shadow cursor-pointer relative">
      <Button
        variant="ghost"
        size="icon"
        className="absolute top-4 right-4 z-10"
        onClick={(e) => {
          e.stopPropagation();
          onToggleFavorite(activity.id);
        }}
      >
        <Heart
          className={`h-5 w-5 ${isFavorite ? 'fill-red-500 text-red-500' : 'text-gray-400'}`}
        />
      </Button>

      <div onClick={() => onClick(activity)}>
        <CardHeader>
          <CardTitle>{activity.title}</CardTitle>
          <div className="flex flex-wrap gap-2 mt-2">
            <Badge className={getSubjectColor(activity.subject)}>
              {activity.subject}
            </Badge>
          </div>
        </CardHeader>

        <CardContent>
          <p className="text-gray-600 mb-4">{activity.description}</p>
          
          <div className="flex flex-wrap gap-4 text-sm text-gray-500">
            <div className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              <span>{activity.duration}</span>
            </div>
            <div className="flex items-center gap-1">
              <Users className="h-4 w-4" />
              <span>{activity.groupSize}</span>
            </div>
          </div>
        </CardContent>
      </div>
    </Card>
  );
}
