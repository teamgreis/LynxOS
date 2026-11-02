# F-001 — Neutral Computation Model v0.1

**Status:** Research hypothesis; not an adopted architecture  
**Date:** 2026-11-02  
**Parent question:** [What Is a Computer at the Most Fundamental Level?](./F-001-what-is-a-computer.md)

## 1. Purpose

This document proposes a deliberately small notation for comparing computational models without assuming a particular operating-system architecture.

It is a research instrument, not a claim of mathematical novelty. Labeled transition systems, operational semantics, process calculi, and related formalisms already provide established foundations for describing state changes and observable behavior.

## 2. Minimal transition structure

Start with:

\[
\mathcal{C}_0 = (S, A, \to, O)
\]

where:

- \(S\) is a set of configurations (complete abstract states relevant to the model).
- \(A\) is a set of action labels, including an optional silent action \(\tau\).
- \(\to\;\subseteq S\times A\times S\) is a transition relation.
- \(O\) is an observation function or observation relation describing what an external observer can distinguish.

Notation:

\[
s \xrightarrow{a} s'
\]

means that configuration \(s\) may evolve to configuration \(s'\) by performing action \(a\).

The relation is intentionally nondeterministic: a configuration may have zero, one, or multiple possible successors. A model that requires deterministic behavior can impose that as an additional property.

## 3. Why this is not yet a computer model

The tuple alone says very little about whether a system is useful, implementable, secure, or efficient. It does not yet specify:

- how configurations are represented;
- whether transitions are atomic;
- how multiple transitions may proceed concurrently;
- how resources constrain execution;
- how communication crosses isolation or physical boundaries;
- how time and deadlines behave;
- how faults, cancellation, and recovery are represented;
- which observations are permitted or meaningful;
- how an abstract transition maps to hardware operations.

These are not minor implementation details. They are likely to determine whether a candidate model can support a practical operating system.

## 4. Candidate extension dimensions

Rather than immediately adding every concept to the tuple, treat these as separately testable dimensions:

| Dimension | Research question | Example property |
|---|---|---|
| State | What belongs in a configuration? | Explicit state components and identity |
| Transition | What makes an operation enabled? | Preconditions and atomicity |
| Concurrency | Can independent transitions overlap? | Independence relation or partial order |
| Communication | How does one part affect another? | Message, shared state, signal, event |
| Resources | What limits an operation? | CPU time, memory, bandwidth, energy |
| Time | How is progress measured or bounded? | Logical order, clock time, deadline |
| Authority | Who or what may cause a transition? | Authorization predicate |
| Failure | What happens when an operation cannot complete? | Fault transition, cancellation, recovery |
| Persistence | Which state survives interruption? | Commit and durability semantics |
| Observation | What can a component or user learn? | Observation boundary and noninterference |

A dimension should become part of the core formalism only when experiments show that treating it externally causes a real loss of expressiveness, clarity, or enforceability.

## 5. Encoding examples

### 5.1 Register machine

A register-machine configuration can be represented as the control state plus the contents of its registers. An instruction is an action label or transition rule. The transition relation expresses increment, decrement, conditional branch, and halt behavior.

This demonstrates that the proposed notation can describe a conventional instruction-oriented model. It does not demonstrate that the notation is better.

### 5.2 Petri net

A Petri-net marking (token distribution over places) can serve as a configuration. A transition is enabled when its input requirements are met; firing it produces a new marking.

This makes concurrency and resource-like token constraints explicit in a way that a simple sequential instruction trace may obscure.

### 5.3 Dataflow

A dataflow graph configuration can include available tokens and actor state. A firing rule determines when an actor may execute and how tokens are consumed and produced.

The semantics must distinguish variants: dataflow models do not all use identical firing, determinism, or scheduling rules.

### 5.4 Actor system

A configuration can include actor-local states and pending message queues. A transition represents an actor processing a message and changing its local state, potentially sending messages or creating actors.

The model must specify delivery, ordering, failure, and supervision assumptions rather than treating "message passing" as a complete semantics.

## 6. Required properties for any extension

Every proposed extension must state:

1. **Meaning:** A precise mathematical definition.
2. **Necessity:** Which concrete research question cannot be answered cleanly without it?
3. **Conservativity:** Does it preserve the behavior of existing examples when the new feature is unused?
4. **Compositionality:** Can systems be assembled from smaller systems while preserving stated properties?
5. **Implementability:** Is there a plausible mapping to finite hardware resources?
6. **Verifiability:** Can relevant properties be tested, model-checked, or proved?
7. **Cost:** What runtime, memory, latency, energy, or engineering overhead does it introduce?

## 7. First hypotheses to test

- **H1:** A labeled transition structure is a useful common comparison layer across otherwise different computation models.
- **H2:** Concurrency cannot be adequately compared using only a total sequence of transitions; causal or partial-order information is needed for some models.
- **H3:** Resource constraints must be explicit to compare abstract models with physical implementations.
- **H4:** Failure and cancellation semantics materially change the behavior of real systems and cannot safely be postponed to implementation notes.
- **H5:** Security authority may be modeled as a condition on transitions, but whether that is enforceable depends on the trusted implementation boundary.

Each hypothesis can be rejected. In particular, if the common structure becomes so general that it explains nothing or enables no useful comparison, it has failed as a research tool.

## 8. Initial experiment

Represent the same producer-consumer workload in:

- a sequential register-machine style;
- a token-based dataflow model;
- a Petri net;
- an actor/message-passing model.

For each representation, record:

- state definition;
- transition rules;
- concurrency semantics;
- ordering assumptions;
- resource assumptions;
- failure behavior;
- observable outputs.

Then compare how naturally each model expresses bounded buffering, backpressure, cancellation, and producer failure.

## 9. Decision

**No architecture decision.** Version 0.1 is a candidate comparison notation only. It must be revised after the first cross-model encoding exercise and independent review.

## 10. References

- [Concurrency and atomicity](https://doi.org/10.1016/0304-3975(88)90096-5), *Theoretical Computer Science*, 1988 — labeled transition relations and concurrent actions.
- [Petri Net Theory and the Modeling of Systems — Basic Definitions](https://jklp.org/profession/books/pn/2.html) — places, transitions, and markings.
- [A Denotational Semantics for Dataflow with Firing](https://ptolemy.berkeley.edu/publications/papers/97/dataflow/) — firing rules and dataflow semantics.
- [43 years of actors: a taxonomy of actor models and their key properties](https://doi.org/10.1145/3001886.3001890) — variations and properties of actor models.
- [Register Machine](https://mathworld.wolfram.com/RegisterMachine.html) — a concise overview of register-machine structure.
