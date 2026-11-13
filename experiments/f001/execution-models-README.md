# F-001-Q experiment — abstract execution strategies

Run:

```sh
python3 experiments/f001/execution_models.py
```

The workload is a small dependency graph: A=2, B=3, C=A+B, D=2×C. Three abstract strategies execute it:
- sequential topological order;
- event queue with readiness-triggered dispatch;
- dataflow-style repeated firing of nodes whose dependencies are available.

All should produce D=10. The trace order is an observation of the chosen abstract strategy, not a timing measurement. The code does not simulate preemption, real concurrency, OS scheduling, or hardware.
