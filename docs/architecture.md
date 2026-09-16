# Architecture

## Purpose

RelayWorld is the environment-side experimental runtime of the Relay family. It exists to make interactions with external or simulated worlds reproducible and evidence-grounded without absorbing self/cognition semantics.

## Primary boundary

A representative coupling is:

```text
WORLD / fixture authority
  -> Observation
  -> Self / Cognition
  -> Action Proposal
  -> Authorization
  -> environment/body execution
  -> Consequence
  -> Observation / Evidence
```

RelayWorld does not require RelaySelf. RelaySelf is one possible self-side implementation; stateless agents, transcript-only agents, scripted policies, or future cognition systems may connect through compatible boundaries.

## Current executable boundaries

RelayWorld currently owns two narrow executable environment-side boundaries.

[`WORLD Fact Snapshot → Observation`](contracts/world-observation.md):

```text
WorldFactSnapshot
  -- deterministic projection --> Observation
```

[`Experiment Intervention → synthetic WORLD transition`](contracts/experiment-intervention.md):

```text
SyntheticFactWorld current snapshot
  + ExperimentIntervention
  -> InterventionTransition(before, after)
```

The second boundary is deliberately a one-fact deterministic fixture, not a general mutable WORLD runtime or adapter abstraction. It preserves experiment-authority provenance separately from WORLD authority and can feed its resulting snapshot into the existing Observation boundary.

## Ownership

RelayWorld currently owns those narrow snapshot/Observation and synthetic Experiment Intervention semantics. Other environment-side responsibilities remain candidates until they become concrete, including:

- broader authoritative WORLD/fixture state exposure;
- environment/body execution boundaries for Actor Actions;
- general consequence attestation;
- scenario loading/validation when a concrete contract exists;
- experiment evidence capture and reproducibility metadata.

RelayWorld does not own:

- persistent cognition or subjective memory;
- belief/appraisal truth inside a cognition system;
- intent-selection semantics belonging to a self-side runtime;
- private scenario lore, cast, secrets, or unpublished experiment configuration;
- authorization policy merely because an action is executed through a RelayWorld adapter.

## Core invariants

```text
Self / Cognition != Environment
WORLD truth != Observation != Belief != Narration
Action Proposal != Authorization != Execution != Consequence
Experiment Intervention != Actor Action
Transport Origin != Semantic Authority
Scenario Semantics != Platform Semantics
```

These distinctions are architectural boundaries, not naming preferences.

## Grand Null

A bespoke script, simulator wrapper, or experiment-specific harness may be enough.

Do not create a general scheduler, adapter hierarchy, event bus, cognition framework, or evidence warehouse until a demonstrated cross-scenario responsibility requires one. Public platform structure should follow repeated real needs rather than predicted module names.
