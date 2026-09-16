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
  -> Actor / Material Body execution
  -> Consequence
  -> Observation / Evidence
```

RelayWorld does not require RelaySelf. RelaySelf is one possible self-side implementation; stateless agents, transcript-only agents, scripted policies, humans, or future cognition systems may connect through compatible boundaries.

An external runtime may preserve a separate issuance/handoff state before WORLD-side execution. RelayWorld does not collapse that handoff into successful execution.

## Foundational Actor / Material Body semantics

RelayWorld distinguishes the WORLD-side execution role from the causal body substrate:

```text
external controller / cognition
        |
        | request / control
        v
Actor
        |
        | concrete Scenario binding
        v
Material Body
        |
        v
Material World / WORLD dynamics
```

`Actor` is a WORLD-side execution and attribution role. It does not imply cognition, intent, authorization policy, or successful execution.

`Material Body` is WORLD state representing the external causal body, avatar, device, or other embodied substrate through which an Actor may affect or sense the WORLD. Material Body is therefore part of the external causal domain, not a cognition system's self-image or body estimate.

The distinction is semantic, not yet executable platform machinery:

```text
Actor != Self / Cognition
Actor != Material Body
Actor != Actor Action
Material Body State != Observation != Belief / Appraisal
```

Concrete Actor identities, Material Body identities, and Actor-to-Body bindings are Scenario/configuration responsibility today. RelayWorld has no global Actor registry, body registry, controller-binding service, or body-control protocol.

This lets a concrete scenario represent cases such as the same external controller operating a different body, or a body being reassigned to a different controller, without rewriting body state into cognition or inventing a platform-wide identity system.

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

No executable Actor, Material Body, Actor-to-Body binding, or Actor Action execution contract exists yet.

## Ownership

RelayWorld currently owns:

- the narrow executable WORLD-fact-snapshot → Observation semantics;
- the narrow executable synthetic Experiment Intervention semantics;
- foundational environment-side semantic distinctions for Actor and Material Body.

Other environment-side responsibilities remain candidates until they become concrete, including:

- broader authoritative WORLD/fixture state exposure;
- executable Actor/Material-Body action execution boundaries;
- general consequence attestation;
- scenario loading/validation when a concrete contract exists;
- experiment evidence capture and reproducibility metadata.

RelayWorld does not own:

- persistent cognition or subjective memory;
- self-image, body-image, or subjective body model inside a cognition system;
- belief/appraisal truth inside a cognition system;
- intent-selection semantics belonging to a self-side runtime;
- action authorization policy merely because an action is executed through a RelayWorld boundary;
- private scenario lore, cast, secrets, or unpublished experiment configuration.

## Core invariants

```text
Self / Cognition != Environment
Actor != Self / Cognition
Actor != Material Body != Actor Action
WORLD truth != Observation != Belief != Narration
Action Proposal != Authorization != Execution != Consequence
Experiment Intervention != Actor Action
Transport Origin != Semantic Authority
Scenario Semantics != Platform Semantics
```

These distinctions are architectural boundaries, not naming preferences.

## Grand Null

A bespoke script, simulator wrapper, or experiment-specific harness may be enough.

Do not create a general Actor runtime, body runtime, controller-binding protocol, scheduler, adapter hierarchy, event bus, cognition framework, or evidence warehouse until a demonstrated cross-scenario responsibility requires one. Public platform structure should follow repeated real needs rather than predicted module names.
