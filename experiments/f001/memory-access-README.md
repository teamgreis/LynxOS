# Memory Access Model

Run: `python3 memory_access_model.py`

The experiment checks a small permission map with two domains, separate private regions, and one explicitly shared region. It validates read/write permissions and rejects cross-domain access to a private region.

This is not a page-table implementation, capability proof, concurrency model, TLB simulation, or benchmark. Real systems must also address mapping races, stale translations, DMA, speculative execution, and revocation.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
