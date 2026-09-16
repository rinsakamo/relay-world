# Ontology

This document defines the small environment-side vocabulary currently needed by RelayWorld. Terms are semantic roles, not promises that a concrete implementation already exists.

## Environment / WORLD

The external state and dynamics being interacted with or studied.

RelayWorld may host, wrap, or observe a WORLD, but a concrete authority contract must identify which source is permitted to attest which state. `authoritative` means authorized for that claim, not omniscient or error-free.

## World State

State attributed to the WORLD by an authorized source.

World State is not automatically visible to an actor. Hidden or privileged fixture state may exist without becoming an Observation.

## Actor

A WORLD-side execution and attribution role through which an external controller, cognition system, human, script, or other control source may participate in the WORLD.

An Actor is not itself evidence of cognition, intent, authorization, or successful execution. RelayWorld uses the role to keep environment-side action attribution distinct from whichever external system produced or authorized a request.

A concrete Scenario may associate an Actor with a Material Body execution path. The platform does not currently define a global Actor registry, controller-binding protocol, or Actor lifecycle.

## Material Body

WORLD state representing the external causal body, avatar, device, or other embodied substrate through which an Actor may affect and sense the WORLD.

`Material` here means that the body belongs to the external causal/world domain rather than to a cognition system's self-model. A Material Body may therefore be physical, simulated, game-based, robotic, or otherwise implemented by a concrete WORLD.

Material Body state may include facts such as pose, geometry, resources, available effectors, or sensor state when a concrete world defines them. Those facts remain WORLD state and are not automatically visible to the Actor or cognition system.

A Material Body is not the Actor role and is not the Self's representation of that body.

Core distinctions:

```text
Actor != Self / Cognition
Actor != Material Body
Actor != Actor Action
Material Body State != Observation about the Body
```

Concrete Actor identity, Body identity, and Actor-to-Body binding remain Scenario/configuration responsibility unless a reusable executable contract is later earned.

## Observation

A bounded projection or measurement exposed from WORLD state to an actor or cognition system.

An Observation records what was exposed or measured, with source/provenance and relevant temporal identity. It is not automatically a belief and does not prove what a model later says about it.

Body-scoped observations such as proprioceptive or interoceptive measurements do not require separate platform types merely because their source is a Material Body. A concrete scenario may distinguish them through fact identity, projection semantics, or future contracts when needed.

The current executable owner for deterministic WORLD-fact-snapshot projection is [`docs/contracts/world-observation.md`](contracts/world-observation.md).

## Actor Action

An attempted environment-affecting operation attributable to an Actor and, when embodied, a Material Body execution path.

The following roles remain distinct:

```text
proposal -> authorization -> execution -> consequence
```

Actor identity or Body binding does not imply that a proposal was authorized, executed, or successful. RelayWorld must not infer successful execution from narration alone.

## Experiment Intervention

A mutation or control operation performed by experiment authority rather than by the actor under evaluation.

Intervention provenance must remain distinguishable from Actor Action provenance so an experiment cannot accidentally credit the actor for fixture/operator behavior.

The current executable owner for deterministic single-fact synthetic interventions is [`docs/contracts/experiment-intervention.md`](contracts/experiment-intervention.md).

## Consequence

An environment-side result observed or attested after an attempted action or intervention.

A Consequence may represent success, failure, partial effect, timeout, unknown result, or another explicitly modeled closure state when a concrete contract requires it.

The current synthetic intervention contract records only a successful deterministic before/after transition. It does not yet define the general Consequence lifecycle or failure taxonomy.

## Evidence

Recorded material used to support an experimental or implementation claim.

Evidence must identify enough subject, provenance, timing/version, and condition information to support the claim being made. Transport metadata is not a substitute for semantic authority.

## Scenario

A configuration of world fixtures, actors/bodies, cognition systems, interventions, temporal protocol, budgets, evidence requirements, and evaluation rules.

A Scenario instantiates platform capabilities. Scenario-specific meaning does not automatically become RelayWorld platform semantics.
