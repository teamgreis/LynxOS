# LynxOS

**LynxOS** is a research-driven operating-system project investigating a new computational and kernel model, a purpose-built systems language, and a high-assurance system architecture. No specific kernel, execution, memory, or authority model is selected.

> **Project status:** Architecture research / pre-implementation. The ideas in this repository are hypotheses and design targets, not claims of proven novelty, correctness, or security.

## Project principles

- A genuinely new kernel model, to be researched and formally specified before implementation.
- A purpose-built systems programming language and assembly layer.
- x86-64 as the first target; ARM64 planned afterward.
- Security architecture designed as a first-class property of the system.
- A complete operating system, including its own graphical environment.
- Maximum long-term independence, including compiler, runtime, core services, and tooling.
- No Rust implementation.

## Current research posture

No computational or kernel architecture is selected. Transition-Centric Computing (TCC), domains, state objects, transitions, authorities, and resource budgets are retained as research candidates only; they are not the assumed direction or preferred answer. Every candidate must compete against established and alternative models under the project-wide Engineering Quality Charter.

LynxOS pursues security, performance, efficiency, and innovation together. Correctness and scoped security guarantees are constraints, not variables to trade away for benchmark gains. Performance and resource/energy efficiency must be measured against baselines, while innovation requires prior-art comparison and falsifiable evidence.

## Documentation

- [Foundational research agenda — clean-slate restart](docs/foundation/research-agenda.md)
- [Engineering Quality Charter — security, performance, efficiency, and innovation](docs/foundation/engineering-quality-charter.md)

- [Technical foundation](docs/architecture/technical-foundation.md)
- [Research model and open questions](docs/research/model.md)
- [Expanded research concept atlas](docs/research/concept-atlas.md)
- [Invention and novelty validation process](docs/research/novelty-validation.md)
- [Frontier architecture proposals](docs/research/frontier-architecture.md)
- [Roadmap](docs/roadmap.md)
- [ADR 0001 — Initial project constraints](docs/decisions/0001-initial-project-constraints.md)
- [ADR 0002 — Engineering Quality Charter](docs/decisions/0002-engineering-quality-charter.md)
- [F-001 experiment suite and runner](experiments/f001/README.md)

## Long-term platform scope (not architecture decisions)

| Area | Research direction |
|---|---|
| Kernel | Open research question; minimize and justify privileged trusted code |
| Computation model | Open research question; compare competing formal and operational models |
| Language | Develop an independently specified systems language and toolchain |
| Assembly | Small architecture-specific layer |
| Initial CPU | Evaluate x86-64 as the first implementation target |
| Later CPU | Evaluate ARM64 portability after the initial model stabilizes |
| IPC | Compare message passing, shared memory, event, and hybrid models |
| Storage | Research native persistence and filesystem design; LynxFS is a working name |
| Networking | Research native networking with explicit, enforceable access policy |
| GUI | Long-term native graphical environment |
| Security | Threat-modelled, enforceable guarantees; least authority and measurable containment |

## Development philosophy

1. Specify before implementing.
2. Make invariants explicit and testable.
3. Keep the trusted computing base small.
4. Treat failure containment and recovery as architectural requirements.
5. Use existing tools only as temporary bootstrap or research dependencies unless explicitly accepted as permanent.
6. Validate security claims through threat modelling, testing, review, and formal methods where practical.

## Naming note

“LynxOS” is currently the repository/project working name. No trademark, company-name, or domain-name clearance is implied. Complete a naming review before public product or commercial use.

## Status

The repository currently contains planning and research documentation. No production-ready kernel, compiler, runtime, drivers, or desktop environment is claimed to exist.


## Project-wide quality rule

All documents, experiments, prototypes, and future architecture decisions are governed by the [Engineering Quality Charter](docs/foundation/engineering-quality-charter.md). Toy-model success is not proof of implementation security or performance. No architecture proposal is preferred by default. The checked-in F-001 experiment scripts have a common runner and a least-privilege CI workflow; green CI means only that the scripts and their assertions complete successfully.

## Interactive TCC research lab

A standalone browser-based model for exploring domains, capabilities, lifecycle transitions, snapshots, bounded event queues, toy scheduling, deterministic adversarial tests, invariant checks, and JSON session export is available at [`experiments/tcc-lab/index.html`](experiments/tcc-lab/index.html). Open the file locally in a modern browser. It has no external dependencies and is explicitly a research simulation, not a kernel or a security proof.
