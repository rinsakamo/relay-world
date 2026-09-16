from dataclasses import FrozenInstanceError

import pytest

from relay_world import (
    ExperimentIntervention,
    InterventionTransition,
    SyntheticFactWorld,
    WorldFactSnapshot,
    project_observation,
)


def _initial_snapshot() -> WorldFactSnapshot:
    return WorldFactSnapshot(
        fact_ref="box.color",
        value="blue",
        world_epoch=1,
        authority_ref="synthetic-world",
    )


def _intervention(*, value: str = "red") -> ExperimentIntervention:
    return ExperimentIntervention(
        intervention_ref="operator-change-1",
        experiment_authority_ref="experiment-operator",
        fact_ref="box.color",
        value=value,
    )


def test_intervention_mutates_synthetic_world_and_preserves_authority_roles() -> None:
    world = SyntheticFactWorld(_initial_snapshot())

    transition = world.apply_intervention(_intervention())

    assert transition.before == WorldFactSnapshot(
        fact_ref="box.color",
        value="blue",
        world_epoch=1,
        authority_ref="synthetic-world",
    )
    assert transition.after == WorldFactSnapshot(
        fact_ref="box.color",
        value="red",
        world_epoch=2,
        authority_ref="synthetic-world",
    )
    assert transition.intervention.experiment_authority_ref == "experiment-operator"
    assert transition.after.authority_ref == "synthetic-world"
    assert transition.after.authority_ref != transition.intervention.experiment_authority_ref
    assert world.snapshot() == transition.after


def test_post_intervention_observation_changes_without_rewriting_history() -> None:
    world = SyntheticFactWorld(_initial_snapshot())
    historical = project_observation(world.snapshot(), producer_ref="synthetic-projector")

    transition = world.apply_intervention(_intervention())
    current = project_observation(transition.after, producer_ref="synthetic-projector")

    assert (historical.value, historical.world_epoch) == ("blue", 1)
    assert (current.value, current.world_epoch) == ("red", 2)
    assert historical.authority_ref == current.authority_ref == "synthetic-world"
    assert historical != current


def test_mismatched_fact_fails_without_mutating_world() -> None:
    world = SyntheticFactWorld(_initial_snapshot())
    before = world.snapshot()
    intervention = ExperimentIntervention(
        intervention_ref="operator-change-1",
        experiment_authority_ref="experiment-operator",
        fact_ref="door.state",
        value="open",
    )

    with pytest.raises(ValueError, match="does not match current WORLD fact"):
        world.apply_intervention(intervention)

    assert world.snapshot() is before


def test_non_intervention_input_fails_without_mutating_world() -> None:
    world = SyntheticFactWorld(_initial_snapshot())
    before = world.snapshot()

    with pytest.raises(TypeError, match="ExperimentIntervention"):
        world.apply_intervention("not-an-intervention")  # type: ignore[arg-type]

    assert world.snapshot() is before


@pytest.mark.parametrize(
    "field",
    ["intervention_ref", "experiment_authority_ref", "fact_ref"],
)
def test_intervention_rejects_empty_identity(field: str) -> None:
    values = {
        "intervention_ref": "operator-change-1",
        "experiment_authority_ref": "experiment-operator",
        "fact_ref": "box.color",
        "value": "red",
    }
    values[field] = "   "

    with pytest.raises(ValueError, match="must not be empty"):
        ExperimentIntervention(**values)


@pytest.mark.parametrize(
    "field",
    ["intervention_ref", "experiment_authority_ref", "fact_ref"],
)
def test_intervention_rejects_non_string_identity(field: str) -> None:
    values: dict[str, object] = {
        "intervention_ref": "operator-change-1",
        "experiment_authority_ref": "experiment-operator",
        "fact_ref": "box.color",
        "value": "red",
    }
    values[field] = 7

    with pytest.raises(TypeError, match="must be a string"):
        ExperimentIntervention(**values)  # type: ignore[arg-type]


def test_intervention_rejects_non_string_value() -> None:
    with pytest.raises(TypeError, match="value must be a string"):
        ExperimentIntervention(
            intervention_ref="operator-change-1",
            experiment_authority_ref="experiment-operator",
            fact_ref="box.color",
            value=7,  # type: ignore[arg-type]
        )


def test_synthetic_world_requires_world_fact_snapshot() -> None:
    with pytest.raises(TypeError, match="WorldFactSnapshot"):
        SyntheticFactWorld("blue")  # type: ignore[arg-type]


def test_same_value_intervention_still_creates_new_world_revision() -> None:
    world = SyntheticFactWorld(_initial_snapshot())

    transition = world.apply_intervention(_intervention(value="blue"))

    assert transition.before.value == transition.after.value == "blue"
    assert (transition.before.world_epoch, transition.after.world_epoch) == (1, 2)


def test_transition_is_immutable() -> None:
    world = SyntheticFactWorld(_initial_snapshot())
    transition = world.apply_intervention(_intervention())

    with pytest.raises(FrozenInstanceError):
        transition.after = transition.before  # type: ignore[misc]


def test_transition_rejects_intervention_fact_mismatch() -> None:
    before = _initial_snapshot()
    intervention = ExperimentIntervention(
        intervention_ref="operator-change-1",
        experiment_authority_ref="experiment-operator",
        fact_ref="door.state",
        value="red",
    )
    after = WorldFactSnapshot(
        fact_ref="box.color",
        value="red",
        world_epoch=2,
        authority_ref="synthetic-world",
    )

    with pytest.raises(ValueError, match="intervention fact_ref must match before"):
        InterventionTransition(intervention=intervention, before=before, after=after)


def test_transition_rejects_after_fact_mismatch() -> None:
    before = _initial_snapshot()
    intervention = _intervention()
    after = WorldFactSnapshot(
        fact_ref="door.state",
        value="red",
        world_epoch=2,
        authority_ref="synthetic-world",
    )

    with pytest.raises(ValueError, match="after fact_ref must match before"):
        InterventionTransition(intervention=intervention, before=before, after=after)


def test_transition_rejects_world_authority_laundering() -> None:
    before = _initial_snapshot()
    intervention = _intervention()
    forged_after = WorldFactSnapshot(
        fact_ref="box.color",
        value="red",
        world_epoch=2,
        authority_ref="experiment-operator",
    )

    with pytest.raises(ValueError, match="WORLD authority must be preserved"):
        InterventionTransition(
            intervention=intervention,
            before=before,
            after=forged_after,
        )


def test_transition_rejects_inconsistent_epoch() -> None:
    before = _initial_snapshot()
    intervention = _intervention()
    forged_after = WorldFactSnapshot(
        fact_ref="box.color",
        value="red",
        world_epoch=3,
        authority_ref="synthetic-world",
    )

    with pytest.raises(ValueError, match="exactly one greater"):
        InterventionTransition(
            intervention=intervention,
            before=before,
            after=forged_after,
        )


def test_transition_rejects_value_not_supplied_by_intervention() -> None:
    before = _initial_snapshot()
    intervention = _intervention()
    forged_after = WorldFactSnapshot(
        fact_ref="box.color",
        value="green",
        world_epoch=2,
        authority_ref="synthetic-world",
    )

    with pytest.raises(ValueError, match="after value must match intervention value"):
        InterventionTransition(
            intervention=intervention,
            before=before,
            after=forged_after,
        )
