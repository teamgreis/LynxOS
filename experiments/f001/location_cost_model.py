#!/usr/bin/env python3
"""Toy cost model for LynxOS F-001-E.

Compares moving data to computation, moving computation to data, and remote
invocation. Costs are abstract and deterministic; this is not a benchmark.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Scenario:
    data_bytes: int
    compute_units: int
    local_compute_cost_per_unit: float
    remote_compute_cost_per_unit: float
    bandwidth_bytes_per_cost_unit: float
    round_trip_cost: float
    migration_fixed_cost: float
    serialization_fixed_cost: float

@dataclass
class Outcome:
    strategy: str
    output: int
    estimated_cost: float
    bytes_transferred: int

def operation(value: int, compute_units: int) -> int:
    # Deterministic abstract workload. Location must not alter its result.
    result = value
    for _ in range(compute_units):
        result = (result * 3 + 7) % 1_000_003
    return result

def evaluate(s: Scenario, input_value: int) -> list[Outcome]:
    data_transfer = s.data_bytes / s.bandwidth_bytes_per_cost_unit
    local_compute = s.compute_units * s.local_compute_cost_per_unit
    remote_compute = s.compute_units * s.remote_compute_cost_per_unit

    # Strategy A: keep computation at its original location; transfer data.
    move_data = Outcome(
        "move-data-to-compute",
        operation(input_value, s.compute_units),
        data_transfer + local_compute + s.serialization_fixed_cost,
        s.data_bytes,
    )

    # Strategy B: move the computation to where the data already resides.
    move_compute = Outcome(
        "move-computation-to-data",
        operation(input_value, s.compute_units),
        s.migration_fixed_cost + remote_compute + s.serialization_fixed_cost,
        0,
    )

    # Strategy C: remote request/response; fixed request/response payload
    # is represented by the serialization term, not by the full data object.
    remote_call = Outcome(
        "remote-invocation",
        operation(input_value, s.compute_units),
        s.round_trip_cost + remote_compute + s.serialization_fixed_cost,
        128,
    )
    return [move_data, move_compute, remote_call]

def run_case(name: str, scenario: Scenario) -> None:
    results = evaluate(scenario, input_value=42)
    outputs = {item.output for item in results}
    print(f"\n[{name}]")
    print(f"semantic_outputs_equal={len(outputs) == 1}")
    for item in results:
        print(
            f"{item.strategy}: output={item.output}, "
            f"estimated_cost={item.estimated_cost:.3f}, "
            f"bytes_transferred={item.bytes_transferred}"
        )

def main() -> None:
    print("F-001-E location cost model (abstract units)")
    run_case(
        "large-data / modest-computation",
        Scenario(10_000_000, 10, 1.0, 1.2, 1_000_000, 2.0, 1.0, 0.2),
    )
    run_case(
        "small-data / expensive-computation",
        Scenario(10_000, 10_000, 1.0, 1.2, 1_000_000, 2.0, 1.0, 0.2),
    )

if __name__ == "__main__":
    main()
