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
      const message = err instanceof Error ? err.message : 'Login failed';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const quickFill = (userType: 'teacher' | 'school_admin' | 'system_admin') => {
    if (userType === 'teacher') {
      setEmail('teacher@test.com');
      setPassword('123456');
    }

    if (userType === 'school_admin') {
      setEmail('schooladmin@test.com');
      setPassword('123456');
    }

    if (userType === 'system_admin') {
      setEmail('admin@test.com');
      setPassword('123456');
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
            Smart activity recommendations for kindergarten education
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Sign In</CardTitle>
            <CardDescription>
              Enter your credentials to access the system
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
                  placeholder="your.email@school.com"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
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
                {loading ? 'Signing in...' : 'Sign In'}
              </Button>
            </form>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Quick Fill</CardTitle>
            <CardDescription className="text-xs">
              Automatically fill demo backend users
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
              Teacher
              <span className="ml-auto text-xs text-gray-500">teacher@test.com</span>
            </Button>

            <Button
              variant="outline"
              className="w-full justify-start"
              onClick={() => quickFill('school_admin')}
              type="button"
            >
              <GraduationCap className="h-4 w-4 mr-2" />
              School Admin
              <span className="ml-auto text-xs text-gray-500">schooladmin@test.com</span>
            </Button>

            <Button
              variant="outline"
              className="w-full justify-start"
              onClick={() => quickFill('system_admin')}
              type="button"
            >
              <GraduationCap className="h-4 w-4 mr-2" />
              System Admin
              <span className="ml-auto text-xs text-gray-500">admin@test.com</span>
            </Button>
          </CardContent>
        </Card>

        <div className="text-center text-xs text-gray-500">
          <p>Backend demo password: 123456</p>
        </div>
      </div>
    </div>
  );
}