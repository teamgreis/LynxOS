# Scheduling Policy Model

Run: `python3 scheduling_policy_model.py`

Compares three deterministic service-selection rules over the same finite workload: round robin, a simple weighted heuristic, and fixed priority. Reports CPU service, finish times, deadline misses, and unfinished demand. The assertions check that fixed priority favors higher-priority classes in this workload.

This is not a production scheduler, a mathematically fair weighted-fair-queueing implementation, a real-time schedulability proof, or a benchmark. It omits multicore placement, preemption costs, blocking, interrupts, priority inheritance, and energy.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
