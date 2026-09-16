"""Executable WORLD-fact-snapshot to Observation boundary."""

from __future__ import annotations

from dataclasses import dataclass


def _require_identity(name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be empty or whitespace-only")


def _require_epoch(world_epoch: int) -> None:
    if isinstance(world_epoch, bool) or not isinstance(world_epoch, int):
        raise TypeError("world_epoch must be an integer")
    if world_epoch < 0:
        raise ValueError("world_epoch must be non-negative")


@dataclass(frozen=True, slots=True)
class WorldFactSnapshot:
    """Authority-attributed snapshot of one WORLD fact at one WORLD epoch."""

    fact_ref: str
    value: str
    world_epoch: int
    authority_ref: str

    def __post_init__(self) -> None:
        _require_identity("fact_ref", self.fact_ref)
        if not isinstance(self.value, str):
            raise TypeError("value must be a string in the initial executable contract")
        _require_epoch(self.world_epoch)
        _require_identity("authority_ref", self.authority_ref)


@dataclass(frozen=True, slots=True)
class Observation:
    """Immutable record of what a producer exposed from a WORLD fact snapshot."""

    fact_ref: str
    value: str
    world_epoch: int
    authority_ref: str
    producer_ref: str

    def __post_init__(self) -> None:
        _require_identity("fact_ref", self.fact_ref)
        if not isinstance(self.value, str):
            raise TypeError("value must be a string in the initial executable contract")
        _require_epoch(self.world_epoch)
        _require_identity("authority_ref", self.authority_ref)
        _require_identity("producer_ref", self.producer_ref)


def project_observation(
    snapshot: WorldFactSnapshot,
    *,
    producer_ref: str,
) -> Observation:
    """Project one WORLD fact snapshot into an Observation deterministically."""

    if not isinstance(snapshot, WorldFactSnapshot):
        raise TypeError("snapshot must be a WorldFactSnapshot")
    _require_identity("producer_ref", producer_ref)
    return Observation(
        fact_ref=snapshot.fact_ref,
        value=snapshot.value,
        world_epoch=snapshot.world_epoch,
        authority_ref=snapshot.authority_ref,
        producer_ref=producer_ref,
    )
