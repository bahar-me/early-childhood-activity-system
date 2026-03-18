import { useEffect, useState } from 'react';
import { getSchoolAdminOverview } from '../api/schoolAdmin';
import { User } from '../types/user';
import { ActivityPlan } from '../types/school';
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
import { Users, GraduationCap, FileText, Eye, LogOut } from 'lucide-react';

interface SchoolAdminDashboardProps {
  user: User;
  onLogout: () => void;
}

export function SchoolAdminDashboard({ user, onLogout }: SchoolAdminDashboardProps) {
  const [overview, setOverview] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const [selectedPlan, setSelectedPlan] = useState<ActivityPlan | null>(null);
  const [showReport, setShowReport] = useState(false);

  const displayName = user.name || user.email;

  useEffect(() => {
    const loadOverview = async () => {
      try {
        const data = await getSchoolAdminOverview();
        setOverview(data);
      } catch (error) {
        console.error('Failed to load school admin overview:', error);
      } finally {
        setLoading(false);
      }
    };

    loadOverview();
  }, []);

  const teachers = overview?.teachers_list || [];
  const classes = overview?.classes_list || [];
  const plans = overview?.plans_list || [];
  const school = overview?.school;
  const stats = overview?.stats;

  const handleViewPlan = (plan: ActivityPlan) => {
    setSelectedPlan(plan);
    setShowReport(true);
  };

  const getTeacherById = (id: string | number) => {
    return teachers.find((t: any) => String(t.id) === String(id));
  };

  const getClassById = (id: string | number) => {
    return classes.find((c: any) => String(c.id) === String(id));
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
            <Button onClick={onLogout} variant="outline">
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </Button>
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
              <CardContent>
                {teachers.length === 0 ? (
                  <p className="text-sm text-gray-500">No teacher data available for this school yet.</p>
                ) : (
                  <Table>
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
                      {teachers.map((teacher: any) => (
                        <TableRow key={teacher.id}>
                          <TableCell>{teacher.name}</TableCell>
                          <TableCell>{teacher.years_experience} years</TableCell>
                          <TableCell>
                            <div className="flex flex-wrap gap-1">
                              {(teacher.specializations || []).slice(0, 2).map((spec: string) => (
                                <Badge key={spec} variant="secondary" className="text-xs">
                                  {spec}
                                </Badge>
                              ))}
                              {(teacher.specializations || []).length > 2 && (
                                <Badge variant="secondary" className="text-xs">
                                  +{teacher.specializations.length - 2}
                                </Badge>
                              )}
                            </div>
                          </TableCell>
                          <TableCell>{teacher.teaching_style || '—'}</TableCell>
                          <TableCell className="text-sm text-gray-500">
                            {teacher.created_at ? new Date(teacher.created_at).toLocaleDateString() : '—'}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                )}
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
              <CardContent>
                {classes.length === 0 ? (
                  <p className="text-sm text-gray-500">No class data available for this school yet.</p>
                ) : (
                  <Table>
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
                      {classes.map((classRecord: any) => (
                        <TableRow key={classRecord.id}>
                          <TableCell>{classRecord.class_name}</TableCell>
                          <TableCell>{classRecord.age_group} years</TableCell>
                          <TableCell>{classRecord.class_size} students</TableCell>
                          <TableCell>
                            <div className="flex flex-wrap gap-1">
                              {(classRecord.learning_focus || []).slice(0, 2).map((focus: string) => (
                                <Badge key={focus} variant="outline" className="text-xs">
                                  {focus}
                                </Badge>
                              ))}
                              {(classRecord.learning_focus || []).length > 2 && (
                                <Badge variant="outline" className="text-xs">
                                  +{classRecord.learning_focus.length - 2}
                                </Badge>
                              )}
                            </div>
                          </TableCell>
                          <TableCell className="text-sm text-gray-500">
                            {classRecord.updated_at ? new Date(classRecord.updated_at).toLocaleDateString() : '—'}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                )}
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
              <CardContent>
                {plans.length === 0 ? (
                  <p className="text-sm text-gray-500">No activity plans created for this school yet.</p>
                ) : (
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Teacher ID</TableHead>
                        <TableHead>Class ID</TableHead>
                        <TableHead>Activities</TableHead>
                        <TableHead>Created</TableHead>
                        <TableHead>Notes</TableHead>
                        <TableHead>Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {plans.map((plan: any) => (
                        <TableRow key={plan.id}>
                          <TableCell>{plan.teacher_id}</TableCell>
                          <TableCell>{plan.class_id}</TableCell>
                          <TableCell>
                            <Badge>{(plan.activity_ids || []).length} activities</Badge>
                          </TableCell>
                          <TableCell className="text-sm text-gray-500">
                            {plan.created_at ? new Date(plan.created_at).toLocaleDateString() : '—'}
                          </TableCell>
                          <TableCell className="text-sm max-w-xs truncate">
                            {plan.notes || '—'}
                          </TableCell>
                          <TableCell>
                            <Button
                              variant="outline"
                              size="sm"
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
                )}
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
            activities={activities.filter((a) => (selectedPlan.activity_ids || []).includes(a.id))}
            teacherProfile={getTeacherById(selectedPlan.teacher_id)!}
            classProfile={getClassById(selectedPlan.class_id)!}
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