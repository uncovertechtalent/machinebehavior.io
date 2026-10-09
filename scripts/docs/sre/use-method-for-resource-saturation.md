title: USE Method for Resource Saturation
summary: When a system is slow and you don't know why, ask three questions of every resource it depends on: how busy is it, what is queued waiting for it, and is it returning errors.
parent: performance
order: 100
labels: diagnostics, method, performance
aliases: USE Method | Utilization Saturation Errors | Brendan Gregg USE
type: method
created: 2026-05-04
updated: 2026-05-04
origin: SRE/pillars/07-performance/USE Method for Resource Saturation.md
reviewed: no
---
> When a system is slow and you don't know why, ask three questions of every resource it depends on: how busy is it, what is queued waiting for it, and is it returning errors. Brendan Gregg's USE method is the diagnostic primitive for performance problems.

## The three signals per resource

For every relevant hardware and logical resource:

- **Utilization** — % of time the resource was busy over an interval. CPU at 80%, disk at 60%, network link at 40%.
- **Saturation** — work waiting because the resource cannot keep up. Run-queue length, disk request queue, TCP retransmits, GC pause time. Even when utilization is sub-100%, saturation can be non-zero (variance + queueing).
- **Errors** — error events from the resource. ECC corrections, dropped packets, failed disk reads, failed memory allocations.

The order matters. Utilization tells you whether the resource is the candidate. Saturation tells you whether the candidate is actually the bottleneck. Errors tell you whether the resource is misbehaving even when nominal.

## The resource list (Linux server, illustrative)

| Resource | Utilization | Saturation | Errors |
|---|---|---|---|
| CPU | `%CPU` from `top`, `mpstat` | run-queue length (`uptime`, `vmstat`) | thermal throttle events |
| Memory | `free -m`, `MemAvailable` | swap-in rate, oom-kill events | ECC errors (`dmesg`, `mcelog`) |
| Disk I/O | `iostat -x`, `%util` | `await`, `aqu-sz` | I/O errors in `dmesg` |
| Network | interface bps vs link cap | `tc -s qdisc`, drops, retransmits | RX/TX errors (`ip -s link`) |
| File descriptors | `cat /proc/sys/fs/file-nr` | EMFILE errors in app logs | per-process limits hit |
| Connection pool | active vs max | wait time for free conn | timeout errors in app logs |

This is the working set for a checklist. Walk it top-to-bottom when you don't know where to look.

## Why the method works

The signal that a resource is the bottleneck is not utilization alone — it is utilization *plus* saturation. A CPU at 95% utilization with run-queue length 0.3 is busy but not bottlenecked. A CPU at 70% utilization with run-queue length 12 *is* the bottleneck — variance + scheduling delay are queueing work.

This is why "the box has CPU headroom" reasoning fails. Average utilization understates queueing. Saturation does not.

## Where USE pairs with RED

USE is resource-driven (server-side). RED (Rate, Errors, Duration) is request-driven (service-side).

- Use **RED** to detect that a service is slow.
- Use **USE** to find which resource on which host is causing it.

A symptom-based alert (see [[Symptoms over Causes for Alerting]]) fires on RED. The investigation that follows uses USE.

## What the method misses

- **Logical contention.** Lock contention inside the application is not visible at the resource level. Tools: `perf lock`, `eBPF` profilers, application metrics.
- **Coherent failure.** When multiple resources are saturated together (CPU + memory + disk), the cause is usually upstream — a thundering-herd retry storm, a runaway batch job. USE finds the symptoms; the cause is in the workload.
- **The cloud-resource layer.** Network ENI bandwidth, EBS IOPS limits, instance-level CPU credits are saturation events that look like the OS is fine. Always check provider-side metrics in parallel.

## See also

[[Symptoms over Causes for Alerting]] · [[CPU Cache Hierarchy and Speculative Execution]] · [[02-scalability]] · [[03-observability]]
