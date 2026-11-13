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
