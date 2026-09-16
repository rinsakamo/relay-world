# Scenario Boundary

## Purpose

RelayWorld is a public reusable platform. Concrete scenario/configuration repositories may be public or private and must remain separate semantic owners for their own experiment-specific content.

## Platform responsibility

Promote a responsibility into RelayWorld only when it is reusable platform meaning, such as a stable observation contract, execution/consequence boundary, evidence rule, or adapter seam demonstrated by concrete scenarios.

RelayWorld may define reusable semantic roles such as Actor and Material Body while leaving every concrete identity and binding to a Scenario until a cross-scenario executable contract is actually justified.

A platform feature should not encode one scenario's lore, coordinates, cast, hidden interventions, secret values, or unpublished evaluation conditions.

## Scenario/configuration responsibility

A scenario may own:

- world fixture identity and version;
- concrete Actor identities;
- concrete Material Body identities and authoritative body/world facts;
- Actor-to-Body and controller-to-Actor bindings;
- cognition-system selection and configuration;
- observation projections;
- allowed actions and capabilities;
- experiment interventions;
- temporal protocol and budgets;
- private prompts/settings/secrets;
- evaluation conditions and unpublished results.

A concrete Actor-to-Body binding is therefore configuration/authority for that Scenario, not a global RelayWorld truth. The platform distinction `Actor != Material Body != Self / Cognition` does not create a repository-wide identity registry.

`Re-lay;World.` is one private scenario/configuration family. It is not required for RelayWorld to function and its private content is not public RelayWorld authority.

## Promotion rule

When a private or public scenario discovers a missing capability:

```text
scenario-specific need
  -> test whether the responsibility is genuinely reusable
  -> define the smallest public meaning/example
  -> add a RelayWorld owner only if the responsibility survives the Grand Null
```

Do not copy scenario configuration into the public platform simply because multiple files need access to it.
