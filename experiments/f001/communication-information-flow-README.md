# F-001-I experiment — Communication and information flow

Run:

```sh
python3 experiments/f001/communication_information_flow_model.py
```

The model injects a duplicate request and compares naive processing with
request-ID deduplication. It also substitutes two secret values while holding
the public input constant and checks that the modeled public observation does
not change.

Expected final line:

```text
PASS: all communication model assertions satisfied
```

Limitations: no real transport, loss/reordering, durable deduplication,
transactional side effect, cryptography, timing channel, or formal
noninterference proof is implemented.
