# Scheduling Policy Model

Run: `python3 scheduling_policy_model.py`

Compares three deterministic service-selection rules over the same finite workload: round robin, a simple weighted heuristic, and fixed priority. Reports CPU service, finish times, deadline misses, and unfinished demand. The assertions check that fixed priority favors higher-priority classes in this workload.

This is not a production scheduler, a mathematically fair weighted-fair-queueing implementation, a real-time schedulability proof, or a benchmark. It omits multicore placement, preemption costs, blocking, interrupts, priority inheritance, and energy.
