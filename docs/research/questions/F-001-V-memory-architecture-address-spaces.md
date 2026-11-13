# F-001-V — Memory Architecture and Address Spaces

**Status:** Initial research draft  
**Program:** R4 — Memory/persistent state  
**Decision status:** No architecture decision

## Research question

How should a computing system represent, allocate, protect, share, persist, and reclaim memory across independent computations?

Memory architecture spans physical storage, virtual address translation, object lifetime, protection, sharing, persistence, and resource governance. A virtual address space is one powerful abstraction, not the definition of memory itself.

## Candidate approaches

1. **Flat physical addressing:** software addresses physical memory directly; simple but difficult to isolate and relocate.
2. **Paged virtual address spaces:** per-domain mappings provide isolation, sparse address spaces, sharing, and demand paging; translation and TLB behavior add complexity.
3. **Segmentation or capability-oriented regions:** bounds and authority are attached to regions or references; hardware and language support vary.
4. **Object/region-based memory:** allocation and lifetime are organized around objects, regions, arenas, or ownership scopes.
5. **Managed/garbage-collected memory:** runtime tracks object reachability and reclamation; integration with low-level system resources requires care.
6. **Hybrid designs:** combine virtual memory, capabilities, object lifetimes, pinned regions, and explicit resource accounting.

## Dimensions to compare

- address identity versus physical location;
- protection granularity and authority;
- sharing and copy-on-write;
- allocation, reclamation, fragmentation, and compaction;
- page faults, TLB invalidation, NUMA and cache effects;
- DMA and device-visible memory;
- persistence and crash consistency;
- memory overcommit, pressure, and denial-of-service behavior;
- debugging, observability, and compatibility.

## Established observations

Commodity systems commonly use virtual memory and page-level access permissions to isolate processes. Translation caches such as TLBs reduce the cost of address translation, while adding coherence and invalidation concerns. Virtualized systems introduce additional layers of translation and resource-management challenges. These facts do not imply that every LynxOS computation must be a conventional process or use one address space per process.

## Falsifiable questions

- V1: Which protection guarantees require hardware page tables, and which can be enforced by software or language-level mechanisms?
- V2: Can memory identity remain stable across relocation or remapping without hiding physical costs?
- V3: Which sharing model minimizes copying while preserving clear authority?
- V4: How should persistent state interact with volatile address spaces?
- V5: Can a unified resource model account for ordinary RAM, pinned memory, DMA buffers, and device memory?

## Experiment plan

Compare two abstract domains with private mappings and an explicitly shared region. Check allowed and denied accesses, mapping changes, and whether revocation affects stale mappings. Extend later with allocation pressure, COW, page faults, and DMA constraints.

## Preliminary conclusion

Memory design is a multi-dimensional trade-off among isolation, sharing, performance, persistence, and manageability. Address spaces are an important candidate abstraction, but their granularity and relationship to computation identity remain open.

## References

- Mishra and Kulkarni, [A survey of memory management techniques in virtualized systems](https://doi.org/10.1016/j.cosrev.2018.06.002), *Computer Science Review*, 2018.
- [Transient-Execution Attacks: A Computer Architect Perspective](https://doi.org/10.1145/3603619), ACM, 2023 (background on translation and page permissions).
- Linux kernel documentation, [Memory Management](https://docs.kernel.org/mm/).

## Limitations

This initial synthesis does not select paging, segmentation, garbage collection, capabilities, or any memory model. The experiment is an access-control abstraction, not a performance simulation.
