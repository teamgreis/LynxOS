# LynxOS

**LynxOS** is a research-driven operating-system project exploring a new computational and kernel model, a purpose-built systems language, and a security architecture designed around explicit authority and controlled state transitions.

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

## Target architecture at a glance

| Area | Direction |
|---|---|
| Kernel | Open research question; minimize and justify privileged trusted code |
| Computation model | Open research question; compare competing formal and operational models |
| Language | Own statically typed systems language |
| Assembly | Small architecture-specific layer |
| Initial CPU | x86-64 |
| Later CPU | ARM64 |
| IPC | Authority-checked message passing and controlled shared memory |
| Storage | Own filesystem design; working name: LynxFS |
| Networking | Native network stack and explicit network authority |
| GUI | Native graphics, compositor, window manager, shell, UI framework |
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

All documents, experiments, prototypes, and future architecture decisions are governed by the [Engineering Quality Charter](docs/foundation/engineering-quality-charter.md). Toy-model success is not proof of implementation security or performance. No architecture proposal is preferred by default.
