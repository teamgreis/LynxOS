#!/usr/bin/env python3
"""Tiny explicit-state experiment for F-001-B.

No third-party dependencies. Run with:
    python3 experiments/f001/concurrency_diamond.py

This is an illustrative finite-state model, not an OS scheduler or a proof
about hardware concurrency. It checks a state-dependent diamond condition.
"""

from collections import deque


def explore(initial, enabled, step):
    """Enumerate all reachable states and count enabled action-pairs."""
    seen = {initial}
    queue = deque([initial])
    tested_pairs = 0
    diamond_pairs = 0
    blocked_or_noncommuting_pairs = []

    while queue:
        state = queue.popleft()
        actions = enabled(state)

        for action in actions:
            successor = step(state, action)
            if successor is not None and successor not in seen:
                seen.add(successor)
                queue.append(successor)

        for index, left in enumerate(actions):
            for right in actions[index + 1:]:
                tested_pairs += 1
                after_left = step(state, left)
                after_right = step(state, right)

                left_then_right = (
                    None if after_left is None else step(after_left, right)
                )
                right_then_left = (
                    None if after_right is None else step(after_right, left)
                )

                if (
                    left_then_right is not None
                    and right_then_left is not None
                    and left_then_right == right_then_left
                ):
                    diamond_pairs += 1
                else:
                    blocked_or_noncommuting_pairs.append(
                        (state, left, right, left_then_right, right_then_left)
                    )

    return seen, tested_pairs, diamond_pairs, blocked_or_noncommuting_pairs


# Model A: two independent one-slot channels.
# State: (queue_a, queue_b, produced_a, consumed_a, produced_b, consumed_b)
def independent_enabled(state):
    qa, qb, pa, ca, pb, cb = state
    actions = []
    if not pa and qa == 0:
        actions.append("produce_a")
    if qa == 1 and not ca:
        actions.append("consume_a")
    if not pb and qb == 0:
        actions.append("produce_b")
    if qb == 1 and not cb:
        actions.append("consume_b")
    return actions


def independent_step(state, action):
    qa, qb, pa, ca, pb, cb = state
    values = {
        "produce_a": (1, qb, True, ca, pb, cb),
        "consume_a": (0, qb, pa, True, pb, cb),
        "produce_b": (qa, 1, pa, ca, True, cb),
        "consume_b": (qa, 0, pa, ca, pb, True),
    }
    if action not in independent_enabled(state):
        return None
    return values[action]


# Model B: two producers compete for one shared one-slot buffer.
# State: (slot_owner, produced_a, produced_b)
def shared_enabled(state):
    owner, produced_a, produced_b = state
    actions = []
    if owner is None and not produced_a:
        actions.append("produce_a")
    if owner is None and not produced_b:
        actions.append("produce_b")
    return actions


def shared_step(state, action):
    owner, produced_a, produced_b = state
    if action not in shared_enabled(state):
        return None
    if action == "produce_a":
        return ("a", True, produced_b)
    if action == "produce_b":
        return ("b", produced_a, True)
    return None


def main():
    independent = explore(
        (0, 0, False, False, False, False),
        independent_enabled,
        independent_step,
    )
    shared = explore(
        (None, False, False),
        shared_enabled,
        shared_step,
    )

    print("F-001-B explicit-state diamond experiment")
    print()
    print("Model A — independent bounded channels")
    print(f"  reachable states: {len(independent[0])}")
    print(f"  enabled action-pairs checked: {independent[1]}")
    print(f"  diamond pairs: {independent[2]}")
    print(f"  blocked/non-commuting pairs: {len(independent[3])}")
    print()
    print("Model B — producers competing for one shared slot")
    print(f"  reachable states: {len(shared[0])}")
    print(f"  enabled action-pairs checked: {shared[1]}")
    print(f"  diamond pairs: {shared[2]}")
    print(f"  blocked/non-commuting pairs: {len(shared[3])}")

    if not independent[3]:
        print()
        print("PASS: every simultaneously enabled pair in Model A forms a diamond.")
    else:
        print()
        print("REVIEW: Model A contains a non-diamond pair.")

    if shared[3]:
        print("PASS: Model B exposes a competing pair that is not independent.")
    else:
        print("REVIEW: Model B did not expose the expected shared-slot conflict.")


if __name__ == "__main__":
    main()
