"""Scenario-local failure probe for lossy transport at the embodiment seam.

All request, consequence, transport, and replay helpers are private test-harness types.
This is deterministic architectural evidence for Issue #11, not a RelayWorld API.
"""

from dataclasses import dataclass

import pytest


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


class _TransportUncertain(RuntimeError):
    """The caller did not receive a consequence and cannot infer execution."""


class _SyntheticWorld:
    def __init__(self) -> None:
        self._actor_to_body = {"actor-1": "body-a", "actor-2": "body-b"}
        self._positions = {"body-a": 0, "body-b": 100}
        self._world_epoch = 0

    @property
    def world_epoch(self) -> int:
        return self._world_epoch

    def position(self, body_ref: str) -> int:
        return self._positions[body_ref]

    def execute(self, issued: _IssuedEffect) -> _Consequence:
        if issued.actor_ref not in self._actor_to_body:
            raise KeyError(issued.actor_ref)
        if issued.effect != "step_forward":
            raise ValueError(f"unsupported effect: {issued.effect}")

        body_ref = self._actor_to_body[issued.actor_ref]
        self._positions[body_ref] += 1
        self._world_epoch += 1
        return _Consequence(
            action_id=issued.action_id,
            actor_ref=issued.actor_ref,
            body_ref=body_ref,
            world_epoch=self._world_epoch,
            outcome="applied",
        )


class _NaiveLossyAdapter:
    """Private adapter with no replay protection."""

    def __init__(self, world: _SyntheticWorld) -> None:
        self._world = world

    def submit(
        self,
        issued: _IssuedEffect,
        *,
        lose_before_delivery: bool = False,
        lose_response: bool = False,
    ) -> _Consequence:
        if lose_before_delivery:
            raise _TransportUncertain("request did not produce an observable response")

        consequence = self._world.execute(issued)
        if lose_response:
            raise _TransportUncertain("request did not produce an observable response")
        return consequence


class _ReplayProtectedAdapter:
    """Private adapter using external action identity as a replay/idempotency key."""

    def __init__(self, world: _SyntheticWorld) -> None:
        self._world = world
        self._completed: dict[str, tuple[_IssuedEffect, _Consequence]] = {}

    def submit(
        self,
        issued: _IssuedEffect,
        *,
        lose_before_delivery: bool = False,
        lose_response: bool = False,
    ) -> _Consequence:
        if lose_before_delivery:
            raise _TransportUncertain("request did not produce an observable response")

        previous = self._completed.get(issued.action_id)
        if previous is not None:
            previous_request, consequence = previous
            if previous_request != issued:
                raise ValueError("action_id was reused for different request meaning")
        else:
            consequence = self._world.execute(issued)
            self._completed[issued.action_id] = (issued, consequence)

        if lose_response:
            raise _TransportUncertain("request did not produce an observable response")
        return consequence


def test_transport_uncertainty_does_not_reveal_whether_execution_happened() -> None:
    before_world = _SyntheticWorld()
    before_adapter = _NaiveLossyAdapter(before_world)
    request = _IssuedEffect("action-1", "actor-1", "step_forward")

    with pytest.raises(_TransportUncertain):
        before_adapter.submit(request, lose_before_delivery=True)

    assert before_world.world_epoch == 0
    assert before_world.position("body-a") == 0

    after_world = _SyntheticWorld()
    after_adapter = _NaiveLossyAdapter(after_world)

    with pytest.raises(_TransportUncertain):
        after_adapter.submit(request, lose_response=True)

    assert after_world.world_epoch == 1
    assert after_world.position("body-a") == 1


def test_naive_retry_after_lost_response_duplicates_world_effect() -> None:
    world = _SyntheticWorld()
    adapter = _NaiveLossyAdapter(world)
    request = _IssuedEffect("action-1", "actor-1", "step_forward")

    with pytest.raises(_TransportUncertain):
        adapter.submit(request, lose_response=True)

    retry_consequence = adapter.submit(request)

    assert world.position("body-a") == 2
    assert world.world_epoch == 2
    assert retry_consequence.world_epoch == 2


def test_existing_action_id_can_make_exact_retry_idempotent_in_adapter() -> None:
    world = _SyntheticWorld()
    adapter = _ReplayProtectedAdapter(world)
    request = _IssuedEffect("action-1", "actor-1", "step_forward")

    with pytest.raises(_TransportUncertain):
        adapter.submit(request, lose_response=True)

    assert world.position("body-a") == 1
    assert world.world_epoch == 1

    replayed = adapter.submit(request)

    assert replayed == _Consequence(
        action_id="action-1",
        actor_ref="actor-1",
        body_ref="body-a",
        world_epoch=1,
        outcome="applied",
    )
    assert world.position("body-a") == 1
    assert world.world_epoch == 1


def test_pre_delivery_loss_then_retry_executes_exactly_once() -> None:
    world = _SyntheticWorld()
    adapter = _ReplayProtectedAdapter(world)
    request = _IssuedEffect("action-1", "actor-1", "step_forward")

    with pytest.raises(_TransportUncertain):
        adapter.submit(request, lose_before_delivery=True)

    consequence = adapter.submit(request)

    assert consequence.world_epoch == 1
    assert world.position("body-a") == 1
    assert world.world_epoch == 1


@pytest.mark.parametrize(
    "conflicting_request",
    [
        _IssuedEffect("action-1", "actor-2", "step_forward"),
        _IssuedEffect("action-1", "actor-1", "teleport"),
    ],
)
def test_same_action_id_with_different_request_meaning_fails_closed(
    conflicting_request: _IssuedEffect,
) -> None:
    world = _SyntheticWorld()
    adapter = _ReplayProtectedAdapter(world)
    original = _IssuedEffect("action-1", "actor-1", "step_forward")

    original_consequence = adapter.submit(original)

    with pytest.raises(ValueError, match="different request meaning"):
        adapter.submit(conflicting_request)

    assert original_consequence.world_epoch == 1
    assert world.world_epoch == 1
    assert world.position("body-a") == 1
    assert world.position("body-b") == 100
