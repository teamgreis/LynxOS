# LynxOS Development Roadmap

**Status:** Proposed sequence. Milestones are research and engineering gates, not delivery-date promises.

## Phase 0 — Research foundation

- [ ] Define project terminology and scope.
- [ ] Review related work: microkernels, capability systems, actor models, transactions, formal methods.
- [ ] Define threat model and security objectives.
- [ ] Formalize domains, state objects, transitions, authorities, and resource budgets.
- [ ] Identify invariants and proof obligations.
- [ ] Record major decisions as ADRs.

**Exit gate:** A reviewable formal model, threat model, and explicit list of unresolved risks.

## Phase 1 — Boot and platform research

- [ ] Select initial x86-64 development environment.
- [ ] Establish reproducible build and test workflow.
- [ ] Boot through UEFI in QEMU.
- [ ] Discover CPU features and memory map.
- [ ] Establish serial diagnostics and exception reporting.
- [ ] Document architecture-specific assembly.

**Exit gate:** Reproducible bootable research image with reliable diagnostics.

## Phase 2 — Minimal privileged core

- [ ] Define privilege boundaries.
- [ ] Implement initial memory management.
- [ ] Establish protected address spaces.
- [ ] Implement exception and interrupt handling.
- [ ] Add basic CPU and timer support.
- [ ] Define kernel invariants and test harnesses.

**Exit gate:** Small, testable privileged core with documented trust boundary.

## Phase 3 — Core computational model

- [ ] Implement domain lifecycle.
- [ ] Define state-object representation.
- [ ] Implement transition request and admission prototype.
- [ ] Add authority representation and validation.
- [ ] Add resource accounting.
- [ ] Define failure and recovery semantics.
- [ ] Test concurrency and isolation.

**Exit gate:** Prototype demonstrates the model's essential guarantees and exposes measurable costs.

## Phase 4 — Scheduling and communication

- [ ] Define execution-unit lifecycle.
- [ ] Implement scheduler prototype.
- [ ] Define IPC semantics.
- [ ] Implement message passing.
- [ ] Add controlled shared memory.
- [ ] Test cancellation, backpressure, starvation, and fault containment.

**Exit gate:** Multiple isolated domains communicate under explicit authority and resource constraints.

## Phase 5 — Language and compiler

- [ ] Specify language grammar and type system.
- [ ] Specify memory, lifetime, and concurrency semantics.
- [ ] Design authority-aware programming constructs.
- [ ] Build lexer, parser, and semantic analysis.
- [ ] Define intermediate representation.
- [ ] Implement x86-64 code generation.
- [ ] Build linker and diagnostics.
- [ ] Add compiler tests and reproducible builds.
- [ ] Plan self-hosting bootstrap.

**Exit gate:** A small kernel/userland program can be compiled with the new toolchain and validated against language semantics.

## Phase 6 — Runtime and core services

- [ ] Define system service interfaces.
- [ ] Implement service lifecycle.
- [ ] Add identity and configuration.
- [ ] Add logging and diagnostics.
- [ ] Define package format and signed update model.

**Exit gate:** Basic applications can run as isolated domains using documented system interfaces.

## Phase 7 — Storage and devices

- [ ] Define LynxFS on-disk format.
- [ ] Implement storage abstraction.
- [ ] Test crash consistency and recovery.
- [ ] Define driver isolation and device authority.
- [ ] Add initial virtual devices and selected hardware drivers.

**Exit gate:** Persistent storage and device access operate with explicit failure and access-control semantics.

## Phase 8 — Networking

- [ ] Define network authority model.
- [ ] Implement Ethernet and address configuration.
- [ ] Implement IPv4/IPv6 and neighbor discovery.
- [ ] Implement UDP and TCP.
- [ ] Add DNS and TLS integration.
- [ ] Add firewall policy and protocol conformance tests.

**Exit gate:** Isolated applications can use network services under explicit policy.

## Phase 9 — Native graphical environment

- [ ] Define graphics and display interfaces.
- [ ] Implement input abstraction.
- [ ] Implement compositor and window management.
- [ ] Build desktop shell.
- [ ] Define native UI framework.
- [ ] Add accessibility and application lifecycle integration.

**Exit gate:** Native graphical applications run without weakening domain isolation.

## Phase 10 — ARM64

- [ ] Define ARM64 platform abstraction.
- [ ] Implement exception-level setup.
- [ ] Implement translation tables and memory protection.
- [ ] Add interrupt controller and timers.
- [ ] Add SMP support and boot flow.
- [ ] Run shared architecture-independent tests.

**Exit gate:** The core model and selected userland operate on ARM64 with documented platform differences.

## Phase 11 — Validation and hardening

- [ ] Expand fuzzing and failure injection.
- [ ] Review compiler and kernel attack surfaces.
- [ ] Verify critical invariants with formal methods where feasible.
- [ ] Conduct independent security review.
- [ ] Publish limitations and residual-risk documentation.
- [ ] Benchmark against appropriate reference systems.

**Exit gate:** Claims about security, correctness, and performance are backed by reproducible evidence.
