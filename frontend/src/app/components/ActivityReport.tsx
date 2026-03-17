import { Activity } from '../types/activity';
import { TeacherProfile, ClassProfile } from '../types/profile';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { ScrollArea } from './ui/scroll-area';
import { Printer, Clock, Users } from 'lucide-react';

interface ActivityReportProps {
  activities: Activity[];
  teacherProfile: TeacherProfile;
  classProfile: ClassProfile;
  open: boolean;
  onClose: () => void;
}

export function ActivityReport({
  activities,
  teacherProfile,
  classProfile,
  open,
  onClose,
}: ActivityReportProps) {
  const handlePrint = () => {
    window.print();
  };

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

  const totalDuration = activities.reduce((acc, activity) => {
    const duration = activity.duration.split('-')[1].replace('min', '');
    return acc + parseInt(duration);
  }, 0);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
      <div className="bg-white w-full max-w-4xl max-h-[90vh] rounded-lg shadow-xl overflow-hidden">
        <div className="flex items-center justify-between p-4 border-b">
          <div>
            <h2 className="text-xl font-semibold">Activity Plan Report</h2>
            <p className="text-sm text-gray-500">
              Review and print your customized activity plan
            </p>
          </div>

          <div className="flex gap-2">
            <Button onClick={handlePrint}>
              <Printer className="h-4 w-4 mr-2" />
              Print
            </Button>
            <Button variant="outline" onClick={onClose}>
              Close
            </Button>
          </div>
        </div>

        <ScrollArea className="max-h-[calc(90vh-80px)] p-4">
          <div className="space-y-6" id="report-content">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="border rounded-lg p-4">
                <h3 className="font-semibold mb-2">Teacher Information</h3>
                <div className="space-y-1 text-sm">
                  <p><strong>Name:</strong> {teacherProfile.name}</p>
                  <p><strong>School:</strong> {teacherProfile.schoolName}</p>
                  <p><strong>Experience:</strong> {teacherProfile.yearsExperience} years</p>
                  <p><strong>Teaching Style:</strong> {teacherProfile.teachingStyle}</p>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h3 className="font-semibold mb-2">Class Information</h3>
                <div className="space-y-1 text-sm">
                  <p><strong>Class:</strong> {classProfile.className}</p>
                  <p><strong>Age Group:</strong> {classProfile.ageGroup} years</p>
                  <p><strong>Class Size:</strong> {classProfile.classSize} students</p>
                  <p><strong>Total Activities:</strong> {activities.length}</p>
                  <p><strong>Est. Duration:</strong> {totalDuration} minutes</p>
                </div>
              </div>
            </div>

            <div className="border rounded-lg p-4">
              <h3 className="font-semibold mb-2">Plan Summary</h3>
              <div className="flex flex-wrap gap-2">
                {Array.from(new Set(activities.map((a) => a.subject))).map((subject) => (
                  <Badge key={subject} className={getSubjectColor(subject)}>
                    {subject} ({activities.filter((a) => a.subject === subject).length})
                  </Badge>
                ))}
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="font-semibold">Planned Activities</h3>
              {activities.map((activity, index) => (
                <div key={activity.id} className="border rounded-lg p-4">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <h4 className="font-semibold">
                        {index + 1}. {activity.title}
                      </h4>
                      <div className="flex flex-wrap gap-2 mt-2">
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
                      </div>
                    </div>
                  </div>

                  <p className="text-sm text-gray-600 mb-3">{activity.description}</p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="font-semibold mb-1">Materials:</p>
                      <ul className="list-disc list-inside text-gray-600 space-y-1">
                        {activity.materials.map((material, i) => (
                          <li key={i}>{material}</li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <p className="font-semibold mb-1">Learning Goals:</p>
                      <ul className="list-disc list-inside text-gray-600 space-y-1">
                        {activity.learningGoals.map((goal, i) => (
                          <li key={i}>{goal}</li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  <div className="mt-3">
                    <p className="font-semibold mb-1 text-sm">Instructions:</p>
                    <ol className="list-decimal list-inside text-gray-600 space-y-1 text-sm">
                      {activity.instructions.map((instruction, i) => (
                        <li key={i}>{instruction}</li>
                      ))}
                    </ol>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </ScrollArea>
      </div>
    </div>
  );
}