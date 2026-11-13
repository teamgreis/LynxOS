# F-001-R — Computation, Information and Boundaries

**Status:** Initial research draft  
**Program:** R0 — Computing foundations  
**Decision status:** No architecture decision

## 1. Research question

How should a computing system distinguish computation from information, representation, communication, and the boundaries at which information becomes available or meaningful?

The question is deliberately broader than data structures or serialization. It asks what a system can know, what it can transform, what it can observe, and which distinctions must remain explicit.

## 2. Scope

Investigate:
- Information as distinguishable states versus semantic content.
- Encoding, representation, interpretation, and decoding.
- Information flow across component, privilege, process, machine, and trust boundaries.
- Lossless and lossy transformations; compression and abstraction.
- Metadata, provenance, labels, and information lifetime.
- The physical costs of storing, moving, and transforming information.

Information-theoretic quantities do not by themselves establish meaning. Shannon information measures uncertainty and communication properties; semantic interpretation requires an additional model. The philosophy and physics of computation literature makes this distinction explicit. [SEP: Computation in Physical Systems](https://plato.stanford.edu/entries/computation-physicalsystems/)

## 3. Competing approaches

| Approach | Core idea | Strength | Open issue |
|---|---|---|---|
| Bit/state-centric | Information is represented by distinguishable physical or logical states | Precise and implementation-near | Meaning is external to the representation |
| Symbolic/semantic | Symbols are interpreted under a formal language or model | Explicit meaning and compositional rules | Interpretation context and ambiguity |
| Information-flow | Track where information can propagate | Useful for confidentiality and integrity analysis | Labels, declassification, and covert channels |
| Provenance-centric | Data carries origin and transformation history | Auditability and accountability | Metadata integrity and overhead |
| Content-addressed | Identity derives from content digest | Deduplication and integrity checks | Mutable identity and hash trust assumptions |

## 4. Key distinctions

1. **Representation is not meaning.** Equal bit patterns may be interpreted differently under different schemas or contexts.
2. **Compression is not automatically semantics-preserving.** Lossless compression preserves recoverability of the encoded input; lossy transformations require an explicit acceptable-distortion criterion.
3. **Information movement has cost.** Latency, bandwidth, energy, and exposure to failure or observation depend on where data travels.
4. **Boundaries are policy-relevant.** A component boundary may also be a trust, authority, confidentiality, or failure boundary—but these boundaries need not coincide.
5. **Provenance is evidence, not truth.** A recorded origin chain can be incomplete, forged, or based on compromised producers.

## 5. Hypotheses and falsifiable questions

- **H-R1:** Explicit representation metadata reduces interpretation errors in heterogeneous components, at measurable storage and processing cost.
- **H-R2:** Information-flow labels can enforce a useful subset of confidentiality policies, but do not alone prevent timing and resource side channels.
- **H-R3:** Provenance improves auditability only when its creation and verification path is itself protected.
- **H-R4:** Separating semantic identity from physical representation enables migration and format evolution, provided conversion rules are explicit.

Tests should use heterogeneous producers/consumers, schema evolution, deliberate label violations, and corrupted provenance records.

## 6. Minimal experiment

The accompanying model compares:
- Raw bytes interpreted without a schema.
- Typed values interpreted with an explicit schema identifier.
- A simple information-flow label check across a boundary.

It is intentionally finite and does not model cryptographic integrity, side channels, or real serialization formats.

## 7. Prior work and references

- Claude E. Shannon, [A Mathematical Theory of Communication](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf), 1948.
- Stanford Encyclopedia of Philosophy, [Computation in Physical Systems](https://plato.stanford.edu/entries/computation-physicalsystems/).
- Dorothy E. Denning, [A Lattice Model of Secure Information Flow](https://doi.org/10.1109/TC.1976.1674681), 1976.
- NIST, [Security and Privacy Controls for Information Systems and Organizations, SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final).

## 8. What this does not decide

No data model, filesystem, object model, serialization format, security-label architecture, or storage design is selected. This document makes no novelty claim.

## 9. Experiment

- [Information-boundary model](../../../experiments/f001/information_boundary_model.py)
- [Experiment notes](../../../experiments/f001/information-boundary-README.md)

The experiment illustrates representation ambiguity and a simple label policy. It is not a security proof.

## Cross-cutting evaluation contract — Engineering Quality Charter

This research item is governed by the project-wide [Engineering Quality Charter](../../foundation/engineering-quality-charter.md). Evaluate its topic-specific claims across:

- **Security:** assets, attacker capabilities, trust boundaries, enforcement path, least authority, abuse/DoS cases, and residual risks.
- **Correctness and reliability:** explicit invariants, safety/liveness properties, concurrency and TOCTOU hazards, failure points, recovery semantics, and falsifying counterexamples.
- **Performance:** credible baseline under the same workload; latency distributions including tail latency, throughput, and worst-case behavior where meaningful.
- **Efficiency:** CPU, memory, allocations, synchronization, context switches, I/O, data movement, storage amplification, and energy where measurable.
- **Innovation:** closest prior art and a precise, falsifiable difference. A new name or combination is not proof of global novelty.
- **Evidence:** label results as conceptual, formalized, modeled, tested, measured, reviewed, verified, implemented, or production-validated. A toy-model PASS is not proof of a real operating-system guarantee.

Where relevant, compare at least three credible approaches under equivalent assumptions. Record negative results and unmodeled behavior. Until threat analysis, comparative evaluation, and reproducibility requirements are met, this remains an initial research draft and cannot justify an architecture decision.
