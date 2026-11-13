# F-001-N experiment — Safe reconfiguration

Run:

```sh
python3 experiments/f001/reconfiguration_model.py
```

The toy model compares an interrupted in-place schema update with a staged
candidate transformation. The staged path validates the candidate invariant
before treating it as active and leaves the original state unchanged during
preparation.

Limitations: no atomic activation primitive, persistent storage, concurrent
reader/writer, external side effect, distributed rollout, or real rollback
mechanism is modeled. It illustrates a pattern, not a production guarantee.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
