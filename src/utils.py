from __future__ import annotations


def format_large_number(value) -> str:
    if value is None:
        return "N/A"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return "N/A"

    abs_value = abs(value)

    if abs_value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T"
    if abs_value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if abs_value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if abs_value >= 1_000:
        return f"{value / 1_000:.2f}K"

    return f"{value:.2f}"


def format_price(value) -> str:
    if value is None:
        return "N/A"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return "N/A"

    return f"${value:,.2f}"