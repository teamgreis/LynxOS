# F-001-T experiment — Bootstrap chain

Run:

```sh
python3 experiments/f001/bootstrap_chain_model.py
```

A deterministic string transformation stands in for successive compiler generations. Changing the seed changes the first artifact and propagates through later stages.

Limitations:
- This is not a compiler, build system, or cryptographic model.
- It does not model reproducibility across machines or malicious compiler behavior.
- Stage outputs are intentionally dependent on their predecessor; real compiler fixed-point checks have different semantics.
- Passing assertions does not establish correctness or trust.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
