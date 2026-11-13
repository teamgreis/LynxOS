# F-001-K — Observation, Control and Feedback

**Status:** Research question; open  
**Program:** R0 — Computing foundations  
**Parent:** [F-001 — What is a computer?](F-001-what-is-a-computer.md)  
**Related:** F-001-D resource-aware computation; F-001-F identity and authority; F-001-G state continuity; F-001-H temporal semantics

## Research question

How can a computational system infer relevant properties of its internal state from observations, and how can it influence future state through controlled actions and feedback?

This investigation connects control theory, observability, controllability, runtime monitoring, feedback loops, and safe actuation. It does not select a monitoring architecture, telemetry stack, scheduler, policy engine, or control plane.

## 1. State, observation, action

A simple discrete model is:

`x(t+1) = f(x(t), u(t), w(t))`

`y(t) = h(x(t), v(t))`

where:
- `x` is the internal state;
- `u` is an applied control action;
- `w` represents disturbances or external influences;
- `y` is an observation;
- `v` represents measurement noise or observation error.

This vocabulary separates the true internal state from what a monitor can actually see.

## 2. Observability

A system is observable, relative to a chosen model and observation interface, when its internal state can be uniquely inferred from available observations over the relevant interval.

A system may expose CPU utilization while hiding queue depth, lock contention, pending I/O, or a resource leak. A single metric is not a complete state description.

For software systems, observability may involve logs, metrics, traces, state snapshots, event histories, probes, and explicit diagnostic interfaces. Each reveals only selected projections of system behavior and may impose overhead or expose sensitive information.

## 3. Controllability

Controllability asks whether permitted inputs can move a system from one state to another within the model.

A system may be observable but not controllable: an administrator can see a failed device but cannot repair it through software. Conversely, a system may be controllable through an actuator whose effect is poorly observable.

In operating systems, candidate actuators include scheduling decisions, resource limits, process lifecycle operations, routing, admission control, and configuration changes. Every actuator needs authority checks, bounded effects, and failure semantics.

## 4. Feedback loops

A feedback loop observes system behavior, compares it with a target or policy, and applies an action.

A generic loop contains:
1. plant/system being controlled;
2. sensors or observations;
3. state estimator or monitor;
4. policy/controller;
5. actuators;
6. feedback delay and sampling schedule.

Poorly designed feedback can oscillate, overreact to noise, amplify load, or create instability. A controller that reacts too slowly may miss hazards; one that reacts too aggressively may cause thrashing.

## 5. Monitoring is not automatically control

Monitoring reports or estimates state. Control changes state. Combining them creates a feedback system, which introduces new risks:
- incorrect or stale observations;
- noisy measurements;
- actuator failure;
- feedback delay;
- conflicting controllers;
- oscillation and unstable policy;
- authority escalation or unintended side effects.

A monitoring subsystem should not silently acquire broad authority merely because it can observe a problem.

## 6. Runtime verification and temporal properties

Some properties concern event histories rather than instantaneous state. Runtime verification checks observed execution traces against formal or semi-formal specifications.

Examples:
- a resource must not be released twice;
- a privileged action must be preceded by authorization;
- after a request is accepted, it must eventually complete or report failure;
- a task must not exceed a defined budget without an explicit transition.

Runtime monitors can detect violations in observed traces, but they cannot prove properties about unobserved behavior unless the observation model is complete enough.

## 7. Hypotheses

- **H-K1:** Observability is relative to a chosen state model and measurement interface.
- **H-K2:** Controllability and observability are independent properties; neither implies the other.
- **H-K3:** Feedback controllers need explicit bounds for sampling delay, measurement error, and actuator effects.
- **H-K4:** Monitoring and actuation should have separable authority boundaries.
- **H-K5:** Runtime verification can detect violations in observed traces but cannot infer unobserved events without additional assumptions.
- **H-K6:** Feedback policies can destabilize a system when they ignore delay, noise, coupling, or resource constraints.

## 8. Minimal finite-state experiment

The accompanying model has a four-state system with two binary state variables. A partial sensor observes only the first variable and cannot distinguish states that differ only in the second. A full sensor distinguishes all four. A partial actuator can change only the first variable; two independent actuators can reach all four states from the initial state.

Run:

```sh
python3 experiments/f001/observation_control_model.py
```

This finite example illustrates observability and reachability concepts; it is not a general proof of control-theoretic properties and does not model noise, time delays, or continuous dynamics.

## 9. Prior art

- R. E. Kalman, *Lectures on Controllability and Observability* (1968): [NASA technical report](https://ntrs.nasa.gov/citations/19700032148).
- Gilbert, *Controllability and Observability in Multivariable Control Systems* (1963): [DOI](https://doi.org/10.1137/0301009).
- Caltech, *Feedback Systems*, output-feedback and observer material: [textbook chapter](https://www.cds.caltech.edu/~murray/books/AM08/pdf/fbs-outputfbk_24Jul2020.pdf).
- NASA, *Runtime Verification — 17 Years Later*: [NASA NTRS](https://ntrs.nasa.gov/citations/20210005928).
- Falcone, Havelund and Reger, *A Tutorial on Runtime Verification*: [paper](https://www.havelund.com/Publications/rv-tutorial-ios-2012.pdf).

## 10. Open questions

1. Which internal state must be observable for safe system operation?
2. How can observation overhead be bounded under load?
3. How should a monitor represent uncertainty and stale measurements?
4. Which actions should be available to automated controllers, and under what authority?
5. How can multiple controllers avoid conflicting actions?
6. What stability properties matter for resource and scheduling feedback loops?
7. How should control policies behave during partitions or sensor failure?
8. Which properties can be checked online, and which require offline proof?
9. How can diagnostic data avoid leaking secrets?
10. How should recovery interact with controller state and historical observations?

## 11. Current conclusion

Observation and control are distinct capabilities. A system cannot safely manage what it cannot adequately observe, but the ability to observe does not justify unrestricted authority to act. Any future architecture must state the limits, uncertainty, cost, and authority of both measurement and actuation.

**Research status:** Initial conceptual survey and finite-state experiment prepared; dynamic-system analysis, controller stability, and formal runtime-monitor verification remain open.

## Cross-cutting evaluation contract — Engineering Quality Charter

This research item is governed by the project-wide [Engineering Quality Charter](../../foundation/engineering-quality-charter.md). Evaluate its topic-specific claims across:

- **Security:** assets, attacker capabilities, trust boundaries, enforcement path, least authority, abuse/DoS cases, and residual risks.
- **Correctness and reliability:** explicit invariants, safety/liveness properties, concurrency and TOCTOU hazards, failure points, recovery semantics, and falsifying counterexamples.
- **Performance:** credible baseline under the same workload; latency distributions including tail latency, throughput, and worst-case behavior where meaningful.
- **Efficiency:** CPU, memory, allocations, synchronization, context switches, I/O, data movement, storage amplification, and energy where measurable.
- **Innovation:** closest prior art and a precise, falsifiable difference. A new name or combination is not proof of global novelty.
- **Evidence:** label results as conceptual, formalized, modeled, tested, measured, reviewed, verified, implemented, or production-validated. A toy-model PASS is not proof of a real operating-system guarantee.

Where relevant, compare at least three credible approaches under equivalent assumptions. Record negative results and unmodeled behavior. Until threat analysis, comparative evaluation, and reproducibility requirements are met, this remains an initial research draft and cannot justify an architecture decision.
