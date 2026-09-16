# Continuous Integration

CI provides deterministic evidence for the exact commit checked by a job. It does not by itself prove simulation quality, model quality, external-environment behavior, or physical qualification.

## Current jobs

### `repository-contracts`

Runs `python tools/check_repository.py` to verify the canonical repository paths, repository-local Markdown links, and absence of unresolved merge-conflict markers in supported text files.

### `pytest`

Runs deterministic Python tests under Python 3.12.

Current tests prove package-surface discipline and two executable boundaries: WORLD-fact-snapshot → Observation, plus Experiment Intervention → deterministic single-fact synthetic WORLD transition. They cover fail-closed validation, authority-role separation, transition consistency, failure atomicity for rejected interventions, epoch progression, and immutable historical observations.

The suite also contains **scenario-local Grand Null probes** around the candidate Self–WORLD Embodiment Interface. Those probes deliberately define adapter/request/consequence/transport helpers inside test modules rather than promoting them into `relay_world`.

The synchronous probe checks whether existing Actor/Scenario/Observation semantics can compose with an externally supplied action identity for correlation, body reassignment, stale-observation detection, and pre-mutation rejection.

The lossy-transport probe distinguishes request loss before delivery from response loss after WORLD execution, demonstrates that blind retry can duplicate a non-idempotent effect, and tests whether adapter-local replay protection can reuse the existing external `action_id` as an idempotency key without inventing another platform identity.

These probes are architectural evidence only. They do not establish a platform Embodiment Interface, Actor Action lifecycle, generic Consequence contract, transport schema, replay service, durable idempotency guarantee, or supported adapter API.

Current tests do not prove a general mutable WORLD/runtime interface, production adapter, simulation quality, external integration, or exactly-once execution across process failure/restart.

### `lint`

Runs Ruff over `src`, `tests`, and `tools`.

## Exact-head rule

Pull-request jobs explicitly check out the PR head SHA and verify `git rev-parse HEAD` matches the expected transaction head. A new push makes prior exact-head results historical.

## Non-claims

A green CI run does not prove that:

- a general world runtime or world adapter exists or works;
- a generic Self–WORLD Embodiment Interface or transport protocol exists;
- adapter-local in-memory replay protection survives a crash or restart;
- a scenario is reproducible outside tested deterministic fixtures;
- a cognition system behaves well;
- Minecraft, Unreal, robotics, or other external integrations work;
- exploratory evidence is qualification evidence.
