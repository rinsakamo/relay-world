import relay_world


def test_package_exposes_only_earned_executable_boundaries() -> None:
    assert relay_world.__all__ == (
        "ExperimentIntervention",
        "InterventionTransition",
        "Observation",
        "SyntheticFactWorld",
        "WorldFactSnapshot",
        "project_observation",
    )
