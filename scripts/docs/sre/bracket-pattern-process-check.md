title: Bracket Pattern Process Check
summary: Use pgrep -f "[b]atchtranscribe.py" or the ps | awk form.
parent: incidents
order: 100
labels: mitigation, transcriber-incidents
type: mitigation
created: 2026-09-21
updated: 2026-09-21
origin: SRE/incidents/Bracket Pattern Process Check.md
reviewed: no
---
Use `pgrep -f "[b]atch_transcribe.py"` or the `ps | awk` form. The bracket stops the pattern from matching the shell that runs the check. Also check the `scrape_runs` table.

## Part of

- [[Transcriber Incident Register]]
