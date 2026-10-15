"""Configurações e constantes da aplicação."""
from dataclasses import dataclass
import streamlit as st

# ============================================================
# ENDPOINTS DO STRAVA
# ============================================================
STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_API_BASE = "https://www.strava.com/api/v3"
STRAVA_SCOPE = "activity:read_all"

# ============================================================
# PARÂMETROS DA APLICAÇÃO
# ============================================================
MAX_PAGES = 10            # máx. de páginas buscadas (100 itens cada)
PER_PAGE = 100            # itens por página (máx. permitido pela API)
TOKEN_REFRESH_MARGIN = 60  # segundos de margem antes de expirar

# ============================================================
# IDENTIDADE VISUAL
# ============================================================
STRAVA_ORANGE = "#FC4C02"
APP_TITLE = "Running Analytics"
APP_ICON = "🏃"

# ============================================================
# CREDENCIAIS (carregadas do secrets.toml)
# ============================================================
@dataclass(frozen=True)
class StravaCredentials:
    client_id: str
    client_secret: str
    redirect_uri: str


def load_credentials() -> StravaCredentials:
    """Carrega as credenciais do Strava a partir do secrets.toml."""
    try:
        section = st.secrets["strava"]
        return StravaCredentials(
            client_id=str(section["client_id"]),
            client_secret=str(section["client_secret"]),
            redirect_uri=str(section["redirect_uri"]),
        )
    except (KeyError, FileNotFoundError) as exc:
        raise RuntimeError(
            "Credenciais do Strava não encontradas. "
            "Crie o arquivo .streamlit/secrets.toml com a seção [strava]."
        ) from exc