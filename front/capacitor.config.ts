import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'ru.emk.intranet',
  appName: 'intranetEMK',
  webDir: 'dist',
  server: {
    allowNavigation: [
      'intranet.emk.ru',
      'intranet.emk.org.ru',
      'portal.emk.ru',
      'test-portal.emk.ru'
    ]
  }
};

export default config;
