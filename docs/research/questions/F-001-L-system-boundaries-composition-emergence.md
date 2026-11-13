# F-001-L — System Boundaries, Composition and Emergence

**Status:** Research question; open  
**Program:** R0 — Computing foundations  
**Parent:** [F-001 — What is a computer?](F-001-what-is-a-computer.md)

## Research question

How can a system be decomposed into interacting parts, how do those parts compose into a larger whole, and which properties of the whole can be derived from properties of its parts?

No component model, hierarchy, service boundary, or system decomposition is selected.

## 1. Boundaries are modeling choices

A boundary separates a system from its environment or one subsystem from another. It may be defined by:
- state ownership;
- execution and failure domain;
- address-space or privilege boundary;
- interface and protocol;
- resource accounting;
- physical location;
- administrative or trust domain.

Different boundaries need not coincide. A component may share a process with another component while having a separate authority boundary; two components on one machine may have distinct failure domains only to a limited extent.

## 2. Composition

Composition combines parts and their interfaces into a larger system. Merely connecting interfaces does not prove that the result is correct.

A component contract can be represented conceptually as:
- assumptions about its environment;
- guarantees it provides when assumptions hold;
- resources or capabilities it requires;
- failure and lifecycle behavior.

Assume-guarantee reasoning attempts to establish system properties from local contracts and the compatibility of their assumptions and guarantees. The challenge is choosing sound assumptions and a useful decomposition.

## 3. Emergent properties

A property is emergent relative to a model when it belongs to the composed system and cannot be inferred by inspecting each component in isolation under the chosen abstraction.

Examples include:
- deadlock caused by a cycle of individually valid waits;
- global throughput limited by a shared bottleneck;
- emergent availability determined by topology and correlated failures;
- system-wide information leakage through composition;
- resource starvation created by competing local policies.

"Emergence" should not be used as a synonym for unexplained behavior. The interaction rules and system boundary must be stated.

## 4. Decomposition trade-offs

| Decomposition | Benefit | Risk |
|---|---|---|
| By function | Clear responsibilities | Hidden shared state or cross-cutting behavior |
| By resource | Explicit ownership/accounting | Tight coupling to resource topology |
| By trust | Stronger authority separation | More interfaces and mediation |
| By failure domain | Limits fault propagation | Replication and coordination costs |
| By location | Maps to deployment topology | Network and migration assumptions leak into design |
| Hierarchical | Local reasoning and delegation | Parent bottlenecks and hidden dependencies |
| Flat/peer | Symmetry and flexible composition | Global coordination complexity |

## 5. Composition properties

Candidate properties include:
- interface compatibility;
- invariant preservation;
- deadlock freedom;
- bounded resource use;
- information-flow constraints;
- progress and liveness;
- fault containment;
- substitutability;
- compositional verifiability.

A property may be locally true and globally false. For example, each component may terminate individually while their composition deadlocks through cyclic resource acquisition.

## 6. Hypotheses

- **H-L1:** A useful system decomposition must state which state, authority, resource, and failure boundaries it establishes.
- **H-L2:** Local component correctness does not imply global correctness without assumptions about interactions.
- **H-L3:** Assume-guarantee contracts can reduce reasoning scope when their assumptions are sound and composable.
- **H-L4:** Shared resources and cyclic dependencies are common sources of emergent global behavior.
- **H-L5:** No single decomposition criterion is optimal for function, security, performance, and fault isolation simultaneously.
- **H-L6:** A system model should make cross-boundary dependencies explicit.

## 7. Minimal experiment

The accompanying graph model creates three individually simple components with resource dependencies. It detects a cyclic wait graph, then compares it with an acyclic composition. The example illustrates that composition can introduce deadlock even when each component's local behavior is simple.

Run:

```sh
python3 experiments/f001/system_composition_model.py
```

This is a graph-level illustration, not a general deadlock detector for arbitrary programs.

## 8. Prior art

- Cimatti, Demasi and Tonetta, *Tightening the contract refinements of a system architecture* (2018): [open-access article](https://link.springer.com/article/10.1007/s10703-017-0312-9). Contract-based design uses component assumptions and guarantees and checks refinement across hierarchical composition.
- Chilton, Jonsson and Kwiatkowska, *Compositional assume–guarantee reasoning for input/output component theories* (2014): [DOI](https://doi.org/10.1016/j.scico.2013.12.010).
- Silva and Perkusich, *Composition of software artifacts modelled using Colored Petri nets* (2005): [DOI](https://doi.org/10.1016/j.scico.2004.11.011).

## 9. Open questions

1. Which boundaries should be explicit in a general computation model?
2. How should shared state be represented across component boundaries?
3. What makes a component contract composable?
4. How can global properties be derived without exploring the full state space?
5. How should dynamic membership affect system invariants?
6. Can a component be substituted without invalidating assumptions elsewhere?
7. How should topology and resource dependencies be modeled together?

## 10. Current conclusion

A system is not merely a bag of components. Its global behavior depends on the contracts, shared resources, dependencies, and failure relationships created by composition. Any later architecture must justify its boundaries and the properties those boundaries actually enforce.

**Research status:** Initial conceptual analysis and graph experiment prepared; formal contract composition and larger-scale evaluation remain open.
