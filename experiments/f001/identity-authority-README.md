# F-001-F experiment — Identity and authority lifecycle

Run:

    python3 experiments/f001/identity_authority_model.py

The model compares two grant-subject choices:

- **Logical-identity-bound:** the grant names the logical computation, so a replacement execution instance may continue to use it if the generation remains current.
- **Instance-bound:** the grant names one concrete execution incarnation, so migration to a new instance does not automatically carry the grant.

A generation change represents a simple revocation/fencing event. Old grants and old execution generations are rejected.

## Expected self-check

    identity grant before migration: ALLOW
    identity grant after migration: ALLOW
    instance grant before migration: ALLOW
    instance grant after migration: DENY
    identity grant after revocation generation: DENY
    stale old instance after generation change: DENY
    self_check: PASS

## Limitations
- This is a semantic toy model, not an implementation of cryptographic identity or capability security.
- A generation integer stands in for a revocation/fencing authority; no distributed propagation protocol is modeled.
- It does not model concurrent replicas, partitions, key rotation, credential theft, delegation, or proof freshness.
- Logical-identity-bound authority is not automatically safe: migration must still prove that the new instance is entitled to act for the logical entity.
- Instance-bound authority is not automatically safer: it may prevent legitimate recovery and migration unless grants can be reissued securely.

The result illustrates a trade-off. It does not select either identity binding as the LynxOS design.