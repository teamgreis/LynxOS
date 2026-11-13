# F-001-O experiment — invariant exploration

Run:

```sh
python3 experiments/f001/invariant_model.py
```

The model starts at counter value 0 and declares (counter \leq 3) as the invariant. It explores all reachable states for a guarded and unguarded increment transition.

Expected result:
- Guarded: states 0, 1, 2, 3; no violation.
- Unguarded: reaches 4; counterexample trace 0 → 1 → 2 → 3 → 4.

The finite model is deliberately tiny. It demonstrates reachability-based invariant checking and counterexample reconstruction, not a general proof method or a claim about LynxOS implementation correctness.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
