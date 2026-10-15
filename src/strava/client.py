"""Cliente HTTP para a API v3 do Strava."""
from __future__ import annotations

from typing import Any

import requests

from src.config import STRAVA_API_BASE, PER_PAGE, MAX_PAGES


class StravaClient:
    """Cliente simples para consumir a API do Strava."""

    def __init__(self, access_token: str, timeout: int = 15) -> None:
        self._access_token = access_token
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {"Authorization": f"Bearer {access_token}"}
        )

    # ------------------------------------------------------------
    # Endpoints
    # ------------------------------------------------------------
    def get_activities(
        self,
        page: int = 1,
        per_page: int = PER_PAGE,
        before: int | None = None,
        after: int | None = None,
    ) -> list[dict[str, Any]]:
        """GET /athlete/activities — busca uma página de atividades."""
        params: dict[str, Any] = {"page": page, "per_page": per_page}
        if before is not None:
            params["before"] = before
        if after is not None:
            params["after"] = after

        url = f"{STRAVA_API_BASE}/athlete/activities"
        response = self._session.get(url, params=params, timeout=self._timeout)
        response.raise_for_status()
        return response.json()

    def get_all_activities(self, max_pages: int = MAX_PAGES) -> list[dict[str, Any]]:
        """Busca todas as atividades com paginação automática."""
        activities: list[dict[str, Any]] = []
        for page in range(1, max_pages + 1):
            batch = self.get_activities(page=page, per_page=PER_PAGE)
            if not batch:
                break
            activities.extend(batch)
            if len(batch) < PER_PAGE:
                break
        return activities