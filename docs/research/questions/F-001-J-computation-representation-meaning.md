# F-001-J — Computation, Representation and Meaning

**Status:** Research question; open  
**Program:** R0 — Computing foundations  
**Parent:** [F-001 — What is a computer?](F-001-what-is-a-computer.md)  
**Related:** F-001 formal model; F-001-D resource-aware computation; F-001-G state continuity

## Research question

How can computational meaning be defined independently of a particular representation or execution mechanism, and under what conditions can different representations or implementations be considered equivalent?

This question concerns the relationship between abstract values, syntax, machine representations, execution steps, and observable behavior. It does not select a programming language, instruction set, compiler architecture, or runtime.

## 1. Representation layers

A computational idea can appear as:
- a mathematical value or specification;
- a symbolic expression or program;
- an abstract syntax tree;
- an intermediate representation;
- bytecode or machine instructions;
- encoded data in memory or storage;
- physical electrical or optical states.

Each layer introduces representation choices. A correct implementation must preserve the relevant meaning across transformations, within stated assumptions.

## 2. Syntax is not semantics

Syntax describes the structure of an expression. Semantics describes what that structure means.

For example, an expression tree for `3 * x + 2` is not the same thing as its source text, bytecode, or evaluated integer result. Those are different representations or stages.

A semantic model must define:
- values and their domains;
- operations and their behavior;
- evaluation order;
- state and side effects;
- errors and exceptional behavior;
- termination and divergence;
- nondeterminism and concurrency where applicable.

## 3. Major semantic approaches

| Approach | Core question | Typical use |
|---|---|---|
| Operational semantics | Which execution steps are permitted? | Machines, interpreters, concurrency |
| Denotational semantics | Which mathematical meaning is assigned? | Compositional reasoning |
| Axiomatic semantics | Which logical properties hold before and after execution? | Verification and program proofs |
| Algebraic semantics | Which equations characterize equivalent behavior? | Transformation and rewriting |
| Trace semantics | Which observable event sequences can occur? | Protocols and concurrency |
| Contextual equivalence | Can any allowed context distinguish two programs? | Compiler correctness and abstraction |

These approaches emphasize different properties and are not automatically interchangeable.

## 4. Equivalence is relative to observations

Two implementations may produce the same final integer while differing in:
- intermediate states;
- timing and resource consumption;
- memory use;
- I/O traces;
- exceptions;
- termination behavior;
- concurrency effects;
- security-relevant side channels.

Therefore, "equivalent" must name the observations being preserved. Value equivalence is weaker than trace equivalence; trace equivalence may still omit timing or resource behavior.

This is important for LynxOS: a compiler or runtime transformation should not be called semantics-preserving without a defined observation model.

## 5. Representation independence

A logical value may be represented in multiple ways. A compiler may lower an expression tree into stack bytecode; a runtime may represent a value as tagged words; a storage system may encode it into bytes.

The transformation is correct only relative to a relation between source and target states and a preservation claim. This is the broad concern behind compiler correctness and refinement.

A representation can also leak into observable behavior through overflow, floating-point rounding, pointer identity, alignment, timing, or undefined behavior. Abstraction boundaries must be explicit.

## 6. Nondeterminism and partiality

Not every computation produces one result:
- it may diverge;
- it may raise an error;
- it may produce multiple allowed outcomes;
- it may depend on environment or input;
- it may interact with concurrent events.

A semantic model that assumes every expression maps to one total mathematical function may be inadequate for operating-system behavior.

## 7. Hypotheses

- **H-J1:** Semantic equivalence is meaningful only relative to a specified set of observations.
- **H-J2:** A transformation can preserve final values while changing traces, resource use, or timing.
- **H-J3:** Operational, denotational, and axiomatic descriptions can provide complementary views of one computation.
- **H-J4:** Compiler correctness requires an explicit relation between source and target behavior.
- **H-J5:** Representation independence fails when representation details become observable through the chosen interface.
- **H-J6:** Models of system computation must account for errors, divergence, nondeterminism, and effects.

## 8. Minimal experiment

The accompanying experiment defines a tiny expression language with constants, variables, addition, and multiplication. It evaluates one expression using:
1. a recursive AST interpreter;
2. a compiler to stack bytecode and a bytecode evaluator.

Both are checked against the same result. This illustrates one narrow semantic-preservation test.

Run:

```sh
python3 experiments/f001/representation_semantics_model.py
```

The experiment is not a compiler correctness proof. It does not cover overflow, types, side effects, exceptions, optimization, concurrency, or arbitrary programs.

## 9. Prior art

- Peter Wegner, *Operational Semantics of Programming Languages* (1972): [DOI](https://doi.org/10.1145/942578.807081).
- *Formal Semantics of Programming Languages: An Overview* (2006): [DOI](https://doi.org/10.1016/j.entcs.2005.12.012).
- G. D. Plotkin, *A Structural Approach to Operational Semantics* (1981), with historical overview: [Origins of structural operational semantics](https://doi.org/10.1016/j.jlap.2004.03.009).
- Microsoft Research, *A Theory of Programming: Denotational, Algebraic and Operational Semantics*: [publication page](https://www.microsoft.com/en-us/research/publication/a-theory-of-programming-denotational-algebraic-and-operational-semantics/).
- Stanford Encyclopedia of Philosophy, *The Philosophy of Computer Science*: [semantics overview](https://plato.stanford.edu/archives/win2018/entries/computer-science/).

## 10. Open questions

1. Which observations define equivalence for system-level computation?
2. How should resource and timing effects enter semantic contracts?
3. What relation should connect a high-level operation to low-level execution?
4. How can nondeterminism and external effects be represented compositionally?
5. When is an abstract representation sufficiently independent of machine details?
6. How can semantics guide optimization without ruling out useful implementations?
7. What proof obligations are appropriate for compilers, interpreters, and runtime transformations?

## 11. Current conclusion

A computation's meaning is not identical to its syntax or physical representation. Equivalence depends on what observers are allowed to see. This makes explicit semantic contracts a prerequisite for meaningful claims about compiler correctness, portability, optimization, and abstraction.

**Research status:** Initial conceptual survey and small interpreter/bytecode comparison prepared; formal refinement proofs and richer language models remain open.
