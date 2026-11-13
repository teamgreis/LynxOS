"""Toy model: common hardware interface versus capability discovery."""
MACHINES = {
    "machine_alpha": {"timer", "dma", "iommu", "vector"},
    "machine_beta": {"timer", "dma"},
}
REQUIRED_COMMON = {"timer", "dma"}

def common_interface(machine):
    return REQUIRED_COMMON <= MACHINES[machine]

def discover(machine, requested):
    native = MACHINES[machine]
    return {feature: ("native" if feature in native else "fallback")
            for feature in requested}

if __name__ == "__main__":
    requested = {"timer", "dma", "iommu", "vector"}
    assert all(common_interface(m) for m in MACHINES)
    alpha = discover("machine_alpha", requested)
    beta = discover("machine_beta", requested)
    assert alpha["iommu"] == "native"
    assert beta["iommu"] == "fallback"
    assert beta["vector"] == "fallback"
    print("common interface supported by both:", sorted(REQUIRED_COMMON))
    print("alpha:", alpha)
    print("beta:", beta)
