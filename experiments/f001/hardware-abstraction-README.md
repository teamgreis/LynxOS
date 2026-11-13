# F-001-S experiment — Hardware abstraction

Run:

```sh
python3 experiments/f001/hardware_abstraction_model.py
```

Two fictional machines share a minimal timer/DMA interface but differ in optional IOMMU and vector capabilities. The model compares a common required subset with explicit capability discovery and fallback classification.

Limitations:
- Fictional capabilities; not based on measured devices.
- No timing, memory-ordering, interrupt, DMA isolation, or power model.
- A fallback is merely labeled, not implemented.
- No claim that the chosen interface is sufficient for an operating system.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
