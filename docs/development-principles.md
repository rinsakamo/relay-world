# Development Principles

This document defines the default development discipline for RelayWorld.

## Governing sequence

For semantic changes:

> **Meaning → Example → Test → Code → Docs / Authority → Audit**

Meaning comes first. Tests freeze executable contracts when executable behavior exists. Code realizes the contract. Current authority converges with implementation. Final review inspects the exact resulting head rather than remembered intent.

## One bounded responsibility per transaction

Discovery may be broad; mutation should remain narrow. If a change requires unrelated semantic expansion, split or redefine the work instead of silently absorbing it.

## One concept, one current owner

A semantic concept should have one current canonical writer. File/module convenience does not create independent owners.

Introduce owner-local machine-readable authority only after a stable semantic boundary and deterministic validation need exists. Do not build an authority hierarchy in anticipation of future adapters.

## Preserve public/private ownership

RelayWorld public semantics must not absorb private scenario state. Scenario repositories configure or instantiate platform capabilities; they do not become platform authority by reference.

## Converge on the canonical path

Avoid by default:

- duplicate internal semantic owners;
- hidden fallback paths;
- compatibility aliases without a real external-contract need;
- dual-read/dual-write semantics for superseded meaning;
- test-only architecture that differs materially from production behavior;
- adapter layers created before a concrete external boundary exists.

Permanent adapters are valid at genuine external boundaries and must not become alternate world-truth owners by accident.

## Preserve authority boundaries

Implementation must preserve:

```text
WORLD truth != Observation != Belief != Narration
Proposal != Authorization != Execution != Consequence
Experiment Intervention != Actor Action
Transport Origin != Semantic Authority
```

Generated language cannot establish world mutation, action completion, or experiment provenance by itself.

## Fresh-head review and exact-head verification

Before merge, reacquire current `main`, competing writers, relevant authority, PR head, review state, and required checks. Review the exact final diff. A new push invalidates earlier exact-head review and CI claims.

Use expected-head merge protection when available.

## Stop conditions

Stop and reconstruct when semantic ownership is ambiguous, fresh authority cannot be obtained, a bounded transaction requires unrelated expansion, an unresolved counterexample invalidates the claim, or required exact-head verification fails/unavailable.

## Completion claims

Never claim more than evidence supports. Distinguish implementation facts, simulation/model results, external qualification, and hypotheses.
