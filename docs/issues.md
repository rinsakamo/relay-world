# Issue Governance

Issues are planning and remaining-work ledgers. They are not semantic authority or execution authority.

## Starting work

Before mutation, reacquire:

- current `main` and tree identity;
- current open Issues and PRs that may compete for the same responsibility;
- relevant current repository authority;
- live repository protection/check requirements when relevant.

Reconstruct the intended transaction from current reality. Do not execute an old Issue body, remembered SHA, or prior CI result as if it were current authority.

## Scope

One Issue should own one bounded responsibility where practical. Record explicit non-goals. If unrelated semantic expansion becomes necessary, split the work or redefine ownership.

## Pull requests

A PR should reference the Issue that owns its remaining-work question. Use auto-closing keywords only when the PR completes the entire current Issue scope; otherwise use a non-closing reference.

Before merge, inspect the exact final PR head, unresolved review threads, current base head/competing writers, and exact-head required checks.

## Reconciliation

After terminal completion, reconcile the Issue against current merged repository state. A merged PR does not automatically prove that all acceptance criteria were satisfied.

Record only verified implementation facts. Simulation, model-quality, or external qualification results require their own evidence.
