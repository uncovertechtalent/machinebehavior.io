// Test for the page tree part of inside/docs/docs.js: closed on a narrow load, opened again when the window grows past
// 820 px, where the tree's summary is hidden and could not open it, and the current page scrolled into view when the
// tree is open (#116). A tree that is already open is left alone on widening, so the reader's scroll stays; on Safari
// before 14, which has addListener only, the reopen works the same, and with no listener method at all the rest of
// docs.js still runs (#118).
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

// api: 'modern' (addEventListener), 'legacy' (addListener, which calls back with the list itself), 'none'
function run(narrowAtLoad, { withTree = true, api = 'modern' } = {}) {
  const attrs = new Map([['open', '']]);
  const wrap = {
    setAttribute: (k, v) => attrs.set(k, String(v)),
    removeAttribute: k => attrs.delete(k),
    get open() { return attrs.has('open'); },
  };
  const box = { clientHeight: 400, scrollTop: 0 };          // the scrolling .side column
  const cur = { offsetTop: 900 };                           // the current page's link, below the fold
  const mql = { matches: narrowAtLoad, handlers: [] };
  if (api === 'modern') mql.addEventListener = function (type, fn) { if (type === 'change') this.handlers.push(fn); };
  if (api === 'legacy') mql.addListener = function (fn) { this.handlers.push(fn); };
  const resize = narrow => { mql.matches = narrow; mql.handlers.forEach(fn => fn(api === 'legacy' ? mql : { matches: narrow })); };
  const found = { '.side-wrap': wrap, '.side': box, '.side a[aria-current="page"]': cur };
  let restRan = false;                                      // the "on this page" part asks for the table of contents
  const document = {
    querySelector: s => (withTree ? found[s] || null : null),
    querySelectorAll: () => { restRan = true; return []; },
  };
  const window = { matchMedia: q => { assert.equal(q, '(max-width: 820px)'); return mql; } };
  vm.runInNewContext(SRC, { window, document, location: { pathname: '/elsewhere/', href: '' } });
  return { wrap, box, resize, restRan: () => restRan };
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

test('widening a tree that is still open keeps the reader\'s scroll', () => {
  const { wrap, box, resize } = run(false);
  box.scrollTop = 0;                                        // the reader scrolled the tree back to the top
  resize(true);
  resize(false);
  assert.equal(wrap.open, true);
  assert.equal(box.scrollTop, 0);
});

test('Safari before 14 (addListener only): widening opens the tree and scrolls the current page into view', () => {
  const { wrap, box, resize } = run(true, { api: 'legacy' });
  resize(false);
  assert.equal(wrap.open, true);
  assert.ok(box.scrollTop > 0);
});

test('no listener method at all: no error, and the rest of docs.js still runs', () => {
  const { wrap, restRan } = run(true, { api: 'none' });
  assert.equal(wrap.open, false);
  assert.equal(restRan(), true);
});

test('a page without a page tree runs without error', () => {
  const { restRan } = run(false, { withTree: false });
  assert.equal(restRan(), true);
});
