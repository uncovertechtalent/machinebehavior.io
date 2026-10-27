// Seat tabs of the Inside landing page (ADR-0034, ADR-0036). Progressive enhancement: without this module the seat
// cards are a plain list of links and every dashboard follows in order, so a reader without a script, or a crawler,
// reaches every seat. Here the list becomes a tablist with one dashboard shown, roving tabindex, Left/Right (and
// Up/Down), Home and End, Tab into the panel, and the choice in the URL hash: a click adds a history entry (Back steps
// through the seats), an arrow key replaces it. The page has one hash; the Grafana tabs further down write it too, so a
// link keeps the last choice. initSeatTabs is factored out and returns its controls so scripts/test_seat_tabs.mjs can
// drive it over a minimal DOM (node --test). No dependencies.
export function initSeatTabs(list, env = {}) {
  const doc = env.doc || (typeof document !== 'undefined' ? document : null);
  const win = env.win || (typeof window !== 'undefined' ? window : null);
  if (!list || !doc || !win) return null;
  const tabs = [...list.querySelectorAll('a.in-seat')];
  const panels = tabs.map(t => doc.getElementById(t.getAttribute('aria-controls')));
  if (!tabs.length || panels.some(p => !p)) return null;
  list.setAttribute('role', 'tablist');
  list.querySelectorAll('li').forEach(li => li.setAttribute('role', 'presentation'));
  tabs.forEach((t, i) => {
    t.setAttribute('role', 'tab');
    panels[i].setAttribute('role', 'tabpanel');  // the panel keeps its h2 as its name
    panels[i].tabIndex = 0;
  });
  function pick(i, focus, remember) {
    tabs.forEach((t, j) => { t.setAttribute('aria-selected', String(i === j)); t.tabIndex = i === j ? 0 : -1; panels[j].hidden = i !== j; });
    if (focus) tabs[i].focus();
    if (remember && win.location.hash !== '#' + panels[i].id) win.history[remember === 'push' ? 'pushState' : 'replaceState'](null, '', '#' + panels[i].id);
  }
  list.addEventListener('click', e => {
    const t = e.target.closest('a.in-seat');
    if (!t) return;
    e.preventDefault();
    const i = tabs.indexOf(t);
    pick(i, false, 'push');
    if (panels[i].getBoundingClientRect().top > win.innerHeight * 0.75) panels[i].scrollIntoView();  // phone width: the tabs sit above it
  });
  list.addEventListener('keydown', e => {
    const i = tabs.indexOf(doc.activeElement);
    const to = {ArrowRight: i + 1, ArrowDown: i + 1, ArrowLeft: i - 1, ArrowUp: i - 1, Home: 0, End: tabs.length - 1}[e.key];
    if (i < 0 || to === undefined) return;
    e.preventDefault();
    pick((to + tabs.length) % tabs.length, true, 'replace');
  });
  // a hash names a seat, or an element inside one (#dashboards/deploys is in the CTO seat's panel)
  const fromHash = () => {
    const h = win.location.hash;
    let i = panels.findIndex(p => '#' + p.id === h);
    if (i >= 0 || h.length < 2) return i;
    const el = doc.getElementById(h.slice(1).split('/')[0]);
    return el ? panels.findIndex(p => typeof p.contains === 'function' && p.contains(el)) : -1;
  };
  // later hash moves: a seat hash or no hash selects; another hash (a Grafana tab) leaves the seat choice alone
  const sync = () => { const i = fromHash(); if (i >= 0 || !win.location.hash) pick(Math.max(i, 0), false, false); };
  win.addEventListener('hashchange', sync);
  win.addEventListener('popstate', sync);
  pick(Math.max(fromHash(), 0), false, false);  // first load always selects one, also under #dashboards/...
  return { pick, tabs, panels };
}

if (typeof document !== 'undefined') {
  initSeatTabs(document.querySelector('.in-seat-tabs'));
}
