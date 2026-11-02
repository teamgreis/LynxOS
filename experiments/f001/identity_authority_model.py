#!/usr/bin/env python3
"""Illustrative identity/authority lifecycle model for LynxOS F-001-F.

No cryptography is implemented. The model contrasts grants bound to a stable
logical identity with grants bound to one execution incarnation.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Grant:
    subject: str
    action: str
    object_name: str
    generation: int

@dataclass
class Execution:
    logical_id: str
    instance_id: str
    placement: str
    generation: int

def authorize_identity_bound(grant: Grant, execution: Execution,
                             action: str, object_name: str,
                             current_generation: int) -> bool:
    return (
        grant.subject == execution.logical_id
        and grant.action == action
        and grant.object_name == object_name
        and grant.generation == current_generation
        and execution.generation == current_generation
    )

def authorize_instance_bound(grant: Grant, execution: Execution,
                             action: str, object_name: str,
                             current_generation: int) -> bool:
    return (
        grant.subject == execution.instance_id
        and grant.action == action
        and grant.object_name == object_name
        and grant.generation == current_generation
        and execution.generation == current_generation
    )

def main():
    logical = "computation:job-42"
    old = Execution(logical, "instance:7", "host-A", generation=1)
    migrated = Execution(logical, "instance:8", "host-B", generation=1)

    logical_grant = Grant(logical, "write", "object:report", generation=1)
    instance_grant = Grant(old.instance_id, "write", "object:report", generation=1)

    checks = [
        ("identity grant before migration",
         authorize_identity_bound(logical_grant, old, "write", "object:report", 1)),
        ("identity grant after migration",
         authorize_identity_bound(logical_grant, migrated, "write", "object:report", 1)),
        ("instance grant before migration",
         authorize_instance_bound(instance_grant, old, "write", "object:report", 1)),
        ("instance grant after migration",
         authorize_instance_bound(instance_grant, migrated, "write", "object:report", 1)),
        ("identity grant after revocation generation",
         authorize_identity_bound(logical_grant, migrated, "write", "object:report", 2)),
        ("stale old instance after generation change",
         authorize_identity_bound(logical_grant, old, "write", "object:report", 2)),
    ]

    print("F-001-F identity and authority model")
    for label, accepted in checks:
        print(f"{label}: {'ALLOW' if accepted else 'DENY'}")

    expected = [True, True, True, False, False, False]
    actual = [value for _, value in checks]
    assert actual == expected, f"Unexpected authorization results: {actual}"
    print("self_check: PASS")

if __name__ == "__main__":
    main()
