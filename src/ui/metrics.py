"""Bloco de métricas agregadas."""
import pandas as pd
import streamlit as st


def render_metrics(df: pd.DataFrame) -> None:
    """Renderiza o resumo do período em 4 colunas."""
    st.subheader("📊 Resumo do Período")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Atividades", len(df))
    col2.metric("Distância Total", f"{df['distance_km'].sum():.1f} km")
    col3.metric("Tempo Total", f"{df['moving_time_h'].sum():.1f} h")
    col4.metric("Elevação Total", f"{df['total_elevation_gain'].sum():.0f} m")