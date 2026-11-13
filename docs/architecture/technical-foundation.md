# LynxOS — Technical Foundation Specification

- **Document:** LYNX-FOUNDATION-001
- **Version:** 1.0
- **Status:** Historical research baseline; superseded by the project-wide Engineering Quality Charter
- **Date:** 2026-11-02

## 1. Purpose

This document records the initial technical direction for LynxOS. It is a baseline for research and design decisions, not a final implementation specification.

The project aims to create an operating system with a new kernel model, its own systems language and assembly layer, an independently designed security architecture, and a native graphical environment.

## 2. Binding project constraints

The following decisions were selected for the project:

- Kernel: a fully new model, still to be researched.
- Languages: a purpose-built language plus assembly.
- Initial architecture: x86-64.
- Subsequent architecture: ARM64.
- Security: research-oriented, independently designed security architecture.
- Scope: complete operating system, including native GUI.
- Independence: maximum practical independence, including compiler and runtime.
- Rust: not an implementation language for this project.

These are project constraints. They do not pre-judge the outcome of technical research.

## 3. Historical candidate: Transition-Centric Computing

**Transition-Centric Computing (TCC) is not the current selected direction.** It is one historical candidate among multiple competing computational and kernel models. It must not be assumed by subsequent research or implementation.

The original proposal explored five primary concepts:

1. **Domains** — isolation, ownership, identity, and resource-accounting boundaries.
2. **States** — explicit state objects representing system or application state.
3. **Transitions** — controlled operations that change state.
4. **Authorities** — explicit, scoped permissions to request or perform operations.
5. **Resource budgets** — limits for memory, CPU time, handles, bandwidth, and other resources.

A transition may declare:

- Preconditions.
- Required authority/capabilities.
- Resource budget.
- Input and referenced state.
- Permitted effects.
- Postconditions.
- Failure and recovery behavior.

The kernel validates security-sensitive transitions. Ordinary execution within an already-authorized context must not require a kernel transition for every instruction.

### 3.1 Critical research caveat

The individual concepts have precedents in operating systems, capability security, transactional systems, actor models, state machines, and formal methods. TCC must be compared against these fields. The project must not claim that the model is unprecedented or more secure until a precise definition and comparative evaluation support that conclusion.

## 4. Kernel and trusted computing base

The kernel should remain the smallest practical privileged component. Candidate responsibilities include:

- CPU and privilege-mode initialization.
- Address-space and memory protection primitives.
- Scheduling and execution isolation.
- Domain lifecycle and identity.
- Authority validation and controlled delegation/revocation.
- Interrupt and exception handling.
- Secure transition admission.
- Minimal hardware mediation.
- Resource accounting and enforcement.

Complex services should run outside the privileged kernel where practical. The exact boundary remains an open research decision.

## 5. Execution and scheduling

A **Domain** is the proposed isolation and resource-management unit. Execution units run within domains and operate on state objects.

Scheduling research must consider:

- Priority and fairness.
- CPU budgets and accounting.
- Dependencies and blocking.
- Deadlines and latency.
- Isolation and denial-of-service resistance.
- Responsiveness for interactive workloads.
- Multiprocessor behavior.

The scheduler must not implicitly grant authority. Scheduling eligibility and permission to access a resource are separate questions.

## 6. Memory model

The design must cover:

- Physical memory management.
- Virtual address spaces and page tables.
- Kernel memory protection.
- Domain isolation.
- Controlled shared-memory regions.
- Explicit mapping and permission changes.
- Page faults and fault containment.
- Memory accounting, limits, and reclamation.
- DMA and IOMMU threat models.
- Safe memory ownership and lifetime rules in the systems language.

The language and kernel model must agree on ownership, aliasing, concurrency, and revocation semantics.

## 7. IPC and communication

The initial direction is authority-checked message passing, with controlled shared memory where required.

Communication primitives may include:

- Requests and responses.
- Events and notifications.
- Resource or handle transfer.
- Explicitly authorized shared-memory exchange.

The specification must define endpoint identity, message ownership, ordering, cancellation, backpressure, denial behavior, and failure semantics.

## 8. Security architecture

Security goals:

- Default deny.
- Least authority.
- Strong address-space and domain isolation.
- Explicit privilege delegation.
- Revocable permissions where technically feasible.
- Controlled memory sharing.
- Fault containment.
- Secure boot chain.
- Authenticated and rollback-aware updates.
- Protected system state.
- Auditable authority changes.
- Defined behavior under resource exhaustion and partial failure.

Security work must begin with a threat model. It must identify attackers, assets, trust boundaries, hardware assumptions, physical-access assumptions, compromised components, and residual risks.

No architecture can guarantee absolute security. Claims must be scoped and evidence-based.

## 9. Purpose-built systems language and compiler

The language is intended to support:

- Static typing.
- Explicit memory and lifetime semantics.
- Resource-aware programming.
- Authority-aware types or equivalent compile-time mechanisms.
- Controlled concurrency.
- Low-level hardware access through explicit unsafe/privileged boundaries.
- Compile-time validation where possible.
- Defined failure behavior.
- Predictable low-level code generation.

### 9.1 Compiler pipeline

The planned compiler research pipeline includes:

1. Lexer.
2. Parser.
3. Type checker.
4. Semantic analysis.
5. Authority analysis.
6. Intermediate representation.
7. Optimization.
8. x86-64 code generation.
9. Linker and object-format support.
10. Build, diagnostics, and debugging infrastructure.

A temporary host toolchain may be used to bootstrap the compiler. This is a development-stage dependency, not a commitment to a permanent external compiler or runtime. Self-hosting is a long-term goal, not an initial assumption.

### 9.2 Assembly boundary

Assembly should be limited to architecture-specific operations such as:

- Boot and CPU initialization.
- Interrupt and exception entry/exit.
- Context switching.
- Privileged instruction sequences.
- Low-level memory and atomic operations.

The amount of assembly should remain small, reviewable, and documented.

## 10. Platform strategy

### 10.1 x86-64 first

Initial platform work includes:

- UEFI boot.
- Long mode and CPU feature discovery.
- Physical memory map.
- Paging and address-space setup.
- GDT/IDT and exception handling.
- APIC and timers.
- SMP initialization.
- Virtualization-based development and testing with QEMU.

Hardware support should be added incrementally with explicit platform assumptions.

### 10.2 ARM64 later

ARM64 support follows after the core model and x86-64 implementation have stabilized.

Research topics include exception levels, translation tables, interrupt controller, generic timers, SMP, boot protocol, and platform-specific firmware interfaces.

## 11. Storage

The working name for the planned native filesystem is **LynxFS**.

Requirements to investigate:

- On-disk format and versioning.
- Metadata integrity.
- Crash consistency and recovery.
- Transaction semantics.
- Access control and authority integration.
- Data integrity checks.
- Storage-device abstraction.
- Encryption and key management.
- Snapshots and backup semantics.

The design must explicitly define behavior after power loss and partial writes.

## 12. Networking

The long-term native networking scope includes:

- Ethernet.
- IPv4 and IPv6.
- ARP and Neighbor Discovery.
- UDP and TCP.
- DNS.
- TLS integration.
- Firewall and network policy.
- Explicit authority for network access.
- Driver and device isolation.

Protocol implementation and cryptographic design require independent review and conformance testing.

## 13. Userland and runtime

The system must eventually provide native services for:

- Application lifecycle.
- Storage.
- Networking.
- Device access.
- Identity and authorization.
- Configuration.
- Logging and diagnostics.
- Package installation, verification, and updates.

The runtime should be designed alongside the language and kernel interfaces, not bolted on afterward.

## 14. Native graphical environment

The GUI scope includes:

- Display and graphics abstraction.
- Graphics driver interface.
- Compositor.
- Window manager.
- Input subsystem.
- Desktop shell.
- Native UI framework.
- Accessibility interfaces.
- Application lifecycle integration.

The GUI must preserve domain isolation and avoid turning the compositor into an unnecessarily large privileged component.

## 15. Tooling and quality

Existing tools may be used for research and bootstrapping. Permanent dependencies require explicit architectural approval.

Quality requirements:

- Written specifications and invariants.
- Unit and integration tests.
- Failure-injection tests.
- Fuzzing of parsers, protocols, and IPC boundaries.
- Static analysis.
- Reproducible builds.
- Security review.
- Formal verification for selected critical components where feasible.
- Independent validation before strong security claims.

## 16. Initial development sequence

1. Research and related-work review.
2. Formal computational model.
3. Threat model and security invariants.
4. Bootable x86-64 research prototype.
5. Minimal privileged core.
6. Memory and isolation primitives.
7. Domains and transition admission.
8. Authority and resource accounting.
9. Scheduling and IPC.
10. Language and compiler bootstrap.
11. Runtime and core services.
12. Drivers and storage.
13. Networking.
14. Userland and package management.
15. Graphics and desktop.
16. ARM64 port.
17. Independent security and correctness evaluation.

## 17. Decision governance

Major architectural decisions must be recorded as Architecture Decision Records (ADRs), including:

- Context and problem.
- Considered alternatives.
- Decision.
- Consequences and trade-offs.
- Security implications.
- Revisit criteria.

Unresolved questions must remain visibly unresolved rather than being silently converted into assumptions.


## 18. Superseding quality and architecture policy

This document records an early research baseline and must be read together with the [Engineering Quality Charter](../foundation/engineering-quality-charter.md). Where this document sounds prescriptive about TCC, domains, transitions, or other mechanisms, those statements describe candidates, not approved architecture. No candidate is preferred until alternatives are compared under the same workload and threat model.

Security and correctness guarantees are hard constraints. Performance and efficiency are optimized within those constraints and reported using reproducible measurements, including tail latency, throughput, CPU, memory, I/O, data movement, and energy where measurable. Novelty requires a defensible prior-art review and a falsifiable difference. All implementation phases require explicit threat models, invariants, failure injection, independent review proportionate to risk, and documented residual risks.
