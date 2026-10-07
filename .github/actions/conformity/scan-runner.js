'use strict';
// scan-runner.js: run the vendored rule table over published pages.
// Input (stdin, JSON): {"files": [...paths...], "tiers": {"rule-name": "block"|"warn"|"off"}}
// Output (stdout, JSON): {"files": n, "rules": [{name, tier}], "hits": [{rule, tier, file, line, snippet}]}
//
// Exemptions (a mention is not a use): script and style elements; blockquote,
// pre, code and q elements; spans and anchors with class "mono"; text inside
// double quotes ("..." or typographic) up to 240 characters; Markdown fenced
// and inline code and quoted lines (stripExempt from the rule table).
const fs = require('fs');
const path = require('path');
const table = require(path.join(__dirname, 'rules', 'vestige-patterns.js'));

function readStdin() {
  return fs.readFileSync(0, 'utf8');
}

function htmlToText(html) {
  let t = html;
  t = t.replace(/<(script|style)[\s\S]*?<\/\1>/gi, ' ');
  t = t.replace(/<(blockquote|pre|code|q)\b[\s\S]*?<\/\1>/gi, ' ');
  t = t.replace(/<(span|a)\b[^>]*class="[^"]*\bmono\b[^"]*"[^>]*>[\s\S]*?<\/\1>/gi, ' ');
  t = t.replace(/<br\s*\/?>/gi, '\n').replace(/<\/(p|div|li|h[1-6]|tr|td|th|dt|dd|section|header)>/gi, '\n');
  t = t.replace(/<[^>]+>/g, ' ');
  t = t.replace(/&quot;/g, '"').replace(/&#39;|&rsquo;|&lsquo;/g, "'").replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&hellip;/g, '...').replace(/&nbsp;/g, ' ');
  return t;
}

function exemptQuoted(text) {
  // Remove quoted spans: straight or typographic double quotes, no newline inside, up to 240 chars.
  return text.replace(/["“]([^"“”\n]{1,240})["”]/g, ' ');
}

function main() {
  const input = JSON.parse(readStdin());
  const tiers = input.tiers || {};
  const rules = [];
  for (const r of table.BLOCK_RULES) rules.push({ rule: r, tier: tiers[r.name] || 'block' });
  for (const r of table.WARN_RULES) rules.push({ rule: r, tier: tiers[r.name] || 'warn' });
  const hits = [];
  for (const f of input.files) {
    let raw = fs.readFileSync(f, 'utf8');
    let text = /\.html?$/i.test(f) ? htmlToText(raw) : raw;
    text = table.stripExempt(exemptQuoted(text));
    const lines = text.split('\n');
    for (const { rule, tier } of rules) {
      if (tier === 'off') continue;
      lines.forEach((line, i) => {
        const re = new RegExp(rule.re.source, rule.re.flags.replace('g', '') + 'g');
        let m;
        while ((m = re.exec(line)) !== null) {
          hits.push({ rule: rule.name, tier, file: f, line: i + 1, snippet: String(m[0]).slice(0, 60) });
          if (m[0].length === 0) re.lastIndex++;
        }
      });
    }
  }
  process.stdout.write(JSON.stringify({
    files: input.files.length,
    rules: rules.map(x => ({ name: x.rule.name, tier: x.tier })),
    hits,
  }));
}

main();
