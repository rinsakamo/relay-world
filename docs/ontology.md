# Ontology

This document defines the small environment-side vocabulary currently needed by RelayWorld. Terms are semantic roles, not promises that a concrete implementation already exists.

## Environment / WORLD

The external state and dynamics being interacted with or studied.

RelayWorld may host, wrap, or observe a WORLD, but a concrete authority contract must identify which source is permitted to attest which state. `authoritative` means authorized for that claim, not omniscient or error-free.

## World State

State attributed to the WORLD by an authorized source.

World State is not automatically visible to an actor. Hidden or privileged fixture state may exist without becoming an Observation.

## Observation

A bounded projection or measurement exposed from WORLD state to an actor or cognition system.

An Observation records what was exposed or measured, with source/provenance and relevant temporal identity. It is not automatically a belief and does not prove what a model later says about it.

The current executable owner for deterministic WORLD-fact-snapshot projection is [`docs/contracts/world-observation.md`](contracts/world-observation.md).

## Actor Action

An attempted environment-affecting operation attributable to an actor/body execution path.

The following roles remain distinct:

```text
proposal -> authorization -> execution -> consequence
```

RelayWorld must not infer successful execution from narration alone.

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
