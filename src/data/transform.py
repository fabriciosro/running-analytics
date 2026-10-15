"""Transformações de dados: JSON do Strava → DataFrame tratado."""
from __future__ import annotations

from typing import Any

import pandas as pd

# Tipos de esporte considerados "corrida"
RUN_SPORT_TYPES = ["Run", "TrailRun", "VirtualRun"]

# Colunas mantidas do payload original
USEFUL_COLUMNS = [
    "id", "name", "type", "sport_type", "start_date_local",
    "distance", "moving_time", "elapsed_time", "total_elevation_gain",
    "average_speed", "max_speed", "average_heartrate", "max_heartrate",
    "average_cadence", "kilojoules",
]


def activities_to_dataframe(activities: list[dict[str, Any]]) -> pd.DataFrame:
    """Converte a lista de atividades em um DataFrame tratado."""
    if not activities:
        return pd.DataFrame()

    df = pd.json_normalize(activities)
    df = df[[c for c in USEFUL_COLUMNS if c in df.columns]].copy()

    # Unidades
    df["distance_km"] = df["distance"] / 1000
    df["moving_time_min"] = df["moving_time"] / 60
    df["moving_time_h"] = df["moving_time"] / 3600
    df["pace_min_km"] = df.apply(_compute_pace, axis=1)

    # Datas
    df["start_date_local"] = pd.to_datetime(df["start_date_local"]).dt.tz_localize(None)
    df["date"] = df["start_date_local"].dt.date
    df["year"] = df["start_date_local"].dt.year
    df["month"] = df["start_date_local"].dt.month

    return df


def _compute_pace(row: pd.Series) -> float | None:
    """Calcula o pace (min/km) com segurança contra divisão por zero."""
    if row["distance_km"] > 0:
        return row["moving_time_min"] / row["distance_km"]
    return None