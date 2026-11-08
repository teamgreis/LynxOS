#!/usr/bin/env python3
"""Deterministic temporal-semantics model for LynxOS F-001-H.

Illustrates (1) Lamport scalar timestamps versus vector-clock causality,
and (2) wall-clock steps versus monotonic elapsed time.

This is an abstract model, not a clock synchronization implementation.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    name: str
    process: str
    lamport: int
    vector: tuple[int, int]


def vector_leq(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return all(a <= b for a, b in zip(left, right))


def vector_lt(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return vector_leq(left, right) and left != right


def main() -> None:
    # A1 sends a message. B1 receives it. A2 is a separate local event on A.
    a1 = Event("A1-send", "A", 1, (1, 0))
    a2 = Event("A2-local", "A", 2, (2, 0))
    b1 = Event("B1-receive", "B", 2, (1, 1))

    assert a1.lamport < b1.lamport
    assert a1.lamport == b1.lamport - 1
    assert a2.lamport == b1.lamport
    assert vector_lt(a1.vector, b1.vector)
    assert not vector_lt(a2.vector, b1.vector)
    assert not vector_lt(b1.vector, a2.vector)

    print("Event clocks:")
    for event in (a1, a2, b1):
        print(
            f"  {event.name}: Lamport={event.lamport}, "
            f"vector={event.vector}"
        )
    print("A2 vs B1: equal Lamport values; vector clocks identify concurrency.")

    # A wall-clock correction steps civil time backwards by 30 seconds.
    wall_start = 1000.0
    wall_after_step = 970.0
    monotonic_start = 500.0
    monotonic_after = 510.0

    wall_elapsed = wall_after_step - wall_start
    monotonic_elapsed = monotonic_after - monotonic_start

    assert wall_elapsed == -30.0
    assert monotonic_elapsed == 10.0

    print(
        "Clock-step example: "
        f"wall elapsed={wall_elapsed:.1f}s, "
        f"monotonic elapsed={monotonic_elapsed:.1f}s"
    )
    print("PASS: all temporal model assertions satisfied")


if __name__ == "__main__":
    main()
