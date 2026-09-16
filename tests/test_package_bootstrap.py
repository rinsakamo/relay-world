import relay_world


def test_package_exposes_only_earned_world_observation_boundary() -> None:
    assert relay_world.__all__ == (
        "Observation",
        "WorldFactSnapshot",
        "project_observation",
    )
