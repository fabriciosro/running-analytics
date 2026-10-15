"""Filtros da sidebar."""
from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st


def render_filters(df: pd.DataFrame) -> tuple[list[str], date, date]:
    """
    Renderiza os filtros na sidebar.
    Retorna (tipos_selecionados, data_inicio, data_fim).
    """
    st.sidebar.header("Filtros")

    tipos = sorted(df["sport_type"].dropna().unique().tolist())
    tipos_selecionados = st.sidebar.multiselect(
        "Tipo de esporte",
        tipos,
        default=tipos,
    )

    data_min = df["start_date_local"].min().date()
    data_max = df["start_date_local"].max().date()

    data_inicio = st.sidebar.date_input("Data de início", data_min)
    data_fim = st.sidebar.date_input("Data de fim", data_max)

    return tipos_selecionados, data_inicio, data_fim