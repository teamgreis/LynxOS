# ADR 0001 — Initial Project Constraints

- **Status:** Accepted as project direction
- **Date:** 2026-11-02
- **Decision owners:** Project maintainers

## Context

LynxOS is intended to be a new operating-system research and engineering project. The project requires a clear initial scope so that later architecture and implementation work can be evaluated consistently.

## Decisions

1. Research a fully new kernel model rather than adopting an existing kernel design as the final architecture.
2. Develop a purpose-built systems language and an assembly layer.
3. Target x86-64 first.
4. Plan ARM64 as a subsequent architecture.
5. Design an independent, research-oriented security architecture.
6. Aim for a complete operating system, including a native GUI.
7. Pursue maximum practical independence, including compiler and runtime.
8. Do not use Rust as an implementation language.

## Consequences

- A formal model and related-work review are prerequisites to claiming architectural novelty.
- A compiler bootstrap may temporarily use host tooling, but the long-term compiler and runtime are project-owned.
- Architecture-specific assembly is expected, but should remain small and auditable.
- The initial scope is ambitious; milestones must be gated by demonstrable results.
- Security claims require threat models, tests, review, and evidence.
- The project must clearly label research hypotheses, accepted decisions, and implemented behavior separately.

## Revisit criteria

Revisit this ADR only if new research demonstrates that a constraint is infeasible, materially harmful, or inconsistent with the project's security and independence goals. Any change must be documented with rationale and impact.
