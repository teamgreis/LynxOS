# Research Note — Transition-Centric Computing

- **Document:** LYNX-RESEARCH-001
- **Status:** Initial hypothesis; not a formal model
- **Version:** 0.1

## 1. Research question

Can a general-purpose operating system be structured around explicit, verifiable state transitions between isolated domains, where authority and resource constraints are part of the transition contract?

The goal is not to route every CPU instruction through the kernel. The goal is to make security-sensitive changes of state explicit and enforceable while keeping ordinary execution efficient.

## 2. Candidate conceptual objects

| Object | Working meaning |
|---|---|
| Domain | Isolation, identity, and resource-accounting boundary |
| Execution Unit | Schedulable computation running within a domain |
| State Object | State that may be observed or changed under defined rules |
| Transition | Operation that attempts a controlled state change |
| Authority | Explicit permission to request or perform an operation |
| Resource Budget | Enforceable allowance for resource consumption |
| Event | A notification or recorded occurrence |
| Invariant | A property that must remain true across valid system behavior |

These definitions are provisional and must be made mathematically precise.

## 3. Candidate transition contract

A transition request can be represented abstractly as:

`T = (D, S, Op, I, A, B, P, Q, E)`

Where:

- `D`: requesting domain.
- `S`: target state object or set of objects.
- `Op`: requested operation.
- `I`: input.
- `A`: required authority.
- `B`: resource budget.
- `P`: preconditions.
- `Q`: postconditions.
- `E`: permitted effects.

A transition is admissible only if identity, authority, preconditions, and resource constraints are valid. The exact semantics of validation, execution, atomicity, and failure are open questions.

## 4. Candidate admission flow

1. A domain submits a transition request through a defined interface.
2. The system resolves the caller and target identities.
3. Required authority is checked.
4. Preconditions and object versions are checked.
5. Resource budget is reserved or validated.
6. The operation is admitted or rejected.
7. If admitted, execution occurs under defined isolation rules.
8. The result, effects, and failure state are made observable according to policy.

This is a conceptual flow, not yet a prescribed syscall ABI or implementation algorithm.

## 5. Example: requesting network access

A domain requests permission to create a network endpoint.

The request should identify the operation and relevant constraints, such as protocol, address family, destination scope, and resource budget. The system checks whether the domain holds the required authority and whether policy permits the requested operation.

Important unresolved details:

- Is authority granted per socket, protocol, destination, or service?
- Can authority be delegated?
- What happens to existing sockets after revocation?
- How are DNS resolution and subsequent connections represented?
- Which component enforces network policy?
- How is resource exhaustion contained?

The example illustrates the model; it is not a finalized API.

## 6. Concurrency and consistency questions

The formal model must define:

- Whether state objects are mutable, immutable, versioned, or transactional.
- How concurrent transitions against the same state are serialized or coordinated.
- Whether transitions are atomic, partially observable, or compensatable.
- How stale references and time-of-check/time-of-use races are prevented.
- How cancellation interacts with in-flight transitions.
- How deadlocks and priority inversion are handled.
- Whether deterministic execution is a goal for selected domains.

A transition contract is not sufficient by itself to prevent races. The model needs precise consistency and synchronization semantics.

## 7. Authority questions

The authority model must specify:

- Authority representation and unforgeability.
- Scope and attenuation.
- Delegation rules.
- Revocation semantics.
- Lifetime and inheritance.
- Cross-domain transfer.
- Auditability.
- Behavior when an authority holder is compromised.

Revocation is especially difficult when a resource is already in use. The design must distinguish preventing new operations from terminating or safely draining existing operations.

## 8. Resource accounting questions

Budgets may cover CPU time, memory, storage, handles, network bandwidth, and device access.

The model must define:

- Reservation versus consumption accounting.
- Hierarchical budgets.
- Budget transfer and delegation.
- Exhaustion behavior.
- Priority and fairness.
- Accounting overhead and resistance to abuse.

## 9. Failure model

The design must distinguish at least:

- Rejected transition.
- Invalid input.
- Authority failure.
- Resource exhaustion.
- Domain crash.
- Service crash.
- Hardware fault.
- Partial operation.
- System-wide invariant violation.

For every category, specify observable results, cleanup, recovery, and whether state can be trusted afterward.

## 10. Related-work comparison required

Before claiming novelty, compare the model against:

- Microkernel architectures and message-passing kernels.
- Capability-based security and object-capability systems.
- Actor models and isolated processes.
- Transactional memory and database transaction models.
- State machines and workflow systems.
- Reference monitors and mandatory access control.
- Formally verified kernels and separation-logic-based reasoning.
- Resource containers, quotas, and real-time scheduling.

The research contribution, if any, must be stated as a precise difference in semantics, guarantees, composition, or measurable behavior—not merely a new name for known mechanisms.

## 11. Proof obligations and prototype criteria

Candidate properties to formalize and test:

1. No domain can exercise authority it does not possess.
2. A domain cannot modify protected state outside permitted transitions.
3. Resource consumption cannot exceed enforceable budgets beyond explicitly documented bounded overshoot.
4. A failed transition cannot silently leave state violating declared invariants.
5. Revocation prevents future use within a defined and testable bound.
6. A compromised unprivileged service cannot directly compromise unrelated domains.
7. Kernel scheduling decisions do not grant resource authority.

Prototype evaluation should measure:

- Transition admission latency.
- IPC throughput and latency.
- Context-switch overhead.
- Memory overhead per domain.
- Resource-accounting cost.
- Revocation latency.
- Fault-containment behavior.
- Performance against suitable baseline systems.

## 12. Open decisions

No final decisions have yet been made for:

- Formal state and transition semantics.
- Atomicity and rollback model.
- Domain hierarchy.
- Authority representation.
- Revocation guarantees.
- Concurrency and memory consistency model.
- Scheduler architecture.
- Kernel/userland boundary.
- IPC ABI.
- Formal verification strategy.

These topics should become individual design documents and ADRs as research progresses.


## 13. Status under the Engineering Quality Charter

This note is a historical candidate model, not an approved LynxOS architecture. TCC must be compared against at least three credible alternatives under identical workloads and threat assumptions. Its evaluation must include enforceable authority boundaries, TOCTOU and concurrency semantics, failure/cancellation behavior, trusted computing base size, transition and IPC latency distributions, CPU/memory overhead, data movement, energy where measurable, and adversarial resource-exhaustion cases. A model-level invariant is not an implementation guarantee until the enforcement path is specified and validated. See [Engineering Quality Charter](../foundation/engineering-quality-charter.md).
