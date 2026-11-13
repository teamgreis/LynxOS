# F-001-C — Crash and Retry Experiment

Run:

```sh
python3 experiments/f001/failure_retry_model.py
```

The script explores two tiny state machines.

1. **Naive protocol:** an internal effect is durable, but the acknowledgement is volatile. A crash between effect and acknowledgement loses the acknowledgement. A retry can repeat the effect.
2. **Atomic internal commit plus request identity:** the effect and a durable request-id marker are committed atomically. A retry after a crash recognizes the committed request and does not apply the internal effect again.

The experiment demonstrates a narrow point: retry semantics depend on the commit boundary and durable identity. It does not establish arbitrary exactly-once delivery, because external side effects may not participate in the same atomic transaction.

## Scope limitations

- One logical request and at most one crash/retry.
- No actual filesystem or database.
- No hardware write reordering or torn writes.
- No network partition or Byzantine fault.
- No external side effect outside the modeled commit boundary.
- No proof of safety or liveness for arbitrary programs.

The next iteration should add cancellation points, multiple concurrent requests, incomplete log writes, and an irreversible external observer.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
