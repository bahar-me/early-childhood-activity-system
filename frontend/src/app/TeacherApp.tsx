import { useState, useEffect } from 'react';
import { Activity, Subject, Duration, GroupSize } from './types/activity';
import { TeacherProfile, ClassProfile } from './types/profile';
import { User } from './types/user';
import { activities } from './data/activities';
import { ActivityCard } from './components/ActivityCard';
import { ActivityDetail } from './components/ActivityDetail';
import { saveTeacherProfile, saveClassProfile, getTeacherProfile, getClassProfile } from './api/profile';
import { createActivityPlan } from './api/activityPlans';
import { FilterPanel } from './components/FilterPanel';
import { TeacherProfileForm } from './components/TeacherProfileForm';
import { ClassProfileForm } from './components/ClassProfileForm';
import { ActivityReport } from './components/ActivityReport';
import { Button } from './components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { WandSparkles, Heart, FileText, Settings, CheckSquare, LogOut } from 'lucide-react';
import { toast } from 'sonner';

type SetupStep = 'teacher' | 'class' | 'complete';

interface TeacherAppProps {
  user: User;
  onLogout: () => void;
}

export function TeacherApp({ user, onLogout }: TeacherAppProps) {
  const [setupStep, setSetupStep] = useState<SetupStep>('teacher');
  const [teacherProfile, setTeacherProfile] = useState<TeacherProfile | null>(null);
  const [classProfile, setClassProfile] = useState<ClassProfile | null>(null);
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(null);
  const [favorites, setFavorites] = useState<string[]>([]);
  const [selectedForReport, setSelectedForReport] = useState<string[]>([]);
  const [selectedSubjects, setSelectedSubjects] = useState<Subject[]>([]);
  const [selectedDurations, setSelectedDurations] = useState<Duration[]>([]);
  const [selectedGroupSizes, setSelectedGroupSizes] = useState<GroupSize[]>([]);
  const [activeTab, setActiveTab] = useState<'all' | 'favorites' | 'selected'>('all');
  const [showReport, setShowReport] = useState(false);

  // Load profiles and favorites from localStorage
  useEffect(() => {
  const savedFavorites = localStorage.getItem(`favorites-${user.id}`);

  const loadProfiles = async () => {
    try {
      const teacher = await getTeacherProfile();
      setTeacherProfile({
        name: teacher.name,
        schoolName: '',
        yearsExperience: String(teacher.years_experience),
        specializations: teacher.specializations || [],
        teachingStyle: teacher.teaching_style || '',
      });

      try {
        const classData = await getClassProfile();
        setClassProfile({
          className: classData.class_name,
          ageGroup: classData.age_group,
          classSize: classData.class_size,
          learningFocus: classData.learning_focus || [],
          availableResources: classData.available_resources || [],
          specialNeeds: classData.special_needs || [],
          dailySchedule: {
            morningActivities: 30,
            afternoonActivities: 30,
          },
        });
        setSetupStep('complete');
      } catch {
        setSetupStep('class');
      }
    } catch {
      setSetupStep('teacher');
    }
  };

  loadProfiles();

  if (savedFavorites) {
    setFavorites(JSON.parse(savedFavorites));
  }
}, [user.id]);

  // Save favorites to localStorage
  useEffect(() => {
    localStorage.setItem(`favorites-${user.id}`, JSON.stringify(favorites));
  }, [favorites, user.id]);

  const handleTeacherProfileSubmit = async (profile: TeacherProfile) => {
  try {
    await saveTeacherProfile({
      name: profile.name,
      years_experience: Number(profile.yearsExperience),
      specializations: profile.specializations,
      teaching_style: profile.teachingStyle,
    });

    setTeacherProfile(profile);
    setSetupStep('class');
    toast.success('Teacher profile saved!');
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Failed to save teacher profile';
    toast.error(message);
  }
};

  const handleClassProfileSubmit = async (profile: ClassProfile) => {
  try {
    await saveClassProfile({
      class_name: profile.className,
      age_group: profile.ageGroup,
      class_size: profile.classSize,
      learning_focus: profile.learningFocus,
      available_resources: profile.availableResources,
      special_needs: profile.specialNeeds,
    });

    setClassProfile(profile);
    setSetupStep('complete');
    toast.success('Class profile saved! Welcome to KinderActivity AI!');
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Failed to save class profile';
    toast.error(message);
  }
};

  const handleEditProfiles = () => {
    setSetupStep('teacher');
  };

  const toggleFavorite = (id: string) => {
    setFavorites((prev) => {
      if (prev.includes(id)) {
        toast.success('Removed from favorites');
        return prev.filter((fav) => fav !== id);
      } else {
        toast.success('Added to favorites');
        return [...prev, id];
      }
    });
  };

  const toggleSelectedForReport = (id: string) => {
    setSelectedForReport((prev) => {
      if (prev.includes(id)) {
        toast.success('Removed from report');
        return prev.filter((item) => item !== id);
      } else {
        toast.success('Added to report');
        return [...prev, id];
      }
    });
  };

  const handleSubjectChange = (subject: Subject) => {
    setSelectedSubjects((prev) =>
      prev.includes(subject)
        ? prev.filter((s) => s !== subject)
        : [...prev, subject]
    );
  };

  const handleDurationChange = (duration: Duration) => {
    setSelectedDurations((prev) =>
      prev.includes(duration)
        ? prev.filter((d) => d !== duration)
        : [...prev, duration]
    );
  };

  const handleGroupSizeChange = (groupSize: GroupSize) => {
    setSelectedGroupSizes((prev) =>
      prev.includes(groupSize)
        ? prev.filter((g) => g !== groupSize)
        : [...prev, groupSize]
    );
  };

  const clearFilters = () => {
    setSelectedSubjects([]);
    setSelectedDurations([]);
    setSelectedGroupSizes([]);
  };

  const getSmartRecommendations = (): Activity[] => {
    if (!classProfile) return activities;

    let scored = activities.map(activity => {
      let score = 0;

      // Score based on learning focus
      if (classProfile.learningFocus.includes('Literacy Development') && activity.subject === 'Language') {
        score += 3;
      }
      if (classProfile.learningFocus.includes('Math Foundations') && activity.subject === 'Math') {
        score += 3;
      }
      if (classProfile.learningFocus.includes('Creative Expression') && activity.subject === 'Art') {
        score += 3;
      }
      if (classProfile.learningFocus.includes('Science Exploration') && activity.subject === 'Science') {
        score += 3;
      }
      if (classProfile.learningFocus.includes('Physical Development') && activity.subject === 'Physical') {
        score += 3;
      }
      if (classProfile.learningFocus.includes('Social Skills') && activity.subject === 'Social-Emotional') {
        score += 3;
      }

      // Score based on class size and group size
      if (classProfile.classSize <= 15) {
        if (activity.groupSize === 'Whole Class' || activity.groupSize === 'Small Group') score += 2;
      } else if (classProfile.classSize >= 25) {
        if (activity.groupSize === 'Individual') score += 2;
      }

      // Score based on available resources
      const activityNeedsTech = activity.materials.some(m => 
        m.toLowerCase().includes('tablet') || m.toLowerCase().includes('computer')
      );
      if (activityNeedsTech && classProfile.availableResources.includes('Tablets/Technology')) {
        score += 2;
      }

      const activityNeedsArt = activity.materials.some(m => 
        m.toLowerCase().includes('paint') || m.toLowerCase().includes('art') || 
        m.toLowerCase().includes('marker') || m.toLowerCase().includes('crayon')
      );
      if (activityNeedsArt && classProfile.availableResources.includes('Art Supplies')) {
        score += 2;
      }

      const activityNeedsMusic = activity.materials.some(m => 
        m.toLowerCase().includes('instrument') || m.toLowerCase().includes('music')
      );
      if (activityNeedsMusic && classProfile.availableResources.includes('Musical Instruments')) {
        score += 2;
      }

      return { activity, score };
    });

    return scored.sort((a, b) => b.score - a.score).map(item => item.activity);
  };

  const getFilteredActivities = () => {
    let filtered = getSmartRecommendations();

    if (selectedSubjects.length > 0) {
      filtered = filtered.filter((activity) =>
        selectedSubjects.includes(activity.subject)
      );
    }

    if (selectedDurations.length > 0) {
      filtered = filtered.filter((activity) =>
        selectedDurations.includes(activity.duration)
      );
    }

    if (selectedGroupSizes.length > 0) {
      filtered = filtered.filter((activity) =>
        selectedGroupSizes.includes(activity.groupSize)
      );
    }

    if (activeTab === 'favorites') {
      filtered = filtered.filter((activity) => favorites.includes(activity.id));
    } else if (activeTab === 'selected') {
      filtered = filtered.filter((activity) => selectedForReport.includes(activity.id));
    }

    return filtered;
  };

  const handleAISuggest = () => {
    const filtered = getSmartRecommendations();
    if (filtered.length === 0) {
      toast.error('No activities available. Try adjusting your filters!');
      return;
    }

    // Get top 3 recommended activities
    const topRecommendations = filtered.slice(0, 3);
    const randomActivity = topRecommendations[Math.floor(Math.random() * topRecommendations.length)];
    setSelectedActivity(randomActivity);
    toast.success('AI suggested a personalized activity for you!', {
      description: randomActivity.title,
    });
  };

  const handleGenerateReport = async () => {
  if (selectedForReport.length === 0) {
    toast.error('Please select at least one activity for the report');
    return;
  }

  try {
    await createActivityPlan({
      activity_ids: selectedForReport,
      notes: 'Generated from teacher activity flow',
    });

    setShowReport(true);
    toast.success('Activity plan saved successfully');
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Failed to save activity plan';
    toast.error(message);
  }
};

  const filteredActivities = getFilteredActivities();
  console.log('Total Activities:', activities.length);
  console.log('Filtered Activities total:', filteredActivities.length);
  const reportActivities = activities.filter(a => selectedForReport.includes(a.id));

  // Show setup steps if not complete
  if (setupStep === 'teacher') {
    return (
      <div className="min-h-screen overflow-y-auto bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 py-12 px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-purple-600 mb-2">
            Welcome to KinderActivity AI
          </h1>
          <p className="text-gray-600">
            Let's get started by setting up your profile
          </p>
        </div>
        <TeacherProfileForm
          onSubmit={handleTeacherProfileSubmit}
          initialData={teacherProfile || undefined}
        />
      </div>
    );
  }

  if (setupStep === 'class') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 py-12 px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-purple-600 mb-2">
            Welcome, {teacherProfile?.name}!
          </h1>
          <p className="text-gray-600">
            Now let's set up your class profile
          </p>
        </div>
        <ClassProfileForm
          onSubmit={handleClassProfileSubmit}
          onBack={() => setSetupStep('teacher')}
          initialData={classProfile || undefined}
        />
      </div>
    );
  }

  // Main app
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 className="text-3xl text-purple-600">
                KinderActivity AI
              </h1>
              <p className="text-gray-600 mt-1">
                Welcome back, {teacherProfile?.name} • {classProfile?.className}
              </p>
              <p className="text-red-500 font-bold">
                Debug - Selected for report: {selectedForReport.length}
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <Button
                onClick={handleAISuggest}
                size="lg"
                className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
              >
                <WandSparkles className="h-5 w-5 mr-2" />
                AI Suggest
              </Button>
              <Button
                onClick={handleGenerateReport}
                size="lg"
                variant="outline"
                disabled={selectedForReport.length === 0}
              >
                <FileText className="h-5 w-5 mr-2" />
                Report ({selectedForReport.length})
              </Button>
              <Button
                onClick={handleEditProfiles}
                size="lg"
                variant="outline"
              >
                <Settings className="h-5 w-5 mr-2" />
                Edit Profile
              </Button>
              <Button
                onClick={onLogout}
                size="lg"
                variant="outline"
              >
                <LogOut className="h-5 w-5 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <FilterPanel
              selectedSubjects={selectedSubjects}
              selectedDurations={selectedDurations}
              selectedGroupSizes={selectedGroupSizes}
              onSubjectChange={handleSubjectChange}
              onDurationChange={handleDurationChange}
              onGroupSizeChange={handleGroupSizeChange}
              onClearFilters={clearFilters}
            />
          </div>

          {/* Activities Grid */}
          <div className="lg:col-span-3">
            <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as 'all' | 'favorites' | 'selected')}>
              <TabsList className="mb-6">
                <TabsTrigger value="all">
                  All Activities ({activities.length})
                </TabsTrigger>
                <TabsTrigger value="favorites" className="flex items-center gap-2">
                  <Heart className="h-4 w-4" />
                  Favorites ({favorites.length})
                </TabsTrigger>
                <TabsTrigger value="selected" className="flex items-center gap-2">
                  <CheckSquare className="h-4 w-4" />
                  For Report ({selectedForReport.length})
                </TabsTrigger>
              </TabsList>

              <TabsContent value="all" className="mt-0">
                {filteredActivities.length === 0 ? (
                  <div className="text-center py-12 bg-white rounded-lg border-2 border-dashed">
                    <p className="text-gray-500">
                      No activities match your filters. Try adjusting them!
                    </p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {filteredActivities.map((activity) => (
                      <div key={activity.id} className="relative">
                        <ActivityCard
                          activity={activity}
                          isFavorite={favorites.includes(activity.id)}
                          onToggleFavorite={toggleFavorite}
                          onClick={setSelectedActivity}
                        />
                        <Button
                          variant={selectedForReport.includes(activity.id) ? "default" : "outline"}
                          size="sm"
                          className="absolute bottom-4 right-4"
                          onClick={(e) => {
                            e.stopPropagation();
                            toggleSelectedForReport(activity.id);
                          }}
                        >
                          <CheckSquare className="h-4 w-4 mr-1" />
                          {selectedForReport.includes(activity.id) ? 'Selected' : 'Select'}
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </TabsContent>

              <TabsContent value="favorites" className="mt-0">
                {filteredActivities.length === 0 ? (
                  <div className="text-center py-12 bg-white rounded-lg border-2 border-dashed">
                    <Heart className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                    <p className="text-gray-500">
                      {favorites.length === 0
                        ? 'No favorite activities yet. Click the heart icon on activities to save them!'
                        : 'No favorite activities match your filters.'}
                    </p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {filteredActivities.map((activity) => (
                      <div key={activity.id} className="relative">
                        <ActivityCard
                          activity={activity}
                          isFavorite={favorites.includes(activity.id)}
                          onToggleFavorite={toggleFavorite}
                          onClick={setSelectedActivity}
                        />
                        <Button
                          variant={selectedForReport.includes(activity.id) ? "default" : "outline"}
                          size="sm"
                          className="absolute bottom-4 right-4"
                          onClick={(e) => {
                            e.stopPropagation();
                            toggleSelectedForReport(activity.id);
                          }}
                        >
                          <CheckSquare className="h-4 w-4 mr-1" />
                          {selectedForReport.includes(activity.id) ? 'Selected' : 'Select'}
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </TabsContent>

              <TabsContent value="selected" className="mt-0">
                {filteredActivities.length === 0 ? (
                  <div className="text-center py-12 bg-white rounded-lg border-2 border-dashed">
                    <CheckSquare className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                    <p className="text-gray-500">
                      {selectedForReport.length === 0
                        ? 'No activities selected for report. Click "Select" on activities to add them!'
                        : 'No selected activities match your filters.'}
                    </p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {filteredActivities.map((activity) => (
                      <div key={activity.id} className="relative">
                        <ActivityCard
                          activity={activity}
                          isFavorite={favorites.includes(activity.id)}
                          onToggleFavorite={toggleFavorite}
                          onClick={setSelectedActivity}
                        />
                        <Button
                          variant={selectedForReport.includes(activity.id) ? "default" : "outline"}
                          size="sm"
                          className="absolute bottom-4 right-4"
                          onClick={(e) => {
                            e.stopPropagation();
                            toggleSelectedForReport(activity.id);
                          }}
                        >
                          <CheckSquare className="h-4 w-4 mr-1" />
                          {selectedForReport.includes(activity.id) ? 'Selected' : 'Select'}
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </main>

      {/* Activity Detail Modal */}
      <ActivityDetail
        activity={selectedActivity}
        open={selectedActivity !== null}
        onClose={() => setSelectedActivity(null)}
      />

      {/* Report Modal */}
      {teacherProfile && classProfile && (
        <ActivityReport
          activities={reportActivities}
          teacherProfile={teacherProfile}
          classProfile={classProfile}
          open={showReport}
          onClose={() => setShowReport(false)}
        />
      )}
    </div>
  );
}
