# Interrupt/Event Model

Run: `python3 interrupt_event_model.py`

The deterministic model checks a constant-cost top-half abstraction, finite queue capacity, bounded deferred batches, and explicit drop accounting under both steady and burst arrivals. The overload case deliberately demonstrates that bounded queues reject excess work rather than grow without limit.

It does not model actual interrupt entry/exit cost, device acknowledgement, concurrent producers, cache locality, DMA ordering, coalescing timers, or a real scheduler. Queue and service outputs are properties of this simplified arrival/service pattern only.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
