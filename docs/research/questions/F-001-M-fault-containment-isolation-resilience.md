# F-001-M — Fault Containment, Isolation and Resilience

**Status:** Research question; open  
**Program:** R0 — Computing foundations  
**Parent:** [F-001 — What is a computer?](F-001-what-is-a-computer.md)  
**Related:** F-001-C failure and recovery; F-001-F identity and authority; F-001-L system composition

## Research question

How can faults be detected, contained, and recovered from so that local failures do not unnecessarily become system-wide failures?

No process model, microkernel design, restart policy, redundancy scheme, or isolation mechanism is selected.

## 1. Faults, errors and failures

A fault is a cause or defect; an error is an incorrect internal state; a failure is externally observable deviation from required service. A fault may remain latent, an error may be detected and corrected, or an error may propagate until service fails.

Fault models must be explicit: crash-stop, omission, timing, corruption, Byzantine behavior, resource exhaustion, and common-cause failures require different defenses.

## 2. Containment boundaries

Possible containment boundaries include:
- process or address space;
- privilege or capability domain;
- virtual machine;
- hardware protection domain;
- device or driver boundary;
- network partition;
- resource quota;
- transaction or consistency boundary.

A boundary is useful only to the extent that the mechanism actually prevents propagation. A process boundary may isolate memory corruption but not shared-kernel bugs, shared power loss, or common storage failure.

## 3. Detection, containment, recovery

A resilience path can be decomposed into:
1. detect a fault or invariant violation;
2. classify the fault and affected scope;
3. contain further propagation;
4. preserve or reconstruct trusted state;
5. restart, replace, degrade, or isolate the failed component;
6. verify service restoration;
7. record evidence for diagnosis.

Detection is imperfect. False positives can trigger disruptive recovery; false negatives allow damage to spread.

## 4. Isolation and shared mechanisms

Isolation often depends on shared enforcement mechanisms. A failure in the enforcement layer can defeat multiple boundaries simultaneously. This creates a trade-off between small trusted mechanisms, performance, compatibility, and complexity.

Redundancy is not equivalent to independence. Replicas that share software defects, power, network paths, credentials, or configuration can fail together.

## 5. Graceful degradation

A system may preserve essential service while reducing optional capability. Degradation policy must specify:
- which functions are essential;
- which resource limits trigger degradation;
- what data or guarantees may be lost;
- how recovery to full service occurs;
- who may authorize a degraded mode.

A silent reduction of safety or security guarantees is not graceful degradation.

## 6. Hypotheses

- **H-M1:** Fault containment depends on explicit boundaries and independently enforced mechanisms.
- **H-M2:** A restart policy without state and side-effect semantics can repeat or lose effects.
- **H-M3:** Redundancy improves resilience only when relevant common-cause dependencies are addressed.
- **H-M4:** Detection, containment, recovery, and verification are distinct stages with distinct failure modes.
- **H-M5:** Graceful degradation requires explicit priority and guarantee policies.
- **H-M6:** Smaller fault domains may reduce propagation but increase communication, coordination, and operational overhead.

## 7. Minimal experiment

The accompanying model compares a fully connected propagation graph with a graph divided by a containment boundary. A fault originating in one node can reach all connected nodes in the first graph, while the boundary blocks propagation in the second.

Run:

```sh
python3 experiments/f001/fault_containment_model.py
```

This models reachability only. It does not prove that real process, kernel, hardware, or network isolation is effective.

## 8. Prior art

- NIST, *Guide to Industrial Control Systems (ICS) Security* discusses segmentation, defense in depth, and containment concerns: [SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final).
- Avizienis et al., *Basic Concepts and Taxonomy of Dependable and Secure Computing* (2004): [DOI](https://doi.org/10.1109/TDSC.2004.2).
- seL4, *Formally Verified Microkernel* project and verification materials: [seL4 project](https://sel4.systems/).
- Saltzer and Schroeder, *The Protection of Information in Computer Systems* (1975): [DOI](https://doi.org/10.1109/PROC.1975.9939).

## 9. Open questions

1. What fault classes must each boundary contain?
2. Which mechanisms enforce isolation, and what happens if they fail?
3. How can common-cause dependencies be discovered and modeled?
4. When should a component restart versus be replaced or degraded?
5. How can recovery avoid duplicating external side effects?
6. What evidence is needed before declaring a component healthy?
7. How should isolation interact with resource accounting and authority?
8. What is the performance and complexity cost of smaller fault domains?

## 10. Current conclusion

Resilience is not a single restart feature. It is a chain of detection, containment, state handling, recovery, and verification. Isolation boundaries must be evaluated against explicit fault models and their shared dependencies.

**Research status:** Initial analysis and propagation model prepared; real isolation validation and quantitative resilience evaluation remain open.
