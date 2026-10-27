// Behavioural test for inside/seat-tabs.js (ADR-0034, ADR-0036): the keyboard moves and the ARIA state of the seat
// tablist, which PR 103 left untested. Runs on node's own test runner over a minimal DOM shim; no dependencies.
//
//   node --test scripts/test_seat_tabs.mjs
//
// The shim carries only what initSeatTabs touches: setAttribute/getAttribute, tabIndex, hidden, focus (which sets
// document.activeElement), querySelectorAll('a.in-seat' | 'li'), closest, addEventListener (handlers kept so the test
// can fire them), getBoundingClientRect and scrollIntoView, plus a window with location, history and listeners.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { initSeatTabs } from '../inside/seat-tabs.js';

const SEATS = ['ceo', 'cto', 'cfo', 'chro', 'publisher', 'cko'];

class El {
  constructor(tag, cls = '') { this.tag = tag; this.className = cls; this.attrs = new Map(); this.children = []; this.parent = null; this.tabIndex = 0; this.hidden = false; this.rectTop = 0; this.scrolled = false; }
  setAttribute(k, v) { this.attrs.set(k, String(v)); if (k === 'id') this.id = String(v); }
  getAttribute(k) { return this.attrs.has(k) ? this.attrs.get(k) : null; }
  get id() { return this._id; } set id(v) { this._id = v; }
  append(c) { c.parent = this; this.children.push(c); return c; }
  matches(sel) {
    if (sel === 'li') return this.tag === 'li';
    if (sel === 'a.in-seat') return this.tag === 'a' && this.className.split(/\s+/).includes('in-seat');
    return false;
  }
  descendants() { return this.children.flatMap(c => [c, ...c.descendants()]); }
  querySelectorAll(sel) { return this.descendants().filter(e => e.matches(sel)); }
  closest(sel) { let e = this; while (e) { if (e.matches(sel)) return e; e = e.parent; } return null; }
  addEventListener(type, fn) { (this._h ||= {})[type] ||= []; this._h[type].push(fn); }
  fire(type, ev) { (this._h?.[type] || []).forEach(fn => fn(ev)); }
  focus() { doc.activeElement = this; }
  getBoundingClientRect() { return { top: this.rectTop }; }
  scrollIntoView() { this.scrolled = true; }
}

let doc, win;

function build() {
  const list = new El('ul', 'in-seat-tabs');
  const tabs = {}, panels = {};
  for (const k of SEATS) {
    const li = list.append(new El('li'));
    const a = li.append(new El('a', 'in-seat'));
    a.setAttribute('id', 'in-tab-' + k);
    a.setAttribute('href', '#seat-' + k);
    a.setAttribute('aria-controls', 'seat-' + k);
    tabs[k] = a;
    const panel = new El('section');
    panel.setAttribute('id', 'seat-' + k);
    panels[k] = panel;
  }
  const byId = {};
  const inner = { id: 'dashboards' };
  panels.cto.contains = el => el === inner;
  byId.dashboards = inner;
  for (const k of SEATS) { byId['in-tab-' + k] = tabs[k]; byId['seat-' + k] = panels[k]; }
  win = {
    innerHeight: 800,
    location: { hash: '' },
    history: {
      calls: [],
      pushState(_s, _t, url) { this.calls.push(['push', url]); win.location.hash = url; },
      replaceState(_s, _t, url) { this.calls.push(['replace', url]); win.location.hash = url; },
    },
    _h: {},
    addEventListener(type, fn) { (this._h[type] ||= []).push(fn); },
    fire(type, ev) { (this._h[type] || []).forEach(fn => fn(ev)); },
  };
  doc = { activeElement: null, getElementById: id => byId[id] || null };
  const ctl = initSeatTabs(list, { doc, win });
  return { list, tabs, panels, ctl };
}

const sel = tabs => SEATS.filter(k => tabs[k].getAttribute('aria-selected') === 'true');
const tabindex = tabs => SEATS.map(k => tabs[k].tabIndex);
const shown = panels => SEATS.filter(k => !panels[k].hidden);

test('init sets the tablist roles and shows the first seat', () => {
  const { list, tabs, panels, ctl } = build();
  assert.ok(ctl, 'initSeatTabs returned controls');
  assert.equal(list.getAttribute('role'), 'tablist');
  assert.ok(SEATS.every(k => tabs[k].getAttribute('role') === 'tab'));
  assert.ok(SEATS.every(k => panels[k].getAttribute('role') === 'tabpanel' && panels[k].tabIndex === 0));
  assert.ok(list.querySelectorAll('li').every(li => li.getAttribute('role') === 'presentation'));
  assert.deepEqual(sel(tabs), ['ceo']);
  assert.deepEqual(tabindex(tabs), [0, -1, -1, -1, -1, -1]);
  assert.deepEqual(shown(panels), ['ceo']);
});

test('ArrowRight moves selection and focus, replaces the hash', () => {
  const { tabs, panels } = build();
  tabs.ceo.focus();
  list_keydown(tabs, 'ArrowRight');
  assert.deepEqual(sel(tabs), ['cto']);
  assert.deepEqual(tabindex(tabs), [-1, 0, -1, -1, -1, -1]);
  assert.deepEqual(shown(panels), ['cto']);
  assert.equal(doc.activeElement, tabs.cto);
  assert.deepEqual(win.history.calls.at(-1), ['replace', '#seat-cto']);
});

test('ArrowLeft wraps from the first seat to the last', () => {
  const { tabs } = build();
  tabs.ceo.focus();
  list_keydown(tabs, 'ArrowLeft');
  assert.deepEqual(sel(tabs), ['cko']);
  assert.equal(doc.activeElement, tabs.cko);
});

test('Home and End jump to the ends', () => {
  const { tabs } = build();
  tabs.cfo.focus();
  list_keydown(tabs, 'End');
  assert.deepEqual(sel(tabs), ['cko']);
  tabs.cko.focus();
  list_keydown(tabs, 'Home');
  assert.deepEqual(sel(tabs), ['ceo']);
});

test('ArrowDown and ArrowUp act like Right and Left', () => {
  const { tabs } = build();
  tabs.ceo.focus();
  list_keydown(tabs, 'ArrowDown');
  assert.deepEqual(sel(tabs), ['cto']);
  list_keydown(tabs, 'ArrowUp');
  assert.deepEqual(sel(tabs), ['ceo']);
});

test('an unrelated key is ignored', () => {
  const { tabs } = build();
  tabs.ceo.focus();
  let prevented = false;
  tabs.ceo.parent.parent.fire('keydown', { key: 'a', preventDefault: () => { prevented = true; } });
  assert.deepEqual(sel(tabs), ['ceo']);
  assert.equal(prevented, false);
});

test('a click selects a seat and pushes a history entry', () => {
  const { list, tabs, panels } = build();
  list.fire('click', { target: tabs.cfo, preventDefault() {} });
  assert.deepEqual(sel(tabs), ['cfo']);
  assert.deepEqual(shown(panels), ['cfo']);
  assert.deepEqual(win.history.calls.at(-1), ['push', '#seat-cfo']);
});

test('a seat hash selects that seat; a hash inside a panel selects its seat; an unknown hash leaves the choice alone', () => {
  const { tabs, panels } = build();
  win.location.hash = '#seat-cko';
  win.fire('hashchange', {});
  assert.deepEqual(sel(tabs), ['cko']);
  win.location.hash = '#dashboards/deploys';
  win.fire('hashchange', {});
  assert.deepEqual(sel(tabs), ['cto'], 'a hash inside a seat panel selects that seat');
  assert.deepEqual(shown(panels), ['cto']);
  win.location.hash = '#nowhere';
  win.fire('hashchange', {});
  assert.deepEqual(sel(tabs), ['cto'], 'an unknown hash leaves the choice alone');
});

test('exactly one seat is selected after every move', () => {
  const { list, tabs } = build();
  tabs.ceo.focus();
  for (const key of ['ArrowRight', 'ArrowRight', 'End', 'Home', 'ArrowLeft']) list_keydown(tabs, key);
  assert.equal(sel(tabs).length, 1);
  list.fire('click', { target: tabs.chro, preventDefault() {} });
  assert.equal(sel(tabs).length, 1);
});

// keydown is bound on the list; it reads document.activeElement for the current tab.
function list_keydown(tabs, key) {
  const list = tabs.ceo.parent.parent;
  list.fire('keydown', { key, preventDefault() {} });
}
