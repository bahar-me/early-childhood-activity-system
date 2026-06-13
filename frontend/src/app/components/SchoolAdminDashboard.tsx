import { useCallback, useEffect, useMemo, useState } from 'react';
import { getSchoolAdminOverview } from '../api/schoolAdmin';
import { User } from '../types/user';
import {
  TeacherOverview,
  ClassOverview,
  PlanOverview,
  SchoolOverviewResponse,
} from '../types/schoolAdmin';
import { activities } from '../data/activities';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { ActivityReport } from './ActivityReport';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from './ui/table';
import { Users, GraduationCap, FileText, Eye, LogOut, RefreshCw } from 'lucide-react';
import { toast } from 'sonner';

interface SchoolAdminDashboardProps {
  user: User;
  onLogout: () => void;
}

export function SchoolAdminDashboard({ user, onLogout }: SchoolAdminDashboardProps) {
  const [overview, setOverview] = useState<SchoolOverviewResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  const [selectedPlan, setSelectedPlan] = useState<PlanOverview | null>(null);
  const [showReport, setShowReport] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  const displayName = user.name || user.email;

  const loadOverview = useCallback (async () => {
    try {
      setLoading(true);
      setErrorMessage('');

      const data = await getSchoolAdminOverview();

      setOverview(data);
    } catch (error) {
      console.error('Okul yöneticisi genel bakış yüklenemedi:', error);
      const message =
        error instanceof Error ? error.message : 'Okula genel bakış yüklenemedi.';
      if (message === 'Oturum süresi doldu. Lütfen tekrar giriş yapın.' || message === 'Yetkiniz yok') {
        toast.error('Oturum süresi doldu. Lütfen tekrar giriş yapın.');
        onLogout();
        return;
      }
      setErrorMessage(message);
    }
    finally {
      setLoading(false);
    }
  }, [onLogout]);

  useEffect(() => {
    loadOverview();
  }, [loadOverview]);

  const teachers: TeacherOverview[] = overview?.teachers_list || [];
  const classes: ClassOverview[] = overview?.classes_list || [];
  const plans: PlanOverview[] = overview?.plans_list || [];
  const school = overview?.school;
  const stats = overview?.stats;

  const teachersMap = useMemo(
    () => Object.fromEntries(teachers.map(t => [String(t.id), t])),
    [teachers]
  );

  const classesMap = useMemo(
    () => Object.fromEntries(classes.map(c => [String(c.id), c])),
    [classes]
  );

  const getTeacherById = (id?: string | number | null) =>
    id != null ? teachersMap[String(id)] : undefined;

  const getClassById = (id?: string | number | null) =>
    id != null ? classesMap[String(id)] : undefined;

  const teacher = selectedPlan
    ? getTeacherById(selectedPlan.teacher_id)
    : null;

  const classRecord = selectedPlan
    ? getClassById(selectedPlan.class_id)
    : null;

  const activityIds = new Set(
    (selectedPlan?.activity_ids || []).map(String)
  );

  const handleRefresh = async () => {
    try {
      setRefreshing(true);
      
      await loadOverview();
      
      toast.success('Panel güncellendi');
    } finally {  
    setRefreshing(false);
    }
  };

  const handleViewPlan = (plan: PlanOverview) => {
    setSelectedPlan(plan);
    setShowReport(true);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex items-center justify-center">
        <div className="bg-white border rounded-lg shadow-sm px-6 py-4 text-gray-600">
          Okul yöneticisi paneli yükleniyor...
        </div>
      </div>
    );
  }

  if (errorMessage) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex items-center justify-center">
        <div className="bg-white border rounded-lg shadow-sm px-6 py-4 text-red-600">
          {errorMessage}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl text-purple-600">
                Okul Yöneticisi Paneli
              </h1>
              <p className="text-gray-600 mt-1">
                Hoş geldiniz, {displayName} • {school?.name || 'School Admin'}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Button onClick={handleRefresh} variant="outline">
                <RefreshCw 
                  className={`h-4 w-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} 
                />
                Yenile
              </Button>
              <Button onClick={onLogout} variant="outline">
                <LogOut className="h-4 w-4 mr-2" />
                Çıkış Yap
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">Toplam Öğretmen</CardTitle>
              <GraduationCap className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.teachers || 0}</div>
              <p className="text-xs text-muted-foreground">
                Sistemde aktif
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">Toplam Sınıf</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.classes || 0}</div>
              <p className="text-xs text-muted-foreground">
                {stats?.students || 0} toplam öğrenci
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">Etkinlik Planları</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.activity_plans || 0}</div>
              <p className="text-xs text-muted-foreground">
                Sistemde oluşturuldu
              </p>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="teachers" className="space-y-6">
          <TabsList>
            <TabsTrigger value="teachers">Öğretmenler</TabsTrigger>
            <TabsTrigger value="classes">Sınıflar</TabsTrigger>
            <TabsTrigger value="plans">Etkinlik Planları</TabsTrigger>
          </TabsList>

          <TabsContent value="teachers">
            <Card>
              <CardHeader>
                <CardTitle>Öğretmenler Genel Bakış</CardTitle>
                <CardDescription>
                  Okulunuza ait tüm öğretmenleri görüntüleyin
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {/* Mobile cards */}
                <div className="md:hidden space-y-4">
                  {teachers.length === 0 ? (
                    <p className="text-sm text-gray-500">
                      Bu okul için henüz öğretmen verisi mevcut değil.
                    </p>
                  ) : (
                    teachers.map((teacher) => (
                      <div key={teacher.id} className="bg-white border rounded-lg p-4 space-y-3">
                        <div>
                          <p className="text-xs text-gray-500">Ad Soyad</p>
                          <p className="font-medium">{teacher.name}</p>
                        </div>

                        <div className="flex items-center justify-between gap-4">
                          <div>
                            <p className="text-xs text-gray-500">Deneyim</p>
                            <p className="text-sm text-gray-700">
                              {teacher.years_experience ?? 0} yıl
                            </p>
                          </div>

                          <div className="text-right">
                            <p className="text-xs text-gray-500">Oluşturulma Tarihi</p>
                            <p className="text-sm text-gray-700">
                              {teacher.created_at
                                ? new Date(teacher.created_at).toLocaleDateString()
                                : '—'}
                            </p>
                          </div>
                        </div>

                        <div>
                          <p className="text-xs text-gray-500">Öğretim Stili</p>
                          <p className="text-sm text-gray-700">
                            {teacher.teaching_style || '—'}
                          </p>
                        </div>

                        <div>
                          <p className="text-xs text-gray-500 mb-1">Uzmanlık Alanları</p>
                          <div className="flex flex-wrap gap-1">
                            {(teacher.specializations || []).length > 0 ? (
                              (teacher.specializations || []).map((spec) => (
                                <Badge key={spec} variant="secondary" className="text-xs">
                                  {spec}
                                </Badge>
                              ))
                            ) : (
                              <span className="text-sm text-gray-700">—</span>
                            )}
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>

                {/* Desktop table */}
                <div className="hidden md:block w-full overflow-x-auto">
                  <Table className="min-w-[900px]">
                    <TableHeader>
                      <TableRow>
                        <TableHead>Ad Soyad</TableHead>
                        <TableHead>Deneyim</TableHead>
                        <TableHead>Uzmanlık Alanları</TableHead>
                        <TableHead>Öğretim Stili</TableHead>
                        <TableHead>Oluşturulma Tarihi</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {teachers.map((teacher) => (
                        <TableRow key={teacher.id}>
                          <TableCell>{teacher.name}</TableCell>
                          <TableCell>{teacher.years_experience ?? 0} yıl</TableCell>
                          <TableCell>
                            <div className="flex flex-wrap gap-1">
                              {(teacher.specializations || []).slice(0, 2).map((spec) => (
                                <Badge key={spec} variant="secondary" className="text-xs">
                                  {spec}
                                </Badge>
                              ))}
                              {(teacher.specializations || []).length > 2 && (
                                <Badge variant="secondary" className="text-xs">
                                  +{(teacher.specializations || []).length - 2}
                                </Badge>
                              )}
                            </div>
                          </TableCell>
                          <TableCell>{teacher.teaching_style || '—'}</TableCell>
                          <TableCell className="text-sm text-gray-500">
                            {teacher.created_at
                              ? new Date(teacher.created_at).toLocaleDateString()
                              : '—'}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="classes">
            <Card>
              <CardHeader>
                <CardTitle>Sınıflar Genel Bakış</CardTitle>
                <CardDescription>
                  Okulunuza ait tüm sınıfları görüntüleyin
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {/* Mobile cards */}
                <div className="md:hidden space-y-4">
                  {classes.length === 0 ? (
                    <p className="text-sm text-gray-500">
                      Bu okul için henüz sınıf verisi mevcut değil.
                    </p>
                  ) : (
                    classes.map((classRecord) => (
                      <div key={classRecord.id} className="bg-white border rounded-lg p-4 space-y-3">
                        <div>
                          <p className="text-xs text-gray-500">Sınıf Adı</p>
                          <p className="font-medium">{classRecord.class_name}</p>
                        </div>

                        <div className="flex items-center justify-between gap-4">
                          <div>
                            <p className="text-xs text-gray-500">Yaş Grubu</p>
                            <p className="text-sm text-gray-700">
                              {classRecord.age_group || '—'} 
                            </p>
                          </div>

                          <div className="text-right">
                            <p className="text-xs text-gray-500">Sınıf Mevcudu</p>
                            <p className="text-sm text-gray-700">
                              {classRecord.class_size ?? 0} öğrenci
                            </p>
                          </div>
                        </div>

                        <div>
                          <p className="text-xs text-gray-500">Güncelleme Tarihi</p>
                          <p className="text-sm text-gray-700">
                            {classRecord.updated_at
                              ? new Date(classRecord.updated_at).toLocaleDateString()
                              : '—'}
                          </p>
                        </div>

                        <div>
                          <p className="text-xs text-gray-500 mb-1">Öğrenme Odakları</p>
                          <div className="flex flex-wrap gap-1">
                            {(classRecord.learning_focus || []).length > 0 ? (
                              (classRecord.learning_focus || []).map((focus) => (
                                <Badge key={focus} variant="outline" className="text-xs">
                                  {focus}
                                </Badge>
                              ))
                            ) : (
                              <span className="text-sm text-gray-700">—</span>
                            )}
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>

                {/* Desktop table */}
                <div className="hidden md:block w-full overflow-x-auto">
                  <Table className="min-w-[900px]">
                    <TableHeader>
                      <TableRow>
                        <TableHead>Sınıf Adı</TableHead>
                        <TableHead>Yaş Grubu</TableHead>
                        <TableHead>Sınıf Mevcudu</TableHead>
                        <TableHead>Öğrenme Odakları</TableHead>
                        <TableHead>Güncelleme Tarihi</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {classes.map((classRecord) => (
                        <TableRow key={classRecord.id}>
                          <TableCell>{classRecord.class_name}</TableCell>
                          <TableCell>{classRecord.age_group || '—'} yaş</TableCell>
                          <TableCell>{classRecord.class_size ?? 0} öğrenci</TableCell>
                          <TableCell>
                            <div className="flex flex-wrap gap-1">
                              {(classRecord.learning_focus || []).slice(0, 2).map((focus) => (
                                <Badge key={focus} variant="outline" className="text-xs">
                                  {focus}
                                </Badge>
                              ))}
                              {(classRecord.learning_focus || []).length > 2 && (
                                <Badge variant="outline" className="text-xs">
                                  +{(classRecord.learning_focus || []).length - 2}
                                </Badge>
                              )}
                            </div>
                          </TableCell>
                          <TableCell className="text-sm text-gray-500">
                            {classRecord.updated_at
                              ? new Date(classRecord.updated_at).toLocaleDateString()
                              : '—'}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="plans">
            <Card>
              <CardHeader>
                <CardTitle>Etkinlik Planları</CardTitle>
                <CardDescription>
                  Öğretmenler tarafından oluşturulan etkinlik planlarını görüntüle ve incele
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {/* Mobile cards */}
                <div className="md:hidden space-y-4">
                  {plans.length === 0 ? (
                    <p className="text-sm text-gray-500">
                      Bu okul için henüz etkinlik planı oluşturulmadı.
                    </p>
                  ) : (
                    plans.map((plan) => (
                      <div key={plan.id} className="bg-white border rounded-lg p-4 space-y-3">
                        <div>
                          <p className="text-xs uppercase tracking-wide text-gray-500">Öğretmen</p>
                          <p className="font-medium">
                            {getTeacherById(plan.teacher_id)?.name || `#${plan.teacher_id}`}
                          </p>
                        </div>

                        <div>
                          <p className="text-xs uppercase tracking-wide text-gray-500">Sınıf</p>
                          <p className="font-medium">
                            {getClassById(plan.class_id)?.class_name || `#${plan.class_id}`}
                          </p>
                        </div>

                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-xs text-gray-500">Etkinlik sayısı</p>
                            <Badge>{(plan.activity_ids || []).length} Etkinlik</Badge>
                          </div>

                          <div className="text-right">
                            <p className="text-xs text-gray-500">Oluşturulma Tarihi</p>
                            <p className="text-sm text-gray-700">
                              {plan.created_at ? new Date(plan.created_at).toLocaleDateString() : '—'}
                            </p>
                          </div>
                        </div>

                        <div>
                          <p className="text-xs text-gray-500">Notlar</p>
                          <p className="text-sm text-gray-700 break-words">
                            {plan.notes || '—'}
                          </p>
                        </div>

                        <Button
                          variant="outline"
                          size="sm"
                          className="w-full rounded-lg"
                          onClick={() => handleViewPlan(plan)}
                        >
                          <Eye className="h-4 w-4 mr-2" />
                          Raporu Görüntüle
                        </Button>
                      </div>
                    ))
                  )}
                </div>

                {/* Desktop table */}
                <div className="hidden md:block w-full overflow-x-auto">
                  <Table className="min-w-[900px]">
                    <TableHeader>
                      <TableRow>
                        <TableHead>Öğretmen</TableHead>
                        <TableHead>Sınıf</TableHead>
                        <TableHead>Etkinlik sayısı</TableHead>
                        <TableHead>Oluşturulma Tarihi</TableHead>
                        <TableHead>Notlar</TableHead>
                        <TableHead>İşlemler</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {plans.map((plan) => (
                        <TableRow key={plan.id}>
                          <TableCell>
                            {getTeacherById(plan.teacher_id)?.name || `#${plan.teacher_id}`}
                          </TableCell>
                          <TableCell>
                            {getClassById(plan.class_id)?.class_name || `#${plan.class_id}`}
                          </TableCell>
                          <TableCell>
                            <Badge>{(plan.activity_ids || []).length} Etkinlik</Badge>
                          </TableCell>
                          <TableCell className="text-sm text-gray-500">
                            {plan.created_at ? new Date(plan.created_at).toLocaleDateString() : '—'}
                          </TableCell>
                          <TableCell className="text-sm max-w-xs truncate">
                            {plan.notes || '—'}
                          </TableCell>
                          <TableCell className="whitespace-nowrap">
                            <Button
                              variant="outline"
                              size="sm"
                              className="rounded-lg"
                              onClick={() => handleViewPlan(plan)}
                            >
                              <Eye className="h-4 w-4 mr-1" />
                              Raporu Görüntüle
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>

      {selectedPlan && showReport &&
        (
          <ActivityReport
            activities={activities.filter((a) =>
              activityIds.has(String(a.id))
            )}
            teacherProfile={{
              name: getTeacherById(selectedPlan.teacher_id)?.name || `Öğretmen #${selectedPlan.teacher_id}`,
              schoolId: Number(school?.id ?? 0),
              schoolName: school?.name || '',
              yearsExperience: teacher?.years_experience ?? 0,
              specializations: teacher?.specializations || [],
              teachingStyle: teacher?.teaching_style || '',
            }}
            classProfile={{
              className: classRecord?.class_name || `Sınıf #${selectedPlan.class_id}`,
              ageGroup: classRecord?.age_group || '',
              classSize: classRecord?.class_size || 0,
              learningFocus: classRecord?.learning_focus || [],
              availableResources: [],
              specialNeeds: [],
              dailySchedule: {
                morningActivities: 30,
                afternoonActivities: 30,
              },
            }}
            open={showReport}
            onClose={() => {
              setShowReport(false);
              setSelectedPlan(null);
            }}
          />
        )}
    </div>
  );
}