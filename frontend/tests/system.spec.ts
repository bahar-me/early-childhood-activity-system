import { test, expect } from '@playwright/test';

test('teacher can login and see activity dashboard', async ({ page }) => {
  await page.goto('https://early-childhood-activity-system.vercel.app');

  await page.fill('input[type="email"]', 'teacher@test.com');
  await page.fill('input[type="password"]', 'Test123!');

  await page.click('button[type="submit"]');

  await expect(page.getByText('KinderActivity AI')).toBeVisible({
    timeout: 15000,
  });

  await expect(page.getByText(/Tekrar hoş geldin/)).toBeVisible({
    timeout: 15000,
  });
});