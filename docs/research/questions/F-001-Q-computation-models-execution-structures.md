# F-001-Q — Computation Models and Execution Structures

**Status:** Research question; no architecture decision  
**Program:** R0 Computing foundations, with links to R1/R5/R6/R7/R8  
**Question:** Which fundamental models can express computation and concurrency, and how can their semantics and implementation costs be compared?

## 1. Scope

A computation model describes how work is represented, when units become eligible to execute, how they communicate, and what determines observable behavior. An execution structure is a concrete organization that realizes some model. These are related but not identical: one model may have multiple runtimes, schedulers, or hardware mappings.

## 2. Candidate model families

| Model | Readiness / progress rule | Communication and state | Key questions |
|---|---|---|---|
| Sequential control flow | Next instruction / explicit branch | Shared local state | Simplicity, control dependence |
| Processes and threads | Scheduler selects runnable context | Shared memory and synchronization | Isolation, preemption, races |
| Event loop / event-driven | Event arrives and handler is dispatched | Queues, callbacks, state machines | Backpressure, handler duration |
| Actors / active objects | Mailbox message enables isolated turn | Asynchronous messages, private state | Ordering, failure supervision, nondeterminism |
| Dataflow / process networks | Required input tokens become available | Explicit dependency edges / streams | Determinism, buffering, parallelism |
| Synchronous-reactive | Logical clock tick / reaction step | Values aligned to logical instants | Timing assumptions, determinism |
| Discrete-event | Next event in logical-time order | Timestamped event queue | Tie-breaking, causality, simulation cost |
| Coroutines / tasks | Explicit suspension and resumption | Runtime-managed continuation | Cancellation, stack/state representation |
| Transactional execution | Transaction begins, validates, commits/aborts | Read/write sets and atomic effects | Conflict rates, isolation, rollback |

These families overlap. “Thread,” “actor,” “task,” and “dataflow node” are not mutually exclusive categories at every abstraction layer.

## 3. Comparison dimensions

A neutral comparison should record:
- operational and denotational semantics;
- determinism and allowed execution traces;
- state ownership and sharing;
- communication and synchronization;
- preemption, scheduling, and fairness;
- parallelism exposure and synchronization overhead;
- failure and cancellation boundaries;
- resource accounting and backpressure;
- temporal guarantees and real-time behavior;
- distribution, migration, and observability;
- implementation complexity and hardware mapping.

No single model is universally superior. A model that constrains nondeterminism may improve reproducibility but reduce flexibility or require coordination. A permissive model may expose parallelism while making reasoning and testing harder.

## 4. Questions and hypotheses

- **H-Q1:** Models differ fundamentally in what they treat as the event that enables progress.
- **H-Q2:** Determinism is a property of the model plus constraints on interaction, not merely a property of the scheduler.
- **H-Q3:** Ownership and communication rules influence both fault isolation and synchronization cost.
- **H-Q4:** A layered system may need multiple models rather than one universal execution abstraction.
- **H-Q5:** Comparisons become misleading unless semantic guarantees are separated from runtime and hardware implementation.

## 5. Toy experiment

`execution_models.py` evaluates the same dependency graph using three abstract strategies: sequential topological execution, event-queue readiness, and dataflow-style firing when inputs are ready. Each strategy must produce the same final value while exposing a different execution trace.

The experiment is intentionally small and deterministic. It does not benchmark performance, model actual CPU scheduling, or establish that one model is faster.

## 6. Open research questions

1. Is there a useful common semantic representation for comparing all these models without erasing their differences?
2. Which models naturally support preemption, isolation, migration, deterministic replay, and resource limits?
3. How should nested or mixed execution models compose?
4. Can a runtime change execution strategy while preserving observable semantics?
5. Which abstractions should be exposed to programs, and which should remain implementation choices?

## 7. Prior work

- Lee and Sangiovanni-Vincentelli, [A Framework For Comparing Models of Computation](https://ptolemy.berkeley.edu/publications/papers/98/framework/), IEEE TCAD 1998.
- De Koster, Van Cutsem, and De Meuter, [43 years of actors: a taxonomy of actor models and their key properties](https://doi.org/10.1145/3001886.3001890), 2016.
- Lohstroh et al., [Toward a Lingua Franca for Deterministic Concurrent Systems](https://doi.org/10.1145/3448128), 2021.
- [A Survey on Parallelism and Determinism](https://doi.org/10.1145/3564529).

## 8. Decision status

**No decision.** No process model, actor runtime, event loop, dataflow engine, scheduler, or universal execution abstraction is selected.
