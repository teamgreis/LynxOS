"""Toy model: artifact propagation across a three-stage bootstrap chain."""
def build(seed: str, source: str, stage: int) -> str:
    # Deterministic toy transformation standing in for a compiler stage.
    return f"artifact[{stage}]<{source}|{seed}>"

def bootstrap(seed: str, source: str):
    stage1 = build(seed, source, 1)
    stage2 = build(stage1, source, 2)
    stage3 = build(stage2, source, 3)
    return stage1, stage2, stage3

if __name__ == "__main__":
    a = bootstrap("seed-A", "compiler-source-v1")
    b = bootstrap("seed-B", "compiler-source-v1")
    assert len(a) == 3 and len(b) == 3
    assert a[0] != b[0]  # seed changes the first generated artifact
    assert a[1] != b[1]  # and propagates through this toy chain
    print("seed A stages:", a)
    print("seed B stages:", b)
    print("different seeds yield different modeled artifacts")
