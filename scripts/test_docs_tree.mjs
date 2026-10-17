// Test for the page tree part of inside/docs/docs.js: closed on a narrow load, opened again when the window grows past
// 820 px, where the tree's summary is hidden and could not open it, and the current page scrolled into view when the
// tree is open (#116).
//
//   node --test scripts/test_docs_tree.mjs
//
// Runs the real file in a vm context with a stub document and matchMedia; the "on this page" and "report an issue"
// parts find nothing in the stub and do nothing. No dependencies.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const SRC = readFileSync(new URL('../inside/docs/docs.js', import.meta.url), 'utf8');

function run(narrowAtLoad, { withTree = true } = {}) {
  const attrs = new Map([['open', '']]);
  const wrap = {
    setAttribute: (k, v) => attrs.set(k, String(v)),
    removeAttribute: k => attrs.delete(k),
    get open() { return attrs.has('open'); },
  };
  const box = { clientHeight: 400, scrollTop: 0 };          // the scrolling .side column
  const cur = { offsetTop: 900 };                           // the current page's link, below the fold
  const mql = { matches: narrowAtLoad, handlers: [], addEventListener(type, fn) { if (type === 'change') this.handlers.push(fn); } };
  const resize = narrow => { mql.matches = narrow; mql.handlers.forEach(fn => fn({ matches: narrow })); };
  const found = { '.side-wrap': wrap, '.side': box, '.side a[aria-current="page"]': cur };
  const document = {
    querySelector: s => (withTree ? found[s] || null : null),
    querySelectorAll: () => [],
  };
  const window = { matchMedia: q => { assert.equal(q, '(max-width: 820px)'); return mql; } };
  vm.runInNewContext(SRC, { window, document, location: { pathname: '/elsewhere/', href: '' } });
  return { wrap, box, resize };
}

test('a narrow load closes the tree and does not scroll it', () => {
  const { wrap, box } = run(true);
  assert.equal(wrap.open, false);
  assert.equal(box.scrollTop, 0);
});

test('a wide load leaves the tree open and scrolls the current page into view', () => {
  const { wrap, box } = run(false);
  assert.equal(wrap.open, true);
  assert.ok(box.scrollTop > 0);
});

test('widening after a narrow load opens the tree and scrolls the current page into view', () => {
  const { wrap, box, resize } = run(true);
  resize(false);
  assert.equal(wrap.open, true);
  assert.ok(box.scrollTop > 0);
});

test('narrowing again leaves the reader\'s choice alone', () => {
  const { wrap, resize } = run(false);
  resize(true);
  assert.equal(wrap.open, true);
});

test('a page without a page tree runs without error', () => {
  run(false, { withTree: false });
});
