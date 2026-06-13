import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Button } from './ui/button';
import { Alert, AlertDescription } from './ui/alert';
import { User } from '../types/user';
import { loginRequest } from '../api/auth';
import { AlertCircle, GraduationCap } from 'lucide-react';

interface LoginPageProps {
  onLogin: (user: User, accessToken: string, refreshToken: string) => void;
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await loginRequest({ email, password });

      onLogin(data.user, data.access_token, data.refresh_token);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Giriş başarısız oldu. Lütfen bilgilerinizi kontrol edip tekrar deneyin.';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const quickFill = (userType: 'teacher' | 'school_admin' | 'system_admin') => {
    if (userType === 'teacher') {
      setEmail('teacher@test.com');
      setPassword('Test123!');
    }

    if (userType === 'school_admin') {
      setEmail('schooladmin@test.com');
      setPassword('Test123!');
    }

    if (userType === 'system_admin') {
      setEmail('admin@test.com');
      setPassword('Test123!');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-purple-600 mb-2">
            KinderActivity AI
          </h1>
          <p className="text-gray-600">
            Anaokulu eğitimi için akıllı etkinlik önerileri
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Oturum Aç</CardTitle>
            <CardDescription>
              Sisteme erişmek için kimlik bilgilerinizi girin
            </CardDescription>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="örnek@okul.com"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Şifre</Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                />
              </div>

              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? 'Oturum açılıyor...' : 'Oturum Aç'}
              </Button>
            </form>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Hızlı Doldurma</CardTitle>
            <CardDescription className="text-xs">
              Otomatik olarak demo backend kullanıcılarını doldur
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-2">
            <Button
              variant="outline"
              className="w-full justify-start"
              onClick={() => quickFill('teacher')}
              type="button"
            >
              <GraduationCap className="h-4 w-4 mr-2" />
              Öğretmen
              <span className="ml-auto text-xs text-gray-500">teacher@test.com</span>
            </Button>

            <Button
              variant="outline"
              className="w-full justify-start"
              onClick={() => quickFill('school_admin')}
              type="button"
            >
              <GraduationCap className="h-4 w-4 mr-2" />
              Okul Yöneticisi
              <span className="ml-auto text-xs text-gray-500">schooladmin@test.com</span>
            </Button>

            <Button
              variant="outline"
              className="w-full justify-start"
              onClick={() => quickFill('system_admin')}
              type="button"
            >
              <GraduationCap className="h-4 w-4 mr-2" />
              Sistem Yöneticisi
              <span className="ml-auto text-xs text-gray-500">admin@test.com</span>
            </Button>
          </CardContent>
        </Card>

        <div className="text-center text-xs text-gray-500">
          <p>Backend demo şifresi: Test123!</p>
        </div>
      </div>
    </div>
  );
}