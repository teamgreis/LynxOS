# F-001-D — Resource-Aware Computation

**Status:** Exploratory research; no architecture decision
**Research program:** R0 — Computing foundations
**Parent:** [F-001 — What is a computer?](F-001-what-is-a-computer.md)

## Research question

Can a computational model represent resource availability, consumption, contention, and limits as first-class parts of computation rather than treating them only as external implementation concerns?

This does not assume resources must be managed by a kernel, scheduler, runtime, compiler, or hardware mechanism. Those remain competing implementation locations.

## Why this matters

A computation may be logically valid and still fail to make progress because CPU time, memory, bandwidth, energy, storage, or communication capacity is unavailable. Deadlines and latency constraints add temporal requirements. Contention means one activity's allocation can affect another activity's observable behavior.

Distinguish at least:
- **Capacity:** what is physically or contractually available.
- **Demand:** what an activity requests or needs.
- **Allocation:** what it is permitted or promised to consume.
- **Consumption:** what it actually uses.
- **Reservation:** capacity withheld for a future or critical obligation.
- **Contention:** competition for a shared resource.
- **Accounting:** attribution of consumption to an activity or principal.
- **Enforcement:** what prevents an allocation from being exceeded.
- **Admission:** whether new work can be accepted without invalidating existing guarantees.
- **Degradation:** what happens when guarantees cannot be maintained.

These concepts must not be collapsed into one number called priority.

## Research boundaries

Consider directly consumable resources (CPU time, energy, I/O bandwidth), capacity-constrained resources (memory, storage, queue slots), shared resources (memory bandwidth, caches, interconnects), temporal constraints (deadlines, latency bounds), and external constraints (network quotas, remote service budgets). Demand may be known, estimated, or observable only after execution.

## Candidate model extension

As provisional notation, an activity x has demand vector d_x, allocation vector a_x, observed consumption vector u_x, optional deadline t_x, reservation r_x, and accounting identity p_x.

For resource dimension k, a simple capacity constraint is:

    sum_x u[x,k](t) <= C[k](t)

This first approximation does not model substitution, burst credits, topology, non-linear interference, or uncertainty. A temporal requirement may be expressed as completion(x) <= deadline(x). A reservation is meaningful only if enforceability under contention and changing capacity is explained.

The notation is provisional; it does not prescribe a resource-vector API or scheduler.

## Competing approaches

| Approach | Core idea | Potential strength | Limitation / question |
|---|---|---|---|
| Best effort | Allocate currently available capacity, often by priority or queue policy | High utilization; simple | No inherent guarantee under overload |
| Reservation / admission control | Promise bounded capacity before accepting work | Predictability for admitted activities | Fragmentation, under-utilization, admission complexity |
| Weighted fairness | Divide capacity according to weights or service history | Understandable adjustable shares | Fairness may conflict with deadlines or criticality |
| Hierarchical accounting | Attribute use to logical activities, not merely execution containers | Better attribution across shared execution contexts | Correct accounting and enforcement are difficult |
| Adaptive allocation | Change allocations based on observed demand and system state | Reacts to dynamic workloads | Feedback instability, opacity, hard-to-prove guarantees |
| Application-managed cooperation | Activities expose demand and cooperate with allocator | Can exploit semantic knowledge | Untrusted activities may lie or fail to cooperate |

Approaches may be combined, but assumptions and trade-offs must first be characterized.

## Prior art

- **Resource Containers (Banga, Druschel, Mogul, OSDI 1999):** separates resource principals from protection domains and accounts for CPU and memory. [Paper](https://www.usenix.org/conference/osdi-99/resource-containers-new-facility-resource-management-server-systems).
- **Linux Energy-Aware Scheduling:** uses CPU energy models to estimate scheduling impact, especially on heterogeneous CPU topologies. [Kernel documentation](https://docs.kernel.org/scheduler/sched-energy.html).
- **Karma (OSDI 2023):** studies fairness under dynamic demands and limitations of classical max-min fairness when demand changes. [USENIX paper](https://www.usenix.org/conference/osdi23/presentation/vuppalapati).
- **Memory bandwidth regulation and cache partitioning (ECRTS 2025):** studies co-allocation for predictable real-time behavior. [Paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol335-ecrts2025/html/LIPIcs.ECRTS.2025.2/LIPIcs.ECRTS.2025.2.html).
- **BALANCER (2023):** evaluates shared cache and memory-bandwidth contention and performance/fairness trade-offs. [Paper overview](https://webdiis.unizar.es/~chus/pubs/balancer/balancer.html).

These works establish substantial prior art. LynxOS makes no novelty claim. The open question is whether a more general model can connect resource semantics, computation semantics, and observable guarantees without assuming a particular OS abstraction.

## Hypotheses

- **H-D1:** Explicitly distinguishing demand, allocation, consumption, and capacity describes overload more precisely than a model of execution transitions alone.
- **H-D2:** CPU-only accounting is insufficient to predict progress when memory, energy, bandwidth, or other resources limit execution.
- **H-D3:** Fairness, deadline satisfaction, and total throughput are distinct objectives and can conflict.
- **H-D4:** Reservations improve predictability only when admission and enforcement assumptions are explicit.
- **H-D5:** Accounting should attach to the logical activity causing consumption, even when execution crosses protection or implementation boundaries.

All hypotheses are falsifiable and may be rejected or narrowed.

## Experiment plan

The accompanying deterministic finite-workload simulation compares best-effort priority, weighted fair allocation, and a protected CPU reservation for a designated critical activity. All policies share CPU capacity, memory admission, and a global energy budget. It records completed work, deadline misses, energy use, and per-activity completion.

The model is intentionally small. It is not a scheduler benchmark and does not model real hardware. Follow-up experiments should vary arrivals, burstiness, demand-estimation error, multiple resource dimensions, memory-bandwidth contention, energy replenishment, admission policy, fairness metrics, and deadline distributions.

## Evaluation criteria

Compare throughput, deadline misses and lateness, per-activity service and starvation, utilization and unused reservations, energy consumption, overload behavior, and sensitivity to inaccurate demand estimates. No single aggregate score should hide trade-offs.

## Open questions

1. Which resources can share an abstraction, and which require distinct semantics?
2. How should uncertain demand be represented?
3. Can guarantees survive dynamic capacity changes?
4. What is fairness across heterogeneous resources?
5. Can computation expose resource demand without exposing implementation details?
6. How should constraints compose across nested or distributed activities?
7. Which guarantees are enforceable in software, and which require hardware support?

## Research conclusion

F-001-D does not establish that resources must be first-class objects in the eventual LynxOS architecture. It establishes a research requirement: any proposed computation model should be tested against scarcity, contention, temporal constraints, and enforceability rather than assuming valid transitions automatically imply progress.

**Decision status:** No kernel model, scheduler, language, runtime, resource API, or allocation policy is selected.

## Cross-cutting evaluation contract — Engineering Quality Charter

This research item is governed by the project-wide [Engineering Quality Charter](../../foundation/engineering-quality-charter.md). Its topic-specific claims must be evaluated across all applicable dimensions:

- **Security:** define assets, attacker capabilities, trust boundaries, enforcement path, least-authority behavior, abuse/DoS cases, and residual risks.
- **Correctness and reliability:** state invariants, safety and liveness properties, concurrency/TOCTOU hazards, failure points, recovery semantics, and falsifying counterexamples.
- **Performance:** compare against a credible baseline using the same workload; report latency distributions (including tail latency), throughput, and worst-case behavior where meaningful.
- **Efficiency:** account for CPU, memory, allocations, synchronization, context switches, I/O, data movement, storage amplification, and energy where measurable.
- **Innovation:** identify closest prior art and state the precise, falsifiable difference. Do not equate a new name or combination with global novelty.
- **Evidence:** label results as conceptual, formalized, modeled, tested, measured, reviewed, verified, implemented, or production-validated. A toy-model PASS is not proof of a real operating-system guarantee.

Where comparison is relevant, evaluate at least three credible approaches under equivalent assumptions. Record negative results and unmodeled behavior. Until the missing threat analysis, comparative evaluation, and reproducibility requirements are met, this document remains an initial research draft and cannot justify an architecture decision.
