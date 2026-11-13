# F-001-G — State, Memory and Continuity

**Status:** Research question; open  
**Program:** R0 — Computing foundations  
**Parent:** [F-001 — What is a computer?](F-001-what-is-a-computer.md)  
**Scope:** Logical state, representation, persistence, recovery and concurrent modification

## Research question

What does it mean for system state to remain the same when memory, execution location, time, or hardware changes?

This question examines whether a computational state can be identified independently of its current physical representation, and what guarantees are required when that state is copied, moved, persisted, reconstructed, or concurrently modified.

No storage architecture, memory model, filesystem, kernel design, or persistence mechanism is selected by this document.

## 1. Why this matters

A program's state may be represented by CPU registers, RAM pages, device state, persistent storage, remote replicas, logs, or a combination of these. Those representations can change while users expect the logical computation to continue.

The phrase "same state" is therefore ambiguous. It may mean:

- the same abstract values are observable;
- the same logical objects retain their identities;
- the same history of committed operations is preserved;
- the system can resume from a valid point after failure;
- concurrent observers see behavior allowed by a defined consistency model.

These are related but not interchangeable guarantees.

## 2. Working vocabulary

| Term | Working meaning |
|---|---|
| Logical state | Abstract information relevant to the computation, independent of a particular storage address |
| Physical representation | Bytes, pages, registers, device state, or remote copies currently encoding logical state |
| Logical identity | Identifier intended to refer to an entity across representation changes |
| Version | A distinguishable revision of an entity or state |
| Volatile state | State that may be lost on reset or power failure |
| Durable state | State guaranteed to survive a specified failure class |
| Checkpoint | Captured state intended to support later restoration |
| Recovery | Reconstruction of a valid state after interruption |
| Consistency | Rules defining which observations of concurrent or recovered state are permitted |
| Commit point | Boundary after which an operation is considered durably or logically accepted under a stated contract |

The durability contract must always name the failure model. "Persistent" without a failure model is underspecified.

## 3. Separate identity, value, version and location

A useful neutral decomposition is:

`entity = (logical\_id, version, value, representation, placement)`

This is a vocabulary aid, not a proposed LynxOS data structure.

- `logical_id` answers which logical entity is being discussed.
- `version` distinguishes successive states of that entity.
- `value` is the abstract information represented.
- `representation` describes how the information is encoded.
- `placement` describes where a representation currently exists.

Changing placement need not change logical identity. Changing value normally creates a new version, but systems differ in whether they model this as mutation, replacement, or a new immutable object.

A memory address is therefore not automatically a durable identity. Addresses can be reused, relocated, remapped, or meaningful only within one process or machine.

## 4. State continuity dimensions

Continuity should be evaluated independently across at least these dimensions:

1. **Value continuity:** Are the same abstract values recoverable?
2. **Identity continuity:** Can references still identify the intended logical entities?
3. **History continuity:** Is the committed operation history preserved without inventing or losing committed effects?
4. **Execution continuity:** Can computation resume at a valid continuation point?
5. **Observation continuity:** Do external observers see behavior allowed by the stated contract?
6. **Authority continuity:** Are permissions still valid after restoration, cloning, migration, or credential rotation?
7. **Temporal continuity:** Are deadlines, timers, leases, and ordering constraints preserved or deliberately re-established?

A checkpoint can preserve memory bytes while failing to preserve external resources, device state, open connections, timers, or authority. The boundary of captured state must be explicit.

## 5. Failure and persistence models

At minimum, distinguish:

- process termination while the machine remains available;
- operating-system crash;
- sudden power loss;
- storage-device loss or corruption;
- partial write or reordering;
- loss of a machine with remote copies available;
- network partition during replication;
- concurrent writers operating on stale versions.

Volatile and durable state should be modeled separately. A recovery procedure must state which data survives and which invariants it reconstructs.

### 5.1 Candidate persistence strategies

| Strategy | Basic idea | Main questions |
|---|---|---|
| In-place update | Modify existing representation | Can partial writes expose torn or mixed state? |
| Write-ahead log | Persist intent/change record before applying data | What counts as a complete committed record? |
| Copy-on-write | Write a new version, then switch a root/reference | Is the root switch atomic and durable? |
| Snapshot/checkpoint | Capture a recoverable state image | Is the capture internally consistent? |
| Event/state-machine replay | Reconstruct state from an ordered history | Is replay deterministic, complete and bounded? |
| Replication | Preserve copies or ordered operations elsewhere | What consistency and failure assumptions apply? |

These techniques can be combined. None is universally best.

## 6. Concurrent modification and version history

Two writers may read the same version and then attempt incompatible updates. A system needs a defined rule, for example:

- serialize updates;
- optimistic version checks and conflict rejection;
- merge operations under explicit semantics;
- last-writer-wins under a defined ordering;
- causal or stronger distributed consistency;
- application-level conflict resolution.

Linearizability is one well-known correctness condition for concurrent objects; it is not synonymous with every useful consistency model. Versioned state and MVCC are important related approaches, but their guarantees depend on transaction and visibility rules.

A state model must distinguish:
- a state that was computed;
- a state that was locally written;
- a state that became durable;
- a state that was committed;
- a state that became externally observable.

## 7. Prior art and related work

This question is grounded in established research and engineering:

- **Persistent memory and crash consistency:** research on persistent software transactions distinguishes volatile and persistent stores and studies recovery invariants. See [Defining and Verifying Durable Opacity](https://pmc.ncbi.nlm.nih.gov/articles/PMC7281866/).
- **Durable concurrent data structures:** [The Path to Durable Linearizability](https://doi.org/10.1145/3571219) studies correctness conditions for concurrent structures that must recover after crashes.
- **Write-ahead logging and persistent-memory techniques:** [Building blocks for persistent memory](https://doi.org/10.1007/s00778-020-00622-9) discusses logging and copy-on-write-related building blocks.
- **Checkpoint/restart:** [A Survey of Checkpoint/Restart Implementations](https://crd.lbl.gov/assets/pubs_presos/CDS/FTG/Papers/2002/checkpointSurvey-020724b.pdf) compares checkpointing and restart requirements, including process and multinode state.
- **Linearizability:** Herlihy and Wing, [Linearizability: A Correctness Condition for Concurrent Objects](https://doi.org/10.1145/78969.78972), defines a widely used correctness condition for concurrent objects.
- **Content-addressed identity:** content-addressed storage identifies objects through content-derived identifiers rather than their physical location. This helps separate identity from placement, but does not by itself solve mutable-state semantics, authorization, or availability.

This list is an initial survey, not an exhaustive literature review.

## 8. Competing conceptual models

The following are candidates for investigation, not architecture decisions:

1. **Address-oriented mutable memory:** identity is largely mediated by references and address spaces.
2. **Object identity plus versioning:** logical objects persist while their values advance through versions.
3. **Immutable content-addressed values:** each value is identified by its content; updates create new values and references.
4. **Event-sourced state:** current state is derived from an ordered or partially ordered history of events.
5. **Snapshot plus log:** checkpoints bound recovery work while logs preserve subsequent changes.
6. **Replicated state machine:** replicas derive state by applying a consistent ordered command history.
7. **Hybrid model:** different state classes use different identity, persistence, and consistency mechanisms.

## 9. Hypotheses

- **H-G1:** Physical address is insufficient as a general identity for state that must survive relocation or restart.
- **H-G2:** A meaningful continuity contract must distinguish value, identity, history, execution, and observation.
- **H-G3:** Crash-safe update protocols can be evaluated by whether every modeled crash point recovers to an allowed committed state.
- **H-G4:** Snapshot correctness requires a consistent boundary across all state that participates in the computation.
- **H-G5:** Concurrent state changes require an explicit conflict and visibility model.
- **H-G6:** Separating logical state from physical representation can improve portability, but introduces costs in indirection, metadata, lookup, and coordination.

These hypotheses are falsifiable and may be rejected or refined.

## 10. Minimal experiment

The accompanying model compares three simplified update protocols:

- unsafe in-place field writes;
- copy-on-write with a final atomic root switch;
- write-ahead logging with replay only after a complete durable commit record.

It injects crashes at selected boundaries and checks whether recovery yields either the complete old state or the complete new state. The in-place example intentionally exposes a torn intermediate state.

The model is deliberately small. It does not model actual disk ordering, CPU cache flush instructions, filesystem guarantees, concurrent writers, checksums, replication, or hardware faults. Passing it demonstrates only the stated abstract model.

Run:

```sh
python3 experiments/f001/state_continuity_model.py
```

## 11. Open research questions

1. Which entities need stable logical identity, and which can be identified solely by immutable content?
2. How should identity behave under clone, fork, snapshot, rollback, and replication?
3. What is the smallest state boundary that can be checkpointed consistently?
4. Which external resources can be reconstructed, and which require explicit cooperation?
5. How should time-dependent state (leases, timers, deadlines) behave after downtime?
6. What durability guarantees can be exposed portably across different hardware?
7. When is replay preferable to snapshots, and how should replay cost be bounded?
8. How can state versioning interact with authority revocation and stale references?
9. Which consistency models are needed for different classes of state?
10. Can a system make recovery semantics explicit without imposing prohibitive overhead?

## 12. Evaluation plan

For each candidate model:

1. Define its logical state and identity rules.
2. Define the failure model and durability boundary.
3. Enumerate crash points and concurrent interleavings.
4. State allowed recovered observations.
5. Implement a minimal executable model.
6. Measure recovery correctness, time, storage amplification, write amplification, metadata overhead, and coordination cost.
7. Review assumptions and compare against prior art.

## 13. Current conclusion

No architecture decision follows from this investigation yet.

The strongest immediate methodological result is that "state continuity" cannot be treated as one binary property. Value, identity, history, execution, observation, authority, and time can survive or fail independently. Future LynxOS research should state which of these guarantees each mechanism actually provides.

**Research status:** Initial model and minimal experiment prepared; broader formalization and hardware-backed evaluation remain open.

## Cross-cutting evaluation contract — Engineering Quality Charter

This research item is governed by the project-wide [Engineering Quality Charter](../../foundation/engineering-quality-charter.md). Its topic-specific claims must be evaluated across all applicable dimensions:

- **Security:** define assets, attacker capabilities, trust boundaries, enforcement path, least-authority behavior, abuse/DoS cases, and residual risks.
- **Correctness and reliability:** state invariants, safety and liveness properties, concurrency/TOCTOU hazards, failure points, recovery semantics, and falsifying counterexamples.
- **Performance:** compare against a credible baseline using the same workload; report latency distributions (including tail latency), throughput, and worst-case behavior where meaningful.
- **Efficiency:** account for CPU, memory, allocations, synchronization, context switches, I/O, data movement, storage amplification, and energy where measurable.
- **Innovation:** identify closest prior art and state the precise, falsifiable difference. Do not equate a new name or combination with global novelty.
- **Evidence:** label results as conceptual, formalized, modeled, tested, measured, reviewed, verified, implemented, or production-validated. A toy-model PASS is not proof of a real operating-system guarantee.

Where comparison is relevant, evaluate at least three credible approaches under equivalent assumptions. Record negative results and unmodeled behavior. Until the missing threat analysis, comparative evaluation, and reproducibility requirements are met, this document remains an initial research draft and cannot justify an architecture decision.
