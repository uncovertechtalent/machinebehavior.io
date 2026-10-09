// Inside docs: the page tree on small screens, the active heading in "On this page", and a "report an issue" link
// that opens a prefilled GitHub issue for the page. Search lives in the top bar (/inside/bar.js).
(function () {
  function el(tag, attrs, kids) {
    var e = document.createElement(tag);
    for (var k in attrs || {}) { if (k === 'text') e.textContent = attrs[k]; else e.setAttribute(k, attrs[k]); }
    (kids || []).forEach(function (c) { e.appendChild(c); });
    return e;
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
})();
