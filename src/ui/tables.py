"""Tabela detalhada de atividades."""
import pandas as pd
import streamlit as st

# Mapeamento de colunas → rótulos em português
COLUMN_LABELS = {
    "date": "Data",
    "name": "Nome",
    "sport_type": "Esporte",
    "distance_km": "Distância (km)",
    "moving_time_min": "Tempo (min)",
    "pace_min_km": "Pace (min/km)",
    "total_elevation_gain": "Elevação (m)",
    "average_heartrate": "FC Média",
}


def render_activities_table(df: pd.DataFrame) -> None:
    """Renderiza a tabela detalhada de atividades."""
    st.subheader("📋 Lista de Atividades")

    columns = list(COLUMN_LABELS.keys())
    display = df[columns].copy()
    display.columns = list(COLUMN_LABELS.values())

    st.dataframe(
        display.sort_values("Data", ascending=False),
        use_container_width=True,
        hide_index=True,
    )