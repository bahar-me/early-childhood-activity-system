import { useEffect, useState } from 'react';
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

  const displayName = user.name || user.email;

  const loadOverview = async () => {
    try {
      setLoading(true);
      setErrorMessage('');
      const data = await getSchoolAdminOverview();
      setOverview(data);
    } catch (error) {
      console.error('Failed to load school admin overview:', error);
      setErrorMessage(
        error instanceof Error ? error.message : 'Failed to load school admin overview'
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOverview();
  }, [user.id]);

  const teachers = overview?.teachers_list || [];
  const classes = overview?.classes_list || [];
  const plans = overview?.plans_list || [];
  const school = overview?.school;
  const stats = overview?.stats;

  const getTeacherById = (id: string | number) => {
    return teachers.find((t) => String(t.id) === String(id));
  };

  const getClassById = (id: string | number) => {
    return classes.find((c) => String(c.id) === String(id));
  };

  const handleViewPlan = (plan: PlanOverview) => {
    const teacher = getTeacherById(plan.teacher_id);
    const classRecord = getClassById(plan.class_id);

    if (!teacher || !classRecord) {
      toast.error('Teacher or class information for this activity plan is missing. Cannot generate report.');
      console.error('Missing teacher or class information for selected plan:', plan);
      return;
    }

    setSelectedPlan(plan);
    setShowReport(true);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex items-center justify-center">
        <div className="bg-white border rounded-lg shadow-sm px-6 py-4 text-gray-600">
          Loading school admin dashboard...
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
                School Administrator Dashboard
              </h1>
              <p className="text-gray-600 mt-1">
                Welcome, {displayName} • {school?.name || 'School Admin'}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Button onClick={loadOverview} variant="outline">
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </Button>
              <Button onClick={onLogout} variant="outline">
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">Total Teachers</CardTitle>
              <GraduationCap className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.teachers || 0}</div>
              <p className="text-xs text-muted-foreground">
                Active in the system
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">Total Classes</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.classes || 0}</div>
              <p className="text-xs text-muted-foreground">
                {stats?.students || 0} total students
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">Activity Plans</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.activity_plans || 0}</div>
              <p className="text-xs text-muted-foreground">
                Created in the system
              </p>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="teachers" className="space-y-6">
          <TabsList>
            <TabsTrigger value="teachers">Teachers</TabsTrigger>
            <TabsTrigger value="classes">Classes</TabsTrigger>
            <TabsTrigger value="plans">Activity Plans</TabsTrigger>
          </TabsList>

          <TabsContent value="teachers">
            <Card>
              <CardHeader>
                <CardTitle>Teachers Overview</CardTitle>
                <CardDescription>
                  View all teachers in your school
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {/* Mobile cards */}
                <div className="md:hidden space-y-4">
                  {teachers.length === 0 ? (
                    <p className="text-sm text-gray-500">
                      No teacher data available for this school yet.
                    </p>
                  ) : (
                    teachers.map((teacher) => (
                      <div key={teacher.id} className="bg-white border rounded-lg p-4 space-y-3">
                        <div>
                          <p className="text-xs text-gray-500">Name</p>
                          <p className="font-medium">{teacher.name}</p>
                        </div>

                        <div className="flex items-center justify-between gap-4">
                          <div>
                            <p className="text-xs text-gray-500">Experience</p>
                            <p className="text-sm text-gray-700">
                              {teacher.years_experience ?? 0} years
                            </p>
                          </div>

                          <div className="text-right">
                            <p className="text-xs text-gray-500">Created</p>
                            <p className="text-sm text-gray-700">
                              {teacher.created_at
                                ? new Date(teacher.created_at).toLocaleDateString()
                                : '—'}
                            </p>
                          </div>
                        </div>

                        <div>
                          <p className="text-xs text-gray-500">Teaching Style</p>
                          <p className="text-sm text-gray-700">
                            {teacher.teaching_style || '—'}
                          </p>
                        </div>

                        <div>
                          <p className="text-xs text-gray-500 mb-1">Specializations</p>
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
                        <TableHead>Name</TableHead>
                        <TableHead>Experience</TableHead>
                        <TableHead>Specializations</TableHead>
                        <TableHead>Teaching Style</TableHead>
                        <TableHead>Created</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {teachers.map((teacher) => (
                        <TableRow key={teacher.id}>
                          <TableCell>{teacher.name}</TableCell>
                          <TableCell>{teacher.years_experience ?? 0} years</TableCell>
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
                <CardTitle>Classes Overview</CardTitle>
                <CardDescription>
                  View all classes in your school
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {/* Mobile cards */}
                <div className="md:hidden space-y-4">
                  {classes.length === 0 ? (
                    <p className="text-sm text-gray-500">
                      No class data available for this school yet.
                    </p>
                  ) : (
                    classes.map((classRecord) => (
                      <div key={classRecord.id} className="bg-white border rounded-lg p-4 space-y-3">
                        <div>
                          <p className="text-xs text-gray-500">Class Name</p>
                          <p className="font-medium">{classRecord.class_name}</p>
                        </div>

                        <div className="flex items-center justify-between gap-4">
                          <div>
                            <p className="text-xs text-gray-500">Age Group</p>
                            <p className="text-sm text-gray-700">
                              {classRecord.age_group || '—'} years
                            </p>
                          </div>

                          <div className="text-right">
                            <p className="text-xs text-gray-500">Class Size</p>
                            <p className="text-sm text-gray-700">
                              {classRecord.class_size ?? 0} students
                            </p>
                          </div>
                        </div>

                        <div>
                          <p className="text-xs text-gray-500">Updated</p>
                          <p className="text-sm text-gray-700">
                            {classRecord.updated_at
                              ? new Date(classRecord.updated_at).toLocaleDateString()
                              : '—'}
                          </p>
                        </div>

                        <div>
                          <p className="text-xs text-gray-500 mb-1">Learning Focus</p>
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
                        <TableHead>Class Name</TableHead>
                        <TableHead>Age Group</TableHead>
                        <TableHead>Class Size</TableHead>
                        <TableHead>Learning Focus</TableHead>
                        <TableHead>Updated</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {classes.map((classRecord) => (
                        <TableRow key={classRecord.id}>
                          <TableCell>{classRecord.class_name}</TableCell>
                          <TableCell>{classRecord.age_group || '—'} years</TableCell>
                          <TableCell>{classRecord.class_size ?? 0} students</TableCell>
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
                <CardTitle>Activity Plans</CardTitle>
                <CardDescription>
                  View and review activity plans created by teachers
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {/* Mobile cards */}
                <div className="md:hidden space-y-4">
                  {plans.length === 0 ? (
                    <p className="text-sm text-gray-500">
                      No activity plans created for this school yet.
                    </p>
                  ) : (
                    plans.map((plan) => (
                      <div key={plan.id} className="bg-white border rounded-lg p-4 space-y-3">
                        <div>
                          <p className="text-xs uppercase tracking-wide text-gray-500">Teacher</p>
                          <p className="font-medium">
                            {getTeacherById(plan.teacher_id)?.name || `#${plan.teacher_id}`}
                          </p>
                        </div>

                        <div>
                          <p className="text-xs uppercase tracking-wide text-gray-500">Class</p>
                          <p className="font-medium">
                            {getClassById(plan.class_id)?.class_name || `#${plan.class_id}`}
                          </p>
                        </div>

                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-xs text-gray-500">Activities</p>
                            <Badge>{(plan.activity_ids || []).length} activities</Badge>
                          </div>

                          <div className="text-right">
                            <p className="text-xs text-gray-500">Created</p>
                            <p className="text-sm text-gray-700">
                              {plan.created_at ? new Date(plan.created_at).toLocaleDateString() : '—'}
                            </p>
                          </div>
                        </div>

                        <div>
                          <p className="text-xs text-gray-500">Notes</p>
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
                          View Report
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
                        <TableHead>Teacher</TableHead>
                        <TableHead>Class</TableHead>
                        <TableHead>Activities</TableHead>
                        <TableHead>Created</TableHead>
                        <TableHead>Notes</TableHead>
                        <TableHead>Actions</TableHead>
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
                            <Badge>{(plan.activity_ids || []).length} activities</Badge>
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
                              View Report
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

      {selectedPlan &&
        showReport &&
        getTeacherById(selectedPlan.teacher_id) &&
        getClassById(selectedPlan.class_id) && (
          <ActivityReport
            activities={activities.filter((a) =>
              (selectedPlan.activity_ids || []).includes(a.id)
            )}
            teacherProfile={{
              name: getTeacherById(selectedPlan.teacher_id)!.name,
              schoolName: school?.name || '',
              yearsExperience: String(getTeacherById(selectedPlan.teacher_id)!.years_experience || 0),
              specializations: getTeacherById(selectedPlan.teacher_id)!.specializations || [],
              teachingStyle: getTeacherById(selectedPlan.teacher_id)!.teaching_style || '',
            }}
            classProfile={{
              className: getClassById(selectedPlan.class_id)!.class_name,
              ageGroup: getClassById(selectedPlan.class_id)!.age_group || '',
              classSize: getClassById(selectedPlan.class_id)!.class_size || 0,
              learningFocus: getClassById(selectedPlan.class_id)!.learning_focus || [],
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