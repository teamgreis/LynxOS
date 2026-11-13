# F-001-L experiment — System composition

Run:

```sh
python3 experiments/f001/system_composition_model.py
```

The graph represents component dependencies. A cycle in a wait-for graph is
a necessary warning for deadlock in the represented model; the acyclic graph
has no such cycle.

Limitations: this is a graph illustration, not a general deadlock proof.
It omits resource multiplicity, preemption, dynamic dependencies, and
component state machines.
