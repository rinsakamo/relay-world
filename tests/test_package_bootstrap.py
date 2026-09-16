import relay_world


def test_package_bootstrap_exposes_no_runtime_api_yet() -> None:
    assert relay_world.__all__ == ()
