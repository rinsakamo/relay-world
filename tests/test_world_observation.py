from dataclasses import FrozenInstanceError

import pytest

from relay_world import Observation, WorldFactSnapshot, project_observation


def test_projection_preserves_world_snapshot_and_records_producer() -> None:
    snapshot = WorldFactSnapshot(
        fact_ref="box.color",
        value="blue",
        world_epoch=1,
        authority_ref="synthetic-world",
    )

    observation = project_observation(snapshot, producer_ref="synthetic-projector")

    assert observation == Observation(
        fact_ref="box.color",
        value="blue",
        world_epoch=1,
        authority_ref="synthetic-world",
        producer_ref="synthetic-projector",
    )
    assert observation.authority_ref != observation.producer_ref


def test_historical_observation_is_unchanged_by_later_world_snapshot() -> None:
    earlier = WorldFactSnapshot(
        fact_ref="box.color",
        value="blue",
        world_epoch=1,
        authority_ref="synthetic-world",
    )
    historical = project_observation(earlier, producer_ref="synthetic-projector")

    later = WorldFactSnapshot(
        fact_ref="box.color",
        value="red",
        world_epoch=2,
        authority_ref="synthetic-world",
    )
    current = project_observation(later, producer_ref="synthetic-projector")

    assert (historical.value, historical.world_epoch) == ("blue", 1)
    assert (current.value, current.world_epoch) == ("red", 2)
    assert historical.fact_ref == current.fact_ref
    assert historical != current


def test_observation_is_immutable() -> None:
    observation = project_observation(
        WorldFactSnapshot("box.color", "blue", 1, "synthetic-world"),
        producer_ref="synthetic-projector",
    )

    with pytest.raises(FrozenInstanceError):
        observation.value = "red"  # type: ignore[misc]


@pytest.mark.parametrize("field", ["fact_ref", "authority_ref"])
def test_world_fact_snapshot_rejects_empty_identity(field: str) -> None:
    kwargs = {
        "fact_ref": "box.color",
        "value": "blue",
        "world_epoch": 1,
        "authority_ref": "synthetic-world",
    }
    kwargs[field] = "   "

    with pytest.raises(ValueError):
        WorldFactSnapshot(**kwargs)  # type: ignore[arg-type]


@pytest.mark.parametrize("world_epoch", [-1, True, 1.5])
def test_world_fact_snapshot_rejects_invalid_epoch(world_epoch: object) -> None:
    error = TypeError if isinstance(world_epoch, (bool, float)) else ValueError
    with pytest.raises(error):
        WorldFactSnapshot(
            fact_ref="box.color",
            value="blue",
            world_epoch=world_epoch,  # type: ignore[arg-type]
            authority_ref="synthetic-world",
        )


def test_projection_rejects_empty_producer_identity() -> None:
    snapshot = WorldFactSnapshot("box.color", "blue", 1, "synthetic-world")

    with pytest.raises(ValueError):
        project_observation(snapshot, producer_ref=" ")
