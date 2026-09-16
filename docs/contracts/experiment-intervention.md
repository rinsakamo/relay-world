# Experiment Intervention Contract

## Status and ownership

This document is the current executable-contract owner for RelayWorld's first concrete Experiment Intervention boundary: applying an explicitly attributed experiment intervention to a deterministic single-fact synthetic WORLD.

It composes with [`WORLD Fact Snapshot → Observation`](world-observation.md) but does not replace that contract. The semantic vocabulary remains defined by [`docs/ontology.md`](../ontology.md).

## Meaning

```text
SyntheticFactWorld current snapshot
  + ExperimentIntervention
  -> InterventionTransition(before, after)
  -> project_observation(after, ...)
```

The boundary preserves semantic-role separation:

```text
Experiment Intervention != Actor Action
Experiment authority role != WORLD authority role
WORLD mutation != narrated/model-reported mutation
Historical snapshot/Observation != current WORLD state
Transport Origin != Semantic Authority
```

Here `!=` means the roles must not be collapsed. Identifier strings may be equal only when a concrete scenario legitimately assigns multiple roles to one component; the contract never infers one role from another.

## `ExperimentIntervention`

An immutable instruction attributed to experiment authority with four fields:

- `intervention_ref` — non-empty identity of this intervention record;
- `experiment_authority_ref` — non-empty identity of the experiment authority responsible for the intervention;
- `fact_ref` — non-empty identity of the single WORLD fact being targeted;
- `value` — the value to set, limited to `str` by the current executable value contract.

`experiment_authority_ref` records provenance. This contract does not implement an ACL or prove that the named authority was legitimately assigned. Assignment belongs to a concrete scenario/world boundary.

The contract does not maintain a global uniqueness registry for `intervention_ref`.

## `SyntheticFactWorld`

`SyntheticFactWorld` is a deliberately narrow deterministic fixture, not a general WORLD runtime or adapter interface.

It owns exactly one current immutable `WorldFactSnapshot` for the lifetime of one Python object. The initial snapshot supplies:

- fact identity;
- current string value;
- WORLD epoch;
- WORLD semantic-authority identity.

The fixture makes no restart, persistence, multi-fact, wall-clock, transport, concurrency, or cross-instance lineage claim.

`snapshot()` returns the current immutable snapshot.

## Applying an intervention

`apply_intervention(intervention)` accepts only an `ExperimentIntervention` targeting the fixture's current `fact_ref`.

For a successful application:

1. `before` is the current `WorldFactSnapshot`;
2. `after.fact_ref` is exactly `before.fact_ref`;
3. `after.value` is exactly `intervention.value`;
4. `after.world_epoch` is exactly `before.world_epoch + 1`;
5. `after.authority_ref` is exactly `before.authority_ref`;
6. the fixture installs `after` as its new current snapshot;
7. an immutable `InterventionTransition(intervention, before, after)` is returned.

The experiment authority therefore does **not** become WORLD authority merely because it caused a mutation.

A successful intervention creates a new synthetic WORLD revision even when the assigned value equals the previous value. In this fixture, `world_epoch` identifies accepted revisions, not only content changes.

## Failure atomicity

A mismatched target `fact_ref`, invalid intervention type, or invalid intervention field fails closed before the fixture changes its current snapshot.

The fixture does not model partial mutation, timeout, retry, or unknown outcome. Those are future consequence/lifecycle questions and are outside this contract.

## `InterventionTransition`

An `InterventionTransition` is an immutable deterministic lineage record for one successful synthetic intervention.

Construction validates that:

- intervention, before, and after have the expected semantic types;
- intervention and both snapshots identify the same fact;
- the after value came from the intervention;
- WORLD authority is preserved from before to after;
- the after epoch is exactly one greater than the before epoch.

This prevents a transition record from laundering experiment authority into WORLD authority or presenting an inconsistent synthetic revision as valid deterministic evidence.

It does not prove that an external/physical world changed.

## Observation after intervention

The existing Observation contract is reused unchanged.

Example:

```text
before WORLD snapshot: box.color = blue, epoch 1, authority synthetic-world
historical Observation: blue / epoch 1

ExperimentIntervention:
  operator-change-1
  experiment authority experiment-operator
  set box.color = red

transition after WORLD snapshot: red, epoch 2, authority synthetic-world
current Observation: red / epoch 2
```

The historical Observation remains unchanged. The new Observation comes only from projecting the new WORLD snapshot; narration or model output cannot establish the mutation.

## Grand Null

A pure `WorldFactSnapshot -> WorldFactSnapshot` function is smaller, but it leaves current-WORLD ownership implicit and encourages generic code to mint a new authority-attributed snapshot without a concrete state owner.

A general mutable WORLD runtime is much larger than current evidence warrants.

`SyntheticFactWorld` is the surviving middle: one fact, one current snapshot, deterministic intervention application, no adapters, no scheduler, no event bus, and no general runtime interface.

## Evidence class

Tests for this contract are deterministic implementation evidence only. They establish current Python invariants for the synthetic fixture. They are not simulation-quality evidence and not external or physical qualification.

## Non-goals

This contract does not define:

- Actor Action, proposal, authorization, execution, or actor consequence;
- a general Consequence lifecycle or failure taxonomy;
- generic WORLD/runtime/adapter interfaces;
- multi-fact state;
- intervention ACL/policy;
- intervention history storage or an evidence warehouse;
- restart or persistence semantics;
- scheduling/background execution;
- transport/network provenance;
- belief, memory, appraisal, or narration;
- RelaySelf integration;
- scenario configuration;
- Minecraft, Unreal, robotics, or other external qualification.
