"""Helper utility functions for Cricbuzz LiveStats."""

import pandas as pd
from datetime import datetime


def format_date(date_str, output_fmt="%d %b %Y"):
    """Format an ISO date string to a readable format."""
    if not date_str:
        return "N/A"
    try:
        if len(date_str) == 10:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        else:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime(output_fmt)
    except (ValueError, TypeError):
        return str(date_str)


def safe_get(data, *keys, default=None):
    """Safely traverse and retrieve nested dictionary values."""
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, default)
        elif isinstance(current, list) and isinstance(key, int) and 0 <= key < len(current):
            current = current[key]
        else:
            return default
    return current if current is not None else default


def format_number(num):
    """Format large numbers with thousands separators."""
    try:
        return f"{int(num):,}"
    except (ValueError, TypeError):
        return str(num)
