# F-001-L experiment — System composition

Run:

```sh
python3 experiments/f001/system_composition_model.py
```

The graph represents component dependencies. A cycle in a wait-for graph is
a necessary warning for deadlock in the represented model; the acyclic graph
has no such cycle.

Limitations: this is a graph illustration, not a general deadlock proof.
It omits resource multiplicity, preemption, dynamic dependencies, and
component state machines.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
