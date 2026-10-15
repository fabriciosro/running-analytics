"""Fluxo OAuth 2.0 com o Strava."""
from __future__ import annotations

import time
import urllib.parse

import requests
import streamlit as st

from src.config import (
    STRAVA_AUTH_URL,
    STRAVA_TOKEN_URL,
    STRAVA_SCOPE,
    TOKEN_REFRESH_MARGIN,
    StravaCredentials,
)


def build_authorization_url(creds: StravaCredentials) -> str:
    """Monta a URL de autorização para redirecionar o usuário ao Strava."""
    params = {
        "client_id": creds.client_id,
        "redirect_uri": creds.redirect_uri,
        "response_type": "code",
        "scope": STRAVA_SCOPE,
        "approval_prompt": "auto",
    }
    return f"{STRAVA_AUTH_URL}?{urllib.parse.urlencode(params)}"


def exchange_code_for_tokens(creds: StravaCredentials, code: str) -> dict:
    """Troca o `code` recebido no callback por access_token e refresh_token."""
    payload = {
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "code": code,
        "grant_type": "authorization_code",
    }
    response = requests.post(STRAVA_TOKEN_URL, data=payload, timeout=15)
    response.raise_for_status()
    return response.json()


def refresh_tokens(creds: StravaCredentials, refresh_token: str) -> dict:
    """Renova o access_token usando o refresh_token."""
    payload = {
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    response = requests.post(STRAVA_TOKEN_URL, data=payload, timeout=15)
    response.raise_for_status()
    return response.json()


def ensure_valid_token(creds: StravaCredentials) -> bool:
    """
    Garante que o access_token em session_state está válido.
    Renova automaticamente se estiver próximo de expirar.
    """
    if "expires_at" not in st.session_state:
        return False

    if time.time() < st.session_state["expires_at"] - TOKEN_REFRESH_MARGIN:
        return True

    try:
        tokens = refresh_tokens(creds, st.session_state["refresh_token"])
        st.session_state.update(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            expires_at=tokens["expires_at"],
        )
        return True
    except requests.RequestException as exc:
        st.error(f"Erro ao renovar token: {exc}")
        return False