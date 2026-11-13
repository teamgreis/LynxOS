#!/usr/bin/env python3
"""F-001-M: compare fault propagation with and without a containment boundary."""


def reachable(graph, start):
    seen = {start}
    pending = [start]
    while pending:
        node = pending.pop()
        for neighbor in graph.get(node, []):
            if neighbor not in seen:
                seen.add(neighbor)
                pending.append(neighbor)
    return seen


def main():
    uncontained = {
        "A": ["B"], "B": ["A", "C"], "C": ["B", "D"], "D": ["C"]
    }
    contained = {
        "A": ["B"], "B": ["A"], "C": ["D"], "D": ["C"]
    }

    spread_all = reachable(uncontained, "A")
    spread_contained = reachable(contained, "A")

    assert spread_all == {"A", "B", "C", "D"}
    assert spread_contained == {"A", "B"}

    print(f"fault spread without boundary: {len(spread_all)} nodes")
    print(f"fault spread with boundary: {len(spread_contained)} nodes")
    print("PASS: fault containment assertions satisfied")


if __name__ == "__main__":
    main()
