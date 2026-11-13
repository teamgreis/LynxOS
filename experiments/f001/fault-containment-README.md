# F-001-M experiment — Fault containment

Run:

```sh
python3 experiments/f001/fault_containment_model.py
```

The model compares reachability in two dependency graphs. In the uncontained
graph a fault at A can propagate to all four nodes. In the second graph a
boundary separates C and D, limiting propagation from A to A and B.

Limitations: edges are assumed to represent possible propagation. No real
fault injection, process isolation, kernel boundary, correlated failure,
recovery, or performance behavior is modeled.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
