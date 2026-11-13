# Device Lifecycle Model

Run: `python3 device_lifecycle_model.py`

The experiment separates discovery, driver matching, authorization, resource assignment, and activation. It checks that mismatches, unauthorized drivers, and resource failures cannot reach the active state.

It does not emulate PCI/USB enumeration, DMA, interrupts, IOMMU isolation, hotplug races, driver crashes, or actual hardware. Its state labels are intentionally simplified.
