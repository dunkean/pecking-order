import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const output = path.join(root, 'output', 'screenshots');
await fs.mkdir(output, { recursive: true });
const edge = process.env.STUDIO_BROWSER || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const executablePath = await fs.access(edge).then(() => edge).catch(() => undefined);
const browser = await chromium.launch({ executablePath, headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
const errors = [];
page.on('pageerror', error => errors.push(error.message));
page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });

async function contains(selector, text) {
  await page.waitForFunction(({ selector, text }) => document.querySelector(selector)?.textContent.includes(text), { selector, text });
}
async function example(name, title) {
  await page.locator(`[data-example="${name}"]`).click();
  await contains('#roles', title);
}
try {
  await page.goto(process.env.PECKING_ORDER_URL || 'http://127.0.0.1:8773');
  await contains('#roles', 'Tsar');
  await page.locator('.role').first().locator('summary').click();
  await contains('.role-body', 'lois');
  await page.screenshot({ path: path.join(output, 'nation-east-fr.png'), fullPage: true });
  await page.screenshot({ path: path.join(output, 'demo.png') });
  await example('west', 'Roi');
  await page.selectOption('#locale', 'en');
  await contains('#roles', 'King');
  await example('tswana', 'Kgosi');
  await contains('#roles', 'Kgotla');
  await example('cult', 'Ritual Celebrant');
  assert.equal(await page.locator('#roles .role').count(), 4);
  await example('family', 'Karta');
  await contains('#roles', 'Kulapati');
  await page.click('#view-lexicon');
  await contains('#lexicon', 'Karta');
  assert.ok(await page.locator('#lexicon tbody tr').count() >= 96);
  await page.click('#view-roles');
  await example('east', 'Tsar');
  const allRoleCount = await page.locator('#roles .role').count();
  await page.fill('#role-search', 'tsar');
  await page.waitForFunction(maximum => {
    const rows = [...document.querySelectorAll('#roles .role')];
    return rows.length > 0 && rows.length < maximum && rows.every(row => row.textContent.toLowerCase().includes('tsar'));
  }, allRoleCount);
  await page.fill('#role-search', '');
  await contains('#roles', 'Kniaz');
  const downloadEvent = page.waitForEvent('download');
  await page.click('#export-query');
  const download = await downloadEvent;
  const requestPath = path.join(output, 'request.json');
  await download.saveAs(requestPath);
  const request = JSON.parse(await fs.readFile(requestPath, 'utf8'));
  assert.equal(request.system, 'aristocratic_nation');
  await example('tswana', 'Kgosi');
  await page.setInputFiles('#import-query', requestPath);
  await contains('#roles', 'Tsar');
  await page.setInputFiles('#import-query', {
    name: 'alias-request.json', mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({ system: 'royaume', theme: 'Europe de l’Est', locale: 'fr' }))
  });
  await contains('#result-heading', 'Royaume');
  await contains('#roles', 'Tsar');
  await page.selectOption('#locale', 'fr');
  await contains('h1', 'Un système');
  await page.setViewportSize({ width: 390, height: 844 });
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  await page.screenshot({ path: path.join(output, 'mobile-fr.png'), fullPage: true });
  assert.deepEqual(errors, []);
  console.log('Browser checks passed: Eastern/Western nation, Tswana village, four-person cell, joint family, FR/EN, lexicon, filters, export/import and mobile.');
} finally {
  await browser.close();
}
