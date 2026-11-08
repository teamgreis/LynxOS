#!/usr/bin/env python3
"""Small abstract crash-recovery model for LynxOS F-001-G.

This is a deterministic teaching/research model, not a simulation of a
particular filesystem, storage device, CPU cache, or persistence API.
"""

from copy import deepcopy
from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    counter: int
    label: str


OLD = State(0, "old")
NEW = State(1, "new")
ALLOWED = {OLD, NEW}


def unsafe_in_place() -> list[State]:
    """Independent field persistence can expose a torn mixed state."""
    return [
        OLD,                         # crash before either field is written
        State(1, "old"),             # counter persisted, label not persisted
        NEW,                         # both fields persisted
    ]


def copy_on_write() -> list[State]:
    """New object is durable before an atomic durable root switch."""
    return [
        OLD,                         # crash before writing new object
        OLD,                         # new object exists, root still points to old
        NEW,                         # root switch completed
    ]


def write_ahead_log() -> list[State]:
    """Recovery replays only after a complete durable commit record."""
    return [
        OLD,                         # no log record
        OLD,                         # incomplete/uncommitted record is ignored
        NEW,                         # committed record is durable; redo it
    ]


def check_recovery(name: str, outcomes: list[State]) -> None:
    invalid = [state for state in outcomes if state not in ALLOWED]
    if invalid:
        print(f"{name}: INVALID RECOVERY STATES: {invalid}")
    else:
        print(f"{name}: all crash points recover to an allowed state")


def main() -> None:
    scenarios = {
        "unsafe_in_place": unsafe_in_place(),
        "copy_on_write": copy_on_write(),
        "write_ahead_log": write_ahead_log(),
    }

    for name, outcomes in scenarios.items():
        check_recovery(name, outcomes)
        print("  outcomes:", " -> ".join(
            f"({state.counter}, {state.label})" for state in outcomes
        ))

    assert any(state not in ALLOWED for state in scenarios["unsafe_in_place"])
    assert all(state in ALLOWED for state in scenarios["copy_on_write"])
    assert all(state in ALLOWED for state in scenarios["write_ahead_log"])

    print("PASS: all model assertions satisfied")


if __name__ == "__main__":
    main()
