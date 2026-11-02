# F-001-D experiment — Resource budget model

Run with Python 3.10 or later:

    python3 experiments/f001/resource_budget_model.py

## Policies
- **best-effort:** fixed task order, up to one work unit per task per tick.
- **weighted-fair:** deterministic weighted round-robin in one-unit quanta.
- **protected-reservation:** one CPU unit per tick goes to the critical task when active; remaining capacity is weighted-shared.

All policies use the same workload, memory admission, CPU capacity, and global energy budget.

## Assumptions and limitations
- CPU capacity is two abstract work units per tick.
- Memory is admitted statically before execution.
- Energy is a finite global budget; tasks have different energy costs per work unit.
- All tasks arrive at tick zero; no dynamic arrivals.
- No preemption cost, cache, memory bandwidth, I/O, multicore topology, or hardware measurements.
- Weighted sharing uses fixed weights and deterministic task order.
- The protected reservation is a simple per-tick preference, not a verified real-time reservation protocol.
- Energy enforcement follows task-list order; task order can determine who receives the final energy units.

This is an explanatory finite workload model, not a benchmark or proof that one policy is generally superior. Results apply only under these assumptions.

## Follow-up experiments
1. Sweep CPU and energy capacities.
2. Vary arrival times and burst sizes.
3. Add memory-bandwidth demand and contention.
4. Compare reservation admission and unused reserved capacity.
5. Add uncertain demand estimates and dynamic capacity.
6. Compare multiple fairness definitions.