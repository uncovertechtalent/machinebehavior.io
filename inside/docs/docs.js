// Inside docs: search over /inside/docs/search.json, the page tree on small screens, the active heading in "On this page".
(function () {
  var q = document.getElementById('q'), hits = document.getElementById('hits');
  var data = null, loading = null, sel = -1;

  function load() {
    if (data) return Promise.resolve(data);
    if (!loading) loading = fetch('/inside/docs/search.json').then(function (r) { return r.json(); }).then(function (d) { data = d; return d; });
    return loading;
  }
  function el(tag, attrs, kids) {
    var e = document.createElement(tag);
    for (var k in attrs || {}) { if (k === 'text') e.textContent = attrs[k]; else e.setAttribute(k, attrs[k]); }
    (kids || []).forEach(function (c) { e.appendChild(c); });
    return e;
  }
  function score(p, terms) {
    var t = p.t.toLowerCase(), d = (p.d || '').toLowerCase(), l = (p.l || []).join(' ').toLowerCase(), x = (p.x || '').toLowerCase(), s = 0;
    for (var i = 0; i < terms.length; i++) {
      var w = terms[i];
      if (t.indexOf(w) === 0) s += 12; else if (t.indexOf(w) >= 0) s += 8;
      else if (l.indexOf(w) >= 0) s += 5; else if (d.indexOf(w) >= 0) s += 3; else if (x.indexOf(w) >= 0) s += 1; else return 0;
    }
    return s;
  }
  function run() {
    var v = q.value.trim().toLowerCase();
    if (!v) { hits.classList.remove('on'); hits.textContent = ''; return; }
    load().then(function (d) {
      var terms = v.split(/\s+/), res = [];
      d.pages.forEach(function (p) { var s = score(p, terms); if (s) res.push([s, p]); });
      res.sort(function (a, b) { return b[0] - a[0] || a[1].t.localeCompare(b[1].t); });
      hits.textContent = ''; sel = -1;
      if (!res.length) hits.appendChild(el('li', {}, [el('div', {class: 'none', text: 'No page matches "' + q.value.trim() + '".'})]));
      res.slice(0, 14).forEach(function (r) {
        var p = r[1], sp = d.spaces[p.s] || {name: p.s, color: '#7D8792'};
        var dot = el('span', {class: 'dot'}); dot.style.background = sp.color;
        var a = el('a', {}, [dot, el('b', {text: p.t}), el('span', {class: 's', text: sp.name}), el('span', {class: 'd', text: p.d || ''})]);
        a.href = p.u;
        hits.appendChild(el('li', {}, [a]));
      });
      hits.classList.add('on');
    });
  }
  if (q) {
    q.addEventListener('focus', load);
    q.addEventListener('input', run);
    q.addEventListener('keydown', function (e) {
      var links = hits.querySelectorAll('a');
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        if (!links.length) return;
        sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + links.length) % links.length;
        links.forEach(function (l, i) { l.classList.toggle('sel', i === sel); });
        links[sel].scrollIntoView({block: 'nearest'});
      } else if (e.key === 'Enter' && links.length) {
        location.href = links[Math.max(sel, 0)].href;
      } else if (e.key === 'Escape') {
        q.value = ''; run(); q.blur();
      }
    });
    document.addEventListener('click', function (e) { if (!e.target.closest('.search')) hits.classList.remove('on'); });
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && document.activeElement !== q && !/input|textarea/i.test(document.activeElement.tagName)) { e.preventDefault(); q.focus(); }
    });
    var m = location.hash.match(/^#q=(.+)$/);
    if (m) { q.value = decodeURIComponent(m[1]); q.focus(); run(); }
  }

  // page tree: collapsed on small screens
  var side = document.querySelector('.side-wrap');
  if (side && window.matchMedia('(max-width: 820px)').matches) side.removeAttribute('open');
  var cur = document.querySelector('.side a[aria-current="page"]');
  if (cur && side && side.open) {
    var box = document.querySelector('.side');
    if (box && cur.offsetTop > box.clientHeight - 80) box.scrollTop = cur.offsetTop - box.clientHeight / 3;
  }

  // on this page: mark the heading in view
  var toc = document.querySelectorAll('.toc a');
  if (toc.length && 'IntersectionObserver' in window) {
    var byId = {};
    toc.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting && byId[en.target.id]) {
          toc.forEach(function (a) { a.classList.remove('on'); });
          byId[en.target.id].classList.add('on');
        }
      });
    }, {rootMargin: '-60px 0px -70% 0px'});
    document.querySelectorAll('.doc h2[id], .doc h3[id]').forEach(function (h) { io.observe(h); });
  }
})();
