# F-001-O — System Invariants and Correctness

**Status:** Research question; no architecture decision  
**Program:** R0 Computing foundations, with links to R1/R2/R11  
**Question:** Which properties must hold in every permitted system state and throughout every permitted execution?

## 1. Scope

An invariant is a property that holds in every reachable state under a stated transition model. This is narrower than saying a system is “correct”: correctness also depends on the specification, environment assumptions, progress requirements, and the observations considered relevant.

We distinguish:
- **State invariant:** predicate over one state (e.g. resource use never exceeds capacity).
- **Trace property:** predicate over an execution history (e.g. authority is never used after revocation).
- **Safety:** something bad never happens.
- **Liveness:** something good eventually happens, under explicit fairness/environment assumptions.
- **Refinement:** an implementation's observable behavior conforms to an abstract specification.

## 2. Formal starting point

Let a transition system be (T=(S,S_0,\rightarrow,Obs)). A state predicate (P) is invariant iff every state reachable from any initial state satisfies (P).

An inductive invariant candidate (I) requires:
1. **Initiation:** every initial state satisfies (I).
2. **Consecution:** if (I(s)) and (s\rightarrow s'), then (I(s')).
3. **Strength:** (I) implies the property being proved.

This proof pattern is powerful but may require strengthening the desired property with auxiliary facts. Finite-state exhaustive exploration can find counterexamples in the modeled state space; it does not prove that the model faithfully captures a real implementation.

## 3. Competing verification approaches

| Approach | Strength | Limitation / question |
|---|---|---|
| Testing and runtime assertions | Concrete, inexpensive feedback | Samples executions; absence of failure is not proof |
| Explicit-state model checking | Exhaustive for finite modeled state spaces; counterexample traces | State explosion; abstraction choices matter |
| Symbolic / SAT / SMT checking | Compact representations; arithmetic and data theories | Solver/model complexity; boundedness or theory limits |
| Inductive invariants and theorem proving | Can establish unbounded properties | Finding useful invariants and proof effort |
| Compositional assume-guarantee reasoning | Scales by component contracts | Assumptions must match at boundaries |
| Runtime monitoring | Checks actual executions | Detects violations, usually not all possible ones |

## 4. Questions and hypotheses

- **H-O1:** A small set of global invariants may expose failures invisible to local component checks.
- **H-O2:** Local invariants compose only when interfaces state sufficient assumptions and guarantees.
- **H-O3:** Safety and liveness require different evidence; a safety proof alone cannot establish progress.
- **H-O4:** State-space reduction can preserve selected properties, but every abstraction needs an explicit preservation argument.
- **H-O5:** Runtime monitoring and static proof are complementary rather than interchangeable.

## 5. Toy experiment

`invariant_model.py` explores a finite counter state space under two transition policies. The safe policy refuses an increment beyond capacity; the unsafe policy permits it. The checker enumerates reachable states and reports the first invariant violation.

This is a teaching model, not a proof about an OS, scheduler, memory manager, or hardware.

## 6. Open research questions

1. Which properties belong in global system contracts versus component contracts?
2. How should temporal, quantitative, security, and resource invariants be represented together?
3. What evidence is required to trust a refinement from abstract model to implementation?
4. How can invariants survive migration, reconfiguration, partial failure, and hardware variation?
5. Which properties are best proved, exhaustively explored, monitored, or tested?

## 7. Prior work

- Invariant checking and inductive invariants: [Verification modulo theories](https://doi.org/10.1007/s10703-023-00434-x).
- Model-checking foundations and temporal logic: [Stanford CS257 model-checking lecture](https://web.stanford.edu/class/cs257/slides/Lecture_5.pdf).
- Compositional reasoning and contracts are relevant adjacent areas; see the research questions F-001-L and F-001-M in this repository.

## 8. Decision status

**No decision.** This question establishes a vocabulary and experimental baseline. It does not select a verification architecture, proof assistant, model checker, or mandatory invariant set.
