"""Serviço de orquestração: buscar, transformar e filtrar atividades."""
from __future__ import annotations

import pandas as pd

from src.data import activities_to_dataframe
from src.strava import StravaClient


def fetch_activities_dataframe(access_token: str) -> pd.DataFrame:
    """Busca todas as atividades e retorna um DataFrame tratado."""
    client = StravaClient(access_token)
    raw = client.get_all_activities()
    return activities_to_dataframe(raw)


def filter_activities(
    df: pd.DataFrame,
    sport_types: list[str],
    start_date,
    end_date,
) -> pd.DataFrame:
    """Aplica filtros de tipo de esporte e intervalo de datas."""
    mask = (
        df["sport_type"].isin(sport_types)
        & (df["date"] >= start_date)
        & (df["date"] <= end_date)
    )
    return df.loc[mask].copy()