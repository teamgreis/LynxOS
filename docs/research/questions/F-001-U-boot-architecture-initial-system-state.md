# F-001-U — Boot Architecture and Initial System State

**Status:** Initial research draft  
**Program:** R1 — System/kernel foundations  
**Decision status:** No architecture decision

## Research question

How does a powered-off machine become a controlled, useful system, and which guarantees must hold during each transition?

Boot is not one event. It is a sequence of authority transfers, hardware initialization, memory establishment, image loading, integrity checks, and service activation. The exact sequence varies by firmware, platform, and operating-system design.

## Scope

Distinguish:
- reset and hardware-defined entry state;
- firmware initialization and platform discovery;
- boot selection and image loading;
- integrity verification versus measurement;
- early kernel or runtime initialization;
- handoff to the normal system;
- recovery, fallback, and interrupted-update behavior.

## Competing approaches

1. **Firmware-centric:** firmware performs substantial initialization and launches a signed OS image.
2. **Minimal firmware + staged loader:** firmware provides a narrow environment; successive stages initialize more facilities.
3. **Direct kernel entry:** firmware loads a kernel or EFI stub directly, reducing loader stages but shifting responsibilities.
4. **Verified/measured chain:** each stage verifies the next, measures it, or does both; verification and measurement are distinct properties.
5. **Recovery-first design:** a small independently recoverable environment validates and activates system generations.

These approaches can be combined. No single sequence is universally optimal.

## Important distinctions

- Secure Boot authenticates eligible boot components according to platform trust policy.
- Measured Boot records measurements; measurement alone does not prevent execution.
- A successful signature check does not prove that a component is bug-free.
- A boot stage must establish explicit preconditions for the next stage: CPU mode, memory map, interrupt state, device access, and ownership of resources.
- A fallback path can improve recoverability but also expands the trusted computing base.

Microsoft's boot documentation describes a chain from firmware and bootloader through kernel and startup components, including Secure Boot, Trusted Boot, and Measured Boot. Debian's reference describes a typical staged UEFI-to-loader-to-initramfs-to-system sequence. These are examples, not mandatory LynxOS architecture.

## Falsifiable questions

- U1: Can the handoff contract between adjacent stages be specified independently of a particular bootloader?
- U2: Which stages must be authenticated, measured, or both to detect unauthorized changes?
- U3: Can an interrupted update always leave at least one bootable system generation?
- U4: What is the smallest early environment capable of validating and activating a complete system?
- U5: Which hardware state must be reset or normalized before a stage can safely assume control?

## Experiment plan

Model a staged boot state machine. Inject failure at each stage and verify that the system either reaches a declared operational state or enters a defined recovery state. The model must not treat a hash check as proof of correctness or a measurement as enforcement.

## Preliminary conclusion

Boot architecture is fundamentally a problem of staged state construction and controlled authority transfer. The right number of stages, trust model, recovery design, and firmware dependence remain open.

## References

- Microsoft Learn, [Secure the Windows boot process](https://learn.microsoft.com/en-us/windows/security/operating-system-security/system-security/secure-the-windows-10-boot-process).
- Debian Reference, [System initialization](https://www.debian.org/doc/manuals/debian-reference/ch03.en.html).
- Apple Developer Archive, [The Early Boot Process](https://developer.apple.com/library/archive/documentation/Darwin/Conceptual/KernelProgramming/booting/booting.html).

## Limitations

This is an initial synthesis, not a systematic review. It does not select UEFI, a bootloader, a chain-of-trust policy, or a kernel entry model.
