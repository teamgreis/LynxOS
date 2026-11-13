#!/usr/bin/env python3
"""Run every checked-in F-001 experiment script with bounded execution time."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SCRIPTS = sorted(p for p in HERE.glob("*.py") if p.name != Path(__file__).name)
TIMEOUT_SECONDS = 30

def main() -> int:
    failures = []
    print(f"Repository: {ROOT}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Experiments: {len(SCRIPTS)}")
    for script in SCRIPTS:
        command = [sys.executable, str(script)]
        print(f"\n=== RUN {script.relative_to(ROOT)} ===")
        try:
            result = subprocess.run(
                command, cwd=ROOT, text=True, capture_output=True,
                timeout=TIMEOUT_SECONDS, check=False,
            )
        except subprocess.TimeoutExpired:
            print(f"FAIL: timeout after {TIMEOUT_SECONDS}s")
            failures.append((script.name, "timeout"))
            continue
        if result.stdout:
            print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
        if result.stderr:
            print("STDERR:")
            print(result.stderr, end="" if result.stderr.endswith("\n") else "\n")
        if result.returncode == 0:
            print("RESULT: PASS (process exit code 0)")
        else:
            print(f"RESULT: FAIL (exit code {result.returncode})")
            failures.append((script.name, f"exit {result.returncode}"))
    print("\n=== SUMMARY ===")
    print(f"Passed: {len(SCRIPTS) - len(failures)}/{len(SCRIPTS)}")
    if failures:
        for name, reason in failures:
            print(f"FAIL: {name}: {reason}")
        return 1
    print("All experiment scripts exited successfully.")
    print("This checks executable sanity only; it does not prove model validity or OS guarantees.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
