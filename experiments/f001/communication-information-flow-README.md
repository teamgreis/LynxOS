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

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
