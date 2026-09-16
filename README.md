# RelayWorld

Experimental world runtime and environment laboratory for Relay.

RelayWorld is the environment-side experimental runtime of the Relay family. It provides public foundations for worlds, observations, external interventions, action execution consequences, and experimental evidence.

RelayWorld does **not** define the self. Self-side cognition may be provided by RelaySelf or by another cognition system through explicit boundaries.

## Core boundaries

```text
Self / Cognition != Environment
WORLD truth != Observation != Belief != Narration
Action Proposal != Authorization != Execution != Consequence
Experiment Intervention != Actor Action
Transport Origin != Semantic Authority
Exploratory Evidence != Qualification Evidence
Scenario Semantics != Platform Semantics
```

Authority is not infallibility. A concrete world source may be authoritative for a field while still carrying uncertainty, freshness limits, sensor error, or implementation defects.

## Public platform and private scenarios

This public repository owns reusable RelayWorld platform semantics and executable infrastructure only when those responsibilities become real.

Concrete worlds, private cast or character data, unpublished experiment conditions, secrets, fixtures, and scenario-specific configuration may live outside this repository. `Re-lay;World.` is one private scenario/configuration family; RelayWorld does not depend on it and must remain usable by independent public or private scenarios.

## Architecture and engineering documents

- [`docs/ontology.md`](docs/ontology.md) — canonical environment-side vocabulary.
- [`docs/architecture.md`](docs/architecture.md) — ownership and system boundaries.
- [`docs/scenario-boundary.md`](docs/scenario-boundary.md) — platform versus scenario/configuration responsibility.
- [`docs/development-principles.md`](docs/development-principles.md) — change, authority, review, and convergence discipline.
- [`docs/evaluation.md`](docs/evaluation.md) — evidence classes and falsification discipline.
- [`docs/ci.md`](docs/ci.md) — meaning and scope of CI guarantees.
- [`docs/issues.md`](docs/issues.md) — Issue scope, freshness, and completion rules.
- [`.ai/README.md`](.ai/README.md) — AI-assisted development authority and read order.

## Status

RelayWorld is in foundational bootstrap. The current repository does not yet claim a general world runtime, world-adapter interface, scheduler, cognition adapter, simulator, Minecraft integration, or physical-environment integration.

A bespoke experiment harness remains the Grand Null. RelayWorld must earn additional machinery through demonstrated reusable responsibilities such as reproducibility, adapter interchangeability, causal/evidence rigor, or cross-world comparability.

## License

Apache License 2.0.
