import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const edge=process.env.STUDIO_BROWSER || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const browser=await chromium.launch({executablePath:await fs.access(edge).then(()=>edge).catch(()=>undefined),headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
const base=process.env.PECKING_ORDER_URL || 'http://127.0.0.1:8773';
async function open(id){await page.locator(`#${id}-trigger`).click();return page.locator(`#${id}`).locator('..');}
try {
  await page.goto(base);await page.waitForFunction(()=>document.querySelector('#system')?.options.length>200);
  for(const id of ['system','theme','family']) {
    const wrapper=await open(id);
    const count=await page.locator(`#${id} option`).count();
    assert.equal(await wrapper.locator('[role=option]').count(),count,'Every option exists before any scrolling');
    assert.equal(await wrapper.locator('.combo-list').evaluate(el=>el.scrollTop),0);
    assert.ok(await wrapper.locator('[role=option]').first().isVisible());
    await page.screenshot({path:`output/screenshots/combobox-${id}.png`});
    await wrapper.locator('input').press('Escape');
  }
  let wrapper=await open('system');await wrapper.locator('input').fill('street_gang');
  assert.equal(await wrapper.locator('[role=option]').count(),1);
  await wrapper.locator('input').press('Enter');assert.equal(await page.locator('#system').inputValue(),'street_gang');
  assert.match(await page.locator('#system-trigger').textContent(),/rue/i);
  wrapper=await open('theme');await wrapper.locator('input').fill('tswana');await wrapper.locator('input').press('Enter');
  assert.equal(await page.locator('#theme').inputValue(),'tswana');
  await page.selectOption('#locale','en');await page.waitForFunction(()=>document.querySelector('#system-trigger')?.textContent==='Street gang');
  await page.goto(`${base}/glossary`);await page.waitForFunction(()=>document.querySelector('#theme')?.options.length>60);
  wrapper=await open('theme');assert.equal(await wrapper.locator('[role=option]').count(),await page.locator('#theme option').count());
  await wrapper.locator('input').press('End');await wrapper.locator('input').press('Enter');
  assert.equal(await page.locator('#theme').inputValue(),await page.locator('#theme option').last().getAttribute('value'));
  await page.setViewportSize({width:390,height:844});wrapper=await open('theme');
  const box=await wrapper.locator('.combo-panel').boundingBox();assert.ok(box.x>=0 && box.x+box.width<=390 && box.y>=0 && box.y+box.height<=844);
  await page.screenshot({path:'output/screenshots/combobox-mobile.png'});
  await page.goto(`${base}/glossary?theme=tswana&system=street_gang&q=Chef%20de%20bande`);
  await page.waitForFunction(()=>document.querySelector('#entries')?.textContent.includes('Chef de bande'));
  assert.ok(await page.locator('#entries').textContent().then(text=>text.includes('Gang leader')),'Context-specific roles stay visible when a culture is selected');
  assert.deepEqual(errors,[]);console.log('Combobox checks passed: all options before scroll, search, keyboard, selection, FR/EN, both pages and mobile bounds.');
}finally{await browser.close();}
