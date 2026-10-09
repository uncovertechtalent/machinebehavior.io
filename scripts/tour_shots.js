// Retake the screenshots of the founder tour (/inside/tour/) from the live pages. ADR-0020.
//
// Needs Node, puppeteer-core and a local Chrome; nothing here is a dependency of the site. Run from a scratch folder:
//   npm install puppeteer-core@23.11.1
//   node /path/to/scripts/tour_shots.js shots
// then crop and compress each PNG into inside/tour/ (1600 px wide, WebP quality 80), for example:
//   magick shots/4-incident.png -crop 1920x830+0+0 +repage -resize 1600x 4-incident.png && cwebp -q 80 -m 6 4-incident.png -o inside/tour/4-incident.webp
//   magick shots/5-gate.png -crop 1920x665+0+280 +repage -resize 1600x 5-gate.png && cwebp -q 80 -m 6 5-gate.png -o inside/tour/5-gate.webp
// and set width and height on each <img> to the new size. Check every line of the tour against the live page before the push.
const puppeteer = require('puppeteer-core');
const out = process.argv[2] || 'shots';
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const SITE = 'https://machinebehavior.io';
const openAndScroll = id => `(()=>{const a=document.getElementById('${id}');a.querySelector('details').open=true;` +
  `window.scrollTo(0,a.getBoundingClientRect().top+window.scrollY-72);})()`;

// w x h is the viewport in CSS pixels; the shot is taken at 1.5x. wait is real time for fetches, d3 layout and frames.
const JOBS = [
  {name: '1-inside', url: SITE + '/inside/', h: 820, wait: 7000},
  {name: '2-service', url: SITE + '/inside/services/local-llm/', w: 1040, h: 1080, wait: 2500},
  {name: '3-adr', url: SITE + '/inside/docs/eng/adr-0002-deploy-is-gated/', h: 780, wait: 2500},
  {name: '4-incident', url: SITE + '/inside/status/', h: 780, wait: 4000, js: openAndScroll('2026-10-09-phantom-spend-counters')},
  {name: '5-gate', url: 'https://github.com/uncovertechtalent/machinebehavior.io/actions/runs/37789638737', h: 800, wait: 4000},
  {name: '6-finops', url: SITE + '/inside/docs/fin/showback/', h: 800, wait: 2500},
  {name: '6-map', url: SITE + '/map/', h: 800, wait: 15000},
];

const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  require('fs').mkdirSync(out, {recursive: true});
  const browser = await puppeteer.launch({executablePath: CHROME, headless: 'new', args: ['--hide-scrollbars', '--force-color-profile=srgb']});
  for (const j of JOBS) {
    const page = await browser.newPage();
    await page.setViewport({width: j.w || 1280, height: j.h || 800, deviceScaleFactor: 1.5});
    await page.goto(j.url, {waitUntil: 'networkidle0', timeout: 90000}).catch(e => console.log(j.name, 'load:', e.message));
    await sleep(j.wait);
    if (j.js) { await page.evaluate(j.js); await sleep(1500); }
    await page.screenshot({path: `${out}/${j.name}.png`});
    console.log(j.name, 'ok');
    await page.close();
  }
  await browser.close();
})();
