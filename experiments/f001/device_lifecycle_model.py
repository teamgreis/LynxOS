#!/usr/bin/env python3
"""Toy device lifecycle: discovery, matching, authorization, resources, activation."""

ORDER = ("discovered", "matched", "authorized", "resources_assigned", "active")

def attach(*, id_matches=True, authorized=True, resources_ok=True):
    state = "absent"
    state = "discovered"
    if not id_matches:
        return state, "rejected: no compatible driver"
    state = "matched"
    if not authorized:
        return state, "rejected: driver not authorized"
    state = "authorized"
    if not resources_ok:
        return state, "failed: resource assignment"
    state = "resources_assigned"
    state = "active"
    return state, "attached"


def main():
    assert attach() == ("active", "attached")
    assert attach(id_matches=False)[0] == "discovered"
    assert attach(authorized=False)[0] == "matched"
    assert attach(resources_ok=False)[0] == "authorized"
    print("PASS: only compatible, authorized devices with assigned resources become active")

if __name__ == "__main__":
    main()
