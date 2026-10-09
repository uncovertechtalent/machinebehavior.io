// Inside status: reads the records this site already publishes and sets the state of each service.
// Sources: each site's /conformity/latest.json, /inside/deploys.json (written by the deploy job), and the map snapshot time
// in /inside/search.json. The service list and its sources come from the page (#st-cfg), built from services/*.yml.
(function () {
  var cfg = JSON.parse(document.getElementById('st-cfg').textContent);
  var getJSON = function (u) { return fetch(u, {cache: 'no-cache'}).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }); };
  var ago = function (t) {
    var s = (Date.now() - new Date(t).getTime()) / 1000;
    if (s < 90) return 'just now'; if (s < 5400) return Math.round(s / 60) + ' min ago';
    if (s < 129600) return Math.round(s / 3600) + ' h ago'; return Math.round(s / 86400) + ' d ago';
  };
  var RANK = {ok: 0, none: 1, warn: 2, bad: 3};
  var gateUrls = cfg.map(function (c) { return c.gate; }).filter(function (u, i, a) { return u && a.indexOf(u) === i; });
  var gates = {};
  var pGates = Promise.all(gateUrls.map(function (u) {
    return getJSON(u).then(function (d) { gates[u] = d; }).catch(function () { gates[u] = null; });
  }));
  var deploys = null, mapAt = null;
  var pDeploys = getJSON('/inside/deploys.json').then(function (d) { deploys = d; }).catch(function () {});
  var pMap = cfg.some(function (c) { return c.map; }) ? getJSON('/inside/search.json').then(function (d) { mapAt = d.map_generated; }).catch(function () {}) : Promise.resolve();

  function lastRun(repo) {
    if (!deploys || !deploys.repos || !deploys.repos[repo]) return null;
    var runs = deploys.repos[repo].filter(function (r) { return r.name === 'Conformity' && r.status === 'completed'; });
    runs.sort(function (a, b) { return b.updated_at.localeCompare(a.updated_at); });
    return runs[0] || null;
  }

  Promise.all([pGates, pDeploys, pMap]).then(function () {
    var counts = {ok: 0, warn: 0, bad: 0, none: 0};
    cfg.forEach(function (c) {
      var li = document.getElementById(c.id);
      if (!li) return;
      var level = null, text = null, why = [];
      function set(l, t) { if (level === null || RANK[l] > RANK[level]) { level = l; text = t; } }
      if (c.gate) {
        var g = gates[c.gate];
        if (!g) { if (c.site) set('bad', 'Outage'); else set('none', 'No record'); why.push('gate record did not load'); }
        else if (g.overall === 'pass') { set('ok', 'Operational'); why.push('gate pass ' + ago(g.last_run)); }
        else { set('warn', 'Degraded'); why.push('gate ' + g.overall + ': new deploys blocked, previous build live'); }
      }
      if (c.deploys) {
        var r = lastRun(c.deploys);
        if (!r) { if (level === null) set('none', 'No record'); why.push('no run in the deploy feed'); }
        else if (r.conclusion === 'success') {
          set('ok', 'Operational');
          why.push('last deploy ' + ago(r.updated_at) + ', ' + Math.round((new Date(r.updated_at) - new Date(r.run_started_at)) / 1000) + ' s push to live');
        } else { set('warn', 'Degraded'); why.push('last run ' + r.conclusion + ' ' + ago(r.updated_at)); }
      }
      if (c.map) {
        if (!mapAt) { if (level === null) set('none', 'No record'); }
        else {
          var age = (Date.now() - new Date(mapAt.replace('Z', ':00Z')).getTime()) / 86400000;
          if (age > 8) set('warn', 'Degraded'); else set('ok', 'Operational');
          why.push('map crawled ' + ago(mapAt.replace('Z', ':00Z')));
        }
      }
      if (c.incident) set('warn', 'Degraded');
      if (level === null) { level = 'none'; text = 'No live check'; }
      counts[level]++;
      li.querySelector('[data-light]').className = 'light ' + level;
      li.querySelector('[data-state]').textContent = text;
      if (why.length) {
        var w = li.querySelector('.st-why');
        w.insertBefore(document.createTextNode(why.join(' · ') + ' · '), w.firstChild);
      }
    });
    var checked = counts.ok + counts.warn + counts.bad, ov = document.getElementById('ov-text'), light = document.getElementById('ov-light');
    if (counts.bad) { ov.textContent = counts.bad + ' of ' + checked + ' checked services down'; light.className = 'light bad'; }
    else if (counts.warn) { ov.textContent = counts.warn + ' of ' + cfg.length + (cfg.length === 1 ? ' service' : ' services') + ' degraded'; light.className = 'light warn'; }
    else { ov.textContent = 'All ' + checked + ' checked services operational'; light.className = 'light ok'; }
    document.getElementById('ov-asof').textContent = counts.none + ' without a live check' + (deploys && deploys.generated ? ' · deploy feed ' + ago(deploys.generated) : '');
  });
})();
