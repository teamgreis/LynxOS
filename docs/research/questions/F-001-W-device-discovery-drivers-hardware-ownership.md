# F-001-W — Device Discovery, Drivers and Hardware Ownership

**Status:** Initial research draft  
**Program:** R7 — Hardware/device architecture  
**Decision status:** No architecture decision

## Research question

How does a system discover hardware, decide which software may control it, allocate its resources, and safely manage its lifecycle?

Device discovery, driver matching, resource assignment, and device ownership are related but distinct problems. A discovered device is not automatically safe to use, and a matching driver is not automatically trusted.

## Candidate approaches

1. **Static platform description:** board or platform tables enumerate known devices; predictable but platform-specific.
2. **Bus enumeration:** buses such as PCI and USB report devices and identifiers; supports dynamic discovery and hotplug.
3. **Firmware-described devices:** firmware tables describe platform devices and resources; avoids blind probing but depends on firmware correctness.
4. **Driver-initiated probing:** drivers search for hardware; useful in constrained legacy settings but can be unsafe or ambiguous.
5. **Brokered device ownership:** a system component mediates assignment, resource allocation, access, and lifecycle.
6. **Direct or mediated assignment:** a driver or isolated domain receives direct device access, or accesses it through a broker; trade-offs include performance, isolation, and shared-device complexity.

## Lifecycle model

A candidate neutral lifecycle is:
discovered → described → matched → authorized → resources-assigned → initialized → active → quiescing → detached/failed.

Transitions may fail. Removal must account for outstanding I/O, DMA, interrupts, mappings, references, and dependent services.

## Key design dimensions

- identity and provenance of device descriptions;
- bus topology and enumeration;
- driver matching and version compatibility;
- memory-mapped I/O, port I/O, interrupts, DMA and IOMMU;
- exclusive versus shared ownership;
- hotplug, reset, suspend, resume and removal;
- driver isolation, crash containment and recovery;
- firmware trust and spoofable identifiers;
- resource conflicts and power management.

## Established observations

Linux's driver model separates device enumeration from driver binding in many cases. Device/driver matching triggers a probe callback, which must still verify that the driver can operate the device. Linux documentation discourages error-prone probing when bus-level or firmware enumeration is available. The model is a useful reference, not a mandatory LynxOS design.

## Falsifiable questions

- W1: Can discovery be performed without granting the discovering component control of the device?
- W2: What minimum evidence is required before a driver is authorized to bind?
- W3: Can device ownership be revoked safely when DMA or asynchronous I/O is outstanding?
- W4: Which devices can be safely shared, and which require exclusive assignment?
- W5: Can driver failure be contained without destabilizing unrelated devices or the whole system?

## Experiment plan

Model discovery, matching, authorization, resource assignment, and activation as separate steps. Inject failures and mismatches. Verify that an unauthorized or mismatched driver never reaches the active state and that resources are released on failed initialization.

## Preliminary conclusion

Device management should be studied as a lifecycle and authority problem, not merely as a driver-loading problem. Enumeration, binding, authorization, and ownership must remain distinguishable in the research model.

## References

- Linux kernel documentation, [The Linux Kernel Device Model](https://www.kernel.org/doc./html/next/driver-api/driver-model/overview.html).
- Linux kernel documentation, [Platform Devices and Drivers](https://kernel.org/doc/html/latest/driver-api/driver-model/platform.html).
- Linux kernel documentation, [Driver Binding](https://docs.kernel.org/driver-api/driver-model/binding.html).
- Linux Kernel Labs, [Linux Device Model](https://linux-kernel-labs.github.io/refs/heads/master/labs/device_model.html).

## Limitations

This draft does not select a driver architecture, bus framework, device broker, IOMMU policy, or isolation boundary. The experiment is a state-machine toy model, not a hardware driver.

## Cross-cutting evaluation contract — Engineering Quality Charter

This research item is governed by the project-wide [Engineering Quality Charter](../../foundation/engineering-quality-charter.md). Evaluate its topic-specific claims across:

- **Security:** assets, attacker capabilities, trust boundaries, enforcement path, least authority, abuse/DoS cases, and residual risks.
- **Correctness and reliability:** explicit invariants, safety/liveness properties, concurrency and TOCTOU hazards, failure points, recovery semantics, and falsifying counterexamples.
- **Performance:** credible baseline under the same workload; latency distributions including tail latency, throughput, and worst-case behavior where meaningful.
- **Efficiency:** CPU, memory, allocations, synchronization, context switches, I/O, data movement, storage amplification, and energy where measurable.
- **Innovation:** closest prior art and a precise, falsifiable difference. A new name or combination is not proof of global novelty.
- **Evidence:** label results as conceptual, formalized, modeled, tested, measured, reviewed, verified, implemented, or production-validated. A toy-model PASS is not proof of a real operating-system guarantee.

Where relevant, compare at least three credible approaches under equivalent assumptions. Record negative results and unmodeled behavior. Until threat analysis, comparative evaluation, and reproducibility requirements are met, this remains an initial research draft and cannot justify an architecture decision.
