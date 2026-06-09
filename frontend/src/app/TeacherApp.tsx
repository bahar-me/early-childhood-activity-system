import { useState, useEffect } from 'react';
import { Activity, Subject, Duration, GroupSize } from './types/activity';
import { TeacherProfile, ClassProfile } from './types/profile';
import { User } from './types/user';
import { createActivity, getActivities, CreateActivityPayload, updateActivity } from './api/activities';
import { ActivityEditModal } from './components/ActivityEditModal';
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
import { explainRecommendations, AIRecommendationExplanationResponse, AdaptActivityDraft } from './api/ai';
import { ActivityAdaptModal } from './components/ActivityAdaptModal';
import { getSchools } from './api/schools';
import { School } from './types/school';

type SetupStep = 'teacher' | 'class' | 'complete';

interface TeacherAppProps {
  user: User;
  onLogout: () => void;
}

export function TeacherApp({ user, onLogout }: TeacherAppProps) {
  const [setupStep, setSetupStep] = useState<SetupStep>('teacher');
  const [teacherProfile, setTeacherProfile] = useState<TeacherProfile | null>(null);
  const [classProfile, setClassProfile] = useState<ClassProfile | null>(null);
  const [schools, setSchools] = useState<School[]>([]);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [visibleCount, setVisibleCount] = useState(30);
  const [loadingActivities, setLoadingActivities] = useState(true);
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(null);
  const [favorites, setFavorites] = useState<string[]>([]);
  const [editingActivity, setEditingActivity] = useState<Activity | null>(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [adaptingActivity, setAdaptingActivity] = useState<Activity | null>(null);
  const [showAdaptModal, setShowAdaptModal] = useState(false);
  const [isCreatingActivity, setIsCreatingActivity] = useState(false);
  const [selectedForReport, setSelectedForReport] = useState<string[]>([]);
  const [selectedSubjects, setSelectedSubjects] = useState<Subject[]>([]);
  const [selectedDurations, setSelectedDurations] = useState<Duration[]>([]);
  const [selectedGroupSizes, setSelectedGroupSizes] = useState<GroupSize[]>([]);
  const [activeTab, setActiveTab] = useState<'all' | 'favorites' | 'selected'>('all');
  const [showReport, setShowReport] = useState(false);
  const [isSavingPlan, setIsSavingPlan] = useState(false);
  const [aiExplanation, setAIExplanation] = useState<AIRecommendationExplanationResponse | null>(null);
  const [isGeneratingAIExplanation, setIsGeneratingAIExplanation] = useState(false);
  const [hasMoreActivities, setHasMoreActivities] = useState(true);
  const [isLoadingMoreActivities, setIsLoadingMoreActivities] = useState(false);

  const normalizeSubject = (subject: string): Subject => {
  const map: Record<string, Subject> = {
    Math: 'Math',
    Matematik: 'Math',

    Language: 'Language',
    'Dil Gelişimi': 'Language',
    Dil: 'Language',

    Art: 'Art',
    Sanat: 'Art',

    Science: 'Science',
    Fen: 'Science',
    'Fen ve Doğa': 'Science',

    Music: 'Music',
    Müzik: 'Music',

    Physical: 'Physical',
    'Fiziksel Gelişim': 'Physical',

    'Social-Emotional': 'Social-Emotional',
    'Sosyal-Duygusal Gelişim': 'Social-Emotional',
  };

  return map[subject] || 'Art';
};

const normalizeDuration = (duration: string): Duration => {
  const map: Record<string, Duration> = {
    '5-15min': '5-15min',
    '5-15 dakika': '5-15min',

    '15-30min': '15-30min',
    '15-30 dakika': '15-30min',

    '30-45min': '30-45min',
    '30-45 dakika': '30-45min',

    '45-60min': '45-60min',
    '45-60 dakika': '45-60min',
  };

  return map[duration] || '15-30min';
};

const normalizeGroupSize = (groupSize: string): GroupSize => {
  const map: Record<string, GroupSize> = {
    Individual: 'Individual',
    Bireysel: 'Individual',

    'Small Group': 'Small Group',
    'Küçük Grup': 'Small Group',

    'Whole Class': 'Whole Class',
    'Tüm Sınıf': 'Whole Class',
  };

  return map[groupSize] || 'Small Group';
};

const handleLoadMoreActivities = async () => {
  try {
    setIsLoadingMoreActivities(true);

    const data = await getActivities(30, activities.length);

    setActivities((prev) => [...prev, ...data]);
    setHasMoreActivities(data.length === 30);
  } catch (error) {
    const message =
      error instanceof Error ? error.message : 'Daha fazla etkinlik yüklenemedi';

    toast.error(message);
  } finally {
    setIsLoadingMoreActivities(false);
  }
};

  // Load profiles and favorites from localStorage
  useEffect(() => {
  const savedFavorites = localStorage.getItem(`favorites-${user.id}`);

  const loadInitialData = async () => {
    let schoolList: School[] = [];

    try {
      schoolList = await getSchools();
      setSchools(schoolList);
    } catch (error) {
      console.error('Okul verileri yüklenemedi:', error);
    }

    try {
      const teacher = await getTeacherProfile();

      const resolvedSchoolName = 
        teacher.school_name ||
        schoolList.find((school) => school.id === teacher.school_id)?.name ||
        '';

      setTeacherProfile({
        name: teacher.name,
        schoolId: teacher.school_id ?? null,
        schoolName: resolvedSchoolName,
        yearsExperience: teacher.years_experience ?? '',
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
            morningActivities: classData.daily_schedule?.morning_activities ?? 45,
            afternoonActivities: classData.daily_schedule?.afternoon_activities ?? 30,
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

  loadInitialData();

  if (savedFavorites) {
    setFavorites(JSON.parse(savedFavorites));
  }
}, [user.id]);

useEffect(() => {
  const loadActivities = async () => {
    try {
      setLoadingActivities(true);

      const data = await getActivities(30, 0);

      setActivities(data);
      setHasMoreActivities(data.length === 30);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : 'Etkinlikler yüklenemedi';

      toast.error(message);
      setActivities([]);
      setHasMoreActivities(false);

      if (message === 'Oturum süresi doldu. Lütfen tekrar giriş yap.') {
        toast.error(message);
        onLogout();
      }
    } finally {
      setLoadingActivities(false);
    }
  };

  loadActivities();
}, [user.id, onLogout]);

useEffect(() => {
  setVisibleCount(30);
}, [selectedSubjects, selectedDurations, selectedGroupSizes, activeTab]);

useEffect(() => {
  localStorage.setItem(`favorites-${user.id}`, JSON.stringify(favorites));
}, [favorites, user.id]);

const handleOpenEditModal = (activity: Activity) => {
  setEditingActivity(activity);
  setShowEditModal(true);
};

const handleCreateEditedActivity = async (payload: Omit<Activity, 'id'>) => {
  if (!editingActivity) return;

  const enrichedPayload: CreateActivityPayload = {
    ...payload,
    sourceType: 'manual_edit',
    parentActivityId: editingActivity.id,
    createdByUserId: user.id,
  };

  try {
    setIsCreatingActivity(true);

    const newActivity = await createActivity(enrichedPayload);
    setActivities((prev) => [...prev, newActivity]);

    toast.success('Etkinlik başarıyla kaydedildi. \nYazdır veya PDF dışa aktar ile dosya oluşturabilirsin.');
    setShowEditModal(false);
    setEditingActivity(null);
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Etkinlik kaydedilemedi';

    toast.error(message);

    if (message === 'Oturum süresi doldu. Lütfen tekrar giriş yap.') {
      onLogout();
    }
  } finally {
    setIsCreatingActivity(false);
  }
};
  

  const handleUpdateEditedActivity = async (
    payload: Omit<CreateActivityPayload, 'sourceType' | 'parentActivityId' | 'createdByUserId'>,
  ) => {
    if (!editingActivity) return;

    try {
      setIsCreatingActivity(true);

      const updatedActivity = await updateActivity(editingActivity.id, payload);

      setActivities((prev) =>
        prev.map((item) => (item.id === updatedActivity.id ? updatedActivity : item)),
      );

      toast.success('Etkinlik başarıyla güncellendi.');
      setShowEditModal(false);
      setEditingActivity(null);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : 'Etkinlik güncellenemedi.';
      toast.error(message);
    } finally {
      setIsCreatingActivity(false);
    }
  };

  const handleOpenAdaptModal = (activity: Activity) => {
    setAdaptingActivity(activity);
    setShowAdaptModal(true);
  };

  const handleSaveAdaptedDraft = async (draft: AdaptActivityDraft) => {
    if (!adaptingActivity) return;

    const enrichedPayload: CreateActivityPayload = {
      ...draft,
      subject: normalizeSubject(draft.subject),
      duration: normalizeDuration(draft.duration),
      groupSize: normalizeGroupSize(draft.groupSize),
      sourceType: 'llm_generated',
      parentActivityId: adaptingActivity.id,
      createdByUserId: user.id,
    };

    try {
      setIsCreatingActivity(true);

      const newActivity = await createActivity(enrichedPayload);
      setActivities((prev) => [...prev, newActivity]);

      toast.success('YZ ile oluşturulan etkinlik başarıyla kaydedildi!');
      setShowAdaptModal(false);
      setAdaptingActivity(null);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Uyarlanan etkinlik kaydedilemedi';

      toast.error(message);

      if (message === 'Oturum süresi doldu. Lütfen tekrar giriş yap.') {
        onLogout();
      }
    } finally {
      setIsCreatingActivity(false);
    }
  };

  const handleTeacherProfileSubmit = async (profile: TeacherProfile) => {
  try {
    await saveTeacherProfile({
      name: profile.name,
      years_experience: 
        profile.yearsExperience === '' ? 0 : Number(profile.yearsExperience),
      specializations: profile.specializations,
      teaching_style: profile.teachingStyle,
      school_id: profile.schoolId,
    });

    setTeacherProfile(profile);
    setSetupStep('class');
    toast.success('Öğretmen profili kaydedildi!');
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Öğretmen profilini kaydetme başarısız oldu';
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
      daily_schedule: {
        morning_activities: profile.dailySchedule.morningActivities,
        afternoon_activities: profile.dailySchedule.afternoonActivities,
      },
    });

    setClassProfile(profile);
    setSetupStep('complete');
    toast.success('Sınıf profili kaydedildi! Hoş geldin!');
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Sınıf profilini kaydetme başarısız oldu';
    toast.error(message);
  }
};

  const handleEditProfiles = () => {
    setSetupStep('teacher');
  };

  const toggleFavorite = (id: string) => {
    setFavorites((prev) => {
      if (prev.includes(id)) {
        toast.success('Favorilerden kaldırıldı');
        return prev.filter((fav) => fav !== id);
      } 
      
      toast.success('Favorilere eklendi');
      return [...prev, id];
    });
  };

  const toggleSelectedForReport = (id: string) => {
    setSelectedForReport((prev) => {
      if (prev.includes(id)) {
        toast.success('Rapordan kaldırıldı');
        return prev.filter((item) => item !== id);
      } 
      
      toast.success('Rapora eklendi');
      return [...prev, id];
    });
  };

  const handleSubjectChange = (subject: Subject) => {
    setSelectedSubjects((prev) =>
      prev.includes(subject)
        ? prev.filter((s) => s !== subject)
        : [...prev, subject],
    );
  };

  const handleDurationChange = (duration: Duration) => {
    setSelectedDurations((prev) =>
      prev.includes(duration)
        ? prev.filter((d) => d !== duration)
        : [...prev, duration],
    );
  };

  const handleGroupSizeChange = (groupSize: GroupSize) => {
    setSelectedGroupSizes((prev) =>
      prev.includes(groupSize)
        ? prev.filter((g) => g !== groupSize)
        : [...prev, groupSize],
    );
  };

  const clearFilters = () => {
    setSelectedSubjects([]);
    setSelectedDurations([]);
    setSelectedGroupSizes([]);
  };

  const normalizeTeachingStyle = (style: string) => {
    const map: Record<string, string> = {
      structured: 'structured',
      Structured: 'structured',

      balanced: 'balanced',
      Balanced: 'balanced',

      exploratory: 'exploratory',
      Exploratory: 'exploratory',

      'Play-based': 'play_based',
      'play-based': 'play_based',

      'Child-led': 'child_led',
      'child-led': 'child_led',

      Interactive: 'interactive',
      interactive: 'interactive',

      Creative: 'creative',
      creative: 'creative',
    };

    return map[style] || style;
  };

  const getTeachingStyleScore = (style: string, activity: Activity) => {
    const normalized = normalizeTeachingStyle(style);
    let score = 0;
    const reasons: string[] = [];

    if (
      normalized === 'structured' &&
      (
        activity.subject === 'Math' || 
        activity.subject === 'Language'
      )
    ) {
      score += 2;
      reasons.push('Yapılandırılmış öğretim stiline uygun');
    }

    if (
      normalized === 'balanced' &&
      (
        activity.subject === 'Art' ||
        activity.subject === 'Social-Emotional' ||
        activity.subject === 'Science'
      )
    ) {
      score += 2;
      reasons.push('Dengeli öğretim stiline uygun');
    }

    if (
      normalized === 'exploratory' &&
      (
        activity.groupSize === 'Individual' ||
        activity.groupSize === 'Small Group' ||
        activity.subject === 'Science'
      )
    ) {
      score += 2;
      reasons.push('Keşfetmeye dayalı öğretim stiline uygun');
    }

    if (
      normalized === 'play_based' &&
      (
        activity.subject === 'Art' ||
        activity.subject === 'Music' ||
        activity.subject === 'Physical' ||
        activity.subject === 'Social-Emotional'
      )
    ) {
      score += 2;
      reasons.push('Oyun temelli öğretim stiline uygun');
    }

    if (
      normalized === 'child_led' &&
      (
        activity.groupSize === 'Individual' ||
        activity.groupSize === 'Small Group'
      )
    ) {
      score += 2;
      reasons.push('Çocuk merkezli öğretim stiline uygun');
    }

    if (
      normalized === 'interactive' &&
      (
        activity.groupSize === 'Whole Class' ||
        activity.groupSize === 'Small Group' ||
        activity.subject === 'Music' ||
        activity.subject === 'Language'
      )
    ) {
      score += 2;
      reasons.push('Etkileşimli öğretim stiline uygun');
    }

    if (
      normalized === 'creative' &&
      (
        activity.subject === 'Art' ||
        activity.subject === 'Music' ||
        activity.subject === 'Language'
      )
    ) {
      score += 2;
      reasons.push('Yaratıcı öğretim stiline uygun');
    }

    return { score, reasons };
  };

  const getSmartRecommendations = (): Activity[] => {
    if (!classProfile || !teacherProfile) return activities;

    const scoredActivities = activities.map((activity) => {
      let score = 0;
      const reasons: string[] = [];

      // 1. Learning focus match
      if (
        classProfile.learningFocus.includes('Okuryazarlık Gelişimi') &&
        activity.subject === 'Language'
      ) {
        score += 4;
        reasons.push('Okuryazarlık gelişimi odağıyla uyumlu');
      }

      if (
        classProfile.learningFocus.includes('Matematik Temelleri') &&
        activity.subject === 'Math'
      ) {
        score += 4;
        reasons.push('Matematik temelleri odağıyla uyumlu');
      }

      if (
        classProfile.learningFocus.includes('Yaratıcı İfade') &&
        activity.subject === 'Art'
      ) {
        score += 4;
        reasons.push('Sanatsal ifade odağıyla uyumlu');
      }

      if (
        classProfile.learningFocus.includes('Bilimsel Keşif') &&
        activity.subject === 'Science'
      ) {
        score += 4;
        reasons.push('Bilimsel keşif odağıyla uyumlu');
      }

      if (
        classProfile.learningFocus.includes('Fiziksel Gelişim') &&
        activity.subject === 'Physical'
      ) {
        score += 4;
        reasons.push('Fiziksel gelişim odağıyla uyumlu');
      }

      if (
        classProfile.learningFocus.includes('Sosyal Beceriler') &&
        activity.subject === 'Social-Emotional'
      ) {
        score += 4;
        reasons.push('Sosyal beceriler odağıyla uyumlu');
      }

      // 2. Age group suitability
      const age = Number(classProfile.ageGroup);

      if (age <= 4 && activity.duration === '5-15min') {
        score += 2;
        reasons.push('Küçük yaş grubu için uygun süreye sahip');
      }

      if (age >= 5 && (activity.duration === '15-30min' || activity.duration === '30-45min' || activity.duration === '45-60min')) {
        score += 2;
        reasons.push('Daha büyük okul öncesi yaş grubu için uygun süreye sahip');
      }

      // 3. Class size suitability
      if (classProfile.classSize <= 15) {
        if (activity.groupSize === 'Whole Class' || activity.groupSize === 'Small Group') {
          score += 2;
          reasons.push('Küçük sınıf mevcudu için uygun');
        }
      } else if (classProfile.classSize >= 25) {
        if (activity.groupSize === 'Individual' || activity.groupSize === 'Small Group') {
          score += 2;
          reasons.push('Daha kalabalık sınıf mevcudu için uygun');
        }
      } else if (activity.groupSize === 'Small Group') {
          score += 1;
          reasons.push('Orta büyüklükteki sınıflar için esnek bir yapı sunuyor');
        }
      
      // 4. Available resources match
      const materialsText = activity.materials.join(' ').toLowerCase();

      if (
        classProfile.availableResources.includes('Tablets/Technology') &&
        (materialsText.includes('tablet') || materialsText.includes('computer') || materialsText.includes('digital'))
      ) {
        score += 2;
        reasons.push('Mevcut teknoloji kaynaklarıyla uyumlu');
      }

      if (
        classProfile.availableResources.includes('Art Supplies') &&
        (materialsText.includes('paint') ||
          materialsText.includes('marker') ||
          materialsText.includes('crayon') ||
          materialsText.includes('paper') ||
          materialsText.includes('art'))
      ) {
        score += 2;
        reasons.push('Mevcut sanat materyalleriyle uyumlu');
      }

      if (
        classProfile.availableResources.includes('Musical Instruments') &&
        (materialsText.includes('music') || materialsText.includes('instrument') || materialsText.includes('rhythm'))
      ) {
        score += 2;
        reasons.push('Mevcut müzik materyalleriyle uyumlu');
      }

      if (
        classProfile.availableResources.includes('Outdoor Space') &&
        (activity.subject === 'Physical' || materialsText.includes('outdoor'))
      ) {
        score += 2;
        reasons.push('Açık alan kullanımı için uygun');
      }

      // 5. Teaching style alignment
      const styleResult = getTeachingStyleScore(teacherProfile.teachingStyle, activity);
      score += styleResult.score;
      reasons.push(...styleResult.reasons);

      // 6. Special needs support
      if (
        classProfile.specialNeeds.length > 0 &&
        (activity.groupSize === 'Individual' || activity.groupSize === 'Small Group')
      ) {
        score += 2;
        reasons.push('Farklılaştırılmış destek için daha uygun');
      }

      return {
        activity,
        score,
        reasons,
      };
    });

    return scoredActivities
      .sort((a, b) => b.score - a.score)
      .map((item) => item.activity);
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
    const filtered = getFilteredActivities();

    if (filtered.length === 0) {
      toast.error('Uygun etkinlik bulunamadı. Filtrelerini değiştirmeyi deneyebilirsin!');
      return;
    }

    const topRecommendations = filtered.slice(0, 3);
    const randomActivity =
      topRecommendations[Math.floor(Math.random() * topRecommendations.length)];

    setSelectedActivity(randomActivity);

    toast.success('YZ senin için kişiselleştirilmiş bir etkinlik önerdi!', {
      description: randomActivity.title,
    });
  };

  const handleGenerateAIExplanation = async () => {
    try {
      setIsGeneratingAIExplanation(true);

      const selectedActivities = activities.filter((activity) =>
        selectedForReport.includes(activity.id)
      );

      if (selectedActivities.length === 0) {
        toast.error('Lütfen önce en az bir etkinlik seç.');
        return;
      }

      const data = await explainRecommendations({
        teacher_profile: {
          name: teacherProfile?.name,
          years_experience: teacherProfile?.yearsExperience,
          specializations: teacherProfile?.specializations,
          teaching_style: teacherProfile?.teachingStyle,
        },
        class_profile: {
          class_name: classProfile?.className,
          age_group: classProfile?.ageGroup,
          class_size: classProfile?.classSize,
          learning_focus: classProfile?.learningFocus,
          available_resources: classProfile?.availableResources,
          special_needs: classProfile?.specialNeeds,
          daily_schedule: {
            morning_activities: classProfile?.dailySchedule.morningActivities,
            afternoon_activities: classProfile?.dailySchedule.afternoonActivities,
          }
        },
        activities: selectedActivities,
        recommendation_reasons: [],
      });

      setAIExplanation(data);
      toast.success('YZ açıklaması başarıyla oluşturuldu.');
    } catch (error) {
      console.error('YZ açıklama hatası:', error);

      const message =
        error instanceof Error ? error.message : 'YZ açıklaması oluşturulamadı';

      toast.error(message);

      if (message === 'Oturum süresi doldu. Lütfen tekrar giriş yap.') {
        onLogout();
      }
    } finally {
      setIsGeneratingAIExplanation(false);
    }
  };

  const handleGenerateReport = async () => {
    if (selectedForReport.length === 0) {
      toast.error('Lütfen rapor için en az bir etkinlik seç.');
      return;
    }

    if (!classProfile) {
      toast.error('Sınıf profili eksik. Rapor oluşturmak için sınıf profilinizi tamamla.');
      return;
    }

    try {
      setIsSavingPlan(true);

      await createActivityPlan({
        activity_ids: selectedForReport,
        notes: 'Öğretmen etkinlik akışından oluşturuldu',
      });

      setShowReport(true);
      toast.success('Etkinlik planı başarıyla kaydedildi');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Etkinlik planı kaydedilemedi';
      toast.error(message);
    } finally {
      setIsSavingPlan(false);
    }
  };

  const filteredActivities = getFilteredActivities();
  const visibleActivities = filteredActivities.slice(0, visibleCount);
  const reportActivities = activities.filter(a => selectedForReport.includes(a.id));

  // Show setup steps if not complete
  if (setupStep === 'teacher') {
    return (
      <div className="min-h-screen overflow-y-auto bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 py-12 px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-purple-600 mb-2">
            Hoş geldin!
          </h1>
          <p className="text-gray-600">
            Profilini oluşturarak başlayalım
          </p>
        </div>
        <TeacherProfileForm
          onSubmit={handleTeacherProfileSubmit}
          initialData={teacherProfile || undefined}
          schools={schools.map((school) => ({
            id: Number(school.id),
            name: school.name,
          }))}
        />
      </div>
    );
  }

  if (setupStep === 'class') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 py-12 px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-purple-600 mb-2">
            Hoş geldin, {teacherProfile?.name}!
          </h1>
          <p className="text-gray-600">
            Şimdi sınıf profilini oluşturalım
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

  if (loadingActivities) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
        <div className="text-center">
          <h2 className="text-2xl font-semibold text-purple-600">Etkinlikler yükleniyor...</h2>
          <p className="text-gray-600 mt-2">Lütfen bekleyin</p>
        </div>
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
                Tekrar hoş geldin, {teacherProfile?.name} • {classProfile?.className}
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <Button
                onClick={handleAISuggest}
                size="lg"
                className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
              >
                <WandSparkles className="h-5 w-5 mr-2" />
                YZ Önerisi Al
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={handleGenerateAIExplanation}
                disabled={isGeneratingAIExplanation || selectedForReport.length === 0}
              >
                {isGeneratingAIExplanation ? 'YZ Açıklaması Oluşturuluyor...' : 'YZ Açıklaması Oluştur'}
              </Button>
              <Button
                onClick={handleGenerateReport}
                size="lg"
                variant="outline"
                disabled={selectedForReport.length === 0 || isSavingPlan}
              >
                <FileText className="h-5 w-5 mr-2" />
                {isSavingPlan ? 'Rapor Oluşturuluyor...' : `Rapor (${selectedForReport.length})`}
              </Button>
              <Button
                onClick={handleEditProfiles}
                size="lg"
                variant="outline"
              >
                <Settings className="h-5 w-5 mr-2" />
                Profili Düzenle
              </Button>
              <Button
                onClick={onLogout}
                size="lg"
                variant="outline"
              >
                <LogOut className="h-5 w-5 mr-2" />
                Çıkış Yap
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
                  Tüm Etkinlikler ({activities.length})
                </TabsTrigger>
                <TabsTrigger value="favorites" className="flex items-center gap-2">
                  <Heart className="h-4 w-4" />
                  Favoriler ({favorites.length})
                </TabsTrigger>
                <TabsTrigger value="selected" className="flex items-center gap-2">
                  <CheckSquare className="h-4 w-4" />
                  Rapora Seçilenler ({selectedForReport.length})
                </TabsTrigger>
              </TabsList>

              <TabsContent value="all" className="mt-0">
                <p className="text-sm text-gray-500 mb-4">
                  Gösterilen etkinlikler: {visibleActivities.length}
                </p>

                {filteredActivities.length === 0 ? (
                  <div className="text-center py-12 bg-white rounded-lg border-2 border-dashed">
                    <p className="text-gray-500">
                      Seçtiğin filtrelere uygun etkinlik bulunamadı. Filtreleri değiştirmeyi deneyebilirsin.
                    </p>
                  </div>
                ) : (
                  <>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {visibleActivities.map((activity) => (
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
                            {selectedForReport.includes(activity.id) ? 'Seçildi' : 'Seç'}
                          </Button>
                        </div>
                      ))}
                    </div>

                    {hasMoreActivities && (
                      <div className="flex justify-center mt-6">
                        <Button
                          variant="outline"
                          onClick={handleLoadMoreActivities}
                          disabled={isLoadingMoreActivities}
                        >
                          {isLoadingMoreActivities ? 'Yükleniyor...' : 'Daha fazla göster'}
                        </Button>
                      </div>
                    )}
                  </>
                )}  
              </TabsContent>

              <TabsContent value="favorites" className="mt-0">
                {filteredActivities.length === 0 ? (
                  <div className="text-center py-12 bg-white rounded-lg border-2 border-dashed">
                    <Heart className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                    <p className="text-gray-500">
                      {favorites.length === 0
                        ? 'Henüz favori etkinlik yok. Etkinliklerdeki kalp simgesine tıklayarak favorilere ekleyebilirsin!'
                        : 'Filtrelerine uygun favori etkinlik bulunamadı.'}
                    </p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {visibleActivities.map((activity) => (
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
                          {selectedForReport.includes(activity.id) ? 'Seçildi' : 'Seç'}
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
                        ? 'Henüz rapor için etkinlik seçilmedi. Eklemek için etkinliklerdeki "Seç" butonunu kullanabilirsin!'
                        : 'Filtrelerine uygun seçili etkinlik bulunamadı.'}
                    </p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {visibleActivities.map((activity) => (
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
                          {selectedForReport.includes(activity.id) ? 'Seçildi' : 'Seç'}
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
        onEdit={(activity) => {
          setSelectedActivity(null);
          handleOpenEditModal(activity);
        }}
        onAdapt={(activity) => {
          setSelectedActivity(null);
          handleOpenAdaptModal(activity);
        }}
      />

      {/* Edit/Create Activity Modal */}
      <ActivityEditModal
        open={showEditModal}
        activity={editingActivity}
        onClose={() => {
          setShowEditModal(false);
          setEditingActivity(null);
        }}
        onSaveAsNew={handleCreateEditedActivity}
        onUpdate={handleUpdateEditedActivity}
        isSaving={isCreatingActivity}
      />

      <ActivityAdaptModal
        open={showAdaptModal}
        activity={adaptingActivity}
        teacherProfile={teacherProfile}
        classProfile={classProfile}
        onClose={() => {
          setShowAdaptModal(false);
          setAdaptingActivity(null);
        }}
        onSaveDraft={handleSaveAdaptedDraft}
        isSaving={isCreatingActivity}
      />
      
      {/* Report Modal */}
      {teacherProfile && classProfile && (
        <ActivityReport
          activities={reportActivities}
          teacherProfile={teacherProfile}
          classProfile={classProfile}
          open={showReport}
          onClose={() => setShowReport(false)}
          aiExplanation={aiExplanation}
        />
      )}
    </div>
  );
}
