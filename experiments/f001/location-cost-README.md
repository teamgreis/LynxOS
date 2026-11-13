# F-001-E experiment — Location cost model

Run:

    python3 experiments/f001/location_cost_model.py

The script compares three abstract strategies for the same deterministic computation:

1. **move-data-to-compute:** transfer the input data to the compute location.
2. **move-computation-to-data:** pay a fixed migration cost and execute at the data location.
3. **remote-invocation:** pay a round-trip communication cost and a small request/response payload cost.

Each strategy runs the same deterministic operation on the same logical input. The script checks that outputs are equal and reports estimated cost and bytes transferred.

## Assumptions
- Cost units are abstract and not milliseconds.
- Data transfer cost is data_bytes / configured_bandwidth.
- Compute cost is linear in abstract work units.
- Migration and serialization are represented by fixed costs.
- Remote invocation transfers a fixed 128-byte request/response payload in this simplified model.
- No mutable process state, failures, consistency protocol, security boundary, hardware heterogeneity, or real network is modeled.

This experiment illustrates a trade-off only. It is not a benchmark, proof of migration safety, or evidence that one placement strategy is generally best. In particular, moving computation is only plausible when the computation can execute at the destination and has the necessary data authority.

## Follow-up
Vary data size, compute intensity, bandwidth, round-trip latency, migration size, serialization cost, and destination compute capability. Then add failure during migration, mutable state, trust boundaries, and consistency semantics.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
