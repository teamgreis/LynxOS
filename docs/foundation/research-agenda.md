# LynxOS — Foundational Research Agenda

- **Document:** LYNX-FOUNDATION-001
- **Revision:** 1.0
- **Status:** Foundational agenda; no technical architecture selected
- **Date:** 2026-11-02

## 1. Mission

LynxOS investigates whether computing systems and operating systems can be founded on substantially different abstractions from those commonly used today.

The project is not initially committed to a monolithic kernel, microkernel, unikernel, capability architecture, actor model, transactional model, or any other established design. These are candidates for comparison, not premises.

The long-term ambition is a complete, independently developed computing platform: system architecture, kernel or alternative execution substrate, systems language, compiler and toolchain, runtime, core services, storage, networking, graphics environment, developer tools, and verification infrastructure.

The project pursues both foundational research and practical engineering. Security, performance, reliability, usability, and independence are co-equal goals. They can conflict; trade-offs must be measured and documented rather than hidden behind a single "best" claim.

## 2. Binding project goals versus open design questions

### Binding project goals

- Explore a fundamentally new computing and system-organizing model.
- Pursue security, performance, and reliability as co-equal design goals.
- Develop the platform's essential technologies independently over time.
- Combine formal research with experimental implementations and hardware evaluation.
- Target a complete operating environment, including a native graphical environment.
- Use x86-64 as the initial practical hardware target and investigate ARM64 afterward, subject to validation.
- Do not implement the project in Rust.

### Not yet decided

- Kernel architecture and privilege structure.
- Whether the system has one kernel, multiple kernels, or no conventional kernel.
- The fundamental computation and execution model.
- Process, task, thread, domain, actor, or other execution abstractions.
- Memory and object model.
- Authority, identity, and access-control model.
- Scheduling and concurrency model.
- IPC and networking abstractions.
- Filesystem and persistent-state architecture.
- Systems language syntax, semantics, and type system.
- Compiler architecture and intermediate representation.
- Runtime and service model.
- GUI composition and interaction model.
- Cryptographic protocols and hardware trust assumptions.

No earlier LynxOS proposal is binding merely because it has already been documented. Existing concepts such as Transition-Centric Computing, domains, capabilities, reversible execution, or covenant-based state changes are retained only as historical research candidates until re-evaluated.

## 3. Research principles

1. **Problem before mechanism:** Define the problem and desired property before naming a solution.
2. **Prior art before novelty claims:** Compare with academic papers, standards, implementations, patents, and related fields.
3. **Formal semantics before critical implementation:** Specify state, operations, invariants, and failure behavior.
4. **Small trusted base:** Minimize what must be trusted; justify every privileged mechanism.
5. **Measurement before performance claims:** Measure latency distributions, throughput, memory use, energy, and worst-case behavior.
6. **Threat models before security claims:** Identify adversaries, assets, trust assumptions, and attack surfaces.
7. **Failure as a first-class case:** Specify partial failure, crash recovery, cancellation, corruption, and degraded operation.
8. **Independent review:** Invite external review of major claims and critical designs.
9. **Reproducibility:** Preserve source, configuration, test data, scripts, tool versions, and results.
10. **Negative results matter:** Record rejected approaches and the evidence behind rejection.

## 4. Research programs

### R0 — Computing foundations

Questions:
- What is computation at the abstraction level LynxOS should expose?
- Must execution be instruction-stream based, task-graph based, state-transition based, dataflow based, or something else?
- What are the fundamental entities: values, objects, events, state, transformations, resources, or other constructs?
- Can one model express sequential, parallel, reactive, and distributed computation?

Deliverables:
- Comparative model survey.
- Candidate formal models.
- Small executable interpreters or simulators.
- Complexity and expressiveness comparisons.

### R1 — System and kernel foundations

Questions:
- Which functions require privilege?
- Can privilege be partitioned or eliminated?
- How should hardware events, faults, interrupts, and resource ownership be represented?
- What is the smallest trusted substrate capable of enforcing the required invariants?

Deliverables:
- Threat and trust boundary diagrams.
- Competing architecture prototypes.
- Privilege and isolation cost measurements.
- A justified trusted-computing-base proposal.

### R2 — Security and authority

Questions:
- What does it mean for an operation to be authorized?
- How should authority be represented, attenuated, delegated, expired, and revoked?
- How can authority amplification be prevented?
- How can security decisions be explained and independently checked?

Deliverables:
- Formal authority model candidates.
- Attack trees and threat models.
- Model-checked policy protocols.
- Prototype enforcement mechanisms and adversarial tests.

### R3 — Performance and resource theory

Questions:
- What should the system measure and allocate: CPU time, memory, bandwidth, energy, latency, device access, or interference?
- Can resource guarantees be composed across services?
- How should overload and contention be handled?

Deliverables:
- Workload taxonomy.
- Resource accounting model.
- Scheduler and admission-control experiments.
- Tail-latency, throughput, and energy benchmarks.

### R4 — Memory and persistent state

Questions:
- What is object identity independent of physical location?
- How should memory ownership, sharing, lifetime, and reclamation work?
- Which state transitions must be atomic or recoverable?
- How can data integrity and provenance be represented efficiently?

Deliverables:
- Memory model comparison.
- Object-lifetime semantics.
- Persistent-state and crash-recovery prototypes.
- Memory safety and performance measurements.

### R5 — Time, concurrency, and coordination

Questions:
- What ordering guarantees do applications actually need?
- How should synchronization, cancellation, preemption, and deadlines be represented?
- Can concurrency be made easier to reason about without sacrificing hardware utilization?

Deliverables:
- Formal concurrency models.
- Race and deadlock test suites.
- Scheduling prototypes.
- Measured latency and scalability results.

### R6 — Language and toolchain

Questions:
- Which language properties are needed to express the chosen system model?
- How can memory, authority, effects, concurrency, and resource constraints be represented?
- What should be statically proven, dynamically checked, or left to unsafe code?
- How can compiler correctness and build provenance be validated?

Deliverables:
- Language requirements and semantics.
- Parser and type-system experiments.
- Intermediate representation candidates.
- Compiler prototype and differential tests.
- Assembler, linker, debugger, and build-system research.

### R7 — Hardware and device architecture

Questions:
- What must be abstracted and what must remain directly visible?
- How should interrupts, DMA, IOMMUs, caches, timers, and device reset be handled?
- Which guarantees depend on specific hardware capabilities?

Deliverables:
- x86-64 hardware capability matrix.
- QEMU and real-hardware test plan.
- Device isolation experiments.
- ARM64 portability analysis.

### R8 — Communication and distributed computing

Questions:
- What should communication endpoints represent?
- How should local IPC and remote communication relate?
- How can tasks move between devices without transferring ambient privilege?
- What happens during partitions, stale state, or partial failure?

Deliverables:
- IPC model comparison.
- Distributed identity and authority model.
- Fault-injection experiments.
- Cross-device prototype.

### R9 — Storage, networking, and core services

Questions:
- Which system services need durable state?
- How should storage transactions, networking policy, identity, configuration, and updates compose?
- How can a compromised service be replaced without compromising the whole system?

Deliverables:
- Service contract model.
- Storage and network prototypes.
- Update and rollback architecture.
- Service lifecycle and recovery tests.

### R10 — Graphics and human interaction

Questions:
- What abstractions best support human intent, accessibility, and predictable system control?
- How should the GUI expose security and resource consequences?
- What is the right relationship between desktop, applications, and system services?

Deliverables:
- Interaction research.
- Accessibility requirements.
- Compositor and input experiments.
- Native desktop prototype after foundational APIs stabilize.

### R11 — Reliability, recovery, and verification

Questions:
- What can be proven, tested, monitored, or independently reconstructed?
- How should failures be contained?
- Which components can restart, migrate, roll back, or degrade safely?
- How can updates preserve integrity and recoverability?

Deliverables:
- System invariant catalog.
- Formal models for critical protocols.
- Fault-injection and fuzzing infrastructure.
- Reproducible verification reports.

## 5. Comparative research method

For each important problem, investigate at least three competing approaches where feasible. Include relevant approaches from:

- Monolithic and modular kernels.
- Microkernels and exokernels.
- Capability-based and object-capability systems.
- Distributed systems and actor/dataflow models.
- Transactional systems and databases.
- Real-time and mixed-criticality systems.
- Programming-language type/effect systems.
- Formal verification and proof-carrying code.
- Secure boot, hardware roots of trust, and measured execution.
- Filesystems, persistent memory, and storage engines.

The goal is not to select the newest-sounding approach. Compare guarantees, assumptions, complexity, attack surface, performance, portability, and implementation cost.

## 6. Experimental platform

Initial experiments may use existing development tools and emulators as temporary research infrastructure. This does not commit LynxOS to those tools or components in its final product.

Recommended initial lab:
- QEMU for repeatable x86-64 experiments.
- A documented x86-64 UEFI test target.
- Automated boot and regression tests.
- Model-checking and theorem-proving tools selected per problem.
- Reproducible benchmark harness.
- A separate ARM64 evaluation track after the first models stabilize.

No hardware-specific implementation should be treated as architecture-neutral without evidence.

## 7. Research lifecycle and decision gates

Every research proposal passes through these states:

1. **Question:** A concrete problem is identified.
2. **Survey:** Prior art, standards, and existing implementations are compared.
3. **Model:** Semantics, assumptions, and invariants are written down.
4. **Analysis:** Threats, failure modes, complexity, and alternatives are evaluated.
5. **Prototype:** A narrow experiment is implemented.
6. **Evaluation:** Measurements and adversarial tests are run.
7. **Review:** Independent review challenges the claims.
8. **Decision:** Adopt, revise, defer, or reject with reasons.

A proposal does not become a binding architecture decision until the relevant gate is passed and an Architecture Decision Record is approved.

## 8. First 90-day research sequence

### Weeks 1–2: Baseline and research infrastructure
- Establish repository structure for questions, surveys, models, experiments, and decisions.
- Define a common research dossier template.
- Create reproducible build, test, and measurement conventions.
- Inventory existing LynxOS documentation and mark all prior architecture concepts as unvalidated historical proposals.

### Weeks 3–4: Fundamental model comparison
- Compare candidate computation models.
- Compare kernel and privilege structures.
- Identify common assumptions shared by mainstream designs.
- Select a small set of falsifiable research questions.

### Weeks 5–6: Formal foundations
- Specify one narrow model for state, operation, authority, and failure.
- Define invariants and counterexamples.
- Use model checking or theorem proving where appropriate.
- Reject models that cannot express useful workloads or whose guarantees are vacuous.

### Weeks 7–8: Minimal experimental prototypes
- Implement small simulators or emulated prototypes.
- Compare against a conventional baseline.
- Measure overhead, complexity, and failure behavior.
- Avoid prematurely implementing a full kernel.

### Weeks 9–10: Security and reliability evaluation
- Threat-model the leading candidates.
- Run adversarial and fault-injection tests.
- Evaluate recovery and revocation behavior.
- Document unresolved risks.

### Weeks 11–12: Architecture review
- Publish results and limitations.
- Obtain external review where possible.
- Select only the decisions supported by evidence.
- Publish an ADR for each adopted foundational choice.

The 90-day plan is a research sequence, not a promise that a complete OS will exist in that period.

## 9. Required research dossier

Every concept must document:

- Identifier and name.
- Problem statement.
- Motivation and target workloads.
- Prior-art survey and references.
- Formal semantics.
- Threat model and trust assumptions.
- Safety, security, and liveness properties.
- Failure and recovery behavior.
- Complexity and performance hypotheses.
- Alternatives and trade-offs.
- Prototype implementation.
- Reproducible evaluation.
- Review feedback.
- Decision and maturity status.

## 10. Maturity labels

| Status | Meaning |
|---|---|
| Question | Open research question |
| Proposed | Initial hypothesis |
| Surveyed | Prior art and alternatives reviewed |
| Specified | Semantics documented |
| Modeled | Formal or executable model exists |
| Prototyped | Experimental implementation exists |
| Evaluated | Reproducible tests and measurements completed |
| Reviewed | External or independent review completed |
| Adopted | Approved as an architecture decision |
| Rejected | Evidence supports rejection |
| Superseded | Replaced by a better-supported approach |

## 11. Claims policy

LynxOS must distinguish:
- Novel to this project from novel to the world.
- Proposed behavior from implemented behavior.
- Intended properties from proven properties.
- Formal proof from testing and empirical evidence.
- Emulator results from real-hardware results.
- Security design goals from independently validated security.

No "world first", "unbreakable", "fastest", or "safest" claim is permitted without evidence that directly supports it.

## 12. Immediate first milestone

**Milestone F0: A neutral, evidence-based map of the design space.**

Exit criteria:
- All major architectural assumptions are listed.
- Each assumption is marked as a requirement, hypothesis, or open question.
- At least three competing approaches are compared for each foundational problem.
- A prioritized set of falsifiable research questions is published.
- No kernel or language architecture is selected prematurely.

The first success is not a boot screen. It is a research foundation strong enough to justify what should be built next.


## 13. Project-wide Engineering Quality Charter

The [Engineering Quality Charter](engineering-quality-charter.md) is binding for all research programs and artifacts. It makes security, performance, efficiency, and evidence-based innovation explicit review dimensions. Correctness and scoped security guarantees are hard constraints; performance and resource/energy efficiency are optimized within them. Every proposal must include a threat model, alternatives, invariants, failure behavior, measurable costs, prior-art comparison, falsification criteria, and an evidence/maturity label. This charter supersedes any earlier wording that could be read as allowing security or correctness to be traded away for speed.

## 14. Research status clarification

The A–Z F-001 documents are an evolving research map, not a complete systematic review. Their small Python models are exploratory and do not establish kernel-level guarantees, real-hardware performance, or global novelty. Items remain drafts until their missing evidence is supplied under the charter.
