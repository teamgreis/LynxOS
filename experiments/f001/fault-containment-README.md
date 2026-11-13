# F-001-M experiment — Fault containment

Run:

```sh
python3 experiments/f001/fault_containment_model.py
```

The model compares reachability in two dependency graphs. In the uncontained
graph a fault at A can propagate to all four nodes. In the second graph a
boundary separates C and D, limiting propagation from A to A and B.

Limitations: edges are assumed to represent possible propagation. No real
fault injection, process isolation, kernel boundary, correlated failure,
recovery, or performance behavior is modeled.
