import { useState } from 'react';
import { User } from '../types/user';
import { mockUsers, mockSchools, mockTeacherRecords, mockClassRecords, mockActivityPlans } from '../data/mockUsers';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { Label } from './ui/label';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from './ui/table';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from './ui/dialog';
import {
  Building2,
  Users,
  GraduationCap,
  Activity,
  LogOut,
  Plus,
  Shield,
  Database,
  TrendingUp,
} from 'lucide-react';
import { toast } from 'sonner';
import { Toaster } from './ui/sonner';

interface SystemAdminDashboardProps {
  user: User;
  onLogout: () => void;
}

export function SystemAdminDashboard({ user, onLogout }: SystemAdminDashboardProps) {
  const [showAddSchool, setShowAddSchool] = useState(false);
  const [newSchoolName, setNewSchoolName] = useState('');

  const totalTeachers = mockTeacherRecords.length;
  const totalClasses = mockClassRecords.length;
  const totalStudents = mockClassRecords.reduce((sum, c) => sum + c.classSize, 0);
  const totalPlans = mockActivityPlans.length;

  const handleAddSchool = () => {
    if (newSchoolName.trim()) {
      toast.success('School added successfully!');
      setNewSchoolName('');
      setShowAddSchool(false);
    }
  };

  const getRoleColor = (role: string) => {
    const colors: Record<string, string> = {
      teacher: 'bg-blue-100 text-blue-800',
      'school-admin': 'bg-purple-100 text-purple-800',
      'system-admin': 'bg-red-100 text-red-800',
    };
    return colors[role] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      <Toaster />
      
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl text-purple-600">
                System Administrator Dashboard
              </h1>
              <p className="text-gray-600 mt-1">
                Welcome, {user.name} • Full System Access
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
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">Total Schools</CardTitle>
              <Building2 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{mockSchools.length}</div>
              <p className="text-xs text-muted-foreground">
                Active institutions
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">Total Users</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{mockUsers.length}</div>
              <p className="text-xs text-muted-foreground">
                {totalTeachers} teachers, {mockUsers.filter(u => u.role === 'school-admin').length} admins
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">Total Students</CardTitle>
              <GraduationCap className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{totalStudents}</div>
              <p className="text-xs text-muted-foreground">
                Across {totalClasses} classes
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">Activity Plans</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{totalPlans}</div>
              <p className="text-xs text-muted-foreground">
                <TrendingUp className="h-3 w-3 inline mr-1" />
                Generated by AI
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="schools" className="space-y-6">
          <TabsList>
            <TabsTrigger value="schools">Schools</TabsTrigger>
            <TabsTrigger value="users">Users</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="system">System</TabsTrigger>
          </TabsList>

          <TabsContent value="schools">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Schools Management</CardTitle>
                    <CardDescription>
                      Manage all schools in the system
                    </CardDescription>
                  </div>
                  <Button onClick={() => setShowAddSchool(true)}>
                    <Plus className="h-4 w-4 mr-2" />
                    Add School
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>School Name</TableHead>
                      <TableHead>Address</TableHead>
                      <TableHead>Contact</TableHead>
                      <TableHead>Teachers</TableHead>
                      <TableHead>Classes</TableHead>
                      <TableHead>Students</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {mockSchools.map((school) => {
                      const schoolTeachers = mockTeacherRecords.filter(t => t.schoolId === school.id);
                      const schoolClasses = mockClassRecords.filter(c => c.schoolId === school.id);
                      const schoolStudents = schoolClasses.reduce((sum, c) => sum + c.classSize, 0);
                      
                      return (
                        <TableRow key={school.id}>
                          <TableCell>{school.name}</TableCell>
                          <TableCell className="text-sm">{school.address}</TableCell>
                          <TableCell className="text-sm">{school.contactEmail}</TableCell>
                          <TableCell>
                            <Badge variant="secondary">{schoolTeachers.length}</Badge>
                          </TableCell>
                          <TableCell>
                            <Badge variant="secondary">{schoolClasses.length}</Badge>
                          </TableCell>
                          <TableCell>
                            <Badge variant="secondary">{schoolStudents}</Badge>
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="users">
            <Card>
              <CardHeader>
                <CardTitle>User Management</CardTitle>
                <CardDescription>
                  View and manage all system users
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Role</TableHead>
                      <TableHead>School</TableHead>
                      <TableHead>Created</TableHead>
                      <TableHead>Status</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {mockUsers.map((user) => {
                      const school = mockSchools.find(s => s.id === user.schoolId);
                      
                      return (
                        <TableRow key={user.id}>
                          <TableCell>{user.name}</TableCell>
                          <TableCell>{user.email}</TableCell>
                          <TableCell>
                            <Badge className={getRoleColor(user.role)}>
                              {user.role === 'teacher' && 'Teacher'}
                              {user.role === 'school-admin' && 'School Admin'}
                              {user.role === 'system-admin' && 'System Admin'}
                            </Badge>
                          </TableCell>
                          <TableCell className="text-sm">
                            {school?.name || '—'}
                          </TableCell>
                          <TableCell className="text-sm text-gray-500">
                            {new Date(user.createdAt).toLocaleDateString()}
                          </TableCell>
                          <TableCell>
                            <Badge variant="outline" className="bg-green-50 text-green-700 border-green-300">
                              Active
                            </Badge>
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analytics">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Activity Plan Statistics</CardTitle>
                  <CardDescription>Plans created by teachers</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {mockTeacherRecords.map((teacher) => {
                      const teacherPlans = mockActivityPlans.filter(p => p.teacherId === teacher.id);
                      const totalActivities = teacherPlans.reduce((sum, p) => sum + p.activityIds.length, 0);
                      
                      return (
                        <div key={teacher.id} className="flex items-center justify-between pb-4 border-b last:border-0">
                          <div>
                            <p className="font-medium">{teacher.name}</p>
                            <p className="text-sm text-gray-500">{teacher.schoolName}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm">{teacherPlans.length} plans</p>
                            <p className="text-xs text-gray-500">{totalActivities} activities</p>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Popular Subjects</CardTitle>
                  <CardDescription>Most used in activity plans</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between pb-4 border-b">
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-purple-500"></div>
                        <span>Language Arts</span>
                      </div>
                      <Badge>35%</Badge>
                    </div>
                    <div className="flex items-center justify-between pb-4 border-b">
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                        <span>Math</span>
                      </div>
                      <Badge>28%</Badge>
                    </div>
                    <div className="flex items-center justify-between pb-4 border-b">
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-green-500"></div>
                        <span>Science</span>
                      </div>
                      <Badge>18%</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-pink-500"></div>
                        <span>Other</span>
                      </div>
                      <Badge>19%</Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="system">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-2">
                    <Database className="h-5 w-5 text-purple-600" />
                    <CardTitle>System Information</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between py-2 border-b">
                    <span className="text-sm text-gray-600">System Version</span>
                    <span className="text-sm font-medium">v2.1.0</span>
                  </div>
                  <div className="flex justify-between py-2 border-b">
                    <span className="text-sm text-gray-600">Database Status</span>
                    <Badge variant="outline" className="bg-green-50 text-green-700 border-green-300">
                      Connected
                    </Badge>
                  </div>
                  <div className="flex justify-between py-2 border-b">
                    <span className="text-sm text-gray-600">API Status</span>
                    <Badge variant="outline" className="bg-green-50 text-green-700 border-green-300">
                      Operational
                    </Badge>
                  </div>
                  <div className="flex justify-between py-2 border-b">
                    <span className="text-sm text-gray-600">AI Engine</span>
                    <Badge variant="outline" className="bg-green-50 text-green-700 border-green-300">
                      Active
                    </Badge>
                  </div>
                  <div className="flex justify-between py-2">
                    <span className="text-sm text-gray-600">Last Backup</span>
                    <span className="text-sm font-medium">2 hours ago</span>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <div className="flex items-center gap-2">
                    <Shield className="h-5 w-5 text-purple-600" />
                    <CardTitle>System Actions</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Button variant="outline" className="w-full justify-start">
                    <Database className="h-4 w-4 mr-2" />
                    Run Database Backup
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Activity className="h-4 w-4 mr-2" />
                    Generate System Report
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Users className="h-4 w-4 mr-2" />
                    Export User Data
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Shield className="h-4 w-4 mr-2" />
                    View Security Logs
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </main>

      {/* Add School Dialog */}
      <Dialog open={showAddSchool} onOpenChange={setShowAddSchool}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add New School</DialogTitle>
            <DialogDescription>
              Create a new school in the system
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="schoolName">School Name</Label>
              <Input
                id="schoolName"
                value={newSchoolName}
                onChange={(e) => setNewSchoolName(e.target.value)}
                placeholder="Enter school name"
              />
            </div>
            <div className="flex gap-2 justify-end">
              <Button variant="outline" onClick={() => setShowAddSchool(false)}>
                Cancel
              </Button>
              <Button onClick={handleAddSchool}>
                Add School
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
