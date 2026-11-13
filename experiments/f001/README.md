# F-001-B — Explicit-State Concurrency Experiment

Run:

```sh
python3 experiments/f001/concurrency_diamond.py
```

The dependency-free script explores two tiny finite-state systems:

1. Two independent one-slot channels, where enabled operations on different channels should commute.
2. Two producers competing for one shared one-slot buffer, where a pair of initially enabled producer operations cannot both complete in either order.

For each reachable state, it examines pairs of distinct actions enabled in that state. A pair passes the diamond check when both execution orders are possible and reach the same resulting state.

## Interpretation

This experiment illustrates why state-dependent independence is more precise than assuming every concurrent-looking operation is independent.

It does **not** prove correctness for arbitrary programs, real hardware, memory models, I/O, failure, or scheduling. The model deliberately omits consumers in the shared-slot example and does not model physical time.

The next experiment should add consumer behavior, cancellation, crash states, bounded resources, and an explicit observation function. A later implementation should compare the same workload in a Petri net, dataflow model, and actor model.


## Initial run

The current script produces:

| Model | Reachable states | Enabled action-pairs checked | Diamond pairs | Non-diamond pairs |
|---|---:|---:|---:|---:|
| Independent bounded channels | 9 | 4 | 4 | 0 |
| Shared one-slot producer competition | 3 | 1 | 0 | 1 |

This is a sanity check for the small model, not evidence of a general performance or correctness advantage.

## Project-wide experiment quality requirements

All experiments in this directory are exploratory models. Their outputs validate only the properties explicitly asserted by each model. They do not prove properties of a real kernel, hardware, cryptographic implementation, or production workload. Before an experiment is cited as evidence, execute the committed file itself and record the exact command, Python/tool versions, environment, output, and revision. Performance claims additionally require a conventional baseline, representative workloads, repeated measurements, tail latency, and resource/energy accounting where available. Security experiments must include attacker assumptions, negative tests, failure injection, and residual-risk notes. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
