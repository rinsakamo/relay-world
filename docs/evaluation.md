# Evaluation

RelayWorld separates deterministic platform correctness, simulation behavior, cognition/model quality, and external/physical qualification. These evidence classes answer different questions and must not be collapsed into one score.

## Evidence classes

### Deterministic invariant evidence

Used for properties that should hold independent of scenario luck or model capability, such as provenance separation, schema validation, lifecycle legality, fail-closed authority checks, and preservation of platform/scenario boundaries.

### Simulation evidence

Used for outcomes produced in simulated or replayable worlds. Results apply only to identified scenario configuration, seeds, world versions, policies/models, interventions, and evaluation horizon.

A scenario definition or planned run is not a simulation result.

### Model or system-quality evidence

Used for claims materially dependent on cognition/model quality, interpretation, planning, language behavior, memory, or end-to-end usefulness.

A correct RelayWorld invariant does not prove useful cognition, and fluent cognition does not prove world authority safety.

### External or physical qualification evidence

Used when claims depend on real hosts, services, networks, game servers, robots, devices, GPUs, or other external execution state.

Qualification must identify the actual subject and conditions being proven.

## Exploratory versus qualification evidence

Exploration and qualification are different evidence classes.

An exploratory run may discover mechanics, reveal defects, or teach a repeatable procedure. It must not be relabeled later as citable qualification evidence. A changed material condition requires a newly identified trial rather than silent promotion of an earlier rehearsal.

## Provenance requirements

Evidence should preserve enough information to distinguish:

- scenario/platform identity and version;
- WORLD/fixture authority;
- observation source;
- actor action versus experiment intervention;
- proposal/authorization/execution/consequence lineage when relevant;
- semantic authority versus transport channel;
- cognition/model/runtime identity when the claim depends on it;
- time/epoch/restart lineage when continuity matters.

Self-reported aggregate counts should be derived or cross-checked from underlying records when they support a claim.

## Counterexample-first review

Evaluation should actively search for falsifying cases such as stale observation, contradictory world state, self-authored fake observation, narrated success without consequence, provenance laundering, event/resource flood, restart ambiguity, partial action failure, world rollback, and external intervention.

## Grand Null and ablation

When claiming a platform mechanism adds value, compare against a smaller alternative where practical. A bespoke script, stateless agent, transcript-only agent, simpler adapter, or mechanism-removed configuration may be the appropriate null.

Do not attribute an improvement to a mechanism merely because the mechanism was present in a successful run.

## Reporting rule

Keep these statements distinct:

```text
Hypothesis:
  the mechanism should improve reproducibility.

Implementation fact:
  current validation rejects an invalid provenance transition.

Simulation result:
  identified runs under configuration X produced outcome Y.

External qualification:
  identified real environment Z satisfied claim C under recorded conditions.
```
