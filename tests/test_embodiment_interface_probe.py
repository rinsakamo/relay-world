"""Scenario-local Grand Null probe for the candidate Embodiment Interface.

This module intentionally defines only private test-harness types. It is evidence for
Issue #9, not a RelayWorld package API or protocol contract.
"""

from dataclasses import dataclass

import pytest

from relay_world import WorldFactSnapshot, project_observation


@dataclass(frozen=True, slots=True)
class _IssuedEffect:
    action_id: str
    actor_ref: str
    effect: str


@dataclass(frozen=True, slots=True)
class _Consequence:
    action_id: str
    actor_ref: str
    body_ref: str
    world_epoch: int
    outcome: str


class _SyntheticActorScenario:
    """Private scenario adapter used only to probe existing semantic composition."""

    def __init__(self) -> None:
        self._actor_to_body = {"actor-1": "body-a"}
        self._positions = {"body-a": 0, "body-b": 100}
        self._world_epoch = 0

    @property
    def world_epoch(self) -> int:
        return self._world_epoch

    def position(self, body_ref: str) -> int:
        return self._positions[body_ref]

    def bind_actor(self, actor_ref: str, body_ref: str) -> None:
        if body_ref not in self._positions:
            raise KeyError(body_ref)
        self._actor_to_body[actor_ref] = body_ref

    def execute(self, issued: _IssuedEffect) -> tuple[_Consequence, object]:
        if issued.actor_ref not in self._actor_to_body:
            raise KeyError(issued.actor_ref)
        if issued.effect != "step_forward":
            raise ValueError(f"unsupported effect: {issued.effect}")

        body_ref = self._actor_to_body[issued.actor_ref]
        self._positions[body_ref] += 1
        self._world_epoch += 1

        consequence = _Consequence(
            action_id=issued.action_id,
            actor_ref=issued.actor_ref,
            body_ref=body_ref,
            world_epoch=self._world_epoch,
            outcome="applied",
        )
        observation = project_observation(
            WorldFactSnapshot(
                fact_ref=f"{body_ref}.position",
                value=str(self._positions[body_ref]),
                world_epoch=self._world_epoch,
                authority_ref="probe-world",
            ),
            producer_ref=f"{issued.actor_ref}:body-view",
        )
        return consequence, observation


def _close_issued(issued: _IssuedEffect, consequence: _Consequence) -> None:
    """Probe whether the existing action identity is enough for causal correlation."""

    if consequence.action_id != issued.action_id:
        raise ValueError("consequence does not belong to the issued action")


def test_action_id_is_sufficient_for_two_in_flight_actions() -> None:
    scenario = _SyntheticActorScenario()
    first = _IssuedEffect("action-1", "actor-1", "step_forward")
    second = _IssuedEffect("action-2", "actor-1", "step_forward")

    second_consequence, _ = scenario.execute(second)
    first_consequence, _ = scenario.execute(first)

    _close_issued(second, second_consequence)
    _close_issued(first, first_consequence)

    with pytest.raises(ValueError):
        _close_issued(first, second_consequence)
    with pytest.raises(ValueError):
        _close_issued(second, first_consequence)


def test_actor_addressing_survives_body_swap_without_body_in_request() -> None:
    scenario = _SyntheticActorScenario()
    before = _IssuedEffect("action-before", "actor-1", "step_forward")
    before_consequence, before_observation = scenario.execute(before)

    scenario.bind_actor("actor-1", "body-b")

    after = _IssuedEffect("action-after", "actor-1", "step_forward")
    after_consequence, after_observation = scenario.execute(after)

    assert before.actor_ref == after.actor_ref == "actor-1"
    assert before_consequence.body_ref == "body-a"
    assert after_consequence.body_ref == "body-b"
    assert before_observation.fact_ref == "body-a.position"
    assert after_observation.fact_ref == "body-b.position"
    assert scenario.position("body-a") == 1
    assert scenario.position("body-b") == 101


def test_world_epoch_distinguishes_stale_feedback_without_new_protocol_time() -> None:
    scenario = _SyntheticActorScenario()

    _, earlier = scenario.execute(_IssuedEffect("action-1", "actor-1", "step_forward"))
    _, later = scenario.execute(_IssuedEffect("action-2", "actor-1", "step_forward"))

    assert earlier.world_epoch == 1
    assert later.world_epoch == 2
    assert earlier.world_epoch < later.world_epoch
    assert earlier.value == "1"
    assert later.value == "2"


def test_local_rejection_can_fail_before_world_mutation() -> None:
    scenario = _SyntheticActorScenario()
    initial_epoch = scenario.world_epoch
    initial_position = scenario.position("body-a")

    with pytest.raises(KeyError):
        scenario.execute(_IssuedEffect("unknown-actor", "actor-missing", "step_forward"))
    with pytest.raises(ValueError):
        scenario.execute(_IssuedEffect("bad-effect", "actor-1", "teleport"))

    assert scenario.world_epoch == initial_epoch
    assert scenario.position("body-a") == initial_position
