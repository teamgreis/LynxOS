# F-001-G experiment — State continuity

Run:

```sh
python3 experiments/f001/state_continuity_model.py
```

The deterministic model injects crashes at three abstract persistence boundaries
for each strategy:

1. unsafe in-place field writes;
2. copy-on-write followed by an atomic root switch;
3. write-ahead logging with replay after a durable commit record.

The invariant is that recovery yields either the complete old state or the
complete new state. The in-place strategy includes a mixed/torn state and must
fail that invariant. Copy-on-write and WAL satisfy it under the assumptions
encoded in this toy model.

Expected output ends with:

```text
PASS: all model assertions satisfied
```

## Assumptions and limitations

- Field writes may persist independently in the unsafe baseline.
- The copy-on-write root switch is assumed atomic and durable.
- The WAL commit record is assumed to distinguish complete committed work
  from incomplete work; recovery replays only committed records.
- No actual storage ordering, cache flush, filesystem, hardware, checksum,
  concurrency, replication, or performance behavior is modeled.

This is a minimal executable illustration, not evidence that any particular
implementation of CoW or WAL is correct. Real systems must validate their
persistence barriers, ordering rules, recovery protocol, and failure model.
