# Continuous Integration

CI provides deterministic evidence for the exact commit checked by a job. It does not by itself prove simulation quality, model quality, external-environment behavior, or physical qualification.

## Current jobs

### `repository-contracts`

Runs `python tools/check_repository.py` to verify the canonical repository paths, repository-local Markdown links, and absence of unresolved merge-conflict markers in supported text files.

### `pytest`

Runs deterministic Python tests under Python 3.12.

Current tests prove package-surface discipline and two executable boundaries: WORLD-fact-snapshot → Observation, plus Experiment Intervention → deterministic single-fact synthetic WORLD transition. They cover fail-closed validation, authority-role separation, transition consistency, failure atomicity for rejected interventions, epoch progression, and immutable historical observations.

The suite also contains a **scenario-local Grand Null probe** for the candidate Self–WORLD Embodiment Interface. That probe deliberately defines its adapter/request/consequence helpers inside the test module rather than promoting them into `relay_world`. It checks whether existing Actor/Scenario/Observation semantics can compose with an externally supplied action identity for correlation, body reassignment, stale-observation detection, and pre-mutation rejection.

The probe is architectural evidence only. It does not establish a platform Embodiment Interface, Actor Action lifecycle, generic Consequence contract, transport schema, or supported adapter API.

Current tests do not prove a general mutable WORLD/runtime interface, production adapter, simulation quality, or external integration.

### `lint`

Runs Ruff over `src`, `tests`, and `tools`.

## Exact-head rule

Pull-request jobs explicitly check out the PR head SHA and verify `git rev-parse HEAD` matches the expected transaction head. A new push makes prior exact-head results historical.

## Non-claims

A green CI run does not prove that:

- a general world runtime or world adapter exists or works;
- a generic Self–WORLD Embodiment Interface or transport protocol exists;
- a scenario is reproducible outside tested deterministic fixtures;
- a cognition system behaves well;
- Minecraft, Unreal, robotics, or other external integrations work;
- exploratory evidence is qualification evidence.
