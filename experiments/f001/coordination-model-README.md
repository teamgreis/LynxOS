# F-001-P experiment — quorum intersection

Run:

```sh
python3 experiments/f001/coordination_model.py
```

For three voters, the script enumerates every subset of size 1 and size 2:
- Threshold 1 permits disjoint quorums.
- Threshold 2 produces pairwise-intersecting quorums.

This illustrates a set-theoretic condition only. A real protocol also needs rules governing terms/epochs, durable promises, accepted values, membership changes, message ordering, and failures. Do not interpret this toy script as proving a particular consensus protocol safe.
