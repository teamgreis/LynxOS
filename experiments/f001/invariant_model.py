#!/usr/bin/env python3
"""Finite-state invariant exploration for F-001-O.

Compares a guarded counter transition with an unsafe transition.
The unsafe model is bounded at the first violating state so that the
counterexample is finite and exploration terminates.
"""
from collections import deque

CAPACITY = 3
INITIAL = 0

def explore(guarded: bool):
    queue = deque([INITIAL])
    seen = {INITIAL}
    parent = {INITIAL: None}
    violation = None

    while queue:
        state = queue.popleft()
        if state > CAPACITY:
            violation = state
            continue  # retain the first bad state; do not explore beyond it
        next_state = state + 1
        if guarded and next_state > CAPACITY:
            continue
        if next_state not in seen:
            seen.add(next_state)
            parent[next_state] = state
            queue.append(next_state)

    trace = []
    if violation is not None:
        cur = violation
        while cur is not None:
            trace.append(cur)
            cur = parent[cur]
        trace.reverse()
    return seen, violation, trace

def main():
    safe_states, safe_violation, _ = explore(guarded=True)
    unsafe_states, unsafe_violation, trace = explore(guarded=False)

    assert safe_violation is None
    assert safe_states == {0, 1, 2, 3}
    assert unsafe_violation == 4
    assert trace == [0, 1, 2, 3, 4]

    print("guarded policy:", sorted(safe_states), "invariant holds")
    print("unguarded policy:", sorted(unsafe_states), "counterexample:", trace)
    print("PASS: finite-state exploration behaved as specified")

if __name__ == "__main__":
    main()
