# F-001-J experiment — Representation and semantics

Run:

```sh
python3 experiments/f001/representation_semantics_model.py
```

A tiny arithmetic expression is evaluated directly from an abstract syntax tree
and after compilation to stack bytecode. The test checks that both paths return
the same result for the chosen input.

Expected final line:

```text
PASS: representation semantics assertions satisfied
```

Limitations: one expression and one environment only; no proof of compiler
correctness, static typing, overflow semantics, exceptions, side effects,
optimization, concurrency, timing, or resource equivalence.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
