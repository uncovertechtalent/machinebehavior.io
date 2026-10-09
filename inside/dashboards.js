// The public Grafana dashboards of the agent-observability stack, framed on Inside (/inside/#dashboards) and on
// Mission Control (/inside/mission-control/). One list for both pages. A frame loads only after the reader asks for it
// or scrolls to it (ADR-0010), so opening a page sends no request to the Grafana host.
window.MB_DASHES = [
  {key: 'deploys', label: 'deploys', token: 'e0f6a0c8f3a64884a67faac5cf4c3ad4', range: 'now-2d',
   about: 'Every GitHub Actions run of the three sites: outcome per hour, push-to-live time, where the time goes per step, the gate result for each check on every run, and what the deploy shipped.'},
  {key: 'agents', label: 'claude code', token: '3a4ba6b21e6f4924ab2845b47a300af0', range: 'now-7d',
   about: 'The Claude Code sessions that build this work, from their OpenTelemetry export: spend by model and by source, tokens by type, prompt-cache reads, and the number of API calls, prompts and tool calls. Every figure is summed from the events Claude Code writes per call, so parallel sessions cannot inflate it. Aggregates only; identifying labels are stripped before storage.'},
  {key: 'llm', label: 'local llm', token: 'e6a9dd2153004ad0a868ce6f0e19071f', range: 'now-7d',
   about: 'The self-hosted model server on the home lab, metered by a pass-through proxy: time to first token, decode speed, token counts, model load time, and which models sit in GPU memory.'},
  {key: 'search', label: 'search', token: '8bfa9ce4bdb946de8c37c738c9e61346', range: 'now-24h',
   about: 'The self-hosted SearXNG instance every research agent searches through: whether each search engine answers, returns nothing, is rate-limited or blocked, how many searches return results, and how long they take.'},
  {key: 'host', label: 'host', token: '81c9dfd269cc430abaf6a6ce7b64c4d6', range: 'now-24h',
   about: 'The box that runs all of this: CPU, memory, ZFS, disks, network, GPU and sensors.'},
];
window.MB_DASH_URL = d => `https://grafana.scoetzee.de/public-dashboards/${d.token}?from=${d.range}&to=now`;
