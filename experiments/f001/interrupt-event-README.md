# Interrupt/Event Model

Run: `python3 interrupt_event_model.py`

The deterministic model checks a constant-cost top-half abstraction, finite queue capacity, bounded deferred batches, and explicit drop accounting under overload.

It does not model actual interrupt entry/exit cost, device acknowledgement, concurrent producers, cache locality, DMA ordering, coalescing timers, or a real scheduler. The queue-high-water and throughput outputs are properties of this simplified arrival/service pattern only.
