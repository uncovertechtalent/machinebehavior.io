// Inside top bar: suggestions under the search box from /inside/search.json (one index: docs, services, the map).
// Enter submits the form to /inside/search/ (the results page); it never opens a hit by itself.
// Arrow down moves focus into the suggestions, where Enter follows the focused link. "/" focuses the box.
// The section sidebar (scripts/site_chrome.py) is open in the page source; on narrow screens it sits above the
// content, so it starts closed there.
(function () {
  var side = document.querySelector('.mb-side-wrap');
  if (side && window.matchMedia('(max-width: 1099px)').matches) side.removeAttribute('open');
})();
(function () {
  var data = null, loading = null;

  function load() {
    if (data) return Promise.resolve(data);
    if (!loading) loading = fetch('/inside/search.json').then(function (r) { return r.json(); }).then(function (d) { data = d; return d; });
    return loading;
  }
  function score(p, terms) {
    var t = p.t.toLowerCase(), d = (p.d || '').toLowerCase(), l = (p.l || []).join(' ').toLowerCase(), x = (p.x || '').toLowerCase(), s = 0;
    for (var i = 0; i < terms.length; i++) {
      var w = terms[i], wb = new RegExp('(^|[^a-z0-9])' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '($|[^a-z0-9])');
      if (t.indexOf(w) === 0) s += 12; else if (wb.test(t)) s += 10; else if (t.indexOf(w) >= 0) s += 6;
      else if (l.indexOf(w) >= 0) s += 5; else if (d.indexOf(w) >= 0) s += 3; else if (x.indexOf(w) >= 0) s += 1; else return 0;
    }
    return s + (p.w || 0);
  }
  function search(d, q) {
    var terms = q.trim().toLowerCase().split(/\s+/).filter(Boolean), res = [];
    if (!terms.length) return res;
    d.items.forEach(function (p) { var s = score(p, terms); if (s) res.push([s, p]); });
    res.sort(function (a, b) { return b[0] - a[0] || a[1].t.localeCompare(b[1].t); });
    return res.map(function (r) { return r[1]; });
  }
  function el(tag, attrs, kids) {
    var e = document.createElement(tag);
    for (var k in attrs || {}) { if (k === 'text') e.textContent = attrs[k]; else e.setAttribute(k, attrs[k]); }
    (kids || []).forEach(function (c) { if (c) e.appendChild(c); });
    return e;
  }
  function hitLink(d, p) {
    var g = d.groups[p.g] || {name: p.g, color: '#7D8792'};
    var dot = el('span', {class: 'ib-dot'}); dot.style.background = g.color;
    var a = el('a', {}, [dot, el('b', {text: p.t}), el('span', {class: 'ib-s', text: g.name}), p.d ? el('span', {class: 'ib-d', text: p.d}) : null]);
    a.href = p.u;
    return a;
  }
  window.InsideSearch = {load: load, search: search, hitLink: hitLink, el: el};

  var q = document.getElementById('ib-q'), hits = document.getElementById('ib-hits');
  if (!q || !hits) return;
  var form = q.form;

  function close() { hits.classList.remove('on'); q.setAttribute('aria-expanded', 'false'); }
  function run() {
    var v = q.value.trim();
    if (!v) { close(); hits.textContent = ''; return; }
    load().then(function (d) {
      if (q.value.trim() !== v) return;
      var res = search(d, v);
      hits.textContent = '';
      if (!res.length) hits.appendChild(el('li', {}, [el('div', {class: 'ib-none', text: 'Nothing matches "' + v + '".'})]));
      res.slice(0, 8).forEach(function (p) { hits.appendChild(el('li', {}, [hitLink(d, p)])); });
      var all = el('a', {class: 'ib-all', text: res.length > 8 ? 'All ' + res.length + ' results for "' + v + '"' : 'Open the results page'});
      all.href = '/inside/search/?q=' + encodeURIComponent(v);
      hits.appendChild(el('li', {}, [all]));
      hits.classList.add('on'); q.setAttribute('aria-expanded', 'true');
    });
  }
  q.setAttribute('aria-expanded', 'false');
  q.addEventListener('focus', load);
  q.addEventListener('input', run);
  q.addEventListener('keydown', function (e) {
    var links = hits.querySelectorAll('a');
    if (e.key === 'ArrowDown' && links.length && hits.classList.contains('on')) { e.preventDefault(); links[0].focus(); }
    else if (e.key === 'Escape') { if (hits.classList.contains('on')) close(); else { q.value = ''; q.blur(); } }
  });
  hits.addEventListener('keydown', function (e) {
    var links = Array.prototype.slice.call(hits.querySelectorAll('a')), i = links.indexOf(document.activeElement);
    if (e.key === 'ArrowDown') { e.preventDefault(); if (i < links.length - 1) links[i + 1].focus(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); if (i > 0) links[i - 1].focus(); else q.focus(); }
    else if (e.key === 'Escape') { e.preventDefault(); close(); q.focus(); }
  });
  form.addEventListener('submit', function (e) { if (!q.value.trim()) e.preventDefault(); });
  document.addEventListener('click', function (e) { if (!e.target.closest('.mb-search')) close(); });
  document.addEventListener('focusin', function (e) { if (!e.target.closest || !e.target.closest('.mb-search')) close(); });
  document.addEventListener('keydown', function (e) {
    var a = document.activeElement;
    if (e.key === '/' && a !== q && !/^(input|textarea|select)$/i.test(a.tagName) && !a.isContentEditable) { e.preventDefault(); q.focus(); q.select(); }
  });
  // old docs label links used /inside/docs/#q=label
  var m = location.hash.match(/^#q=(.+)$/);
  if (m) location.replace('/inside/search/?q=' + m[1]);
  // on the results page the box shows the query
  var pq = new URLSearchParams(location.search).get('q');
  if (pq && location.pathname === '/inside/search/') q.value = pq;
})();
