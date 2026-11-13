#!/usr/bin/env python3
"""Deterministic toy model for bounded interrupt work and deferred event handling."""
from collections import deque

def simulate(arrival_counts, capacity, batch, budget):
    queue = deque()
    processed = dropped = irq_work = batches = high_water = 0
    for cycle, arrivals in enumerate(arrival_counts):
        # Each event causes bounded top-half work; queue capacity is finite.
        for event in range(arrivals):
            irq_work += 1
            if len(queue) < capacity:
                queue.append((cycle, event))
                high_water = max(high_water, len(queue))
            else:
                dropped += 1
        # Deferred context has a strict per-cycle service bound.
        served = 0
        while queue and served < min(batch, budget):
            queue.popleft()
            processed += 1
            served += 1
        if served:
            batches += 1
    while queue:
        for _ in range(min(batch, budget)):
            if queue:
                queue.popleft()
                processed += 1
    return {"processed": processed, "dropped": dropped, "irq_work": irq_work,
            "batches": batches, "queue_high_water": high_water}

def main():
    steady = simulate([1] * 1000, capacity=64, batch=8, budget=8)
    assert steady["processed"] == 1000 and steady["dropped"] == 0
    assert steady["queue_high_water"] <= 1
    burst = simulate([10] * 100, capacity=16, batch=4, budget=4)
    assert burst["processed"] + burst["dropped"] == 1000
    assert burst["dropped"] > 0 and burst["queue_high_water"] <= 16
    print("PASS steady:", steady)
    print("PASS burst:", burst)

if __name__ == "__main__":
    main()
