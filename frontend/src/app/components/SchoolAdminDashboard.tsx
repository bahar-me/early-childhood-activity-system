import { useState } from 'react';
import { User } from '../types/user';
import { ActivityPlan } from '../types/school';
import { activities } from '../data/activities';
import { mockTeacherRecords, mockClassRecords, mockActivityPlans } from '../data/mockUsers';
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
  const [selectedPlan, setSelectedPlan] = useState<ActivityPlan | null>(null);
  const [showReport, setShowReport] = useState(false);
   
  const displayName = user.name || user.email;
  // Filter data by school
  const currentSchoolId = user.schoolId ?? (user.school_id ? String(user.school_id) : '');

  const teachers = mockTeacherRecords.filter((t) => t.schoolId === currentSchoolId);
  const classes = mockClassRecords.filter((c) => c.schoolId === currentSchoolId);
  const plans = mockActivityPlans.filter((p) => p.schoolId === currentSchoolId);

  const handleViewPlan = (plan: ActivityPlan) => {
    setSelectedPlan(plan);
    setShowReport(true);
  };

  const getTeacherById = (id: string) => {
    return teachers.find((t) => t.id === id);
  };

  const getClassById = (id: string) => {
    return classes.find((c) => c.id === id);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl text-purple-600">
                School Administrator Dashboard
              </h1>
              <p className="text-gray-600 mt-1">
                Welcome, {displayName} • {teachers[0]?.schoolName || 'School Admin'}
              </p>
            </div>
            <Button onClick={onLogout} variant="outline">
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">Total Teachers</CardTitle>
              <GraduationCap className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{teachers.length}</div>
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
              <div className="text-2xl font-bold">{classes.length}</div>
              <p className="text-xs text-muted-foreground">
                {classes.reduce((sum, c) => sum + c.classSize, 0)} total students
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">Activity Plans</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{plans.length}</div>
              <p className="text-xs text-muted-foreground">
                Created this month
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
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
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Experience</TableHead>
                      <TableHead>Specializations</TableHead>
                      <TableHead>Last Active</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {teachers.map((teacher) => (
                      <TableRow key={teacher.id}>
                        <TableCell>{teacher.name}</TableCell>
                        <TableCell>{teacher.email}</TableCell>
                        <TableCell>{teacher.yearsExperience} years</TableCell>
                        <TableCell>
                          <div className="flex flex-wrap gap-1">
                            {teacher.specializations.slice(0, 2).map((spec) => (
                              <Badge key={spec} variant="secondary" className="text-xs">
                                {spec}
                              </Badge>
                            ))}
                            {teacher.specializations.length > 2 && (
                              <Badge variant="secondary" className="text-xs">
                                +{teacher.specializations.length - 2}
                              </Badge>
                            )}
                          </div>
                        </TableCell>
                        <TableCell className="text-sm text-gray-500">
                          {new Date(teacher.lastActive).toLocaleDateString()}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
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
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Class Name</TableHead>
                      <TableHead>Teacher</TableHead>
                      <TableHead>Age Group</TableHead>
                      <TableHead>Class Size</TableHead>
                      <TableHead>Learning Focus</TableHead>
                      <TableHead>Updated</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {classes.map((classRecord) => (
                      <TableRow key={classRecord.id}>
                        <TableCell>{classRecord.className}</TableCell>
                        <TableCell>{classRecord.teacherName}</TableCell>
                        <TableCell>{classRecord.ageGroup} years</TableCell>
                        <TableCell>{classRecord.classSize} students</TableCell>
                        <TableCell>
                          <div className="flex flex-wrap gap-1">
                            {classRecord.learningFocus.slice(0, 2).map((focus) => (
                              <Badge key={focus} variant="outline" className="text-xs">
                                {focus}
                              </Badge>
                            ))}
                            {classRecord.learningFocus.length > 2 && (
                              <Badge variant="outline" className="text-xs">
                                +{classRecord.learningFocus.length - 2}
                              </Badge>
                            )}
                          </div>
                        </TableCell>
                        <TableCell className="text-sm text-gray-500">
                          {new Date(classRecord.updatedAt).toLocaleDateString()}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
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
                <Table>
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
                        <TableCell>{plan.teacherName}</TableCell>
                        <TableCell>{plan.className}</TableCell>
                        <TableCell>
                          <Badge>{plan.activityIds.length} activities</Badge>
                        </TableCell>
                        <TableCell className="text-sm text-gray-500">
                          {new Date(plan.createdAt).toLocaleDateString()}
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
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>

      {/* Report Modal */}
      {selectedPlan && showReport && getTeacherById(selectedPlan.teacherId) && getClassById(selectedPlan.classId) && (
        <ActivityReport
          activities={activities.filter((a) => selectedPlan.activityIds.includes(a.id))}
          teacherProfile={getTeacherById(selectedPlan.teacherId)!}
          classProfile={getClassById(selectedPlan.classId)!}
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
