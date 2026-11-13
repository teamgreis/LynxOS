# F-001-S — Hardware Abstraction and Machine Independence

**Status:** Initial research draft  
**Program:** R7 — Hardware/device architecture; cross-reference R0  
**Decision status:** No architecture decision

## 1. Research question

Which properties of computation and system services can be expressed independently of a particular processor, memory hierarchy, interrupt controller, timer, or device—and what information must remain hardware-specific?

The objective is not to hide hardware at any cost. Abstraction can improve portability but can also erase capabilities, performance characteristics, failure modes, and security-relevant behavior.

## 2. Abstraction layers to investigate

- Instruction-set architecture (ISA) and execution environment.
- Privilege levels, traps, interrupts, and exception delivery.
- Physical and virtual memory, address translation, cache and coherency.
- Timers, clocks, counters, and scheduling facilities.
- DMA, IOMMU, device discovery, and interrupt routing.
- Power management, thermal limits, accelerators, and heterogeneous cores.
- Firmware, boot protocols, and platform description.

The RISC-V specification describes execution environments as layered interfaces; more abstract environments can improve portability while defining which resources and behaviors software can rely on. [RISC-V ISA introduction](https://docs.riscv.org/reference/isa/v20250508/unpriv/intro.html)

## 3. Competing approaches

| Approach | Description | Benefits | Costs / risks |
|---|---|---|---|
| Direct hardware access | Services use architecture/device details directly | Maximum control and optimization | Porting burden; wider trusted surface |
| Thin HAL | Small set of low-level primitives | Explicit boundary and low overhead | Leaks hardware differences upward |
| Rich virtual platform | Stable abstract machine with emulated capabilities | Portability and testability | Lowest-common-denominator risk; virtualization cost |
| Capability discovery | Query optional hardware features and constraints | Preserves specialization | More complex feature negotiation |
| Portable core + optimized backends | Common semantics with architecture-specific implementations | Balance of portability and performance | Backend correctness and maintenance burden |

## 4. Research dimensions

For each proposed abstraction, record:
1. Semantic contract: what behavior is guaranteed?
2. Optionality: absent, emulated, or mandatory?
3. Cost visibility: can latency, bandwidth, alignment, and energy be observed?
4. Failure model: can operations fail, time out, or partially complete?
5. Security boundary: who controls the device and its DMA/interrupt behavior?
6. Verification: how can implementations be tested against the contract?
7. Versioning: how do new capabilities evolve without breaking old consumers?

## 5. Hypotheses and falsifiable questions

- **H-S1:** A small stable primitive interface can support multiple machine families without forcing every platform into identical performance behavior.
- **H-S2:** Capability discovery preserves more useful specialization than a strict lowest-common-denominator abstraction.
- **H-S3:** Hiding timing and failure characteristics causes correctness or performance surprises in latency-sensitive services.
- **H-S4:** A portable semantic contract plus architecture-specific implementation can be tested with shared conformance suites.

Test with at least two distinct execution environments, synthetic device models, and workloads that stress timers, memory ordering, interrupts, and DMA.

## 6. Minimal experiment

The accompanying model represents two machines with different native capabilities. It compares a strict common interface with capability discovery, tracking which operations are available and whether a fallback is needed.

This is a set-coverage model only; it does not benchmark real hardware or emulate an ISA.

## 7. Prior work and references

- [RISC-V Unprivileged ISA — Introduction and execution environments](https://docs.riscv.org/reference/isa/v20250508/unpriv/intro.html).
- [Towards a Unified Hardware Abstraction Layer Architecture for Embedded Systems](https://www.cecs.uci.edu/~doemer/publications/CECS_TR_12_14.pdf).
- [ACPI Specification](https://uefi.org/specifications), for platform configuration and power-management interfaces.
- [UEFI Specifications](https://uefi.org/specifications), for firmware-to-OS boot interfaces.

## 8. What this does not decide

No ISA, HAL design, device model, boot protocol, memory model, or initial target platform is selected. x86-64 and ARM64 remain candidate targets to validate, not a final commitment.

## 9. Experiment

- [Hardware abstraction model](../../../experiments/f001/hardware_abstraction_model.py)
- [Experiment notes](../../../experiments/f001/hardware-abstraction-README.md)

No real hardware measurements or portability claims are made.
