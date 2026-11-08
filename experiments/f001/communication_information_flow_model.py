#!/usr/bin/env python3
"""F-001-I: tiny deterministic model of delivery and information flow."""


def apply_without_dedup(deliveries):
    effects = []
    for request_id in deliveries:
        effects.append(request_id)
    return effects


def apply_with_dedup(deliveries):
    seen = set()
    effects = []
    for request_id in deliveries:
        if request_id not in seen:
            seen.add(request_id)
            effects.append(request_id)
    return effects


def public_observation(secret, public_value):
    # The modeled public channel deliberately does not depend on secret.
    return f"status={public_value}"


def main():
    deliveries = ["request-1", "request-1", "request-2"]
    naive = apply_without_dedup(deliveries)
    deduplicated = apply_with_dedup(deliveries)

    assert len(naive) == 3
    assert len(deduplicated) == 2
    assert deduplicated == ["request-1", "request-2"]

    public_a = public_observation("SECRET-A", "ready")
    public_b = public_observation("SECRET-B", "ready")
    assert public_a == public_b

    print(f"duplicate deliveries: {len(deliveries)}")
    print(f"effects without deduplication: {len(naive)}")
    print(f"effects with request-ID deduplication: {len(deduplicated)}")
    print("secret substitution leaves public observation unchanged")
    print("PASS: all communication model assertions satisfied")


if __name__ == "__main__":
    main()
