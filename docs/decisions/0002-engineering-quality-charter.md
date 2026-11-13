# ADR 0002 — Project-Wide Engineering Quality Charter

- **Status:** Accepted
- **Date:** 2026-11-13
- **Decision owners:** Project maintainers
- **Supersedes:** Any earlier wording that could imply security, correctness, or reliability may be traded away for speed

## Context

LynxOS has an ambitious goal: pursue the strongest practical combination of security, performance, efficiency, and innovation. The existing research portfolio spans computation models, kernel foundations, memory, scheduling, storage, devices, and boot. Without a shared evaluation standard, individual documents can use inconsistent evidence levels, omit threat assumptions, overstate toy-model results, or favor a mechanism before alternatives have been compared.

## Decision

Adopt [Engineering Quality Charter](../foundation/engineering-quality-charter.md) as the binding project-wide research and engineering standard.

1. Correctness and scoped security guarantees are hard constraints.
2. Performance and efficiency are optimized within those constraints and must be measured or modeled transparently.
3. Innovation requires prior-art review, a precise difference, and falsifiable evidence.
4. Research proposals compare at least three credible alternatives where feasible.
5. Experiments document assumptions, negative cases, failure behavior, reproducibility, and limitations.
6. Evidence labels distinguish conceptual, formalized, modeled, tested, measured, reviewed, verified, implemented, and production-validated work.
7. No candidate architecture—including TCC, domains, transitions, capabilities, or budgets—is preferred by default.
8. Architecture decisions require explicit alternatives, evidence, risks, costs, and revisit criteria.

## Consequences

- The charter applies retroactively to all F-001 research documents A–Z and supporting research material.
- Existing small Python models remain exploratory evidence only. Their PASS results are limited to the modeled properties.
- Claims about security, performance, efficiency, and novelty must be scoped and traceable to appropriate evidence.
- Some research items will remain drafts until stronger threat models, comparative evaluations, and reproducible measurements are added.
- A simple established mechanism may be preferred over a novel complex one when it provides better verified properties and lower total cost.

## Revisit criteria

Revisit this ADR if the project changes its top-level quality objectives or if the charter's evidence and review requirements prove materially inadequate. Any change must preserve explicit security, correctness, performance, efficiency, and novelty criteria.
