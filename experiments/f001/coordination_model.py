#!/usr/bin/env python3
"""Small quorum-intersection experiment for F-001-P.

Enumerates all voter subsets in a three-member configuration.
This is not a consensus implementation or a full protocol proof.
"""
from itertools import combinations

NODES = (0, 1, 2)

def subsets_of_size(nodes, size):
    return [frozenset(x) for x in combinations(nodes, size)]

def conflicting_quorums(nodes, threshold):
    quorums = subsets_of_size(nodes, threshold)
    pairs = []
    for i, left in enumerate(quorums):
        for right in quorums[i + 1:]:
            if left.isdisjoint(right):
                pairs.append((left, right))
    return quorums, pairs

def main():
    one_vote, one_conflicts = conflicting_quorums(NODES, 1)
    majority, majority_conflicts = conflicting_quorums(NODES, 2)

    assert len(one_vote) == 3
    assert len(one_conflicts) == 3
    assert len(majority) == 3
    assert majority_conflicts == []

    print("threshold 1 quorums:", [sorted(q) for q in one_vote])
    print("disjoint threshold-1 pairs:", len(one_conflicts))
    print("threshold 2 quorums:", [sorted(q) for q in majority])
    print("disjoint threshold-2 pairs:", len(majority_conflicts))
    print("PASS: all threshold-2 quorums intersect in this 3-node model")

if __name__ == "__main__":
    main()
