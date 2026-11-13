# Memory Access Model

Run: `python3 memory_access_model.py`

The experiment checks a small permission map with two domains, separate private regions, and one explicitly shared region. It validates read/write permissions and rejects cross-domain access to a private region.

This is not a page-table implementation, capability proof, concurrency model, TLB simulation, or benchmark. Real systems must also address mapping races, stale translations, DMA, speculative execution, and revocation.
