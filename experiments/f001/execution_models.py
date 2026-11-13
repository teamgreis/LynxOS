#!/usr/bin/env python3
"""Compare abstract execution traces for one dependency graph (F-001-Q).

All three strategies compute the same DAG. This is semantic illustration,
not a runtime benchmark.
"""
from collections import deque

GRAPH = {
    "A": (),
    "B": (),
    "C": ("A", "B"),
    "D": ("C",),
}
VALUE = {"A": 2, "B": 3}
def compute(node, values):
    if node in VALUE:
        return VALUE[node]
    if node == "C":
        return values["A"] + values["B"]
    if node == "D":
        return values["C"] * 2
    raise ValueError(node)

def sequential():
    values, trace = {}, []
    for node in ("A", "B", "C", "D"):
        values[node] = compute(node, values)
        trace.append(node)
    return values, trace

def event_queue():
    values, trace = {}, []
    ready = deque(["A", "B"])
    while ready:
        node = ready.popleft()
        values[node] = compute(node, values)
        trace.append(node)
        if node == "B" and "A" in values and "B" in values:
            ready.append("C")
        if node == "C":
            ready.append("D")
    return values, trace

def dataflow():
    values, trace = {}, []
    pending = set(GRAPH)
    while pending:
        ready = sorted(n for n in pending if all(dep in values for dep in GRAPH[n]))
        if not ready:
            raise RuntimeError("dependency cycle or blocked graph")
        for node in ready:
            values[node] = compute(node, values)
            trace.append(node)
            pending.remove(node)
    return values, trace

def main():
    results = {
        "sequential": sequential(),
        "event-queue": event_queue(),
        "dataflow": dataflow(),
    }
    for name, (values, trace) in results.items():
        assert values["D"] == 10
        print(f"{name:12} result={values['D']} trace={trace}")
    assert len({result[0]["D"] for result in results.values()}) == 1
    print("PASS: all abstract strategies preserve this workload's result")

if __name__ == "__main__":
    main()
