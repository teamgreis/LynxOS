#!/usr/bin/env python3
"""Small abstract model of staged boot and recoverable activation.

This is a teaching model, not a firmware emulator or a security proof.
"""
from dataclasses import dataclass

STAGES = ("firmware", "loader", "kernel", "runtime", "operational")

@dataclass(frozen=True)
class BootState:
    stage: int
    verified: bool
    measured: bool
    active_generation: int
    recovery_available: bool
    failed: bool = False


def advance(state: BootState, *, verify_ok=True, measure=True):
    if state.failed or state.stage >= len(STAGES):
        return state
    # Each transition represents one stage handing off to the next.
    if not verify_ok:
        return BootState(state.stage, state.verified, state.measured,
                         state.active_generation, state.recovery_available, True)
    return BootState(state.stage + 1, state.verified and verify_ok,
                     state.measured or measure, state.active_generation,
                     state.recovery_available)


def activate_candidate(active, candidate, validation_ok):
    """Atomic generation switch: failed validation leaves active unchanged."""
    return candidate if validation_ok else active


def main():
    s = BootState(0, True, False, 7, True)
    for _ in STAGES:
        s = advance(s)
        assert not s.failed
    assert s.stage == len(STAGES)
    # A failed verification must stop progression.
    bad = advance(BootState(1, True, False, 7, True), verify_ok=False)
    assert bad.failed and bad.stage == 1
    # Candidate activation is all-or-nothing in this abstraction.
    assert activate_candidate(7, 8, False) == 7
    assert activate_candidate(7, 8, True) == 8
    print("PASS: staged handoff, verification stop, atomic activation")

if __name__ == "__main__":
    main()
