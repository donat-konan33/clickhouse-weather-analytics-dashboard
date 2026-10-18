import pytest

from weatherdashboard.functions.energy import calculate_required_panel_count


@pytest.mark.parametrize(
    ("consumption", "production_per_panel", "expected"),
    [
        (0, 1.5, 0),
        (3, 1.5, 2),
        (3.1, 1.5, 3),
    ],
)
def test_calculate_required_panel_count(
    consumption,
    production_per_panel,
    expected,
):
    assert (
        calculate_required_panel_count(consumption, production_per_panel)
        == expected
    )


def test_calculate_required_panel_count_returns_none_without_solar_production():
    assert calculate_required_panel_count(3, 0) is None
