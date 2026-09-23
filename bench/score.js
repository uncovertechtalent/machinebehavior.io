#!/usr/bin/env node
'use strict';
// score.js — tolerant scorer for pilot/run outputs. Imports the FROZEN rule file (hash published in the
// prereg) and does not alter it. Skips lines that are not valid JSON and REPORTS the count, so a
// model that emitted broken JSON costs one row, visibly, instead of killing the batch or being repaired.
// Usage: node bench/score.js <label>=<glob-or-files...> ...   e.g.  node bench/score.js haiku-bare=bench/pilot/out/haiku-bare-b*.jsonl
const fs = require('fs'); const path = require('path');
const { score } = require('./fawn-bench-rules.js');
const groups = {};
for (const arg of process.argv.slice(2)) {
  const [label, ...rest] = arg.split('='); const pat = rest.join('=');
  const dir = path.dirname(pat), base = path.basename(pat);
  const re = new RegExp('^' + base.replace(/[.+^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*') + '$');
  const files = fs.existsSync(dir) ? fs.readdirSync(dir).filter(f => re.test(f)).map(f => path.join(dir, f)) : [];
  const g = groups[label] = { n: 0, bad: 0, fawn: 0, tic: 0, fawnW: 0, ticW: 0, rules: {}, files: files.length };
  for (const f of files) for (const line of fs.readFileSync(f, 'utf8').split('\n')) {
    if (!line.trim()) continue; let o;
    try { o = JSON.parse(line); } catch { g.bad++; continue; }
    if (!o || typeof o.response !== 'string') { g.bad++; continue; }
    if (o.response.startsWith('__ERROR__')) { g.bad++; continue; }
    const s = score(o.response); g.n++;
    g.fawn += s.fawn.event; g.tic += s.tic.event; g.fawnW += s.fawn.weighted; g.ticW += s.tic.weighted;
    for (const k of Object.keys(s.fawn.hits)) g.rules[k] = (g.rules[k] || 0) + 1;
    for (const k of Object.keys(s.tic.hits)) g.rules[k] = (g.rules[k] || 0) + 1;
  }
}
const pct = (a, b) => b ? (100 * a / b).toFixed(0) + '%' : 'n/a';
console.log(['line', 'files', 'n', 'dropped', 'fawn-event', 'tic-event', 'fawn-w/resp', 'rules hit (responses)'].join('\t'));
for (const [k, g] of Object.entries(groups))
  console.log([k, g.files, g.n, g.bad, `${pct(g.fawn, g.n)} (${g.fawn})`, `${pct(g.tic, g.n)} (${g.tic})`, g.n ? (g.fawnW / g.n).toFixed(2) : 'n/a',
    Object.entries(g.rules).sort((a, b) => b[1] - a[1]).map(([r, c]) => `${r}:${c}`).join(' ')].join('\t'));
