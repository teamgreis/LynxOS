# F-001-H — Time, Ordering and Temporal Semantics

**Status:** Research question; open  
**Program:** R0 — Computing foundations  
**Parent:** [F-001 — What is a computer?](F-001-what-is-a-computer.md)  
**Related:** [F-001-B — Causality and concurrent transitions](F-001-B-causality-concurrent-transitions.md), [F-001-G — State, Memory and Continuity](F-001-G-state-memory-continuity.md)

## Research question

What does time mean inside a computer system, and how can temporal guarantees be represented when clocks drift, events are concurrent, machines suspend, or components fail?

The investigation separates physical time, elapsed time, logical event order, causality, deadlines, and externally observable time. No global clock service, clock representation, scheduler, or distributed ordering protocol is selected.

## 1. Why time is not one thing

A system may need to answer several different questions:

- What civil time is it?
- How much time has elapsed since an event?
- Did event A causally precede event B?
- Are two events concurrent?
- Has a deadline expired?
- Can two machines agree that one operation happened before another?
- What happens to a timeout when the machine suspends or restarts?

A timestamp is not automatically an answer to all of these questions. A wall-clock timestamp may be useful for logs and calendar semantics but can jump when corrected. A monotonic clock is useful for measuring intervals but does not by itself identify a globally meaningful date. A logical clock captures ordering properties, not elapsed seconds.

## 2. Working vocabulary

| Term | Working meaning |
|---|---|
| Physical clock | A clock intended to approximate a physical time scale |
| Wall clock | A clock representing civil/epoch time and subject to correction |
| Monotonic clock | A clock that does not move backward within its defined scope |
| Boot-time clock | Monotonic elapsed time that may include system suspend |
| Logical clock | A counter or structure used to represent event ordering |
| Causality | A relation describing which events can influence or precede others |
| Partial order | An ordering in which some pairs are intentionally incomparable |
| Total order | An ordering that compares every pair, possibly using tie-breakers |
| Clock uncertainty | A bound or interval describing uncertainty in a clock reading |
| Deadline | A time constraint by which an action should complete |
| Timeout | A bound on waiting duration under a specified clock and suspend policy |
| Lease | A time-bounded grant whose validity depends on a temporal contract |

## 3. Physical time versus elapsed time

Wall-clock time can be adjusted by synchronization, administrative changes, leap handling, virtualization, or other platform mechanisms. A clock that moves backward can make naive timeout calculations incorrect.

For elapsed-time measurement, systems commonly provide monotonic clocks. But monotonic clocks differ in scope and suspend behavior. For example, Linux documents CLOCK_MONOTONIC as stopping during suspend and CLOCK_BOOTTIME as including suspend time. Neither choice is universally correct: an interactive timeout might intentionally pause during suspend, while a lease or expiration policy may need to continue.

A temporal API should therefore specify:
- clock domain and scope;
- whether the clock can be adjusted;
- whether suspend time is included;
- resolution and accuracy;
- behavior across reboot or migration;
- uncertainty and failure behavior.

## 4. Event order is not identical to timestamp order

Lamport's happened-before relation defines a partial order over distributed events. If one event causally influences another, the first must precede the second in that relation. Events with no causal path between them are concurrent in the model.

Lamport logical clocks assign scalar values that preserve causal order, but the converse does not hold: a lower timestamp does not prove causality. A deterministic tie-breaker can create a total order for processing, but that artificial order must not be mistaken for a causal fact.

Vector clocks can distinguish causally ordered events from concurrent events under their model. Their metadata cost and management complexity grow with the set of participating processes; dynamic membership and process lifecycle add further concerns.

This connects directly to [F-001-B](F-001-B-causality-concurrent-transitions.md), but F-001-H focuses on temporal representation and guarantees rather than the general semantics of concurrent transitions.

## 5. Uncertainty and distributed physical clocks

A distributed system cannot simply assume that clocks on different machines are identical. Synchronization has finite error, network delay, drift, and failure modes.

One approach is to expose time as an interval or estimate with an uncertainty bound rather than a single unquestionable value. Google's Spanner is a notable example: its TrueTime API exposes clock uncertainty and uses that information in externally consistent transaction design.

This is an existence proof for one engineering approach, not evidence that every system needs globally synchronized physical time. Logical ordering, consensus, bounded uncertainty, and application-level policies are competing tools for different requirements.

## 6. Deadlines, timers and leases

A deadline is meaningful only relative to a clock domain and a policy.

Examples:
- A UI animation may use monotonic elapsed time and pause while suspended.
- A network request timeout may need a monotonic duration.
- A credential expiration may be tied to civil/epoch time and require clock uncertainty handling.
- A distributed lease must define what happens when clocks drift, nodes pause, or a node loses contact with its authority.
- A real-time task may have a completion deadline and a defined response to a miss.

A system must distinguish:
- **hard deadline:** missing it violates the required contract;
- **firm deadline:** late output is no longer useful;
- **soft deadline:** late output remains useful but quality or value decreases.

Scheduling policy, admission control, overload behavior, and deadline semantics are related but separate questions.

## 7. Competing conceptual approaches

These are research candidates, not architecture decisions.

1. **Physical-time centric:** timestamps and synchronized clocks are primary; suitable where external time semantics dominate.
2. **Monotonic-duration centric:** durations and deadlines use monotonic clocks; civil time is separate.
3. **Lamport scalar ordering:** compact logical timestamps preserve happened-before implications but cannot identify concurrency.
4. **Vector-clock causality:** causal relationships and concurrency can be distinguished at additional metadata cost.
5. **Hybrid logical/physical clocks:** combine physical-time intuition with logical ordering properties; their guarantees and assumptions require separate evaluation.
6. **Uncertainty-aware physical time:** expose clock bounds and require callers to account for ambiguity.
7. **Consensus/sequence-based order:** derive a committed order from coordination rather than trusting physical timestamp order.
8. **Application-defined temporal contracts:** different subsystems choose clock domains and semantics appropriate to their work.

## 8. Hypotheses

- **H-H1:** A single scalar timestamp cannot represent all of civil time, elapsed duration, causality, and concurrency.
- **H-H2:** A correct timeout contract must specify clock domain and suspend behavior.
- **H-H3:** Lamport clocks preserve causal precedence but cannot prove that two events are causally related.
- **H-H4:** Vector clocks can identify concurrency under their process and message model, at non-zero metadata and lifecycle cost.
- **H-H5:** Distributed physical-time guarantees must account for uncertainty and clock failure.
- **H-H6:** Deadline semantics should be separated from the scheduling mechanism used to attempt to meet them.
- **H-H7:** Temporal behavior after restart, migration, or suspend must be explicitly defined rather than inferred from timestamp values.

## 9. Minimal executable experiment

The accompanying model demonstrates two distinct points:

1. Two events can receive equal Lamport timestamps while remaining concurrent. A vector-clock comparison distinguishes them in this small two-process example.
2. If a wall clock is stepped backward, naive wall-clock elapsed-time calculation can become negative while monotonic elapsed time remains positive.

The experiment is deterministic and self-checking. It does not simulate real clock synchronization, drift distributions, NTP/PTP, leap seconds, suspend/resume hardware, scheduler behavior, or production distributed protocols.

Run:

```sh
python3 experiments/f001/temporal_semantics_model.py
```

## 10. Prior art and references

- Leslie Lamport, **Time, Clocks, and the Ordering of Events in a Distributed System** (1978), establishes happened-before and logical clocks: [Microsoft Research publication page](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/) and [DOI](https://doi.org/10.1145/359545.359563).
- Mukesh Singhal and Ajay Kshemkalyani, **An Efficient Implementation of Vector Clocks** (1992): [DOI](https://doi.org/10.1016/0020-0190(92)90028-T).
- Google, **Spanner: Google's Globally-Distributed Database** (OSDI 2012), describes TrueTime and exposed clock uncertainty: [Google Research](https://research.google/pubs/spanner-googles-globally-distributed-database-2/).
- Linux kernel documentation, **ktime accessors**, documents clock domains including monotonic and boot-time clocks: [Linux kernel documentation](https://docs.kernel.org/core-api/timekeeping.html).
- Francisco J. Torres-Rojas and Mustaque Ahamad, **Plausible Clocks: Constant Size Logical Clocks for Distributed Systems** (1999): [DOI](https://doi.org/10.1007/S004460050065).

This is an initial related-work map, not an exhaustive survey.

## 11. Open research questions

1. Which LynxOS subsystems need civil time, elapsed time, causal order, or some combination?
2. What clock guarantees can survive suspend, reboot, migration, and virtualization?
3. How should a task express a deadline without depending on one global clock?
4. How should uncertainty be represented and propagated through APIs?
5. When are scalar logical clocks sufficient, and when is explicit concurrency detection necessary?
6. What are the metadata and coordination costs of vector or hybrid clocks at changing scale?
7. How should leases behave during long pauses, partitions, and clock corrections?
8. How should real-time guarantees degrade under overload or resource exhaustion?
9. Can a portable temporal contract be defined across heterogeneous hardware?
10. How should event order be reconstructed for debugging and deterministic replay?

## 12. Evaluation plan

For each candidate:

1. Define the event and clock model.
2. State assumptions about drift, synchronization, message delay, suspend, and failure.
3. Enumerate causal and concurrent event patterns.
4. Specify deadline and timeout behavior.
5. Build executable models and adversarial tests.
6. Measure timestamp metadata, synchronization overhead, coordination latency, deadline misses, and uncertainty.
7. Compare guarantees against established work and document limitations.

## 13. Current conclusion

No architecture decision follows from this investigation.

Time is not one universal scalar available to every subsystem. Civil time, elapsed duration, causal order, concurrency, and deadlines are different abstractions. Any future LynxOS design must state which abstraction a given operation requires and what guarantees it can actually provide.

**Research status:** Initial conceptual analysis and deterministic model prepared; deeper formalization, clock-source evaluation, and hardware-backed experiments remain open.

## Cross-cutting evaluation contract — Engineering Quality Charter

This research item is governed by the project-wide [Engineering Quality Charter](../../foundation/engineering-quality-charter.md). Its topic-specific claims must be evaluated across all applicable dimensions:

- **Security:** define assets, attacker capabilities, trust boundaries, enforcement path, least-authority behavior, abuse/DoS cases, and residual risks.
- **Correctness and reliability:** state invariants, safety and liveness properties, concurrency/TOCTOU hazards, failure points, recovery semantics, and falsifying counterexamples.
- **Performance:** compare against a credible baseline using the same workload; report latency distributions (including tail latency), throughput, and worst-case behavior where meaningful.
- **Efficiency:** account for CPU, memory, allocations, synchronization, context switches, I/O, data movement, storage amplification, and energy where measurable.
- **Innovation:** identify closest prior art and state the precise, falsifiable difference. Do not equate a new name or combination with global novelty.
- **Evidence:** label results as conceptual, formalized, modeled, tested, measured, reviewed, verified, implemented, or production-validated. A toy-model PASS is not proof of a real operating-system guarantee.

Where comparison is relevant, evaluate at least three credible approaches under equivalent assumptions. Record negative results and unmodeled behavior. Until the missing threat analysis, comparative evaluation, and reproducibility requirements are met, this document remains an initial research draft and cannot justify an architecture decision.
