"""Tela de autenticação (login com Strava)."""
import streamlit as st

from src.config import StravaCredentials, STRAVA_ORANGE
from src.strava import build_authorization_url


def render_login_page(creds: StravaCredentials) -> None:
    """Exibe a tela inicial com o botão de conectar ao Strava."""
    st.markdown("### Conecte sua conta do Strava")
    st.markdown(
        "Clique no botão abaixo para autorizar o acesso aos seus dados de treino. "
        "Você será redirecionado para o Strava e depois voltará para cá."
    )

    auth_url = build_authorization_url(creds)
    st.markdown(
        f'<a href="{auth_url}" target="_self">'
        f'<button style="background-color:{STRAVA_ORANGE};color:white;'
        f'padding:12px 24px;border:none;border-radius:5px;'
        f'font-size:16px;cursor:pointer;">'
        f'🔗 Conectar com Strava</button></a>',
        unsafe_allow_html=True,
    )