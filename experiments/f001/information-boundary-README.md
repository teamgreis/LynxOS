# F-001-R experiment — Information boundaries

Run with Python 3:

```sh
python3 experiments/f001/information_boundary_model.py
```

The same byte sequence can be treated as opaque bytes, UTF-8 text, or an unsigned integer depending on its schema. The small flow function demonstrates a two-level policy where secret data cannot flow to a public destination.

Limitations:
- No actual serialization protocol or schema registry.
- No cryptography, provenance authentication, timing channel, or implicit-flow analysis.
- The label policy is illustrative and not a complete information-flow system.
- Passing assertions demonstrates only the behavior of this toy model.
