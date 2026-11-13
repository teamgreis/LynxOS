# F-001-H experiment — Temporal semantics

Run:

```sh
python3 experiments/f001/temporal_semantics_model.py
```

The deterministic model demonstrates:

1. A send event and its receive event are causally ordered.
2. A separate local event can have the same Lamport scalar timestamp as
   the receive event while remaining concurrent with it.
3. Vector-clock comparison distinguishes the causal pair from the concurrent
   pair in this two-process example.
4. A backward wall-clock step can produce a negative naive elapsed duration,
   while a monotonic clock's elapsed duration remains positive.

Expected output ends with:

```text
PASS: all temporal model assertions satisfied
```

## Assumptions and limitations

- The vector clocks are manually assigned according to the stated event graph.
- The wall-clock step and monotonic readings are illustrative fixed values.
- No real clock source, NTP/PTP synchronization, drift, uncertainty interval,
  suspend/resume hardware, distributed message transport, scheduler, or
  real-time deadline behavior is implemented.
- Equal Lamport timestamps do not always imply concurrency; this example
  demonstrates one concurrent pair. Lamport scalar order preserves causal
  precedence but does not encode the complete causal relation.

This is an executable conceptual model, not a benchmark or proof of a
production clock protocol.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
