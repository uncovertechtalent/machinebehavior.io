// Test for the section sidebar part of inside/bar.js (ADR-0022): closed on a narrow load, opened again when the window
// grows to 1100 px or more, where the sidebar's summary is hidden and could not open it (#114); on Safari before 14,
// which has addListener only, the same, and with no listener method at all no error and the search part still runs (#118).
//
//   node --test scripts/test_bar.mjs
//
// Runs the real file in a vm context with a stub document and matchMedia; the search part of bar.js returns early
// because the stub has no search box. No dependencies.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const SRC = readFileSync(new URL('../inside/bar.js', import.meta.url), 'utf8');

// api: 'modern' (addEventListener), 'legacy' (addListener, which calls back with the list itself), 'none'
function run(narrowAtLoad, api = 'modern') {
  const attrs = new Map([['open', '']]);
  const side = {
    setAttribute: (k, v) => attrs.set(k, String(v)),
    removeAttribute: k => attrs.delete(k),
    get open() { return attrs.has('open'); },
  };
  const mql = { matches: narrowAtLoad, handlers: [] };
  if (api === 'modern') mql.addEventListener = function (type, fn) { if (type === 'change') this.handlers.push(fn); };
  if (api === 'legacy') mql.addListener = function (fn) { this.handlers.push(fn); };
  const resize = narrow => { mql.matches = narrow; mql.handlers.forEach(fn => fn(api === 'legacy' ? mql : { matches: narrow })); };
  let searchRan = false;
  const document = {
    querySelector: s => (s === '.mb-side-wrap' ? side : null),
    getElementById: () => { searchRan = true; return null; },
  };
  const window = { matchMedia: q => { assert.equal(q, '(max-width: 1099px)'); return mql; } };
  vm.runInNewContext(SRC, { window, document });
  return { side, resize, searchRan: () => searchRan };
}

test('a narrow load closes the sidebar', () => {
  assert.equal(run(true).side.open, false);
});

test('a wide load leaves the sidebar open', () => {
  assert.equal(run(false).side.open, true);
});

test('widening after a narrow load opens the sidebar again', () => {
  const { side, resize } = run(true);
  resize(false);
  assert.equal(side.open, true);
});

test('narrowing again leaves the reader\'s choice alone', () => {
  const { side, resize } = run(false);
  resize(true);
  assert.equal(side.open, true);
});

test('Safari before 14 (addListener only): widening opens the sidebar again', () => {
  const { side, resize } = run(true, 'legacy');
  resize(false);
  assert.equal(side.open, true);
});

test('no listener method at all: no error, and the search part still runs', () => {
  const { side, searchRan } = run(true, 'none');
  assert.equal(side.open, false);
  assert.equal(searchRan(), true);
});

test('a page without a sidebar runs without error', () => {
  const document = { querySelector: () => null, getElementById: () => null };
  const window = { matchMedia: () => { throw new Error('not reached'); } };
  vm.runInNewContext(SRC, { window, document });
});
