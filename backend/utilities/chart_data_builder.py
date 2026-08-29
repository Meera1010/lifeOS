"""
LifeOS Interactive Chart & Data Analytics Builder
"""

def build_line_chart_data(labels: list, datasets: list, title: str = "") -> dict:
    """Builds standard line chart configuration object for UI renderer."""
    return {
        "type": "line",
        "title": title,
        "labels": labels,
        "datasets": datasets
    }

def build_bar_chart_data(labels: list, datasets: list, title: str = "", is_stacked: bool = False) -> dict:
    """Builds bar chart configuration object."""
    return {
        "type": "bar",
        "title": title,
        "is_stacked": is_stacked,
        "labels": labels,
        "datasets": datasets
    }

def build_pie_chart_data(labels: list, values: list, colors: list, title: str = "") -> dict:
    """Builds pie/doughnut chart configuration object."""
    return {
        "type": "pie",
        "title": title,
        "labels": labels,
        "values": values,
        "colors": colors
    }

def build_radial_chart_data(score: float, max_score: float = 100.0, label: str = "Life Score") -> dict:
    """Builds gauge / radial progress chart object."""
    percentage = round(min(100.0, max(0.0, (score / max_score) * 100.0)), 1)
    return {
        "type": "radial",
        "label": label,
        "score": score,
        "max_score": max_score,
        "percentage": percentage
    }
