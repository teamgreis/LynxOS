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
