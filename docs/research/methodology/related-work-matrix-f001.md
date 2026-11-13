# F-001 — Related-Work Matrix

**Status:** Initial map; incomplete literature review  
**Date:** 2026-11-02  
**Purpose:** Prevent rediscovery claims and identify useful comparison models.

## 1. Comparison matrix

| Family | Core abstraction | What it makes explicit | What must be investigated before comparison |
|---|---|---|---|
| Turing machines | Tape, control state, transition | Effective computation and computability | Physical cost and practical concurrency |
| Lambda calculus | Function abstraction and reduction | Substitution, evaluation, functional composition | Effects, mutable state, resources, concurrency |
| Register machines | Finite control plus registers and instructions | Simple imperative computation | Idealized register assumptions; encoding and cost |
| Stored-program / von Neumann | Instructions, memory, control flow | Sequential instruction execution and memory | Memory hierarchy, parallel execution, I/O |
| Dataflow | Operations connected by dependencies; tokens | Readiness and data dependencies | Firing rules, cycles, buffering, scheduling |
| Actor models | Isolated actors and asynchronous messages | Encapsulation and communication | Delivery, ordering, failure, supervision, backpressure |
| Petri nets | Places, transitions, markings | Concurrency, synchronization, conflict, reachability | Expressiveness, state-space growth, data representation |
| Process calculi | Processes and communication actions | Interaction, equivalence, compositional reasoning | Mapping to resources and physical implementation |
| Term rewriting | Terms and rewrite rules | Transformation rules and reduction strategies | Confluence, termination, strategy and cost |
| Graph rewriting | Graphs and local rewrite rules | Structural transformation and sharing | Matching cost, concurrency, identity and memory |
| Cellular automata | Local cells and synchronous/asynchronous updates | Locality and emergent global behavior | Programming model, universality, physical mapping |
| Synchronous/reactive systems | Logical instants and reactions | Timing assumptions and deterministic reaction | Asynchrony, clock domains, distribution |
| Distributed computation | Nodes, messages, partial knowledge | Communication, partial failure, consistency | Network assumptions, coordination and latency |

## 2. Important cautions

- These families are not all at the same abstraction level.
- Some are models of computability; others are programming semantics, concurrency models, or analysis formalisms.
- Turing completeness is not a sufficient comparison metric for a practical OS.
- A model's elegance does not establish performance, security, reliability, or usability.
- Similar vocabulary does not establish equivalent semantics. For example, actor systems and dataflow actors have different historical meanings and operational rules.
- The table is an index for further study, not an exhaustive survey.

## 3. Priority for deeper review

1. **Operational semantics and labeled transition systems:** common notation for behavior and observable actions.
2. **Petri nets and partial-order concurrency:** explicit representation of concurrency, conflict, and synchronization.
3. **Dataflow semantics:** dependency-driven execution, firing rules, bounded buffers, and determinism.
4. **Actor model variants:** isolation, message delivery, failure, and supervision semantics.
5. **Process calculi:** compositionality and behavioral equivalence.
6. **Term and graph rewriting:** state transformation, confluence, termination, and parallel rewriting.
7. **Register machines and cost models:** simple imperative baseline and resource accounting.
8. **Synchronous/reactive models:** time and deadline semantics.

## 4. Initial source set

- [Stanford Encyclopedia of Philosophy — The Church-Turing Thesis](https://plato.stanford.edu/entries/church-turing/)
- [Cambridge — Computation Theory notes: Register Machines](https://www.cl.cam.ac.uk/teaching/2021/CompTheory/comt-notes.pdf)
- [Wolfram MathWorld — Register Machine](https://mathworld.wolfram.com/RegisterMachine.html)
- [Petri Net Theory and the Modeling of Systems — Basic Definitions](https://jklp.org/profession/books/pn/2.html)
- [Molloy and Peterson — Petri Nets](https://www.jklp.org/profession/papers/Epetri/paper.html)
- [Lee — A Denotational Semantics for Dataflow with Firing](https://ptolemy.berkeley.edu/publications/papers/97/dataflow/)
- [Lee and Matsikoudis — The Semantics of Dataflow with Firing](https://ptolemy.berkeley.edu/publications/papers/08/DataflowWithFiring/)
- [De Koster et al. — 43 years of actors: a taxonomy of actor models and their key properties](https://doi.org/10.1145/3001886.3001890)
- [Concurrency and atomicity](https://doi.org/10.1016/0304-3975(88)90096-5)
- [Lamport — Time, Clocks, and the Ordering of Events in a Distributed System](https://doi.org/10.1145/359545.359563)
- [Mazurkiewicz trace theory — Theory of traces](https://doi.org/10.1016/0304-3975(88)90051-5)
- [C++ draft — Multi-threaded executions and data races](https://eel.is/c++draft/intro.races)

## 5. Review log

| Date | Change | Status |
|---|---|---|
| 2026-11-02 | Initial model families and source set collected | Preliminary; needs primary-source review |
| 2026-11-02 | Added causal partial orders, trace theory, and language memory-model references | Preliminary; source review pending |

## 6. Next actions

- Add seminal primary sources and publication metadata for every family.
- Record search queries and inclusion/exclusion criteria before calling this a systematic review.
- Add one worked example per model using the same producer-consumer workload.
- Record known limitations and counterexamples rather than only strengths.
- Compare causal order and independence explicitly; do not conflate partial-order concurrency with simultaneous hardware execution.

## Comparative evaluation dimensions

The matrix must not rank models on novelty or elegance alone. For each relevant family, record: security model and enforcement point; formal correctness evidence; fault/recovery behavior; latency and throughput under comparable workloads; CPU, memory, communication, storage and energy costs; trusted code and conceptual complexity; hardware assumptions; and closest prior art. Distinguish theoretical expressiveness from practical implementation performance. The [Engineering Quality Charter](../../foundation/engineering-quality-charter.md) defines the evidence standard.
