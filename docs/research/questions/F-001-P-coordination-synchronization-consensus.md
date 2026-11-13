# F-001-P — Coordination, Synchronization and Consensus

**Status:** Research question; no architecture decision  
**Program:** R0 Computing foundations, with links to R5/R8/R11  
**Question:** How can independent computational entities coordinate access, ordering, and decisions under concurrency, delay, and failure?

## 1. Scope

Coordination is broader than consensus. It includes mutual exclusion, rendezvous, barriers, ordering, leader election, replicated-log agreement, resource arbitration, and distributed decisions.

Important properties must be separated:
- **Agreement:** correct participants do not decide conflicting values.
- **Validity:** a decision is justified by permitted proposals.
- **Termination / liveness:** participants eventually decide, under stated assumptions.
- **Mutual exclusion:** critical sections do not overlap.
- **Fairness:** eligible participants are not postponed indefinitely.
- **Linearizability / ordering:** operations appear to take effect in a permitted order.

## 2. Coordination families

| Family | Typical mechanism | Main trade-off |
|---|---|---|
| Shared-memory synchronization | Locks, atomics, condition variables, barriers | Fast local coordination; contention and memory-model complexity |
| Message passing | Request/reply, channels, mailboxes | Explicit ownership and communication; delay and delivery semantics |
| Token / permission protocols | Token passing, distributed permission | Clear authority; token loss/recovery and latency |
| Leader-based coordination | Leader orders commands or grants leases | Simple ordering; leader failure and election |
| Quorum-based replication | Intersecting voting sets | Fault tolerance; quorum availability and membership assumptions |
| Optimistic coordination | Execute speculatively, validate/commit | High concurrency; conflicts and retries |
| Randomized / failure-detector approaches | Randomization or additional failure information | Progress under weaker timing assumptions; probabilistic or detector assumptions |

## 3. Fundamental limitation

The Fischer–Lynch–Paterson result shows that deterministic consensus cannot guarantee termination in a fully asynchronous message-passing system if even one process may crash, under the theorem's assumptions. It does **not** say consensus is never achievable in practice. Practical protocols add assumptions or mechanisms: partial synchrony, failure detectors, randomization, or restrictions on failures. Safety and liveness claims must state those assumptions.

A quorum is not a magic “majority makes it safe” rule by itself. Correctness depends on quorum intersection, membership configuration, failure model, and the protocol's rules for promises/epochs/commit.

## 4. Questions and hypotheses

- **H-P1:** Coordination costs depend strongly on contention, communication delay, and failure assumptions.
- **H-P2:** A protocol may preserve agreement while temporarily sacrificing progress.
- **H-P3:** Quorum intersection can prevent conflicting commits only when combined with protocol-specific state and configuration rules.
- **H-P4:** Local synchronization and distributed consensus solve different scales of coordination and should not be conflated.
- **H-P5:** Explicitly modeling timeout uncertainty prevents treating “slow” as equivalent to “failed.”

## 5. Toy experiment

`coordination_model.py` compares a naive single-vote acceptance rule with a two-of-three quorum threshold. It enumerates possible voter sets and checks whether two disjoint sets can each reach the threshold.

This isolates quorum intersection as one necessary structural property for this simplified voting abstraction. It does not implement a consensus protocol, leader election, crash recovery, Byzantine tolerance, or durable commit.

## 6. Open research questions

1. Which coordination guarantees are required locally, across cores, and across machines?
2. What are the acceptable trade-offs between availability, safety, and progress?
3. How should leases, epochs, fencing tokens, and revocation interact?
4. Can deterministic replay or causal ordering reduce coordination without imposing global serialization?
5. How should membership changes preserve quorum safety?

## 7. Prior work

- Fischer, Lynch, Paterson, [Impossibility of Distributed Consensus with One Faulty Process](https://ying-zhang.cn/dist/1985-flp.html), JACM 1985.
- Lynch and Sastry, [Consensus using Asynchronous Failure Detectors](https://dspace.mit.edu/entities/publication/540f2dfe-a684-4be4-91da-329f67a9f939), MIT-CSAIL-TR-2015-006.
- [Consensus and Replicated State Machines](https://people.cs.rutgers.edu/~pxk/classes/417/notes/consensus-guide.html), Rutgers course notes.

## 8. Decision status

**No decision.** No lock model, distributed protocol, quorum size, failure detector, or consistency guarantee is selected.
