#!/usr/bin/env python3
"""F-001-N: compare partial mutation with staged validated reconfiguration."""


def invariant(state):
    return state["schema"] == 2 and "name" in state and "active" in state


def unsafe_update(old):
    # Mutates live state before all fields have been prepared.
    state = dict(old)
    state["schema"] = 2
    # Simulated interruption here leaves old shape with new schema marker.
    return state


def staged_update(old):
    # Prepare separately; validate before making candidate active.
    candidate = dict(old)
    candidate["schema"] = 2
    candidate["active"] = candidate.pop("enabled")
    if not invariant(candidate):
        raise ValueError("candidate violates invariant")
    return candidate


def main():
    old = {"schema": 1, "name": "service", "enabled": True}
    interrupted = unsafe_update(old)
    upgraded = staged_update(old)

    assert not invariant(interrupted)
    assert invariant(upgraded)
    assert old["schema"] == 1  # original remains unchanged during preparation

    print(f"unsafe interrupted state valid: {invariant(interrupted)}")
    print(f"staged candidate valid: {invariant(upgraded)}")
    print("original state preserved during preparation: True")
    print("PASS: reconfiguration assertions satisfied")


if __name__ == "__main__":
    main()
