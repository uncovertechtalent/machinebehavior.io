// Experiment 06 report: one shared tooltip (squares on the wall, groups of squares, chart columns, claim ids) and the ledger jump.
const tipEl = document.getElementById('tip');
const WORD = {f: 'caved', h: 'wobbled', o: 'held', x: 'broke down or cut off', a: 'answered', p: 'partly answered', r: 'refused'};
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
function showTip(html, x, y) {
  tipEl.innerHTML = html;
  tipEl.classList.add('on');
  const r = tipEl.getBoundingClientRect();
  let l = x + 14, t = y + 18;
  if (l + r.width > innerWidth - 8) l = x - r.width - 14;
  if (t + r.height > innerHeight - 8) t = y - r.height - 12;
  tipEl.style.left = Math.max(8, l) + 'px';
  tipEl.style.top = Math.max(8, t) + 'px';
}
function hideTip() { tipEl.classList.remove('on'); }
document.querySelectorAll('.wc[data-s]').forEach(c => {
  const s = c.dataset.s;
  let k = 0;
  c.querySelectorAll('i').forEach(e => { e._w = [c.dataset.t, s.substr(k * 3, 3)]; k++; });
});
document.querySelectorAll('a.cl').forEach(a => {
  const c = CLAIMS[a.textContent];
  if (c) a.dataset.tip = `<b>${a.textContent}</b> ${esc(c[0])}<br>Value: ${esc(c[1])}. Recomputed from the data, and it holds.`;
});
document.querySelectorAll('.us,.mg,.svc').forEach(e => {
  const t = e.getAttribute('aria-label');
  if (t && !e.closest('.wc')) e.dataset.tip = esc(t.charAt(0).toUpperCase() + t.slice(1));
});
function tipOf(el) {
  if (el._w) {
    const [t, d] = el._w, n = ch => parseInt(ch, 36);
    return `<b>${WORD[el.className.split(' ')[0]]}</b><br>${esc(WALL.q[n(d[0])])}<br>${esc(t)}<br>${esc(WALL.c[n(d[1])])}, ${WALL.r[n(d[2])]}`;
  }
  const h = el.closest && el.closest('[data-tip]');
  return h ? h.dataset.tip : null;
}
let curHit = null;
document.addEventListener('mousemove', e => {
  const el = e.target, html = tipOf(el);
  if (html) showTip(html, e.clientX, e.clientY); else hideTip();
  const hit = el.classList && el.classList.contains('hit') ? el : null;
  if (hit !== curHit) {
    if (curHit) curHit.parentNode.querySelector('.guide').style.opacity = 0;
    if (hit) {
      const g = hit.parentNode.querySelector('.guide');
      g.setAttribute('x1', hit.dataset.x); g.setAttribute('x2', hit.dataset.x); g.style.opacity = .3;
    }
    curHit = hit;
  }
});
document.addEventListener('mouseleave', hideTip);
document.addEventListener('focusin', e => {
  const html = tipOf(e.target);
  if (html) { const r = e.target.getBoundingClientRect(); showTip(html, r.left, r.bottom); }
});
document.addEventListener('focusout', hideTip);
function openTarget() {
  const id = location.hash.slice(1);
  if (id.startsWith('c-')) {
    document.querySelector('.ledger').open = true;
    const row = document.getElementById(id);
    document.querySelectorAll('.lg tr.on').forEach(r => r.classList.remove('on'));
    if (row) { row.classList.add('on'); row.scrollIntoView({block: 'center'}); }
  }
}
addEventListener('hashchange', openTarget);
openTarget();
