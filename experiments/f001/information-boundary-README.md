# F-001-R experiment — Information boundaries

Run with Python 3:

```sh
python3 experiments/f001/information_boundary_model.py
```

The same byte sequence can be treated as opaque bytes, UTF-8 text, or an unsigned integer depending on its schema. The small flow function demonstrates a two-level policy where secret data cannot flow to a public destination.

Limitations:
- No actual serialization protocol or schema registry.
- No cryptography, provenance authentication, timing channel, or implicit-flow analysis.
- The label policy is illustrative and not a complete information-flow system.
- Passing assertions demonstrates only the behavior of this toy model.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
