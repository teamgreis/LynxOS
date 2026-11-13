# F-001-N experiment — Safe reconfiguration

Run:

```sh
python3 experiments/f001/reconfiguration_model.py
```

The toy model compares an interrupted in-place schema update with a staged
candidate transformation. The staged path validates the candidate invariant
before treating it as active and leaves the original state unchanged during
preparation.

Limitations: no atomic activation primitive, persistent storage, concurrent
reader/writer, external side effect, distributed rollout, or real rollback
mechanism is modeled. It illustrates a pattern, not a production guarantee.
