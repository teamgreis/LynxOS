#!/usr/bin/env python3
"""Toy access-control model for private and explicitly shared memory regions."""

MAPS = {
    "alpha": {"private_A": {"read", "write"}, "shared_X": {"read", "write"}},
    "beta":  {"private_B": {"read", "write"}, "shared_X": {"read"}},
}

def allowed(domain, region, operation):
    return operation in MAPS.get(domain, {}).get(region, set())


def main():
    cases = [
        ("alpha", "private_A", "write", True),
        ("beta", "private_A", "read", False),
        ("beta", "private_B", "write", True),
        ("beta", "shared_X", "read", True),
        ("beta", "shared_X", "write", False),
        ("alpha", "shared_X", "write", True),
    ]
    for domain, region, op, expected in cases:
        actual = allowed(domain, region, op)
        assert actual == expected, (domain, region, op, actual, expected)
    print(f"PASS: {len(cases)} access checks; private isolation and shared permissions hold")

if __name__ == "__main__":
    main()
