// Fills the conformity line in the page footer from /conformity/latest.json.
// Static fallback text stays when JavaScript is off or the fetch fails.
(function () {
  var el = document.querySelector('[data-conformity]');
  if (!el) return;
  fetch('/conformity/latest.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (d) {
    var open = 0;
    (d.findings || []).forEach(function (f) { if (f.status === 'open') open++; });
    var when = (d.last_run || '').replace('T', ' ').replace('Z', ' UTC');
    el.innerHTML = 'conformity: <a class="mono" href="/conformity/">last run ' + when + '</a>, ' + open + ' open, ' + (d.overall || 'unknown');
  }).catch(function () {});
})();
