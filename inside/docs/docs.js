// Inside docs: the page tree on small screens, the active heading in "On this page", and a "report an issue" link
// that opens a prefilled GitHub issue for the page. Search lives in the top bar (/inside/bar.js).
(function () {
  function el(tag, attrs, kids) {
    var e = document.createElement(tag);
    for (var k in attrs || {}) { if (k === 'text') e.textContent = attrs[k]; else e.setAttribute(k, attrs[k]); }
    (kids || []).forEach(function (c) { e.appendChild(c); });
    return e;
  }
  // page tree: collapsed on small screens. Above 820 px its summary is hidden, so a tree closed on a narrow load could
  // not be opened again: it opens when the window grows past that width (scripts/test_docs_tree.mjs). An open tree
  // scrolls the current page into view. Safari before 14 has addListener only; a call to a missing addEventListener
  // would throw and stop the rest of this script ("on this page", "report an issue").
  var side = document.querySelector('.side-wrap');
  function reveal() {
    var cur = document.querySelector('.side a[aria-current="page"]'), box = document.querySelector('.side');
    if (cur && box && cur.offsetTop > box.clientHeight - 80) box.scrollTop = cur.offsetTop - box.clientHeight / 3;
  }
  if (side) {
    var narrow = window.matchMedia('(max-width: 820px)');
    if (narrow.matches) side.removeAttribute('open');
    if (side.open) reveal();
    var onChange = function (e) { if (!e.matches && !side.open) { side.setAttribute('open', ''); reveal(); } };
    if (narrow.addEventListener) narrow.addEventListener('change', onChange);
    else if (narrow.addListener) narrow.addListener(onChange);
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

  // report an issue: a new GitHub issue with the page title and URL filled in. Built here, not in the page
  // source, so the crawler does not count one GitHub link per page.
  var h1 = location.pathname.indexOf('/inside/docs/') === 0 && document.querySelector('main h1');
  if (h1) {
    var title = h1.textContent.trim(), canon = document.querySelector('link[rel="canonical"]');
    var page = canon ? canon.href : location.href.split('#')[0];
    var rep = el('a', {class: 'report', text: 'report an issue'});
    rep.href = 'https://github.com/uncovertechtalent/machinebehavior.io/issues/new?title=' + encodeURIComponent('Docs: ' + title) +
      '&body=' + encodeURIComponent('Page: ' + title + '\n' + page + '\n\nWhat is wrong or missing:\n\n');
    rep.target = '_blank'; rep.rel = 'noopener';
    var by = document.querySelector('.byline');
    if (by) by.appendChild(rep);
    else h1.insertAdjacentElement('afterend', el('div', {class: 'byline'}, [rep]));
  }

  // on-call snapshot (#36, ADR-0037): the docs build embeds the committed copy; the deploy job writes a fresh
  // /inside/oncall/oncall.json, whose html comes from the same renderer (scripts/build_oncall.py). Same origin only.
  var oncall = document.querySelectorAll('[data-oncall-src]');
  if (oncall.length && typeof fetch === 'function') {
    fetch(oncall[0].getAttribute('data-oncall-src'), {cache: 'no-store'})
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d || typeof d.html !== 'string' || d.html.indexOf('<div class="oncall-snapshot">') !== 0) return;
        oncall.forEach(function (box) { box.innerHTML = d.html; });
      })
      .catch(function () {});
  }
})();
