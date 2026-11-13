# F-001-S experiment — Hardware abstraction

Run:

```sh
python3 experiments/f001/hardware_abstraction_model.py
```

Two fictional machines share a minimal timer/DMA interface but differ in optional IOMMU and vector capabilities. The model compares a common required subset with explicit capability discovery and fallback classification.

Limitations:
- Fictional capabilities; not based on measured devices.
- No timing, memory-ordering, interrupt, DMA isolation, or power model.
- A fallback is merely labeled, not implemented.
- No claim that the chosen interface is sufficient for an operating system.
