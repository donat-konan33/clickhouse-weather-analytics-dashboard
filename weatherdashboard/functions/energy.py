from math import ceil


def calculate_required_panel_count(
    daily_consumption_kwh: float,
    daily_production_per_panel_kwh: float,
) -> int | None:
    """Return the panel count needed for a day's consumption."""
    if daily_consumption_kwh <= 0:
        return 0
    if daily_production_per_panel_kwh <= 0:
        return None
    return ceil(daily_consumption_kwh / daily_production_per_panel_kwh)
