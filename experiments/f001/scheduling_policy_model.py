#!/usr/bin/env python3
"""Toy deterministic CPU service allocator: round robin, weighted, fixed priority."""
TASKS = [
    {"name": "interactive", "demand": 12, "weight": 3, "priority": 3, "deadline": 8},
    {"name": "system",      "demand": 10, "weight": 2, "priority": 2, "deadline": 15},
    {"name": "batch",       "demand": 20, "weight": 1, "priority": 1, "deadline": 40},
]

def run(policy, horizon=30):
    remaining = {t["name"]: t["demand"] for t in TASKS}
    service = {t["name"]: 0 for t in TASKS}
    finish = {}
    order = []
    rr = 0
    for tick in range(horizon):
        runnable = [t for t in TASKS if remaining[t["name"]] > 0]
        if not runnable:
            break
        if policy == "priority":
            chosen = max(runnable, key=lambda t: (t["priority"], -TASKS.index(t)))
        elif policy == "weighted":
            chosen = max(runnable, key=lambda t: (t["weight"] / (service[t["name"]] + 1), -TASKS.index(t)))
        else:
            chosen = runnable[rr % len(runnable)]
            rr += 1
        name = chosen["name"]
        remaining[name] -= 1
        service[name] += 1
        order.append(name)
        if remaining[name] == 0:
            finish[name] = tick + 1
    misses = sum(1 for t in TASKS if t["name"] in finish and finish[t["name"]] > t["deadline"])
    return {"service": service, "finish": finish, "deadline_misses": misses,
            "unfinished": sum(remaining.values()), "order": order}

def main():
    results = {p: run(p) for p in ("round_robin", "weighted", "priority")}
    assert all(sum(v["service"].values()) <= 30 for v in results.values())
    assert all(v["unfinished"] >= 0 for v in results.values())
    # Fixed priority favors higher classes; lower priority receives less service.
    assert results["priority"]["service"]["batch"] < results["priority"]["service"]["system"]
    assert results["priority"]["service"]["system"] < results["priority"]["service"]["interactive"]
    assert results["round_robin"]["service"]["interactive"] > 0
    for name, result in results.items():
        print(name, result["service"], "misses=", result["deadline_misses"],
              "unfinished=", result["unfinished"])

if __name__ == "__main__":
    main()
