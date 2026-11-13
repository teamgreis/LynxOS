#!/usr/bin/env python3
"""Deterministic toy model for bounded interrupt work and deferred event handling."""
from collections import deque

def simulate(events, capacity, batch, budget):
    queue = deque()
    processed = dropped = irq_work = batches = high_water = 0
    for event in events:
        # Interrupt top half: constant bounded work, enqueue or account a drop.
        irq_work += 1
        if len(queue) < capacity:
            queue.append(event)
            high_water = max(high_water, len(queue))
        else:
            dropped += 1
        # Deferred context: bounded batch and per-source service budget.
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
    events = list(range(1000))
    r = simulate(events, capacity=64, batch=8, budget=8)
    assert r["processed"] == 1000
    assert r["dropped"] == 0
    assert r["irq_work"] == 1000
    assert r["queue_high_water"] <= 1
    # A deliberately constrained consumer must drop rather than grow unbounded.
    overloaded = simulate(events, capacity=4, batch=1, budget=1)
    assert overloaded["processed"] + overloaded["dropped"] == 1000
    assert overloaded["queue_high_water"] <= 4
    print("PASS:", r)
    print("PASS overload:", overloaded)

if __name__ == "__main__":
    main()
