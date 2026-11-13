# F-001-Q experiment — abstract execution strategies

Run:

```sh
python3 experiments/f001/execution_models.py
```

The workload is a small dependency graph: A=2, B=3, C=A+B, D=2×C. Three abstract strategies execute it:
- sequential topological order;
- event queue with readiness-triggered dispatch;
- dataflow-style repeated firing of nodes whose dependencies are available.

All should produce D=10. The trace order is an observation of the chosen abstract strategy, not a timing measurement. The code does not simulate preemption, real concurrency, OS scheduling, or hardware.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
