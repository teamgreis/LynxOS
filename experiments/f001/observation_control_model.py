#!/usr/bin/env python3
"""F-001-K: finite-state observability and controllability illustration."""


STATES = {(x, y) for x in (0, 1) for y in (0, 1)}


def partial_sensor(state):
    return state[0]


def full_sensor(state):
    return state


def partial_actuator(state):
    return (1 - state[0], state[1])


def full_actuators(state):
    x, y = state
    return [(1 - x, y), (x, 1 - y)]


def reachable_from(start, actuators):
    reached = {start}
    frontier = [start]
    while frontier:
        state = frontier.pop()
        for next_state in actuators(state):
            if next_state not in reached:
                reached.add(next_state)
                frontier.append(next_state)
    return reached


def main():
    # The partial sensor cannot distinguish states differing only in y.
    assert partial_sensor((0, 0)) == partial_sensor((0, 1))
    assert full_sensor((0, 0)) != full_sensor((0, 1))

    # A control input that flips only x cannot reach states with y=1 from (0,0).
    partial_reachable = reachable_from(
        (0, 0), lambda state: [partial_actuator(state)]
    )
    assert partial_reachable == {(0, 0), (1, 0)}

    # Two independent actuators can reach every state in this finite model.
    full_reachable = reachable_from((0, 0), full_actuators)
    assert full_reachable == STATES

    print(f"states in model: {len(STATES)}")
    print(f"states reachable with partial actuator: {len(partial_reachable)}")
    print(f"states reachable with both actuators: {len(full_reachable)}")
    print("partial sensor cannot distinguish (0,0) from (0,1)")
    print("PASS: observation and control assertions satisfied")


if __name__ == "__main__":
    main()
