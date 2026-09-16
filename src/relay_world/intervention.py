"""Executable Experiment Intervention boundary for a single-fact synthetic WORLD."""

from __future__ import annotations

from dataclasses import dataclass

from .observation import WorldFactSnapshot


def _require_identity(name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be empty or whitespace-only")


@dataclass(frozen=True, slots=True)
class ExperimentIntervention:
    """Experiment-authority mutation targeted at one WORLD fact."""

    intervention_ref: str
    experiment_authority_ref: str
    fact_ref: str
    value: str

    def __post_init__(self) -> None:
        _require_identity("intervention_ref", self.intervention_ref)
        _require_identity("experiment_authority_ref", self.experiment_authority_ref)
        _require_identity("fact_ref", self.fact_ref)
        if not isinstance(self.value, str):
            raise TypeError("value must be a string in the initial executable contract")


@dataclass(frozen=True, slots=True)
class InterventionTransition:
    """Immutable lineage for one successfully applied synthetic intervention."""

    intervention: ExperimentIntervention
    before: WorldFactSnapshot
    after: WorldFactSnapshot

    def __post_init__(self) -> None:
        if not isinstance(self.intervention, ExperimentIntervention):
            raise TypeError("intervention must be an ExperimentIntervention")
        if not isinstance(self.before, WorldFactSnapshot):
            raise TypeError("before must be a WorldFactSnapshot")
        if not isinstance(self.after, WorldFactSnapshot):
            raise TypeError("after must be a WorldFactSnapshot")
        if self.intervention.fact_ref != self.before.fact_ref:
            raise ValueError("intervention fact_ref must match before snapshot")
        if self.after.fact_ref != self.before.fact_ref:
            raise ValueError("after fact_ref must match before snapshot")
        if self.after.value != self.intervention.value:
            raise ValueError("after value must match intervention value")
        if self.after.authority_ref != self.before.authority_ref:
            raise ValueError("WORLD authority must be preserved across intervention")
        if self.after.world_epoch != self.before.world_epoch + 1:
            raise ValueError("after world_epoch must be exactly one greater than before")


class SyntheticFactWorld:
    """Minimal deterministic mutable WORLD owning exactly one current fact snapshot."""

    __slots__ = ("_current",)

    def __init__(self, initial_snapshot: WorldFactSnapshot) -> None:
        if not isinstance(initial_snapshot, WorldFactSnapshot):
            raise TypeError("initial_snapshot must be a WorldFactSnapshot")
        self._current = initial_snapshot

    def snapshot(self) -> WorldFactSnapshot:
        """Return the current immutable WORLD fact snapshot."""

        return self._current

    def apply_intervention(
        self,
        intervention: ExperimentIntervention,
    ) -> InterventionTransition:
        """Apply one experiment intervention atomically to the synthetic WORLD."""

        if not isinstance(intervention, ExperimentIntervention):
            raise TypeError("intervention must be an ExperimentIntervention")

        before = self._current
        if intervention.fact_ref != before.fact_ref:
            raise ValueError("intervention fact_ref does not match current WORLD fact")

        after = WorldFactSnapshot(
            fact_ref=before.fact_ref,
            value=intervention.value,
            world_epoch=before.world_epoch + 1,
            authority_ref=before.authority_ref,
        )
        transition = InterventionTransition(
            intervention=intervention,
            before=before,
            after=after,
        )
        self._current = after
        return transition
