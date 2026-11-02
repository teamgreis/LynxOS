#!/usr/bin/env python3
"""Deterministic resource-budget model for LynxOS research question F-001-D."""

from dataclasses import dataclass

@dataclass
class Task:
    name: str
    demand: int
    memory: int
    energy_per_unit: int
    weight: int
    deadline: int
    critical: bool = False
    completed: int = 0
    completion_tick: int | None = None

    @property
    def remaining(self):
        return self.demand - self.completed

@dataclass
class Result:
    policy: str
    ticks: int
    energy_used: int
    tasks: list
    rejected: list

    @property
    def completed_work(self):
        return sum(t.completed for t in self.tasks)

    @property
    def deadline_misses(self):
        return sum(t.completion_tick is None or t.completion_tick > t.deadline
                   for t in self.tasks)

CPU_PER_TICK = 2
MEMORY_CAPACITY = 16
ENERGY_BUDGET = 22
MAX_TICKS = 30

def workload():
    return [
        Task("critical-control", 5, 2, 1, 3, 5, True),
        Task("interactive", 8, 4, 1, 2, 8),
        Task("batch", 12, 8, 2, 1, 12),
    ]

def admit(tasks):
    accepted, rejected, used = [], [], 0
    for task in tasks:
        if used + task.memory <= MEMORY_CAPACITY:
            accepted.append(task)
            used += task.memory
        else:
            rejected.append(task.name)
    return accepted, rejected

def best_effort(active, capacity):
    result, left = {}, capacity
    for task in active:
        amount = min(1, task.remaining, left)
        if amount:
            result[task.name] = amount
            left -= amount
        if not left:
            break
    return result

def weighted_fair(active, capacity):
    result = {t.name: 0 for t in active}
    left = capacity
    while left:
        progressed = False
        for task in active:
            for _ in range(task.weight):
                if not left:
                    break
                if result[task.name] < task.remaining:
                    result[task.name] += 1
                    left -= 1
                    progressed = True
        if not progressed:
            break
    return result

def protected_reservation(active, capacity):
    result = {t.name: 0 for t in active}
    left = capacity
    critical = next((t for t in active if t.critical), None)
    if critical is not None and left:
        result[critical.name] = 1
        left -= 1
    others = [t for t in active if t is not critical]
    result.update(weighted_fair(others, left))
    return result

POLICIES = {
    "best-effort": best_effort,
    "weighted-fair": weighted_fair,
    "protected-reservation": protected_reservation,
}

def simulate(name):
    tasks, rejected = admit(workload())
    energy, tick = 0, 0
    allocator = POLICIES[name]
    while tick < MAX_TICKS and any(t.remaining for t in tasks):
        tick += 1
        active = [t for t in tasks if t.remaining]
        proposed = allocator(active, CPU_PER_TICK)
        # Explicit deterministic order: workload order consumes final energy.
        for task in active:
            for _ in range(proposed.get(task.name, 0)):
                if energy + task.energy_per_unit > ENERGY_BUDGET:
                    break
                task.completed += 1
                energy += task.energy_per_unit
                if task.remaining == 0:
                    task.completion_tick = tick
        if energy >= ENERGY_BUDGET:
            break
    return Result(name, tick, energy, tasks, rejected)

def main():
    print("F-001-D resource budget model")
    print(f"CPU/tick={CPU_PER_TICK}, memory={MEMORY_CAPACITY}, energy={ENERGY_BUDGET}")
    for name in POLICIES:
        r = simulate(name)
        print(f"\n[{r.policy}] completed={r.completed_work} energy={r.energy_used} "
              f"deadline_misses={r.deadline_misses} ticks={r.ticks}")
        print("rejected=" + (",".join(r.rejected) or "-"))
        for t in r.tasks:
            done = str(t.completion_tick) if t.completion_tick is not None else "incomplete"
            print(f"  {t.name}: {t.completed}/{t.demand}, completion={done}, deadline={t.deadline}")

if __name__ == "__main__":
    main()
