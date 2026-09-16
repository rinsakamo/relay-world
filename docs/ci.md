# Continuous Integration

CI provides deterministic evidence for the exact commit checked by a job. It does not by itself prove simulation quality, model quality, external-environment behavior, or physical qualification.

## Current jobs

### `repository-contracts`

Runs `python tools/check_repository.py` to verify the canonical bootstrap paths, repository-local Markdown links, and absence of unresolved merge-conflict markers in supported text files.

### `pytest`

Runs the deterministic Python bootstrap tests under Python 3.12.

The initial test proves only that the minimal `relay_world` package is importable and intentionally exposes no runtime API yet.

### `lint`

Runs Ruff over `src`, `tests`, and `tools`.

## Exact-head rule

Pull-request jobs explicitly check out the PR head SHA and verify `git rev-parse HEAD` matches the expected transaction head. A new push makes prior exact-head results historical.

## Non-claims

A green CI run does not prove that:

- a world adapter exists or works;
- a scenario is reproducible outside tested deterministic fixtures;
- a cognition system behaves well;
- Minecraft, Unreal, robotics, or other external integrations work;
- exploratory evidence is qualification evidence.
