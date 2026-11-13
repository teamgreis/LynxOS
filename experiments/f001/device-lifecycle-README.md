# Device Lifecycle Model

Run: `python3 device_lifecycle_model.py`

The experiment separates discovery, driver matching, authorization, resource assignment, and activation. It checks that mismatches, unauthorized drivers, and resource failures cannot reach the active state.

It does not emulate PCI/USB enumeration, DMA, interrupts, IOMMU isolation, hotplug races, driver crashes, or actual hardware. Its state labels are intentionally simplified.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
