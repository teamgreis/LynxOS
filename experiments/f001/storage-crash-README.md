# Storage Crash Model

Run: `python3 storage_crash_model.py`

The model explores crashes around simplified write-ahead-log and copy-on-write publication steps and checks the old-or-new recovery property. It is deliberately a tiny transaction model.

Important limitations: it assumes atomic individual abstract steps and does not model torn sectors, volatile device caches, flush/FUA ordering, checksums, concurrent writers, log corruption, allocator metadata, or real power loss. The in-place contrast also assumes one atomic overwrite and therefore is not a realistic general filesystem model.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
