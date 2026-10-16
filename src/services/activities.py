"""Serviço de orquestração: buscar, transformar e filtrar atividades."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pandas as pd

from src.data import activities_to_dataframe
from src.strava import StravaClient


def fetch_activities_dataframe(
    access_token: str,
    months: int = 3,
) -> pd.DataFrame:
    """
    Busca atividades dos últimos `months` meses e retorna um DataFrame tratado.

    Args:
        access_token: token de acesso do Strava.
        months: quantos meses para trás buscar (padrão: 3).
    """
    after_ts = _months_ago_to_epoch(months)
    client = StravaClient(access_token)
    raw = client.get_all_activities(after=after_ts)
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


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def _months_ago_to_epoch(months: int) -> int:
    """Retorna o timestamp Unix (epoch) correspondente a `months` meses atrás."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=30 * months)
    return int(cutoff.timestamp())