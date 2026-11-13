#!/usr/bin/env python3
"""F-001-L: detect cycles in a small component wait-for graph."""


def has_cycle(graph):
    visiting = set()
    visited = set()

    def visit(node):
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for neighbor in graph.get(node, []):
            if visit(neighbor):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph)


def main():
    # A -> B -> C -> A: each dependency is locally simple, composition cycles.
    cyclic = {"A": ["B"], "B": ["C"], "C": ["A"]}
    acyclic = {"A": ["B"], "B": ["C"], "C": []}

    assert has_cycle(cyclic)
    assert not has_cycle(acyclic)

    print("cyclic composition detected: True")
    print("acyclic composition detected: False")
    print("PASS: composition graph assertions satisfied")


if __name__ == "__main__":
    main()
