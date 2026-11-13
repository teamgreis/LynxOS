# F-001-C — Failure, Cancellation, and Recovery Semantics

**Status:** Research draft; no architecture decision  
**Date:** 2026-11-02  
**Program:** R0 — Computing foundations  
**Parent:** F-001 — What Is a Computer at the Most Fundamental Level?  
**Related:** F-001-B — Causality and Concurrent State Transitions

## 1. Research question

Can a computation model describe failure, cancellation, and recovery as explicit behavior rather than treating them as exceptional details outside the model?

The goal is not to promise that every operation can be rolled back or that every failure can be hidden. The goal is to specify exactly:

- what may have happened before failure;
- what state survives;
- what observers may have seen;
- what cancellation guarantees;
- what recovery is allowed to do;
- when retry is safe;
- which guarantees are impossible under the selected assumptions.

## 2. Failure is not one thing

A model must distinguish at least these failure classes:

| Failure class | Meaning | Typical consequence |
|---|---|---|
| Crash-stop | Component stops and does not recover | Its volatile state and future actions disappear |
| Crash-recovery | Component stops and later restarts | Volatile state may be lost; persistent state may survive |
| Crash-amnesia | Component restarts without remembering prior volatile history | Retries may repeat work unless durable evidence exists |
| Omission | A send, receive, or other action does not occur | A peer may wait or time out |
| Link failure / partition | Communication is interrupted | Components may disagree about reachability |
| Byzantine | Component may behave arbitrarily or maliciously | Crash-only assumptions are insufficient |
| Resource exhaustion | Memory, CPU, storage, or another resource is unavailable | Progress or correctness may be affected |
| Power-loss / storage failure | Persistent writes may be incomplete or reordered | Durability assumptions must be explicit |

These are different models, not interchangeable synonyms. A proof under crash-stop assumptions does not automatically apply to Byzantine behavior or to power loss during storage updates.

Useful prior art:
- Fred B. Schneider, [Implementing Fault-Tolerant Services Using the State Machine Approach](https://doi.org/10.1145/98163.98167), 1990.
- [A Formal Model of Crash Recovery in a Distributed System](https://doi.org/10.1109/TSE.1983.236608), 1983.
- [A Behavioral Theory for Distributed Systems with Weak Recovery](https://doi.org/10.46298/lmcs-21(3:1)2025), 2025.

## 3. State must distinguish volatile and durable facts

A useful model must not treat "state" as one undifferentiated store.

Let a configuration be:

\[
s=(V,D,E)
\]

where:

- \(V\) is volatile state, which may be lost on a crash;
- \(D\) is durable state, which survives only under a stated storage assumption;
- \(E\) is externally observable history, such as messages, acknowledgements, or physical effects.

This separation is essential. A process can lose its memory while a remote service has already observed a request. A local rollback cannot undo an external event that has already happened.

A crash transition may therefore be modeled as:

\[
(V,D,E,\text{up})\xrightarrow{crash}(V_0,D,E,\text{down})
\]

where \(V_0\) is the restart baseline. This rule is only valid under a specific crash model: it assumes durable state \(D\) survives and external history \(E\) is not magically erased.

## 4. Operation lifecycle: do not assume atomicity

An operation may have multiple stages:

1. **Requested:** caller submits an operation.
2. **Accepted:** system records responsibility for it.
3. **Prepared:** required resources or participants are ready.
4. **Committed:** the system crosses a defined point after which the effect is considered durable or irrevocable.
5. **Acknowledged:** caller is told the result.
6. **Observed:** external parties may have acted on the result.

Not every operation needs every stage. More importantly, these stages are not automatically atomic.

A crash after a durable effect but before acknowledgement creates ambiguity: the caller may retry an operation that already happened.

### Exactly-once caution

"Exactly once" is not a magic delivery property. A system must define the operation's identity, durable deduplication state, effect/commit boundary, and failure assumptions. For arbitrary external side effects, exactly-once behavior may be impossible without cooperation from the external system or an idempotent operation.

A common safe pattern is to use a stable request identifier and atomically record both the deduplication marker and the internal state change. This only covers effects inside the same atomic durability boundary. It does not automatically include email delivery, physical actuation, or a remote API.

## 5. Cancellation is a request with semantics

Cancellation can mean different things:

- **Prevent-start:** operation has not started and will never start.
- **Cooperative cancellation:** operation observes a cancellation request at a defined safe point.
- **Forced termination:** execution is stopped, possibly leaving partial effects.
- **Compensation:** a new operation attempts to counteract a previous effect.
- **Rollback:** internal state is restored to a previous state, if the operation and effects support it.

These are not equivalent. A cancellation request arriving after an external effect cannot truthfully promise that the effect never happened. Compensation is not rollback: it is a new action with its own failure modes.

## 6. Recovery strategies to compare

| Strategy | Core idea | Strength | Main limitation |
|---|---|---|---|
| Restart from initial state | Recreate component and retry | Simple for stateless/idempotent work | Can repeat effects or lose accepted work |
| Checkpoint and restore | Persist a known consistent state | Can reduce recomputation | Checkpoint cost and consistency coordination |
| Write-ahead log / event log | Record intent or operations durably before applying | Supports replay and recovery | Log ordering, corruption, compaction, replay determinism |
| Transactional commit | Make a set of internal effects atomic | Clear commit boundary | Coordination and storage costs; external effects remain separate |
| Replication / state-machine replication | Maintain multiple copies with agreed operation order | Can tolerate selected failures | Requires explicit fault and synchrony assumptions; consensus costs |
| Compensation / saga | Apply forward actions and compensating actions | Useful for long-running workflows | Compensation may be incomplete or fail |
| Idempotent retry with deduplication | Repeat request safely using stable identity | Practical for retryable operations | Requires durable identity and bounded deduplication semantics |

Prior art:
- Schneider's state-machine approach describes fault-tolerant services and reconfiguration under specified failure models: [ACM DOI](https://doi.org/10.1145/98163.98167).
- Crash-recovery research shows that losing volatile state while retaining or losing persistent state changes what recovery protocols can guarantee: [Recovering Shared Objects Without Stable Storage](https://doi.org/10.4230/LIPIcs.DISC.2017.36).
- Recent work formalizes distributed systems with weak recovery, where a restarted node's resumed state is not assumed to be exactly known: [Fabbretti, Lanese, Stefani, 2025](https://doi.org/10.46298/lmcs-21(3:1)2025).

## 7. Candidate formal extension

Extend the earlier transition model with explicit fault and durability annotations:

\[
\mathcal{C}_F=(S,A,\to,Obs,Dur,F)
\]

where:

- \(S\): configurations;
- \(A\): action labels;
- \(\to\): transition relation;
- \(Obs\): observation semantics;
- \(Dur\): durability assumptions and persistence boundary;
- \(F\): modeled fault events and fault constraints.

This notation is deliberately provisional. It may be better to encode durability and faults as ordinary state and transition structure rather than as separate tuple components. That is an open modeling question, not a settled design choice.

## 8. Safety and liveness must be separated

A system can be safe but make no progress, or make progress while violating correctness.

- **Safety:** nothing forbidden happens. Example: a committed request is never applied twice inside the modeled atomic boundary.
- **Liveness:** something desirable eventually happens under stated assumptions. Example: an accepted request eventually completes if a correct component and required storage remain available.

Every claim must state its assumptions. An asynchronous network with unbounded message delays cannot support the same liveness guarantees as a network with known timing bounds. A crash-recovery protocol also needs explicit assumptions about stable storage, recovery behavior, and the number or placement of failures.

## 9. Hypotheses

- **H-C1:** Separating volatile, durable, and externally observable state is necessary to reason correctly about crash recovery.
- **H-C2:** A cancellation request cannot guarantee rollback of already-observed external effects without cooperation or compensation.
- **H-C3:** Retry safety requires explicit operation identity and idempotence or durable deduplication semantics.
- **H-C4:** A model that makes commit points and recovery transitions explicit can expose correctness bugs earlier than a model that treats failures as implementation exceptions.
- **H-C5:** Failure semantics can be integrated into the same transition framework used for ordinary computation, but the resulting model may become too complex to be useful.

All five hypotheses are falsifiable. In particular, H-C5 should be rejected if the unified notation obscures distinctions that separate fault models express more clearly.

## 10. Initial executable experiment

The accompanying small Python model contrasts two internal operation protocols:

1. **Naive retry:** an effect becomes durable, then an acknowledgement is recorded only in volatile state. A crash between these steps loses the acknowledgement; retry repeats the effect.
2. **Atomic commit with request identity:** the effect and deduplication marker are committed together. After a crash before acknowledgement, retry recognizes the committed request and does not apply the effect twice.

Expected result for this deliberately bounded example:
- Naive retry can produce two effects for one logical request.
- Atomic internal commit plus durable deduplication produces one effect and can safely acknowledge the retry.

This does not solve arbitrary exactly-once delivery. It only demonstrates the value and limits of an atomic internal commit boundary.

## 11. Next experiments

- Add multiple operations with dependencies and concurrent commits.
- Model cancellation before prepare, during prepare, after commit, and after external observation.
- Add crash during log write and storage reordering.
- Add a remote side effect that cannot be rolled back.
- Add recovery from corrupted or incomplete checkpoints.
- Compare restart, checkpoint, log replay, transaction, and compensation approaches.
- State explicit assumptions for every safety and liveness property.

## 12. Research integrity

Failure models, transactions, write-ahead logging, checkpointing, state-machine replication, idempotent requests, and recovery calculi are established research areas. This document does not claim novelty for them.

Any proposed LynxOS contribution must identify a specific gap in existing work and demonstrate a measurable or provable improvement.

## 13. References

1. Fred B. Schneider, [Implementing Fault-Tolerant Services Using the State Machine Approach](https://doi.org/10.1145/98163.98167), ACM Computing Surveys, 1990.
2. [A Formal Model of Crash Recovery in a Distributed System](https://doi.org/10.1109/TSE.1983.236608), IEEE Transactions on Software Engineering, 1983.
3. Michael et al., [Recovering Shared Objects Without Stable Storage](https://doi.org/10.4230/LIPIcs.DISC.2017.36), DISC 2017.
4. Fabbretti, Lanese, Stefani, [A Behavioral Theory for Distributed Systems with Weak Recovery](https://doi.org/10.46298/lmcs-21(3:1)2025), LMCS, 2025.
5. Rahli et al., [EventML: Specification, verification, and implementation of crash-tolerant state machine replication systems](https://doi.org/10.1016/j.scico.2017.05.009), Science of Computer Programming, 2017.

## Cross-cutting evaluation contract — Engineering Quality Charter

This research item is governed by the project-wide [Engineering Quality Charter](../../foundation/engineering-quality-charter.md). Its topic-specific claims must be evaluated across all applicable dimensions:

- **Security:** define assets, attacker capabilities, trust boundaries, enforcement path, least-authority behavior, abuse/DoS cases, and residual risks.
- **Correctness and reliability:** state invariants, safety and liveness properties, concurrency/TOCTOU hazards, failure points, recovery semantics, and falsifying counterexamples.
- **Performance:** compare against a credible baseline using the same workload; report latency distributions (including tail latency), throughput, and worst-case behavior where meaningful.
- **Efficiency:** account for CPU, memory, allocations, synchronization, context switches, I/O, data movement, storage amplification, and energy where measurable.
- **Innovation:** identify closest prior art and state the precise, falsifiable difference. Do not equate a new name or combination with global novelty.
- **Evidence:** label results as conceptual, formalized, modeled, tested, measured, reviewed, verified, implemented, or production-validated. A toy-model PASS is not proof of a real operating-system guarantee.

Where comparison is relevant, evaluate at least three credible approaches under equivalent assumptions. Record negative results and unmodeled behavior. Until the missing threat analysis, comparative evaluation, and reproducibility requirements are met, this document remains an initial research draft and cannot justify an architecture decision.
