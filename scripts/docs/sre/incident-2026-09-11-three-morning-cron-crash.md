title: Incident 2026-09-11 Three-Morning Cron Crash
summary: The 06:15 cron died three mornings running with CalledProcessError.
parent: incidents
order: 100
labels: incident, transcriber-incidents
type: incident
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Incident 2026-09-11 Three-Morning Cron Crash.md
reviewed: no
---
The 06:15 cron died three mornings running with `CalledProcessError`. The log showed a traceback and no cause. The login session was the obvious suspect and was fine. Jar enumeration failed 9 of 9, no-cookie enumeration succeeded 3 of 3, and the jar with two entries removed succeeded. Both entries had expired on 2026-09-10, the day before the first crash.

## Caused by

- [[Expired Bot-Manager Cookie Returns Empty Body]]
- [[Swallowed Stderr Hides the Cause]]

## Mitigated by

- [[Filter Expired Cookies Before Each Run]]
- [[Enumeration Retry With Unauthenticated Fallback]]

## Detected by

- [[Differential Test in the Same Minutes]]

## Part of

- [[Transcriber Incident Register]]
