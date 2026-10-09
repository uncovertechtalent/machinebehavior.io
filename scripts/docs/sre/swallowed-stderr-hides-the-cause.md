title: Swallowed Stderr Hides the Cause
summary: subprocess.run(..., checkTrue, captureoutputTrue) captures the child's stderr and raises CalledProcessError.
parent: incidents
order: 100
labels: root-cause, transcriber-incidents
type: root-cause
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Swallowed Stderr Hides the Cause.md
reviewed: no
---
`subprocess.run(..., check=True, capture_output=True)` captures the child's stderr and raises `CalledProcessError`. The log then holds a Python traceback and none of the child's own error text, so the failure is visible and its reason is not.

## Part of

- [[Transcriber Incident Register]]
