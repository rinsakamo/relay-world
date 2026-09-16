# WORLD Fact Snapshot → Observation Contract

## Status and ownership

This document is the current executable-contract owner for RelayWorld's first concrete environment-side boundary: deterministic projection of one authority-attributed WORLD fact snapshot into one Observation.

The semantic vocabulary remains defined by [`docs/ontology.md`](../ontology.md). This contract owns the narrower executable meaning and validation rules introduced with `src/relay_world/observation.py`.

## Meaning

```text
WorldFactSnapshot
  -- project_observation(producer_ref=...) --> Observation
```

The two records are distinct semantic types even when they carry overlapping fields.

A `WorldFactSnapshot` is state attributed to the WORLD by a named semantic authority at a named WORLD epoch. An `Observation` is an immutable record of what a named producer exposed from that snapshot.

This preserves semantic-role separation:

```text
WORLD truth != Observation
Observation != Belief
Observation != Narration
Semantic authority role != Observation producer role
Historical Observation != current WORLD truth
```

Here `!=` means that the roles must not be collapsed. It does not require their identifier strings to differ. One component may legitimately be both semantic authority and Observation producer when a concrete world/scenario assigns both roles to it.

## Fields

### `fact_ref`

Stable identity of the fact within the authority/scenario lineage. It must be a non-empty string.

The initial contract does not impose a global naming hierarchy.

### `value`

The observed fact value.

The initial executable contract deliberately accepts only `str`. This is a bounded first step, not a claim that all future WORLD values are strings. A general serialization/value schema must earn its own contract instead of being predicted here.

### `world_epoch`

Non-negative integer temporal identity supplied by the WORLD/fixture authority.

It is not a wall-clock timestamp and RelayWorld does not infer global ordering across unrelated authorities, resets, or scenario lineages. Comparing epochs as earlier/later is valid only when the surrounding authority/scenario contract establishes that relationship.

### `authority_ref`

Identity of the semantic authority permitted to attest the WORLD fact. It must be a non-empty string.

Authority means authorized for this claim; it does not imply omniscience or absence of sensor/implementation error.

### `producer_ref`

Identity of the component that produced/exposed the Observation. It must be a non-empty string.

`producer_ref` is not promoted into semantic authority. The producer and authority are distinct semantic roles, but their identifiers may be equal when one component legitimately holds both roles. Transport identity is not represented by this contract and must not be inferred from either field.

## Deterministic projection

`project_observation(snapshot, producer_ref=...)` copies `fact_ref`, `value`, `world_epoch`, and `authority_ref` exactly from the supplied `WorldFactSnapshot`, then records the explicit `producer_ref`.

The function does not read a clock, mutate WORLD state, perform transport, infer authority, consult cognition, or establish belief.

## Historical observations

An Observation is frozen after construction.

For example:

```text
snapshot 1: box.color = blue, epoch 1
observation 1: box.color = blue, epoch 1

snapshot 2: box.color = red, epoch 2
observation 2: box.color = red, epoch 2
```

Observation 1 remains valid evidence that blue/1 was exposed. It is not silently rewritten to red/2 and it is not, by itself, a claim about current WORLD truth.

## Validation

The contract fails closed for:

- non-string or empty/whitespace-only `fact_ref`;
- non-string or empty/whitespace-only `authority_ref`;
- non-string or empty/whitespace-only `producer_ref`;
- non-integer `world_epoch`, including `bool`;
- negative `world_epoch`;
- non-string `value` in this initial contract.

Validation does not prove that an authority was legitimately assigned. Assignment of authority belongs to a concrete scenario/world boundary.

## Grand Null

A plain dictionary and direct read may be enough for a one-off experiment. This contract is justified only by the recurring need to keep semantic authority, producer provenance, temporal identity, and historical/current claims explicit across worlds/scenarios.

## Non-goals

This contract does not define:

- mutable WORLD state;
- Experiment Intervention;
- Actor Action, authorization, execution, or consequence;
- adapters or transport;
- scheduling/background execution;
- evidence storage;
- belief, memory, appraisal, or narration;
- RelaySelf integration;
- scenario configuration;
- Minecraft, Unreal, robotics, or other external qualification.
