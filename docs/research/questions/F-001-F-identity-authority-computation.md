# F-001-F — Identity, Authority and Computation

**Status:** Exploratory research; no architecture decision
**Research program:** R0 — Computing foundations
**Parent:** [F-001 — What is a computer?](F-001-what-is-a-computer.md)

## Research question

What makes a computation the same logical entity across execution, migration, replication, restart, and recovery—and how should its authority be represented, granted, delegated, limited, and revoked?

Identity and authority are related but distinct. An identity answers which entity is being referred to. Authority answers which actions that entity is permitted to perform, on which objects, and under what conditions. Neither should be confused with the current execution instance, memory address, process identifier, host, or credential used to prove an identity.

## Concepts to keep separate

- **Logical identity:** a stable name for an entity within a defined namespace and lifecycle.
- **Execution instance:** a concrete incarnation currently performing work; it may start, stop, move, or be replaced.
- **Placement:** where an instance currently executes.
- **State continuity:** the rule determining whether a restarted or migrated instance continues the same logical computation.
- **Credential / proof:** evidence presented to convince another component of an identity claim.
- **Authority:** permission to perform a defined action on a defined object or class of objects.
- **Capability:** a possible representation of authority, commonly an unforgeable reference combined with permitted operations.
- **Delegation:** transferring or deriving a bounded subset of authority.
- **Revocation:** making previously granted authority unusable under a stated revocation model.
- **Provenance:** evidence about origin, derivation, execution history, or responsible authority.

An identifier is not proof. Proof of identity is not permission. Permission is not necessarily transferable when an execution instance moves.

## Candidate identity model

Represent a logical entity as `L`, an execution incarnation as `I`, placement as `P`, and a set of authority grants as `G`.

An execution relation may be written:

    executes(I, L, P, epoch)

This says that incarnation I is currently an execution of logical entity L at placement P under a particular epoch or generation. It does not imply that two incarnations are simultaneously equivalent, nor that they hold identical authority.

A grant can be described provisionally as:

    grant = (subject, object, actions, constraints, issuer, validity, generation)

Constraints may include time, resource bounds, location, purpose, delegation depth, or required proof strength. This tuple is a research aid, not a proposed wire format or kernel object.

## Identity continuity cases

| Event | Possible identity interpretation | Main question |
|---|---|---|
| Process restart | New incarnation, same logical entity | Which state and authority survive restart? |
| Migration | New placement, perhaps new incarnation | What must be transferred or re-established? |
| Replication | Multiple concurrent incarnations of one logical service | Are they one principal, several principals, or a group? |
| Clone / fork | Related but distinct logical entities or shared identity | Which identity and grants are inherited? |
| Recovery from checkpoint | Resumed entity with restored state | How are stale incarnations fenced off? |
| Credential rotation | Same entity, new proof material | How are old credentials invalidated safely? |

These cases must not be silently treated as equivalent.

## Competing authority models

| Model | Authorization basis | Potential strength | Limitation / research question |
|---|---|---|---|
| Identity + policy lookup | Named subject is checked against an external policy | Central policy visibility and straightforward revocation | Policy availability, lookup cost, identity spoofing if proof is weak |
| Object capabilities | Holder presents an unforgeable reference carrying specific authority | Least authority and explicit delegation | Revocation and capability discovery can be difficult |
| Hybrid | Identity establishes principal; capabilities or policy grant concrete actions | Combines auditability with fine-grained authority | More mechanisms and consistency rules |
| Ambient authority | Code inherits broad authority from its environment | Convenient legacy compatibility | Hidden dependencies and excessive privilege |
| Proof-carrying authorization | Request includes evidence checked against a policy or proof rule | Potentially portable, independently verifiable decisions | Proof complexity, freshness, revocation, and trusted roots |

No model is selected. Identity-based and capability-based approaches answer different questions and may be combined.

## Prior art

- **Dennis and Van Horn (1966), Programming Semantics for Multiprogrammed Computations:** foundational capability-system work. Capabilities combine designation of an object with authority to perform operations; the model is closely tied to controlled sharing and protection. [Bibliographic record](https://dl.acm.org/doi/10.1145/365230.365252).
- **seL4 capability model:** capability-based access control is central to seL4's kernel object model. The seL4 manual documents capability derivation, authority, and revocation mechanisms. [seL4 documentation](https://docs.sel4.systems/Tutorials/capabilities.html).
- **SPIFFE specifications:** define portable workload identity using SPIFFE IDs and cryptographically verifiable identity documents (SVIDs), with a workload API for retrieving identity material. This separates naming from the proof presented by a workload. [SPIFFE overview](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE.md), [SPIFFE ID specification](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE-ID.md).
- **SPIFFE Workload API:** supports identity material updates and streaming responses; its specification describes caller identification and the need for out-of-band authenticity checks at the local endpoint. [Workload API](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Workload_API.md).
- **Capability revocation:** capability systems face a known revocation challenge because a holder may possess a reference without a central list of all holders. Indirection and revocation structures are established approaches, each with trade-offs. [Overview](https://plus.tut.fi/comp.sec.100/fall-2025/m11_operating_systems/primitives/).

Prior art is substantial. LynxOS makes no novelty claim. The research question is how identity continuity and authority semantics should behave across the lifecycle events studied in F-001-C and F-001-E.

## Hypotheses

- **H-F1:** Logical identity should be distinguishable from a concrete execution incarnation and its placement.
- **H-F2:** A migration or restart should not silently imply either preservation or expansion of authority; the continuity rule must be explicit.
- **H-F3:** Identity proof and authorization are separate checks, even when one credential carries claims used by both.
- **H-F4:** Replication requires an explicit decision about whether replicas share a principal, hold distinct principals, or act under a group identity.
- **H-F5:** Revocation semantics must define scope, propagation, and behavior for disconnected or stale instances.
- **H-F6:** Delegation should be constrained by object, action, validity, and delegation depth, rather than implicitly copying all authority.

## Experiment plan

The accompanying small model contrasts two illustrative grant bindings across migration: a grant bound to a logical identity, and a grant bound to one execution incarnation. It also models revocation by generation change and checks whether a stale incarnation or stale grant remains accepted under each rule.

The experiment is deliberately abstract. It does not implement cryptography, a capability kernel, a distributed revocation protocol, or a secure identity provider. It is intended to make the semantic difference between stable logical identity and replaceable execution instance visible.

## Evaluation criteria

- Identity continuity across restart and migration.
- Prevention of stale-incarnation actions after fencing or revocation.
- Least-authority behavior under delegation.
- Revocation latency and behavior during disconnection.
- Correctness under concurrent replicas.
- Auditability and provenance without conflating identity with permission.
- Cost and availability of identity proof and authorization checks.

## Open questions

1. Is identity an immutable name, a lifecycle-scoped name, or a relation between state and authority?
2. When does a restart continue an entity, and when does it create a new one?
3. How are duplicate or concurrent incarnations fenced?
4. Can authority be location-independent without becoming transferable to an untrusted host?
5. How should authority be attenuated during delegation?
6. What revocation guarantees are possible during partitions?
7. How can provenance be verified without requiring a globally trusted central identity provider?
8. How should a system represent anonymous computation that needs limited authority but no durable identity?

## Research conclusion

A robust model should not identify a computation solely by its process ID, memory address, host, or current credential. It should define the relationship between logical identity, execution incarnation, placement, state continuity, and authority—and specify how that relationship changes under migration, replication, restart, and revocation.

**Decision status:** No identity namespace, credential format, capability representation, authorization model, delegation protocol, or revocation mechanism is selected.