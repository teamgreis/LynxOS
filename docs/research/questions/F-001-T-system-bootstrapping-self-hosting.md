# F-001-T — System Bootstrapping and Self-Hosting

**Status:** Initial research draft  
**Program:** R6 — Language/toolchain; R1 — System/kernel foundations  
**Decision status:** No architecture decision

## 1. Research question

How can a system be built from a minimal trusted starting point, progressively replace external dependencies, and eventually build or verify its own essential components?

Bootstrapping is a dependency problem and a trust problem. A compiler written in its own language still requires an earlier implementation or seed. A self-hosted system may reduce long-term dependencies, but it does not automatically eliminate trust in firmware, hardware, seed binaries, build tools, or source inputs.

## 2. Concepts

- **Stage 0 / seed:** Minimal compiler, assembler, interpreter, VM, or trusted binary capable of producing the next stage.
- **Cross-compilation:** Build on a host for a different target.
- **Self-hosting:** A toolchain compiles its own implementation.
- **Reproducible build:** Independent builds from equivalent inputs produce identical outputs under a defined environment.
- **Diverse double-compiling:** Use an independently implemented compiler path to reduce trust in a potentially compromised compiler.
- **Trust chain:** Explicit record of source, tools, binaries, signatures, provenance, and verification.
- **System self-sufficiency:** Ability to rebuild selected components without relying on an external runtime or compiler.

GCC documents a three-stage bootstrap as a way to test its compiler by having the generated compiler rebuild the compiler system. [GCC build documentation](https://gcc.gnu.org/install/build.html) Ken Thompson's “Reflections on Trusting Trust” remains essential background on why source review alone cannot establish compiler-binary trust.

## 3. Competing bootstrap strategies

| Strategy | Seed | Strength | Main limitation |
|---|---|---|---|
| Existing external toolchain | Host compiler/toolchain | Fastest practical start | External dependency and trust |
| Tiny independently auditable seed | Small compiler/assembler/VM | Small trust base | Limited initial language/features |
| Staged language bootstrap | Multiple progressively richer stages | Clear dependency chain | Stage complexity and audit burden |
| Portable bytecode/IR seed | VM or target-neutral intermediate form | Cross-platform leverage | VM/IR implementation becomes critical |
| Diverse double-compilation | Independent compiler implementations | Helps detect compiler compromise | Independence is difficult to establish |
| Reproducible fixed-point builds | Rebuild until outputs converge | Detects nondeterminism/divergence | Byte equality is not proof of semantic correctness |

Examples include GCC's staged bootstrap and projects such as Onramp, which describes a small staged toolchain intended to bootstrap itself. [Onramp](https://github.com/ludocode/onramp/)

## 4. Trust and dependency questions

A credible plan must identify:
1. The smallest seed needed to begin.
2. How the seed is built, obtained, audited, and verified.
3. Which components depend on firmware or external tools.
4. How source inputs and dependencies are pinned.
5. Whether builds are deterministic and under what environmental assumptions.
6. How independent rebuilders compare results.
7. What remains outside the self-hosted trust boundary.
8. How recovery works if the canonical build chain is lost.

A byte-identical rebuild is useful evidence of reproducibility, but it does not prove that the source is benign, that the compiler is correct, or that two builds are independent.

## 5. Hypotheses and falsifiable questions

- **H-T1:** A small seed with a documented interface can reduce the trusted bootstrap base, but may increase development and audit cost.
- **H-T2:** Multi-stage rebuild comparison detects some compiler inconsistencies but not all malicious or systematic errors.
- **H-T3:** Reproducible builds improve independent verification only when inputs and build environments are sufficiently controlled.
- **H-T4:** Cross-compilation can enable early target support before the target can execute its own toolchain, while introducing host/target boundary risks.

Experiments should inject controlled nondeterminism, alter seed behavior, vary build inputs, and compare outputs across independent environments.

## 6. Minimal experiment

The accompanying model represents a three-stage compiler chain. It checks whether successive stages produce identical artifacts and demonstrates that a changed seed can propagate a changed output. It does not implement a compiler or prove trustworthiness.

## 7. Prior work and references

- Ken Thompson, [Reflections on Trusting Trust](https://www.ece.cmu.edu/~ganger/711.fall02/papers/Thompson82.pdf), 1984.
- [GCC — Building](https://gcc.gnu.org/install/build.html), including three-stage bootstrap.
- [Onramp — portable self-bootstrapping C compiler](https://github.com/ludocode/onramp/).
- [NixOS — Reproducible builds](https://reproducible.nixos.org/).
- [Reproducible Builds project](https://reproducible-builds.org/docs/).

## 8. What this does not decide

No implementation language, compiler seed, assembler, linker, bootloader, build system, or self-hosting milestone is selected. The project prohibition on Rust remains in force; it is not relaxed by this research.

## 9. Experiment

- [Bootstrap chain model](../../../experiments/f001/bootstrap_chain_model.py)
- [Experiment notes](../../../experiments/f001/bootstrap-chain-README.md)

The experiment is a dependency-chain illustration, not a compiler-security test.

## Cross-cutting evaluation contract — Engineering Quality Charter

This research item is governed by the project-wide [Engineering Quality Charter](../../foundation/engineering-quality-charter.md). Evaluate its topic-specific claims across:

- **Security:** assets, attacker capabilities, trust boundaries, enforcement path, least authority, abuse/DoS cases, and residual risks.
- **Correctness and reliability:** explicit invariants, safety/liveness properties, concurrency and TOCTOU hazards, failure points, recovery semantics, and falsifying counterexamples.
- **Performance:** credible baseline under the same workload; latency distributions including tail latency, throughput, and worst-case behavior where meaningful.
- **Efficiency:** CPU, memory, allocations, synchronization, context switches, I/O, data movement, storage amplification, and energy where measurable.
- **Innovation:** closest prior art and a precise, falsifiable difference. A new name or combination is not proof of global novelty.
- **Evidence:** label results as conceptual, formalized, modeled, tested, measured, reviewed, verified, implemented, or production-validated. A toy-model PASS is not proof of a real operating-system guarantee.

Where relevant, compare at least three credible approaches under equivalent assumptions. Record negative results and unmodeled behavior. Until threat analysis, comparative evaluation, and reproducibility requirements are met, this remains an initial research draft and cannot justify an architecture decision.
