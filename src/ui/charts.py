"""Gráficos interativos (Plotly)."""
import pandas as pd
import streamlit as st

from src.config import STRAVA_ORANGE
from src.data import RUN_SPORT_TYPES


def render_charts(df: pd.DataFrame) -> None:
    """Renderiza todos os gráficos do dashboard."""
    st.subheader("📈 Evolução dos Treinos")
    _render_distance_chart(df)
    _render_distance_histogram(df)
    _render_pace_chart(df)


# ------------------------------------------------------------
# Gráficos individuais
# ------------------------------------------------------------
def _render_distance_chart(df: pd.DataFrame) -> None:
    df_sorted = df.sort_values("start_date_local")
    fig = {
        "data": [{
            "x": df_sorted["start_date_local"].tolist(),
            "y": df_sorted["distance_km"].tolist(),
            "type": "scatter",
            "mode": "lines+markers",
            "name": "Distância (km)",
            "line": {"color": STRAVA_ORANGE},
        }],
        "layout": {
            "title": "Distância por Atividade",
            "xaxis": {"title": "Data"},
            "yaxis": {"title": "Distância (km)"},
            "hovermode": "x unified",
        },
    }
    st.plotly_chart(fig, use_container_width=True)


def _render_distance_histogram(df: pd.DataFrame) -> None:
    fig = {
        "data": [{
            "x": df["distance_km"].tolist(),
            "type": "histogram",
            "marker": {"color": STRAVA_ORANGE},
            "nbinsx": 20,
        }],
        "layout": {
            "title": "Distribuição de Distâncias",
            "xaxis": {"title": "Distância (km)"},
            "yaxis": {"title": "Frequência"},
        },
    }
    st.plotly_chart(fig, use_container_width=True)


def _render_pace_chart(df: pd.DataFrame) -> None:
    runs = df[df["sport_type"].isin(RUN_SPORT_TYPES)].copy()
    if runs.empty:
        return

    st.subheader("🏃 Pace Médio (Corridas)")
    runs_sorted = runs.sort_values("start_date_local")

    fig = {
        "data": [{
            "x": runs_sorted["start_date_local"].tolist(),
            "y": runs_sorted["pace_min_km"].tolist(),
            "type": "scatter",
            "mode": "lines+markers",
            "name": "Pace (min/km)",
            "line": {"color": STRAVA_ORANGE},
        }],
        "layout": {
            "title": "Pace por Corrida",
            "xaxis": {"title": "Data"},
            "yaxis": {"title": "Pace (min/km)", "autorange": "reversed"},
            "hovermode": "x unified",
        },
    }
    st.plotly_chart(fig, use_container_width=True)