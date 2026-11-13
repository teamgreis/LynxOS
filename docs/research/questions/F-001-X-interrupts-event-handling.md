# F-001-X — Interrupts and Event Handling

**Status:** Initial research draft  
**Program:** R7 — Hardware/device architecture; R5 — Time/concurrency  
**Decision status:** No architecture decision

## Research question

How should a system detect, prioritize, dispatch, defer, coalesce, and recover from asynchronous hardware events while preserving bounded latency, isolation, and throughput?

Interrupt handling is a critical boundary between devices and computation. A design that performs too much work in a high-priority interrupt context can create latency spikes and denial-of-service risks. A design that defers everything may add latency and queue pressure.

## Candidate approaches

1. **Direct top-half handling:** perform the minimum device-specific work immediately in interrupt context. Low dispatch overhead, but strict execution bounds are essential.
2. **Top-half plus deferred work:** acknowledge/mask the source and enqueue work for a schedulable context. Separates urgent handling from heavier processing.
3. **Polling / hybrid polling:** periodically or adaptively inspect queues. Can reduce interrupt storms at high event rates but may waste cycles or add latency at low rates.
4. **Interrupt moderation/coalescing:** combine multiple events or delay notification until a threshold/time bound. Improves throughput and reduces interrupt overhead, but affects latency.
5. **Per-queue/per-core vectors and affinity:** use MSI/MSI-X and queue locality to reduce sharing and cross-core traffic; requires balancing and careful NUMA placement.
6. **Brokered event delivery:** isolate device-facing code and deliver validated event records to consumers. Improves containment but adds mediation and queue costs.

## Security and performance constraints

- Treat device-provided event data as untrusted input.
- Bound work per interrupt and per deferred batch.
- Prevent one device from monopolizing CPU time or queue capacity.
- Validate queue indices, lengths, ownership, and DMA completion before consuming data.
- Define overflow behavior, loss accounting, backpressure, and recovery.
- Avoid unsafe shared mutable state between interrupt and normal contexts.
- Measure tail latency and worst-case execution, not only average throughput.
- Consider interrupt affinity, cache locality, NUMA, and cross-core wakeups.
- Ensure masking, acknowledgement, and teardown cannot race with device removal.

Linux MSI/MSI-X documentation describes advantages of message-signaled interrupts, including non-shared vectors and per-queue specialization. NAPI demonstrates a hybrid interrupt/polling model for network receive processing. These are useful reference points, not prescriptions.

## Falsifiable questions

- X1: Under what event rates does bounded deferred processing outperform direct handling?
- X2: Can per-device quotas prevent interrupt storms from starving unrelated work?
- X3: What coalescing policy minimizes total cost subject to a declared latency bound?
- X4: Can event delivery remain safe when a device is reset or removed with work queued?
- X5: Which synchronization costs dominate on multicore systems?

## Experiment plan

Use a deterministic event-arrival model with bounded interrupt work, deferred batches, finite queue capacity, and per-source budgets. Compare immediate processing, bounded deferred processing, and coalesced processing. Record processed events, drops, handler work, queue high-water mark, and modeled notification latency. This is a mechanism comparison, not a hardware benchmark.

## Preliminary conclusion

A promising research direction is to keep the interrupt-critical path minimal and bounded, while making deferred work schedulable, quota-controlled, observable, and locality-aware. Whether that should be universal or selectively applied remains open.

## References

- Linux kernel documentation, [The MSI Driver Guide HOWTO](https://docs.kernel.org/PCI/msi-howto.html).
- Linux kernel documentation, [NAPI](https://docs.kernel.org/networking/napi.html).
- Microsoft Learn, [Overview of NDIS MSI-X](https://learn.microsoft.com/en-us/windows-hardware/drivers/network/ndis-msi-x).

## Limitations

No interrupt controller, CPU architecture, driver ABI, or event framework is selected. The model does not simulate real interrupt latency, cache effects, memory ordering, or device behavior.

## Cross-cutting evaluation contract — Engineering Quality Charter

This research item is governed by the project-wide [Engineering Quality Charter](../../foundation/engineering-quality-charter.md). Evaluate its topic-specific claims across:

- **Security:** assets, attacker capabilities, trust boundaries, enforcement path, least authority, abuse/DoS cases, and residual risks.
- **Correctness and reliability:** explicit invariants, safety/liveness properties, concurrency and TOCTOU hazards, failure points, recovery semantics, and falsifying counterexamples.
- **Performance:** credible baseline under the same workload; latency distributions including tail latency, throughput, and worst-case behavior where meaningful.
- **Efficiency:** CPU, memory, allocations, synchronization, context switches, I/O, data movement, storage amplification, and energy where measurable.
- **Innovation:** closest prior art and a precise, falsifiable difference. A new name or combination is not proof of global novelty.
- **Evidence:** label results as conceptual, formalized, modeled, tested, measured, reviewed, verified, implemented, or production-validated. A toy-model PASS is not proof of a real operating-system guarantee.

Where relevant, compare at least three credible approaches under equivalent assumptions. Record negative results and unmodeled behavior. Until threat analysis, comparative evaluation, and reproducibility requirements are met, this remains an initial research draft and cannot justify an architecture decision.
