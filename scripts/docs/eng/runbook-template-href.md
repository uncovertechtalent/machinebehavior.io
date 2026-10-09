title: Link check flags a template string
summary: The gate reads every href in the page source, including ones inside JavaScript template strings; build such links with a.href in code.
parent: runbooks
order: 30
labels: runbook, gate, javascript
owner: Stefan Coetzee
reviewed: 2026-10-09
review_by: 2027-01-07
type: how-to
---
**Symptom.** `site.consistency` fails with "relative link" and a value that starts with a dollar sign and a brace, which does not appear on the rendered page.

**Cause.** The check scans the page source with a regular expression for `href="..."`. An attribute written inside a JavaScript template string matches, and its value is not root-absolute.

## Fix

Create the element in code and set the property:

```js
const a = document.createElement('a');
a.href = item.url;
a.textContent = item.title;
```

Inside, the map page and the docs search all build links this way. Code in a separate `.js` file is not scanned as a page.
