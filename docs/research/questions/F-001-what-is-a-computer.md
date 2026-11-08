# F-001 — What Is a Computer at the Most Fundamental Level?

**Status:** Initial research draft  
**Program:** R0 — Computing foundations  
**Milestone:** F0 — A Neutral, Evidence-Based Map of the Design Space  
**Decision status:** No architecture decision  
**Last updated:** 2026-11-02

## 1. Research question

What is the most fundamental abstraction of a computer, independent of today's familiar operating-system and hardware conventions?

This question must not be confused with either of these narrower questions:

1. Which mathematical functions are computable in principle?
2. How should a practical machine organize the execution of computations?

The first is a question of computability. The second concerns execution models, state, communication, resources, physical realization, and system organization. A useful foundation for LynxOS must investigate both while keeping them distinct.

## 2. Scope and terminology

For this research, distinguish four layers:

- **Computability:** Which transformations or problems can be computed under a formal model?
- **Operational model:** What entities exist, what changes state, and what rules cause execution to advance?
- **Physical realization:** How are operations, state, communication, timing, and energy realized by hardware?
- **System organization:** How are computation, authority, resources, failures, persistence, and interaction composed into a usable platform?

A model may be universal in computability while being unsuitable or inefficient for a particular physical system. Conversely, an execution model may expose useful properties such as parallelism or analyzable synchronization without expanding the class of computable functions.

## 3. Established foundations

### 3.1 Turing machines and the Church–Turing thesis

Turing machines formalize effective mechanical computation through a finite description of states and transition rules operating over an abstract tape. The Church–Turing thesis identifies effectively calculable functions with those computable by a Turing machine. This is a foundational thesis about effective calculability, not a mandate that real computers or operating systems must literally be organized as Turing machines.

Reference: [Stanford Encyclopedia of Philosophy — The Church-Turing Thesis](https://plato.stanford.edu/entries/church-turing/)

### 3.2 Lambda calculus and recursive functions

The lambda calculus expresses computation through function abstraction and application, with computation represented by reduction. Church's approach and Turing's machine model were shown to be equivalent in the class of functions they capture. Their equivalence is important evidence that computation can be represented through substantially different formal structures.

Reference: [Stanford Encyclopedia of Philosophy — The Church-Turing Thesis](https://plato.stanford.edu/entries/church-turing/)

### 3.3 Stored-program / von Neumann execution

The familiar stored-program model organizes execution around instructions, memory, and a control-flow mechanism commonly represented by a program counter. This is an extremely successful practical organization, but it is only one operational organization of computation.

The research question is not whether this model works. It demonstrably does. The question is which of its properties are necessary constraints and which are design choices with trade-offs.

### 3.4 Dataflow

In dataflow models, operations become executable when their required inputs are available. A computation can be represented as a graph of operations and dependencies rather than solely as a sequential instruction stream. This can expose parallelism, but introduces challenges around token management, memory traffic, iteration, and scheduling.

References:
- [Najjar, Lee, Gao — Advances in the Dataflow Computational Model](https://ptolemy.berkeley.edu/publications/papers/99/dataflow/)
- [MIT — A Computer Architecture for Data-flow Computation](https://hdl.handle.net/1721.1/148928)

### 3.5 Actor model

The Actor model treats isolated active entities as primitives of concurrent computation. Actors communicate through messages and can be used to reason about parallel and distributed systems. This changes the organization of concurrency and communication; it does not by itself solve resource governance, failure recovery, scheduling guarantees, or physical locality.

References:
- [Agha — Actors: A Model of Concurrent Computation in Distributed Systems](https://doi.org/10.7551/mitpress/1086.001.0001)
- [Hewitt — Actor Model of Computation](https://arxiv.org/abs/1008.1459)

### 3.6 Petri nets

Petri nets model systems using places, transitions, and tokens. They provide a formal way to reason about causality, concurrency, conflicts, and synchronization. They are especially useful as an analysis model; they should not automatically be assumed to be a complete execution architecture.

Reference: [Technical University of Munich — Petri Nets](https://www.cs.cit.tum.de/en/tcs/lehre/ss26/petri-nets/)

## 4. Initial comparison

| Model | Primary abstraction | Strengths to investigate | Open costs / limitations |
|---|---|---|---|
| Turing machine | State, tape, transition | Precise computability foundation | Not a direct practical systems architecture |
| Lambda calculus | Functions, application, reduction | Compositional semantics; functional reasoning | Practical state, effects, resources, and concurrency need additional models |
| Stored-program | Instructions, memory, control flow | Generality, mature tooling, direct hardware mapping | Sequential control-flow bias; explicit concurrency coordination |
| Dataflow | Operations and dependency graph | Exposed parallelism; dependency-driven execution | Token/state overhead, memory traffic, cycles and scheduling |
| Actor model | Isolated entities and messages | Isolation, asynchronous communication, distribution | Message ordering, backpressure, resource control, failure semantics |
| Petri nets | Places, transitions, tokens | Formal concurrency and reachability analysis | Often an analysis/specification model rather than a full general-purpose platform |

This table is a research map, not a ranking. The models operate at different abstraction levels and cannot be fairly compared using a single performance or expressiveness score.

## 5. Preliminary findings

1. There is no reason to equate the mathematical definition of computation with a particular operating-system structure.
2. Equivalent computability does not imply equivalent performance, analyzability, security, reliability, or usability.
3. Concurrency and distribution require explicit treatment of causality, communication, synchronization, and failure.
4. A practical system needs a model of physical resources and time in addition to a model of abstract computation.
5. No single candidate model currently justifies being selected as LynxOS's foundational execution model.

These are preliminary conclusions from the sources listed above. They are not claims of novelty.

## 6. Falsifiable research questions

### F-001-A — Minimal operational description
Can a useful general-purpose computing system be described using a smaller or more coherent set of primitive concepts than the conventional combination of instructions, address spaces, processes, threads, and system calls?

**Test:** Define candidate primitive sets; express representative workloads and system services in each; compare semantic completeness, complexity, and implementation cost.

### F-001-B — Computation and physical location
Can computation be specified independently of where its state and execution physically reside, without hiding costs that matter for correctness or performance?

**Test:** Model local and remote execution with explicit latency, bandwidth, failure, and consistency assumptions. Check whether location-independent semantics remain valid.

### F-001-C — State and transition
Can mutable state, immutable values, events, and transitions be unified in a formal model without making reasoning or implementation less efficient?

**Test:** Define operational semantics and encode representative stateful and concurrent workloads. Compare proof obligations and implementation overhead.

### F-001-D — Concurrency as a primitive
Does making concurrency fundamental simplify correctness and resource management, or merely move complexity into scheduling and communication?

**Test:** Implement the same workloads in sequential, dataflow, actor, and hybrid prototypes. Measure throughput, tail latency, memory use, scheduling overhead, and failure behavior.

### F-001-E — Guarantees as part of execution
Can security, resource limits, and failure boundaries be represented as enforceable properties of the computation model itself rather than only as external operating-system policy?

**Test:** Specify authority and resource invariants, attempt counterexamples, and prototype enforcement mechanisms. Do not assume that a model-level description is enforceable until the trusted implementation path is identified.

## 7. Proposed experimental workload set

Any candidate model should eventually be tested against the same small workload suite:

- Pure deterministic calculation
- Mutable data structure with concurrent readers and writers
- Producer/consumer pipeline
- Cyclic dataflow computation
- Many independent message-driven tasks
- Local and remote request/response
- Deadline-sensitive operation
- Resource exhaustion
- Component crash and recovery
- Persistent update with crash consistency

The suite must include both successful execution and adversarial/failure cases.

## 8. What this research does not decide

This document does **not** select:

- A kernel, microkernel, monolithic kernel, exokernel, or kernel-less design
- A process, actor, task, object, graph, or other primitive as the final system abstraction
- A programming language or compiler architecture
- A memory model, filesystem, or security architecture
- A hardware execution strategy
- A claim that LynxOS is the first or only system to use any proposed concept

Those decisions require separate evidence and approved architecture decision records.

## 9. Next work

1. Expand the related-work matrix, including register machines, rewriting systems, cellular automata, synchronous/reactive models, process calculi, and distributed computation.
2. Formalize a neutral notation for state, operation, dependency, communication, resource, and failure.
3. Select a tiny set of workloads and model them in at least three distinct approaches.
4. Record counterexamples and negative results.
5. Publish a reviewed comparison before proposing any architecture.

## 10. References

- Stanford Encyclopedia of Philosophy, [The Church-Turing Thesis](https://plato.stanford.edu/entries/church-turing/), substantive revision 2023.
- Najjar, Lee, Gao, [Advances in the Dataflow Computational Model](https://ptolemy.berkeley.edu/publications/papers/99/dataflow/), *Parallel Computing*, 1999.
- Misunas, [A Computer Architecture for Data-flow Computation](https://hdl.handle.net/1721.1/148928), MIT, 1978.
- Agha, [Actors: A Model of Concurrent Computation in Distributed Systems](https://doi.org/10.7551/mitpress/1086.001.0001), MIT Press, 1986.
- Hewitt, [Actor Model of Computation: Scalable Robust Information Systems](https://arxiv.org/abs/1008.1459), 2010.
- Technical University of Munich, [Petri Nets](https://www.cs.cit.tum.de/en/tcs/lehre/ss26/petri-nets/).

---

**Research integrity note:** This is an initial synthesis, not a systematic literature review. The next revision must broaden the source base, distinguish primary sources from surveys, and record search terms, inclusion criteria, and unresolved disagreements.


## 11. Supporting research artifacts

- [Neutral Computation Model v0.1](./F-001-formal-model-v0.1.md) — candidate transition-based notation for cross-model comparison.
- [F-001 Related-Work Matrix](../methodology/related-work-matrix-f001.md) — broader map of computation and execution-model families.

Both artifacts are preliminary research instruments. Neither constitutes an architecture decision.


## 12. F-001-B supporting work

- [Causality and Concurrent State Transitions](./F-001-B-causality-concurrent-transitions.md) — causal partial orders, state-dependent independence, diamond checks, and counterexamples.
- [Executable explicit-state experiment](../../../experiments/f001/README.md) — small finite-state checker for independent channels and shared-slot contention.


## 13. F-001-C supporting work

- [Failure, Cancellation & Recovery Semantics](./F-001-C-failure-cancellation-recovery.md) — explicit fault classes, volatile/durable/observable state, cancellation, commit boundaries, and recovery strategies.
- [Crash/retry finite-state experiment](../../../experiments/f001/failure_retry_model.py) — contrasts naive retry with atomic internal commit and durable request identity.
- [Experiment notes](../../../experiments/f001/failure-retry-README.md) — scope and limitations.


- [F-001-D — Resource-Aware Computation](F-001-D-resource-aware-computation.md): capacity, demand, allocation, consumption, contention, fairness, deadlines, and energy limits.


- [F-001-E — Location-Independent Computation](F-001-E-location-independent-computation.md): separates location-invariant semantics from placement-dependent costs, capabilities, authority, and failures.


- [F-001-F — Identity, Authority and Computation](F-001-F-identity-authority-computation.md): separates logical identity, execution incarnation, placement, proof, and authority across lifecycle events.
- [F-001-G — State, Memory and Continuity](F-001-G-state-memory-continuity.md)
- [F-001-H — Time, Ordering and Temporal Semantics](F-001-H-time-ordering-temporal-semantics.md)
- [F-001-I — Communication, Interaction and Information Flow](F-001-I-communication-interaction-information-flow.md)
- [F-001-J — Computation, Representation and Meaning](F-001-J-computation-representation-meaning.md)
- [F-001-K — Observation, Control and Feedback](F-001-K-observation-control-feedback.md)
