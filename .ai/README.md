# AI Development Authority

This directory defines repository-level guidance for AI-assisted RelayWorld development.

## Read order

Before making architectural or behavioral changes, read:

1. `README.md`
2. `docs/ontology.md`
3. `docs/architecture.md`
4. `docs/scenario-boundary.md`
5. `docs/development-principles.md`
6. `docs/evaluation.md`
7. `docs/ci.md`
8. `docs/issues.md`
9. relevant executable contracts when they are introduced

Do not create contract files, machine-readable authority, adapters, or runtime modules merely to anticipate future components. Introduce a narrower owner only when a real semantic responsibility and implementation/test consequence exists.

## Current executable contracts

- `docs/contracts/world-observation.md` owns the executable WORLD-fact-snapshot → Observation boundary.

## Authority rules

- RelayWorld owns environment-side claims only through explicit world/fixture authority.
- Keep world truth, observation, belief, appraisal, and narration separate.
- Keep action proposal, authorization, execution, and consequence separate.
- Keep experiment interventions separate from actor actions.
- Keep transport origin separate from semantic authority.
- Keep platform semantics separate from scenario/configuration semantics.
- Keep exploratory evidence separate from qualification evidence.
- Model output is not world authority by itself.
- Prefer one current owner for each semantic concept; avoid hand-maintained duplicate projections.
- Fix the canonical path rather than introducing compatibility residue, hidden fallback, or a second internal owner.
- Historical Issues, comments, earlier SHAs, and prior runs are evidence, not fresh authority.
- Issues are planning / remaining-work ledgers, not semantic or execution authority.

## Evidence discipline

Always distinguish:

1. **Hypothesis** — a design proposal or unverified explanation.
2. **Deterministic implementation evidence** — behavior confirmed by current code/tests for a stated invariant.
3. **Simulation result** — an outcome actually produced under identified configuration, seeds, versions, and horizon.
4. **Model/system-quality result** — behavior materially dependent on a cognition/model implementation.
5. **External or physical qualification** — evidence requiring real external hosts, devices, services, or worlds.

An exploratory rehearsal may teach mechanics but must not be retroactively presented as qualification evidence.

## Change discipline

For semantic changes, follow:

> **Meaning → Example → Test → Code → Docs / Authority → Audit**

Keep each transaction bounded. Resolve semantic ownership before adding state, adapters, fallbacks, or new authority surfaces. Review the exact final head and verify exact-head CI before merge when repository tooling supports it.

When work begins from an Issue, reconstruct the transaction from current authority, current `main`, and current competing work instead of executing the historical Issue body blindly.
