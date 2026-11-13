# F-001-Z — Storage Architecture and Persistence

**Status:** Initial research draft  
**Program:** R9 — Storage/networking/core services; R4 — Memory/persistent state  
**Decision status:** No architecture decision

## Research question

How should LynxOS represent, update, protect, index, cache, and recover persistent data across power loss, software failure, media errors, and concurrent access?

Persistence is not simply “write bytes to disk.” The system must define atomicity, ordering, durability, integrity, recovery, access control, and the boundary between volatile caches and stable media.

## Candidate approaches

1. **In-place updates with write-ahead logging (journaling):** record intent or changes before applying updates; recovery replays or rolls back committed transactions. Write ordering and flush semantics are critical.
2. **Copy-on-write trees / shadow paging:** write new blocks and atomically publish a new root or metadata pointer. Preserves prior versions but can amplify writes and fragment free space.
3. **Log-structured storage:** append updates sequentially and reclaim/compact later. Can make writes efficient but imposes cleaning and write-amplification costs.
4. **Object/content-addressed storage:** immutable objects identified by content or stable IDs; integrity and deduplication opportunities, with indexing and garbage-collection complexity.
5. **Byte-addressable persistent memory model:** exploit load/store access to persistent media where available; requires explicit persistence ordering and cache-line flush/fence semantics.
6. **Hybrid tiered storage:** combine volatile caches, persistent logs, immutable data, and block devices according to latency, endurance, capacity, and durability needs.

## Correctness and security dimensions

- Define what a successful write/commit acknowledgement guarantees.
- Distinguish atomicity, consistency, isolation, and durability.
- Specify flush, barrier, FUA, and device-cache assumptions.
- Recover safely from every crash point in a transaction.
- Detect corruption using checksums/authentication where appropriate; checksums detect accidental corruption, not malicious modification.
- Protect data confidentiality and metadata integrity.
- Control rollback, snapshots, deletion, and secure erasure expectations.
- Bound write amplification, garbage collection, fragmentation, and recovery time.
- Handle concurrent writers and torn writes.
- Test real devices: advertised flush behavior and power-loss guarantees vary.

Copy-on-write and journaling are established families with different performance and recovery trade-offs. Non-volatile memory changes the storage hierarchy and can make software-stack overhead dominant. No one technique is universally best.

## Falsifiable questions

- Z1: Which persistence contract gives applications the strongest useful guarantee at the lowest write and latency cost?
- Z2: Can transactional updates be made crash-atomic with bounded recovery work?
- Z3: How do journaling, copy-on-write, and append-only logs compare under small random writes and large sequential writes?
- Z4: Can integrity verification be performed incrementally without making reads prohibitively expensive?
- Z5: How should storage policy adapt to device endurance, latency, and failure characteristics without weakening declared durability?

## Experiment plan

Model a small metadata update as a sequence of writes and inject a crash after every step. Compare in-place update without a log, write-ahead logging, and copy-on-write root publication. After recovery, assert that state is either the complete old value or complete new value for the transactional approaches. Record writes and recovery operations as simple cost proxies.

## Preliminary conclusion

The most important design decision is not a particular filesystem layout but the explicit persistence contract: what becomes durable, when, and under which failure assumptions. Storage mechanisms must be evaluated against that contract and measured on target media.

## References

- [A Survey on Copy-on-Write File Systems](https://doi.org/10.1109/ICTC62082.2024.10826721), IEEE ICTC, 2024.
- [A Survey of Non-Volatile Main Memory File Systems](https://doi.org/10.1007/s11390-023-1054-3), *Journal of Computer Science and Technology*, 2023.
- [Survey of Distributed File System Design Choices](https://doi.org/10.1145/3465405), ACM Computing Surveys, 2021.
- Linux kernel documentation, [ext4 journal](https://docs.kernel.org/filesystems/ext4/journal.html).

## Limitations

This initial synthesis does not choose a filesystem, block format, database model, encryption scheme, or hardware durability contract. The experiment is a crash-state abstraction, not a filesystem implementation or power-failure test.

## Cross-cutting evaluation contract — Engineering Quality Charter

This research item is governed by the project-wide [Engineering Quality Charter](../../foundation/engineering-quality-charter.md). Evaluate its topic-specific claims across:

- **Security:** assets, attacker capabilities, trust boundaries, enforcement path, least authority, abuse/DoS cases, and residual risks.
- **Correctness and reliability:** explicit invariants, safety/liveness properties, concurrency and TOCTOU hazards, failure points, recovery semantics, and falsifying counterexamples.
- **Performance:** credible baseline under the same workload; latency distributions including tail latency, throughput, and worst-case behavior where meaningful.
- **Efficiency:** CPU, memory, allocations, synchronization, context switches, I/O, data movement, storage amplification, and energy where measurable.
- **Innovation:** closest prior art and a precise, falsifiable difference. A new name or combination is not proof of global novelty.
- **Evidence:** label results as conceptual, formalized, modeled, tested, measured, reviewed, verified, implemented, or production-validated. A toy-model PASS is not proof of a real operating-system guarantee.

Where relevant, compare at least three credible approaches under equivalent assumptions. Record negative results and unmodeled behavior. Until threat analysis, comparative evaluation, and reproducibility requirements are met, this remains an initial research draft and cannot justify an architecture decision.
