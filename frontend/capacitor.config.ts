import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.bahar.earlychildhood',
  appName: 'Early Childhood Activity System',
  webDir: 'dist',
  server:{
  androidScheme: 'http',
  cleartext: true,
  },
};

export default config;
