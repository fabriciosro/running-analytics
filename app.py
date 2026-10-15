import streamlit as st

from src.config import (
    APP_ICON,
    APP_TITLE,
    load_credentials,
)
from src.services import fetch_activities_dataframe, filter_activities
from src.strava import ensure_valid_token, exchange_code_for_tokens
from src.ui import (
    render_activities_table,
    render_charts,
    render_filters,
    render_login_page,
    render_metrics,
)

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title=f"Strava {APP_TITLE}",
    page_icon=APP_ICON,
    layout="wide",
)

# ============================================================
# CREDENCIAIS
# ============================================================
creds = load_credentials()

# ============================================================
# CABEÇALHO
# ============================================================
st.title(f"{APP_ICON} Strava {APP_TITLE}")


# ============================================================
# FLUXO DE AUTENTICAÇÃO
# ============================================================
def _handle_callback() -> None:
    """Processa o retorno do Strava com o `code` na URL."""
    code = st.query_params.get("code")
    if not code:
        return

    with st.spinner("Autenticando com Strava..."):
        try:
            tokens = exchange_code_for_tokens(creds, code)
            st.session_state.update(
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                expires_at=tokens["expires_at"],
                athlete=tokens.get("athlete", {}),
            )
            st.query_params.clear()
            st.rerun()
        except Exception as exc:
            st.error(f"Erro na autenticação: {exc}")
            st.stop()


if "access_token" not in st.session_state:
    _handle_callback()
    if "access_token" not in st.session_state:
        render_login_page(creds)
        st.stop()


# ============================================================
# USUÁRIO AUTENTICADO
# ============================================================
ensure_valid_token(creds)

athlete = st.session_state.get("athlete", {})
full_name = f"{athlete.get('firstname', '')} {athlete.get('lastname', '')}".strip()
if full_name:
    st.success(f"✅ Conectado como **{full_name}**")

if st.sidebar.button("🚪 Desconectar"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


# ============================================================
# BUSCAR E TRATAR DADOS
# ============================================================
with st.spinner("Carregando atividades do Strava..."):
    try:
        df = fetch_activities_dataframe(st.session_state["access_token"])
    except Exception as exc:
        st.error(f"Erro ao buscar atividades: {exc}")
        st.stop()

if df.empty:
    st.warning("Nenhuma atividade encontrada na sua conta.")
    st.stop()


# ============================================================
# FILTROS E DASHBOARD
# ============================================================
sport_types, start_date, end_date = render_filters(df)
df_filtered = filter_activities(df, sport_types, start_date, end_date)

if df_filtered.empty:
    st.warning("Nenhuma atividade corresponde aos filtros selecionados.")
    st.stop()

render_metrics(df_filtered)
render_charts(df_filtered)
render_activities_table(df_filtered)