// Test for the section sidebar part of inside/bar.js (ADR-0022): closed on a narrow load, opened again when the window
// grows to 1100 px or more, where the sidebar's summary is hidden and could not open it (#114).
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

function run(narrowAtLoad) {
  const attrs = new Map([['open', '']]);
  const side = {
    setAttribute: (k, v) => attrs.set(k, String(v)),
    removeAttribute: k => attrs.delete(k),
    get open() { return attrs.has('open'); },
  };
  const mql = { matches: narrowAtLoad, handlers: [], addEventListener(type, fn) { if (type === 'change') this.handlers.push(fn); } };
  const resize = narrow => { mql.matches = narrow; mql.handlers.forEach(fn => fn({ matches: narrow })); };
  const document = { querySelector: s => (s === '.mb-side-wrap' ? side : null), getElementById: () => null };
  const window = { matchMedia: q => { assert.equal(q, '(max-width: 1099px)'); return mql; } };
  vm.runInNewContext(SRC, { window, document });
  return { side, resize };
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

test('a page without a sidebar runs without error', () => {
  const document = { querySelector: () => null, getElementById: () => null };
  const window = { matchMedia: () => { throw new Error('not reached'); } };
  vm.runInNewContext(SRC, { window, document });
});
