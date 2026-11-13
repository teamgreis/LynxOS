# F-001-E — Location-Independent Computation

**Status:** Exploratory research; no architecture decision
**Research program:** R0 — Computing foundations
**Parent:** [F-001 — What is a computer?](F-001-what-is-a-computer.md)

## Research question

Can a computation retain its defined meaning when its execution location changes, while the model still represents the real costs and constraints introduced by location?

This is not the claim that local and remote execution are physically equivalent. It asks which semantic properties can remain invariant, which properties necessarily change, and what information a computation must expose to make placement, migration, replication, or remote execution safe.

## Terminology: do not conflate the transparencies

- **Location transparency:** a name or reference does not encode the current physical location.
- **Migration transparency:** an activity or resource can move without changing how it is addressed.
- **Relocation transparency:** movement can occur while an operation or interaction is in progress.
- **Access transparency:** differences in access mechanisms or representation are hidden.
- **Replication transparency:** multiple copies are presented through a defined consistency model.
- **Failure transparency:** failures are masked or represented through an explicit recovery contract.

These are distinct properties. A system may provide one and not the others.

## The central distinction: semantics versus cost

Let a computation be described by an abstract specification P, an initial logical state s, and an execution location l. Let Obs(P,s,l) denote the observations visible at the specified interface.

A candidate semantic location-independence condition is:

    Obs(P, s, location_a) ≈ Obs(P, s, location_b)

where ≈ is an explicitly chosen observational equivalence, not necessarily equality of timing, energy use, failure probability, or resource consumption.

Location can affect:
- communication latency and bandwidth;
- data movement and locality;
- available instruction sets, accelerators, and device capabilities;
- memory capacity and memory consistency;
- trust boundaries and authority to access data;
- availability, partition behavior, and failure modes;
- energy cost and resource budgets.

Therefore, hiding location from an application interface does not make location irrelevant to system behavior.

## Candidate execution-location model

Represent an execution placement as a mapping:

    place : activity -> execution_location

A location may identify a core, processor, device, host, region, or an abstract execution resource. A placement change is a transition from place_0 to place_1. The model must separately describe:

1. the logical state transferred or reconstructed;
2. the authority and data dependencies required at the destination;
3. the communication and migration costs;
4. the consistency boundary during movement;
5. what happens if source, destination, or network fails mid-transition;
6. which observations must remain equivalent and which are allowed to differ.

This is a research vocabulary, not a selected implementation model.

## Competing approaches

| Approach | Description | Potential strength | Key limitation |
|---|---|---|---|
| Fixed placement | Activity remains bound to a known processor or host | Predictable locality and simple assumptions | Limited mobility and load balancing |
| Remote invocation | Caller stays in place and invokes a remote service | Clear request/response boundary | Network latency, partial failure, serialization |
| Mobile computation | Code or an activity moves toward data or capacity | Can reduce repeated data transfer or exploit idle resources | State transfer, identity, trust, and migration consistency |
| Data movement | Computation stays put; required data is transferred | Simple execution-location semantics | Large data may dominate cost and expose security concerns |
| Replication | Multiple copies serve work or hold state | Availability and locality | Consistency, coordination, stale reads, write conflicts |
| Location-aware placement | Application/system exposes location and locality constraints | Avoids pretending location has no cost | More complex programming and placement contracts |
| Distributed-by-default model | Interactions are asynchronous messages even locally; local execution is an optimization | Avoids assuming remote calls behave like local calls | Requires serialization and asynchronous interaction semantics everywhere |

No approach is selected. Several can coexist for different activity types.

## Prior art and existing systems

- **Distributed Systems: Principles and Paradigms:** distinguishes access, location, migration, relocation, replication, concurrency, and failure transparency. Logical naming is a key mechanism for location transparency. [Reference text](https://ndl.ethernet.edu.et/bitstream/123456789/90350/10/Distributed%20systems%20Reference%20book.pdf).
- **Apache Pekko location transparency:** deliberately uses asynchronous message passing both locally and across nodes. Its documentation explicitly notes that distributed execution imposes constraints such as serialization and asynchronous interactions; it argues for designing remote-first and optimizing local execution. [Documentation](https://pekko.apache.org/docs/pekko/current/general/remoting.html).
- **ActOp (EuroSys 2016):** dynamically co-locates frequently communicating actors to reduce remote communication and queuing latency. The published evaluation reports workload-specific improvements, not universal guarantees. [Microsoft Research publication](https://www.microsoft.com/en-us/research/publication/optimizing-distributed-actor-systems-for-dynamic-interactive-services/).
- **Geo (OOPSLA 2017):** studies geo-distributed actor services, using caching and replication with explicit consistency choices to manage latency and locality. [Google Research publication](https://research.google/pubs/geo-distribution-of-actor-based-services/).
- **Kim and Agha (SC 1995):** investigates location transparency, actor placement, migration, naming, and load balancing in a concurrent object-oriented language runtime. [Publication record](https://experts.illinois.edu/en/publications/efficient-support-of-location-transparency-in-concurrent-object-o).
- **Serverless End Game (2020):** explores disaggregated compute, memory, and storage, while identifying locality as an enduring challenge even when resources are abstracted. [arXiv](https://arxiv.org/abs/2006.01251).

Prior art is extensive. LynxOS makes no novelty claim. The research opportunity is to define a precise separation between location-invariant semantics and location-dependent execution properties.

## Hypotheses

- **H-E1:** Some classes of computation can preserve their specified observations across locations when their state, inputs, capabilities, and consistency contract are preserved.
- **H-E2:** Location transparency without explicit latency, failure, and resource semantics encourages incorrect assumptions about remote execution.
- **H-E3:** Moving computation toward data can outperform moving data toward computation when data-transfer cost dominates migration cost.
- **H-E4:** Replication can improve read locality and availability only under a clearly specified consistency contract.
- **H-E5:** A location-independent identity and a location-dependent placement should be represented separately.
- **H-E6:** A distributed-by-default asynchronous interaction model can avoid local/remote semantic mismatches, but imposes serialization and asynchronous control-flow requirements even for local execution.

## Experiment plan

The accompanying deterministic cost model compares three placements for the same abstract operation: move the input data to a fixed compute location, move the computation to the data, and execute remotely with a fixed round-trip communication cost. It uses identical logical input and a deterministic operation so that output equivalence can be checked separately from cost.

The model measures estimated elapsed cost and bytes transferred. It is a toy analytical model, not a network benchmark. It does not model failures, consistency protocols, serialization overhead beyond a configurable fixed term, trust, heterogeneous instruction sets, or migration of mutable state.

## Evaluation criteria

- Semantic equivalence of visible results under the declared assumptions.
- End-to-end latency, including data transfer and migration overhead.
- Bytes transferred in each direction.
- Sensitivity to data size, compute cost, bandwidth, and round-trip latency.
- Behavior when destination capabilities differ.
- Failure and recovery behavior during migration or remote invocation.
- Security and authority changes when computation moves to another trust domain.

## Open questions

1. Which computations are safely movable: pure functions, stateful activities, transactions, or arbitrary execution contexts?
2. What is the minimum state required to resume an activity elsewhere?
3. How should references remain valid when their targets move?
4. When is location transparency harmful because it hides meaningful cost?
5. Can locality be an optimization hint without becoming a semantic dependency?
6. How do authority, identity, and trust travel with computation?
7. What guarantees can be made during partitions or partial migration?
8. How should the model represent heterogeneous hardware capabilities?

## Research conclusion

Location independence should not mean pretending all locations are equivalent. A useful model must separate logical identity and specified behavior from physical placement, while retaining explicit costs, capabilities, authority, and failure semantics.

**Decision status:** No distributed execution model, actor model, migration protocol, naming scheme, consistency model, or placement policy is selected.

## Cross-cutting evaluation contract — Engineering Quality Charter

This research item is governed by the project-wide [Engineering Quality Charter](../../foundation/engineering-quality-charter.md). Its topic-specific claims must be evaluated across all applicable dimensions:

- **Security:** define assets, attacker capabilities, trust boundaries, enforcement path, least-authority behavior, abuse/DoS cases, and residual risks.
- **Correctness and reliability:** state invariants, safety and liveness properties, concurrency/TOCTOU hazards, failure points, recovery semantics, and falsifying counterexamples.
- **Performance:** compare against a credible baseline using the same workload; report latency distributions (including tail latency), throughput, and worst-case behavior where meaningful.
- **Efficiency:** account for CPU, memory, allocations, synchronization, context switches, I/O, data movement, storage amplification, and energy where measurable.
- **Innovation:** identify closest prior art and state the precise, falsifiable difference. Do not equate a new name or combination with global novelty.
- **Evidence:** label results as conceptual, formalized, modeled, tested, measured, reviewed, verified, implemented, or production-validated. A toy-model PASS is not proof of a real operating-system guarantee.

Where comparison is relevant, evaluate at least three credible approaches under equivalent assumptions. Record negative results and unmodeled behavior. Until the missing threat analysis, comparative evaluation, and reproducibility requirements are met, this document remains an initial research draft and cannot justify an architecture decision.
