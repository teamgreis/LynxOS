# F-001-Y — CPU Scheduling and Execution Contexts

**Status:** Initial research draft  
**Program:** R3 — Performance/resource theory; R5 — Time/concurrency  
**Decision status:** No architecture decision

## Research question

How should CPU time be allocated among execution contexts to provide high throughput, low latency, fairness, bounded interference, and predictable deadline behavior?

Scheduling is inherently multi-objective. No policy can be assumed optimal across interactive, batch, real-time, throughput, and energy-sensitive workloads.

## Candidate approaches

1. **Fixed-priority preemptive scheduling:** fast decisions and explicit criticality, but priority inversion and starvation require treatment.
2. **Round robin / time slicing:** simple sharing and bounded turns under assumptions, but quantum choice affects overhead and response.
3. **Fair-share / virtual-runtime scheduling:** approximate proportional fairness; accounting and placement across cores matter.
4. **Deadline scheduling:** order work by deadlines and reservations; requires admission control and runtime assumptions.
5. **Work stealing / locality-aware multicore scheduling:** improves load balance, but migration can harm cache and NUMA locality.
6. **Hierarchical scheduling:** allocate budgets to groups/domains, then schedule within them; improves isolation but introduces hierarchy and accounting overhead.
7. **Adaptive scheduling:** use observed workload behavior to tune policy; must remain bounded, explainable, and resistant to adversarial workload manipulation.

## Security, performance and efficiency requirements

- Enforce CPU budgets and prevent starvation across protection domains.
- Bound scheduler critical-section time and avoid unbounded global locks.
- Account for interrupt, kernel, and deferred work rather than hiding it.
- Consider priority inversion, donation/ceiling protocols, and deadlock.
- Preserve cache/NUMA locality where beneficial without sacrificing fairness.
- Define behavior for overload and missed deadlines.
- Treat scheduler inputs and workload classification as untrusted.
- Keep policy complexity off the most latency-sensitive path where possible.
- Measure throughput, p50/p95/p99 latency, fairness, context-switch cost, deadline misses, and energy per unit of work.

## Falsifiable questions

- Y1: Which scheduling policy best satisfies a declared workload mix under equal CPU capacity?
- Y2: Can hierarchical budgets bound interference without excessive scheduling overhead?
- Y3: When does migration improve throughput enough to justify cache and NUMA penalties?
- Y4: Can deadline admission control prevent overload from becoming unbounded latency?
- Y5: Can adaptive policy improve performance without creating unstable feedback or exploitable priority manipulation?

## Experiment plan

Compare round robin, weighted service, and fixed-priority selection on a deterministic set of runnable tasks with CPU demand, weight, priority, and deadlines. Record service share, maximum wait, completion time, and deadline misses. Keep the workload and tie-breaking rules fixed. The model should expose trade-offs, not crown a universal winner.

## Preliminary conclusion

Scheduling should be evaluated as a constrained multi-objective resource allocator. A plausible research direction is hierarchical resource budgets combined with workload-specific policies, but this must be tested against simpler schedulers and measured overhead.

## References

- Hossain, Banu and Arefin, [CPU scheduling from classical heuristics to learning-based and multicore paradigms](https://doi.org/10.1007/s00607-026-01736-8), *Computing*, 2026.
- Linux kernel documentation, [EEVDF Scheduler](https://docs.kernel.org/scheduler/sched-eevdf.html).
- Linux kernel documentation, [Deadline Task Scheduling](https://docs.kernel.org/scheduler/sched-deadline.html).

## Limitations

No scheduler, execution-context primitive, priority model, or real-time guarantee is selected. Toy-model results cannot predict production behavior without hardware and workload measurements.

## Cross-cutting evaluation contract — Engineering Quality Charter

This research item is governed by the project-wide [Engineering Quality Charter](../../foundation/engineering-quality-charter.md). Evaluate its topic-specific claims across:

- **Security:** assets, attacker capabilities, trust boundaries, enforcement path, least authority, abuse/DoS cases, and residual risks.
- **Correctness and reliability:** explicit invariants, safety/liveness properties, concurrency and TOCTOU hazards, failure points, recovery semantics, and falsifying counterexamples.
- **Performance:** credible baseline under the same workload; latency distributions including tail latency, throughput, and worst-case behavior where meaningful.
- **Efficiency:** CPU, memory, allocations, synchronization, context switches, I/O, data movement, storage amplification, and energy where measurable.
- **Innovation:** closest prior art and a precise, falsifiable difference. A new name or combination is not proof of global novelty.
- **Evidence:** label results as conceptual, formalized, modeled, tested, measured, reviewed, verified, implemented, or production-validated. A toy-model PASS is not proof of a real operating-system guarantee.

Where relevant, compare at least three credible approaches under equivalent assumptions. Record negative results and unmodeled behavior. Until threat analysis, comparative evaluation, and reproducibility requirements are met, this remains an initial research draft and cannot justify an architecture decision.
