#!/usr/bin/env python3
"""Finite-state illustration of crash/retry semantics for F-001-C.

No third-party dependencies. Run:
    python3 experiments/f001/failure_retry_model.py

The model contrasts:
  1. A durable effect followed by a volatile acknowledgement.
  2. An atomic internal commit of effect + durable request-id marker.

This is an intentionally tiny model, not a proof about real filesystems,
databases, hardware write ordering, networks, or arbitrary external effects.
"""

from collections import deque


def explore(initial, transitions):
    seen = {initial}
    queue = deque([initial])
    edges = []
    while queue:
        state = queue.popleft()
        for label, successor in transitions(state):
            edges.append((state, label, successor))
            if successor not in seen:
                seen.add(successor)
                queue.append(successor)
    return seen, edges


# Naive protocol state:
# (alive, phase, durable_effect_count, volatile_ack, retry_used)
# phase is idle or applied. A crash loses phase and ack, not durable effect.
def naive_transitions(s):
    alive, phase, effects, ack, retry = s
    out = []
    if alive and phase == "idle" and not ack:
        out.append(("apply-effect", (True, "applied", effects + 1, False, retry)))
    if alive and phase == "applied":
        out.append(("acknowledge", (True, "idle", effects, True, retry)))
    if alive and phase == "applied":
        out.append(("crash-before-ack", (False, "idle", effects, False, retry)))
    if not alive:
        out.append(("restart", (True, "idle", effects, False, retry)))
    if alive and phase == "idle" and not ack and not retry:
        out.append(("retry-request", (True, "idle", effects, False, True)))
    return out


# Atomic protocol state:
# (alive, committed_request, durable_effect_count, volatile_ack, retry_used)
# Commit atomically records both effect and request identity.
def atomic_transitions(s):
    alive, committed, effects, ack, retry = s
    out = []
    if alive and not committed and not ack:
        out.append(("atomic-commit-effect-and-id", (True, True, effects + 1, False, retry)))
    if alive and committed and not ack:
        out.append(("acknowledge-committed-request", (True, True, effects, True, retry)))
    if alive and committed and not ack:
        out.append(("crash-before-ack", (False, True, effects, False, retry)))
    if not alive:
        out.append(("restart", (True, committed, effects, False, retry)))
    if alive and committed and not ack and not retry:
        out.append(("retry-deduplicated-request", (True, True, effects, False, True)))
    return out


def main():
    naive_initial = (True, "idle", 0, False, False)
    atomic_initial = (True, False, 0, False, False)

    naive_states, naive_edges = explore(naive_initial, naive_transitions)
    atomic_states, atomic_edges = explore(atomic_initial, atomic_transitions)

    naive_terminal_effects = sorted({
        state[2] for state in naive_states if state[4] and state[3]
    })
    atomic_terminal_effects = sorted({
        state[2] for state in atomic_states if state[4] and state[3]
    })

    print("F-001-C crash/retry finite-state experiment")
    print()
    print("Naive protocol: durable effect, volatile acknowledgement")
    print(f"  reachable states: {len(naive_states)}")
    print(f"  transitions: {len(naive_edges)}")
    print(f"  effect counts after retry and acknowledgement: {naive_terminal_effects}")
    print()
    print("Atomic internal commit + durable request identity")
    print(f"  reachable states: {len(atomic_states)}")
    print(f"  transitions: {len(atomic_edges)}")
    print(f"  effect counts after retry and acknowledgement: {atomic_terminal_effects}")
    print()

    if 2 in naive_terminal_effects:
        print("PASS: naive retry exposes a duplicate-effect execution.")
    else:
        print("REVIEW: expected naive duplicate-effect path was not found.")

    if atomic_terminal_effects == [1]:
        print("PASS: atomic commit + deduplication avoids duplicate internal effect.")
    else:
        print("REVIEW: atomic protocol did not preserve exactly one internal effect.")


if __name__ == "__main__":
    main()
