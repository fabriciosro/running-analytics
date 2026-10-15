"""Componentes de interface."""
from .auth_view import render_login_page
from .sidebar import render_filters
from .metrics import render_metrics
from .charts import render_charts
from .tables import render_activities_table

__all__ = [
    "render_login_page",
    "render_filters",
    "render_metrics",
    "render_charts",
    "render_activities_table",
]