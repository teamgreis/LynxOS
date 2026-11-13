# F-001-P experiment — quorum intersection

Run:

```sh
python3 experiments/f001/coordination_model.py
```

For three voters, the script enumerates every subset of size 1 and size 2:
- Threshold 1 permits disjoint quorums.
- Threshold 2 produces pairwise-intersecting quorums.

This illustrates a set-theoretic condition only. A real protocol also needs rules governing terms/epochs, durable promises, accepted values, membership changes, message ordering, and failures. Do not interpret this toy script as proving a particular consensus protocol safe.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
