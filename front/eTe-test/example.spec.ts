// test('test', async ({ page }) => {
//   await page.goto('localhost:5173');
//   await page.getByRole('textbox').first().click();
//   await page.getByRole('textbox').first().fill('gazinskii.iv');
//   await page.getByRole('textbox').first().press('Tab');
//   await page.getByRole('textbox').first().fill('gazinskii.i.v');
//   await page.getByRole('textbox').first().press('Tab');
//   await page.getByRole('textbox').nth(1).fill('B(tu0xm5)');
//   await page.getByRole('button', { name: 'Войти' }).click();
//   await page.getByText('Капитал ЭМК').click();
//   await page.getByText('Магазин мерча').click();
//   await page.getByRole('link', { name: 'Gallery image Блокнот А5 ЭМК' }).click();
//   await page.locator('.merch-store-item__action__button').click();
//   await page.locator('.modal__overlay > .modal__overlay__close-button').click();
//   await page.getByRole('link', { name: 'Энергомашкомплект' }).click();
//   await page.getByRole('link', { name: 'С Днём Рождения!' }).click();
// });