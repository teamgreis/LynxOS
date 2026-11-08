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
