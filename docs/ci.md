# Continuous Integration

CI provides deterministic evidence for the exact commit checked by a job. It does not by itself prove simulation quality, model quality, external-environment behavior, or physical qualification.

## Current jobs

### `repository-contracts`

Runs `python tools/check_repository.py` to verify the canonical repository paths, repository-local Markdown links, and absence of unresolved merge-conflict markers in supported text files.

### `pytest`

Runs deterministic Python tests under Python 3.12.

Current tests prove package-surface discipline and the executable WORLD-fact-snapshot → Observation invariants: validation, deterministic projection, authority/producer separation, and immutable historical observations. They do not prove a mutable WORLD, adapter, simulation, or external integration.

### `lint`

Runs Ruff over `src`, `tests`, and `tools`.

## Exact-head rule

Pull-request jobs explicitly check out the PR head SHA and verify `git rev-parse HEAD` matches the expected transaction head. A new push makes prior exact-head results historical.

## Non-claims

A green CI run does not prove that:

- a mutable world runtime or world adapter exists or works;
- a scenario is reproducible outside tested deterministic fixtures;
- a cognition system behaves well;
- Minecraft, Unreal, robotics, or other external integrations work;
- exploratory evidence is qualification evidence.
