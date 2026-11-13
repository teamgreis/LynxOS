# F-001-I — Communication, Interaction and Information Flow

**Status:** Research question; open  
**Program:** R0 — Computing foundations  
**Parent:** [F-001 — What is a computer?](F-001-what-is-a-computer.md)  
**Related:** F-001-B causality; F-001-E location independence; F-001-F identity and authority

## Research question

What does it mean for computational entities to communicate, coordinate, and exchange information, and what guarantees govern delivery, ordering, visibility, and permitted information flow?

No IPC mechanism, network protocol, message format, shared-memory model, or security architecture is selected.

## 1. Communication is more than transport

Communication has at least four layers of meaning:
- **Interaction:** one entity influences another's state or observations.
- **Transport:** information is moved through memory, a bus, a channel, or a network.
- **Protocol:** participants agree on framing, ordering, acknowledgement, retries, and failure handling.
- **Information policy:** rules determine who may learn, modify, forward, or derive information.

A successful local write does not prove that a remote receiver processed a message. A send acknowledgement does not necessarily prove that an application effect committed. Delivery, processing, and effect commitment must be distinguished.

## 2. Communication models

| Model | Strengths | Costs / questions |
|---|---|---|
| Shared memory | Low-copy exchange; natural for tightly coupled components | Synchronization, races, aliasing, isolation, NUMA and failure boundaries |
| Message passing | Explicit ownership transfer and communication events | Serialization, queues, latency, delivery semantics |
| RPC | Procedure-like interface over a communication boundary | Partial failure, timeout ambiguity, retry and idempotency |
| Streams | Ordered sequences and backpressure | Buffering, flow control, cancellation, partial consumption |
| Publish/subscribe | Decoupled producers and consumers | Fan-out, ordering, filtering, retention and delivery guarantees |
| Actor-style messaging | Encapsulated state and asynchronous messages | Mailbox growth, supervision, message ordering scope |
| Shared log / event stream | Replay and durable history | Retention, consumer offsets, schema evolution, coordination |

These approaches are not mutually exclusive.

## 3. Delivery and effect semantics

Common delivery descriptions include:
- **At-most-once:** duplicates are suppressed or discarded; loss may remain possible.
- **At-least-once:** retries seek eventual delivery; duplicates are possible.
- **Effectively-once application effect:** deduplication and transactional boundaries can make repeated requests behave as one effect under explicit assumptions.
- **Exactly-once delivery:** a much stronger claim that must define the scope, failure model, and acknowledgement boundary.

A transport cannot generally guarantee exactly-once arbitrary external side effects without cooperation from the effecting system. Stable request identity, durable deduplication, and an atomic effect boundary are common ingredients, but they do not make every external action transactional.

## 4. Ordering and coordination

Ordering may be:
- per sender-recipient channel;
- per connection or stream;
- per object or key;
- causal across multiple senders;
- total and globally sequenced;
- intentionally unspecified.

A total order can simplify state replication but may require coordination and constrain availability or latency. Causal ordering preserves dependencies without forcing unrelated events into an artificial order. See [F-001-B](F-001-B-causality-concurrent-transitions.md) and [F-001-H](F-001-H-time-ordering-temporal-semantics.md).

## 5. Backpressure, buffering and flow control

Communication capacity is finite. Queues can grow without bound if producers outpace consumers. Candidate controls include bounded queues, producer blocking, dropping, sampling, admission control, credits, explicit demand, and load shedding.

Each policy changes observable behavior. Dropping may be acceptable for telemetry but not for durable commands. Blocking can propagate congestion and deadlock. Buffering absorbs bursts but consumes memory and increases latency.

## 6. Information flow and confidentiality

Communication policy is not only about whether a sender is authorized to call a receiver. It also concerns what information can flow through outputs, timing, errors, resource use, and derived values.

Noninterference is a foundational security idea: changes to secret inputs should not change observations available to an unauthorized observer, subject to a stated declassification policy. Real systems may intentionally release selected information; the release boundary must be explicit.

Access control and information-flow control answer different questions:
- Access control: may this entity perform this operation?
- Information-flow control: can protected information influence an observation or recipient?

Relevant prior work includes Myers and Liskov's decentralized information-flow control model.

## 7. Failure semantics

Communication can fail through loss, duplication, reordering, corruption, delay, partition, endpoint restart, identity change, or overload. A protocol must specify what each participant can conclude after timeout. A timeout is not proof that a remote operation did not happen.

The system should distinguish:
- message accepted by local transport;
- message transmitted;
- message received;
- message validated;
- request processed;
- effect committed;
- acknowledgement observed.

## 8. Hypotheses

- **H-I1:** Communication semantics must distinguish transport delivery from application effect commitment.
- **H-I2:** Retry-safe effects require stable operation identity and a defined deduplication/commit boundary.
- **H-I3:** Ordering guarantees should be scoped explicitly rather than implied globally.
- **H-I4:** Unbounded queues make resource exhaustion possible when producer and consumer rates diverge.
- **H-I5:** Authorization to communicate does not by itself prevent information leakage through derived observations.
- **H-I6:** A uniform communication abstraction may improve portability while hiding costs and failure semantics unless those remain observable.

## 9. Minimal experiment

The accompanying model:
1. demonstrates how duplicate delivery can cause three effects from two unique requests without deduplication;
2. demonstrates request-identity deduplication in a small deterministic model;
3. checks a simple noninterference property: changing a secret input does not change the modeled public output.

Run:

```sh
python3 experiments/f001/communication_information_flow_model.py
```

This model does not implement networking, cryptography, real IPC, distributed transactions, timing channels, or a formal information-flow type system.

## 10. Prior art

- Aspnes, *Notes on Theory of Distributed Systems*: formal message-passing model with process states and channels: [course notes](https://ac.informatik.uni-freiburg.de/teaching/ss_24/ds_lectures/pdf/Aspnes2020.pdf).
- NIST, *The Neutral Message Language*: illustrates a common API spanning shared memory, backplane memory, and network transports: [NIST publication](https://www.nist.gov/publications/neutral-message-language-model-and-method-message-passing-heterogeneous-environments).
- Myers and Liskov, *A Decentralized Model for Information Flow Control* (SOSP 1997): [paper](https://www.cs.cornell.edu/andru/papers/iflow-sosp97/).
- Lamport, *Time, Clocks, and the Ordering of Events in a Distributed System*: [DOI](https://doi.org/10.1145/359545.359563).

## 11. Open questions

1. Which communication guarantees should be visible to a caller?
2. What is the minimum stable identity needed for retry and deduplication?
3. How should message schemas evolve across versions and heterogeneous machines?
4. How can backpressure propagate without causing system-wide deadlock?
5. Which ordering scopes are sufficient for different workloads?
6. How should information-flow labels or policies compose across multiple hops?
7. What can be guaranteed during partitions and endpoint restarts?
8. How should cancellation interact with messages already transmitted or effects already committed?

## 12. Current conclusion

Communication cannot be reduced to moving bytes. Its semantics include delivery, processing, ordering, resource limits, failure, and information disclosure. These dimensions must be evaluated separately before selecting mechanisms.

**Research status:** Initial survey and executable conceptual model prepared; protocol-level and formal security evaluation remain open.

## Cross-cutting evaluation contract — Engineering Quality Charter

This research item is governed by the project-wide [Engineering Quality Charter](../../foundation/engineering-quality-charter.md). Its topic-specific claims must be evaluated across all applicable dimensions:

- **Security:** define assets, attacker capabilities, trust boundaries, enforcement path, least-authority behavior, abuse/DoS cases, and residual risks.
- **Correctness and reliability:** state invariants, safety and liveness properties, concurrency/TOCTOU hazards, failure points, recovery semantics, and falsifying counterexamples.
- **Performance:** compare against a credible baseline using the same workload; report latency distributions (including tail latency), throughput, and worst-case behavior where meaningful.
- **Efficiency:** account for CPU, memory, allocations, synchronization, context switches, I/O, data movement, storage amplification, and energy where measurable.
- **Innovation:** identify closest prior art and state the precise, falsifiable difference. Do not equate a new name or combination with global novelty.
- **Evidence:** label results as conceptual, formalized, modeled, tested, measured, reviewed, verified, implemented, or production-validated. A toy-model PASS is not proof of a real operating-system guarantee.

Where comparison is relevant, evaluate at least three credible approaches under equivalent assumptions. Record negative results and unmodeled behavior. Until the missing threat analysis, comparative evaluation, and reproducibility requirements are met, this document remains an initial research draft and cannot justify an architecture decision.
