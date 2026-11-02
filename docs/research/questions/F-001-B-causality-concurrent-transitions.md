# F-001-B — Causality and Concurrent State Transitions

**Status:** Research draft; no architecture decision  
**Date:** 2026-11-02  
**Program:** R0 — Computing foundations  
**Parent:** F-001 — What Is a Computer at the Most Fundamental Level?

## 1. Research question

When must computational events be ordered, and when may they occur independently?

The objective is to distinguish:

- causal dependence;
- independence under a defined observation model;
- conflicts and shared constraints;
- concurrency as a semantic property;
- parallel execution as a physical implementation choice.

These concepts are related but not identical. Two events may be causally unordered in an abstract model without literally executing at the same physical instant.

## 2. Established foundations

### 2.1 Lamport's happened-before relation

Lamport defines a causal relation over events using three rules:

1. If two events occur in one process, and the first precedes the second in that process, the first happened before the second.
2. Sending a message happened before receiving that message.
3. The relation is transitive.

The resulting relation is a partial order. Events that are not ordered by this relation are concurrent in the model's causal sense.

Important limitation: causal incomparability does not prove simultaneous physical execution. It means the model contains no causal path ordering the events. Physical scheduling, resource constraints, and additional dependencies may still constrain implementation.

Reference: Lamport, *Time, Clocks, and the Ordering of Events in a Distributed System*, Communications of the ACM 21(7), 1978. [Microsoft Research](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/) · [DOI](https://doi.org/10.1145/359545.359563)

### 2.2 Mazurkiewicz trace theory

Trace theory formalizes concurrent behavior through an independence relation over actions. Sequences that differ only by swapping adjacent independent actions can represent the same concurrent behavior.

This is a major prior-art result and must be treated as such. LynxOS must not claim novelty for partial orders, event independence, or equivalence under swapping independent actions.

Reference: *Theory of traces*, Theoretical Computer Science 60(1), 1988. [DOI](https://doi.org/10.1016/0304-3975(88)90051-5)

### 2.3 Petri nets

Petri nets model concurrency through enabled transitions and markings. Multiple transitions may be enabled at once; whether they can fire independently depends on their input/output conditions and the net's semantics.

Petri nets are a useful comparison and analysis model, not automatically a proposed LynxOS execution substrate.

## 3. Candidate formal definitions

### 3.1 Events and causal order

Let \(E\) be a set of event instances.

Define \(\prec\;\subseteq E\times E\) as a strict causal order with:

- irreflexivity: no event precedes itself;
- transitivity: if \(e_1\prec e_2\) and \(e_2\prec e_3\), then \(e_1\prec e_3\).

For events \(e_1,e_2\):

- \(e_1\prec e_2\): the first causally precedes the second;
- \(e_2\prec e_1\): the second causally precedes the first;
- neither relation holds: the events are causally incomparable in this model.

Causal incomparability is not by itself a guarantee that execution can be parallelized. Other constraints may exist.

### 3.2 State-dependent independence

Let a labeled transition system be \((S,A,\to)\), with states \(s\in S\) and action labels \(a,b\in A\).

A strong candidate test for independence at state \(s\) is a diamond property:

\[
\begin{array}{ccc}
& s & \\
a\swarrow & & \searrow b \\
s_a & & s_b \\
b\searrow & & \swarrow a \\
& s_{ab} &
\end{array}
\]

More precisely, if:

\[
s\xrightarrow{a}s_a
\qquad
s\xrightarrow{b}s_b
\]

then there must be a common state \(s_{ab}\) such that:

\[
s_a\xrightarrow{b}s_{ab}
\qquad
s_b\xrightarrow{a}s_{ab}
\]

The two paths must also be equivalent under the chosen observation semantics. Exact state equality may be too strong for some abstractions; observational equivalence may be appropriate, but must be defined explicitly.

This is a candidate criterion, not a universal definition for all concurrent systems. It may need weakening or refinement for nondeterministic, distributed, irreversible, or externally observable actions.

### 3.3 Read/write footprints as a conservative test

For an action \(a\), define:

- \(R(a)\): state locations or resources read by the action;
- \(W(a)\): state locations or resources written by the action.

A conservative sufficient condition for disjoint data access is:

\[
W(a)\cap(R(b)\cup W(b))=\varnothing
\]

and

\[
W(b)\cap(R(a)\cup W(a))=\varnothing
\]

This is only a conservative approximation. It does not capture all hidden effects, I/O, timing, locks, resource contention, external observers, or semantic dependencies. A correct footprint must include every effect relevant to the stated observation and correctness model.

## 4. Worked examples

### Example A — Independent state components

Initial state:

\[
s=(x=0,y=0)
\]

Actions:

- \(a\): increment \(x\);
- \(b\): increment \(y\).

Both orders reach:

\[
(x=1,y=1)
\]

If there are no hidden shared effects and observations do not distinguish the intermediate order, these actions satisfy the diamond test.

### Example B — Read/write conflict

Initial state:

\[
s=(x=0)
\]

Actions:

- \(a\): set \(x:=1\);
- \(b\): read \(x\) and publish the value externally.

The final memory state alone is insufficient to establish independence. The published output may differ depending on the order. The observation model must include the external publication.

### Example C — Two increments of one shared counter

Two atomic increments of the same counter can produce the same final value regardless of order. That does not automatically make them independent in every sense: intermediate observations, event identity, transaction boundaries, overflow, memory ordering, and other side effects may distinguish the executions.

This example prevents a simplistic rule that "same write location always means conflict" or that "same final state always means independence." The answer depends on semantics.

### Example D — Producer and consumer

A producer writes an item into a bounded queue; a consumer removes an available item.

The consumer's operation depends on the producer when the queue is empty. If an item is already available, they may still conflict on queue metadata or capacity. A correct model must express availability, buffer bounds, ordering, and backpressure.

## 5. Hypotheses

- **H-B1:** A causal partial order is a more faithful semantic description of concurrent behavior than a single total event order for models with independent events.
- **H-B2:** A state-dependent diamond criterion can identify some safe action reorderings, provided the observation model includes all relevant effects.
- **H-B3:** Read/write footprints are useful as a conservative approximation, but are insufficient as a complete independence semantics.
- **H-B4:** Resource constraints can serialize operations that are semantically independent.
- **H-B5:** Cancellation, failure, and external I/O can invalidate independence that appears valid in a simplified state model.

Every hypothesis is falsifiable. A counterexample should be recorded, not patched away by silently changing definitions.

## 6. Experiment plan

Encode the same bounded producer-consumer workload in four models:

1. Sequential register-machine style.
2. Dataflow graph with explicit token/firing semantics.
3. Petri net with bounded places.
4. Actor system with message queues.

For each, document:

- state representation;
- event identity;
- causal edges;
- action preconditions;
- read/write footprint;
- independent and dependent event pairs;
- observable traces;
- resource constraints;
- failure and cancellation behavior.

Then test these cases:

- Empty queue: consumer must wait or fail according to the model.
- One item: producer and consumer interact.
- Full queue: producer experiences backpressure.
- Two producers: item ordering and capacity contention.
- Producer crash: queued and in-flight work semantics.
- Consumer cancellation: ownership and item disposition.
- Resource exhaustion: progress and recovery.

## 7. Evaluation criteria

A candidate model is useful only if it supports:

- **Soundness:** declared reorderings preserve the specified observable behavior.
- **Clarity:** dependencies and conflicts can be identified without ambiguous hidden assumptions.
- **Compositionality:** local reasoning remains useful when components are combined.
- **Implementability:** physical resource and scheduling limits can be represented.
- **Verifiability:** relevant properties can be tested or formally checked.
- **Cost visibility:** serialization, synchronization, memory, and scheduling costs are measurable.

No performance advantage is claimed until a prototype is measured against a relevant baseline.

## 8. What this does not decide

This research does not select:

- a global scheduler or scheduler-free architecture;
- actors, dataflow, Petri nets, or any other model as the final execution substrate;
- a memory consistency model;
- a synchronization primitive;
- a kernel design;
- a new programming language.

## 9. Research integrity and prior art

The central ideas of causal partial orders, happened-before, logical clocks, independence relations, trace equivalence, and Petri-net concurrency are established prior art.

Potentially novel work, if any, must emerge from a precise combination or extension that offers a demonstrated benefit not already covered by existing literature. No novelty claim is made here.

## 10. References

1. Leslie Lamport, [Time, Clocks, and the Ordering of Events in a Distributed System](https://doi.org/10.1145/359545.359563), *Communications of the ACM*, 21(7), 1978.
2. *Theory of traces*, [Theoretical Computer Science 60(1)](https://doi.org/10.1016/0304-3975(88)90051-5), 1988.
3. [Petri Net Theory and the Modeling of Systems — Basic Definitions](https://jklp.org/profession/books/pn/2.html).
4. [C++ draft — Multi-threaded executions and data races](https://eel.is/c++draft/intro.races), for a concrete example of language-level memory-order constraints. The C++ memory model is not a universal concurrency model; it is one implementation-relevant semantics.

## 11. Next step

Create a worked, executable small-state model for the bounded producer-consumer example. Enumerate reachable states and transitions, then check whether proposed independent transitions satisfy the diamond condition and preserve observations.
