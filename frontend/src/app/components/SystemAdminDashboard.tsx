import { useEffect, useMemo, useState } from 'react';
import { User } from '../types/user';
import { School } from '../types/school';
import { getSchools, createSchool, updateSchool, deleteSchool } from '../api/schools';

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
  LogOut,
  Plus,
  Shield,
  Database,
  Pencil,
  Trash2,
  RefreshCw,
} from 'lucide-react';
import { toast } from 'sonner';
import { Toaster } from './ui/sonner';

interface SystemAdminDashboardProps {
  user: User;
  onLogout: () => void;
}

export function SystemAdminDashboard({ user, onLogout }: SystemAdminDashboardProps) {
  const [schools, setSchools] = useState<School[]>([]);
  const [loading, setLoading] = useState(false);

  const [showAddSchool, setShowAddSchool] = useState(false);
  const [showEditSchool, setShowEditSchool] = useState(false);

  const [newSchoolName, setNewSchoolName] = useState('');
  const [newSchoolAddress, setNewSchoolAddress] = useState('');

  const [editingSchool, setEditingSchool] = useState<School | null>(null);
  const [editSchoolName, setEditSchoolName] = useState('');
  const [editSchoolAddress, setEditSchoolAddress] = useState('');

  const displayName = user.name || user.email;

  const totalSchools = schools.length;

  const loadSchools = async () => {
    try {
      setLoading(true);
      const data = await getSchools();
      setSchools(data);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to load schools';
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSchools();
  }, []);

  const handleAddSchool = async () => {
    if (!newSchoolName.trim()) {
      toast.error('School name is required');
      return;
    }

    try {
      await createSchool({
        name: newSchoolName.trim(),
        address: newSchoolAddress.trim(),
      });

      toast.success('School added successfully');
      setNewSchoolName('');
      setNewSchoolAddress('');
      setShowAddSchool(false);
      await loadSchools();
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to add school';
      toast.error(message);
    }
  };

  const handleOpenEdit = (school: School) => {
    setEditingSchool(school);
    setEditSchoolName(school.name || '');
    setEditSchoolAddress(school.address || '');
    setShowEditSchool(true);
  };

  const handleUpdateSchool = async () => {
    if (!editingSchool) return;

    if (!editSchoolName.trim()) {
      toast.error('School name is required');
      return;
    }

    try {
      await updateSchool(Number(editingSchool.id), {
        name: editSchoolName.trim(),
        address: editSchoolAddress.trim(),
      });

      toast.success('School updated successfully');
      setShowEditSchool(false);
      setEditingSchool(null);
      await loadSchools();
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to update school';
      toast.error(message);
    }
  };

  const handleDeleteSchool = async (schoolId: number) => {
    const confirmed = window.confirm('Are you sure you want to delete this school?');
    if (!confirmed) return;

    try {
      await deleteSchool(schoolId);
      toast.success('School deleted successfully');
      await loadSchools();
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to delete school';
      toast.error(message);
    }
  };

  const stats = useMemo(
    () => ({
      totalSchools,
    }),
    [totalSchools]
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      <Toaster />

      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl text-purple-600">
                Sistem Yöneticisi Paneli
              </h1>
              <p className="text-gray-600 mt-1">
                Hoş geldiniz, {displayName} • Tam Sistem Yetkisi
              </p>
            </div>

            <div className="flex gap-2">
              <Button onClick={loadSchools} variant="outline" disabled={loading}>
                <RefreshCw className="h-4 w-4 mr-2" />
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
              <CardTitle className="text-sm">Toplam Okul</CardTitle>
              <Building2 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalSchools}</div>
              <p className="text-xs text-muted-foreground">Sistemde kayıtlı okullar</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">Veritabanı Durumu</CardTitle>
              <Database className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <Badge variant="outline" className="bg-green-50 text-green-700 border-green-300">
                Bağlı
              </Badge>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm">Sistem Rolü</CardTitle>
              <Shield className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <Badge className="bg-red-100 text-red-800">Sistem Yöneticisi</Badge>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="schools" className="space-y-6">
          <TabsList>
            <TabsTrigger value="schools">Okullar</TabsTrigger>
            <TabsTrigger value="system">Sistem</TabsTrigger>
          </TabsList>

          <TabsContent value="schools">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <CardTitle>Okul Yönetimi</CardTitle>
                    <CardDescription>
                      Tüm okulları backend API'sinden yönetin
                    </CardDescription>
                  </div>

                  <Button onClick={() => setShowAddSchool(true)}>
                    <Plus className="h-4 w-4 mr-2" />
                    Okul Ekle
                  </Button>
                </div>
              </CardHeader>

              <CardContent>
                {loading ? (
                  <p className="text-sm text-gray-500">Loading schools...</p>
                ) : schools.length === 0 ? (
                  <p className="text-sm text-gray-500">No schools found.</p>
                ) : (
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>ID</TableHead>
                        <TableHead>Okul Adı</TableHead>
                        <TableHead>Adres</TableHead>
                        <TableHead>Oluşturulma Tarihi</TableHead>
                        <TableHead>İşlemler</TableHead>
                      </TableRow>
                    </TableHeader>

                    <TableBody>
                      {schools.map((school) => (
                        <TableRow key={school.id}>
                          <TableCell>{school.id}</TableCell>
                          <TableCell>{school.name}</TableCell>
                          <TableCell>{school.address || '—'}</TableCell>
                          <TableCell>
                            {(school.created_at || school.createdAt)
                              ? new Date(school.created_at || school.createdAt || '').toLocaleDateString()
                              : '—'}
                          </TableCell>
                          <TableCell>
                            <div className="flex gap-2">
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleOpenEdit(school)}
                              >
                                <Pencil className="h-4 w-4 mr-1" />
                                Düzenle
                              </Button>

                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleDeleteSchool(Number(school.id))}
                              >
                                <Trash2 className="h-4 w-4 mr-1" />
                                Sil
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="system">
            <Card>
              <CardHeader>
                <CardTitle>Sistem Bilgileri</CardTitle>
                <CardDescription>Mevcut frontend-backend entegrasyon durumu</CardDescription>
              </CardHeader>

              <CardContent className="space-y-3">
                <div className="flex justify-between py-2 border-b">
                  <span className="text-sm text-gray-600">Frontend</span>
                  <Badge variant="outline" className="bg-green-50 text-green-700 border-green-300">
                    Çalışıyor
                  </Badge>
                </div>

                <div className="flex justify-between py-2 border-b">
                  <span className="text-sm text-gray-600">Backend API</span>
                  <Badge variant="outline" className="bg-green-50 text-green-700 border-green-300">
                    Bağlı
                  </Badge>
                </div>

                <div className="flex justify-between py-2 border-b">
                  <span className="text-sm text-gray-600">JWT Auth</span>
                  <Badge variant="outline" className="bg-green-50 text-green-700 border-green-300">
                    Aktif
                  </Badge>
                </div>

                <div className="flex justify-between py-2">
                  <span className="text-sm text-gray-600">Okul CRUD</span>
                  <Badge variant="outline" className="bg-green-50 text-green-700 border-green-300">
                    Yetkilendirildi
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>

      <Dialog open={showAddSchool} onOpenChange={setShowAddSchool}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Yeni Okul Ekle</DialogTitle>
            <DialogDescription>Sistemde yeni bir okul oluştur</DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="schoolName">Okul Adı</Label>
              <Input
                id="schoolName"
                value={newSchoolName}
                onChange={(e) => setNewSchoolName(e.target.value)}
                placeholder="Okul adını girin"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="schoolAddress">Address</Label>
              <Input
                id="schoolAddress"
                value={newSchoolAddress}
                onChange={(e) => setNewSchoolAddress(e.target.value)}
                placeholder="Okul adresini girin"
              />
            </div>

            <div className="flex gap-2 justify-end">
              <Button variant="outline" onClick={() => setShowAddSchool(false)}>
                İptal
              </Button>
              <Button onClick={handleAddSchool}>Okul Ekle</Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      <Dialog open={showEditSchool} onOpenChange={setShowEditSchool}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Okul Düzenle</DialogTitle>
            <DialogDescription>Okul bilgilerini güncelle</DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="editSchoolName">Okul Adı</Label>
              <Input
                id="editSchoolName"
                value={editSchoolName}
                onChange={(e) => setEditSchoolName(e.target.value)}
                placeholder="Okul adını girin"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="editSchoolAddress">Okul Adresi</Label>
              <Input
                id="editSchoolAddress"
                value={editSchoolAddress}
                onChange={(e) => setEditSchoolAddress(e.target.value)}
                placeholder="Okul adresini girin"
              />
            </div>

            <div className="flex gap-2 justify-end">
              <Button
                variant="outline"
                onClick={() => {
                  setShowEditSchool(false);
                  setEditingSchool(null);
                }}
              >
                İptal
              </Button>
              <Button onClick={handleUpdateSchool}>Değişiklikleri Kaydet</Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}