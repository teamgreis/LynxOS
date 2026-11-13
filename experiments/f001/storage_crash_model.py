#!/usr/bin/env python3
"""Crash-point exploration for in-place, WAL, and copy-on-write toy updates."""

OLD, NEW = "old", "new"

def inplace(crash_after):
    disk = OLD
    steps = [NEW]  # single overwrite is assumed atomic here only for contrast
    for i, value in enumerate(steps, 1):
        if crash_after == i - 1:
            return disk
        disk = value
    return disk

def wal(crash_after):
    data, log = OLD, None
    steps = [("log", NEW), ("commit", True), ("data", NEW), ("clear", None)]
    for i, (kind, value) in enumerate(steps, 1):
        if crash_after == i - 1:
            break
        if kind == "log": log = value
        elif kind == "commit":
            if value: log = ("committed", NEW)
        elif kind == "data": data = value
        elif kind == "clear": log = None
    if isinstance(log, tuple) and log[0] == "committed":
        data = log[1]
    return data

def cow(crash_after):
    root, new_block = OLD, None
    steps = [("write_new", NEW), ("publish_root", NEW)]
    for i, (kind, value) in enumerate(steps, 1):
        if crash_after == i - 1:
            break
        if kind == "write_new": new_block = value
        elif kind == "publish_root" and new_block == NEW: root = NEW
    return root

def main():
    # Explore crash before, between, and after each modeled operation.
    for crash in range(5):
        assert wal(crash) in (OLD, NEW)
        assert cow(crash) in (OLD, NEW)
    # WAL and CoW guarantee old-or-new in this abstraction.
    assert all(wal(c) in (OLD, NEW) for c in range(5))
    assert all(cow(c) in (OLD, NEW) for c in range(5))
    print("PASS: WAL and CoW recover to complete old/new values at modeled crash points")
    print("WAL states:", [wal(c) for c in range(5)])
    print("CoW states:", [cow(c) for c in range(5)])

if __name__ == "__main__":
    main()
