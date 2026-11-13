# Boot State Model

Run: `python3 boot_state_model.py`

The model checks a five-stage abstract boot progression, stops when verification fails, and models candidate-generation activation as an atomic choice.

It deliberately does not emulate UEFI, CPU reset behavior, cryptographic verification, TPM measurements, power loss, or actual boot recovery. The boolean verification and measurement flags are abstractions only.
