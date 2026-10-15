import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# ============================================================
# CONFIGURAÇÃO INICIAL
# ============================================================
st.set_page_config(
    page_title="Strava Running Analytics",
    page_icon="🏃",
    layout="wide"
)

# Credenciais do secrets.toml
CLIENT_ID = st.secrets["strava"]["client_id"]
CLIENT_SECRET = st.secrets["strava"]["client_secret"]
REDIRECT_URI = st.secrets["strava"]["redirect_uri"]

STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_API_BASE = "https://www.strava.com/api/v3"
SCOPE = "activity:read_all"

# ============================================================
# FUNÇÕES DE AUTENTICAÇÃO
# ============================================================

def get_authorization_url():
    """Gera a URL para o usuário autorizar o app no Strava."""
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "approval_prompt": "auto"
    }
    query = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{STRAVA_AUTH_URL}?{query}"


def exchange_code_for_token(code):
    """Troca o 'code' recebido no callback por access_token e refresh_token."""
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    response = requests.post(STRAVA_TOKEN_URL, data=payload)
    response.raise_for_status()
    return response.json()


def refresh_access_token(refresh_token):
    """Renova o access_token usando o refresh_token."""
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    response = requests.post(STRAVA_TOKEN_URL, data=payload)
    response.raise_for_status()
    return response.json()


def ensure_valid_token():
    """Verifica se o token expirou e renova se necessário."""
    if "expires_at" not in st.session_state:
        return False
    if time.time() > st.session_state["expires_at"] - 60:  # margem de 60s
        try:
            tokens = refresh_access_token(st.session_state["refresh_token"])
            st.session_state["access_token"] = tokens["access_token"]
            st.session_state["refresh_token"] = tokens["refresh_token"]
            st.session_state["expires_at"] = tokens["expires_at"]
            return True
        except Exception as e:
            st.error(f"Erro ao renovar token: {e}")
            return False
    return True


# ============================================================
# FUNÇÕES DA API DO STRAVA
# ============================================================

def get_activities(access_token, page=1, per_page=100, before=None, after=None):
    """Busca uma página de atividades do atleta autenticado."""
    url = f"{STRAVA_API_BASE}/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"page": page, "per_page": per_page}
    if before:
        params["before"] = before
    if after:
        params["after"] = after
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def get_all_activities(access_token, max_pages=10):
    """Busca todas as atividades com paginação automática."""
    all_activities = []
    for page in range(1, max_pages + 1):
        activities = get_activities(access_token, page=page, per_page=100)
        if not activities:
            break
        all_activities.extend(activities)
        if len(activities) < 100:
            break
    return all_activities


def activities_to_dataframe(activities):
    """Converte a lista de atividades JSON em DataFrame tratado."""
    if not activities:
        return pd.DataFrame()
    
    df = pd.json_normalize(activities)
    
    # Colunas úteis
    cols = [
        "id", "name", "type", "sport_type", "start_date_local",
        "distance", "moving_time", "elapsed_time", "total_elevation_gain",
        "average_speed", "max_speed", "average_heartrate", "max_heartrate",
        "average_cadence", "kilojoules"
    ]
    df = df[[c for c in cols if c in df.columns]]
    
    # Tratamentos
    df["distance_km"] = df["distance"] / 1000
    df["moving_time_min"] = df["moving_time"] / 60
    df["moving_time_h"] = df["moving_time"] / 3600
    df["pace_min_km"] = df.apply(
        lambda r: r["moving_time_min"] / r["distance_km"] 
        if r["distance_km"] > 0 else None, axis=1
    )
    df["start_date_local"] = pd.to_datetime(df["start_date_local"])
    df["start_date_local"] = df["start_date_local"].dt.tz_localize(None)
    df["date"] = df["start_date_local"].dt.date
    df["year"] = df["start_date_local"].dt.year
    df["month"] = df["start_date_local"].dt.month
    
    return df


# ============================================================
# FLUXO PRINCIPAL — AUTENTICAÇÃO
# ============================================================

st.title("🏃 Strava Running Analytics")

# Verifica se já está autenticado
if "access_token" not in st.session_state:
    # 1. Verifica se o Strava redirecionou de volta com um 'code'
    query_params = st.query_params
    code = query_params.get("code")
    
    if code:
        # 2. Troca o code por tokens
        with st.spinner("Autenticando com Strava..."):
            try:
                tokens = exchange_code_for_token(code)
                st.session_state["access_token"] = tokens["access_token"]
                st.session_state["refresh_token"] = tokens["refresh_token"]
                st.session_state["expires_at"] = tokens["expires_at"]
                st.session_state["athlete"] = tokens.get("athlete", {})
                
                # Limpa o code da URL
                st.query_params.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Erro na autenticação: {e}")
                st.stop()
    else:
        # 3. Usuário não autenticado — mostra botão de login
        st.markdown("""
        ### Conecte sua conta do Strava
        
        Clique no botão abaixo para autorizar o acesso aos seus dados de treino.
        Você será redirecionado para o Strava e depois voltará para cá.
        """)
        
        auth_url = get_authorization_url()
        st.markdown(
            f'<a href="{auth_url}" target="_self">'
            f'<button style="background-color:#FC4C02;color:white;'
            f'padding:12px 24px;border:none;border-radius:5px;'
            f'font-size:16px;cursor:pointer;">'
            f'🔗 Conectar com Strava</button></a>',
            unsafe_allow_html=True
        )
        st.stop()

# ============================================================
# USUÁRIO AUTENTICADO — DASHBOARD
# ============================================================

# Garante que o token está válido
ensure_valid_token()

athlete = st.session_state.get("athlete", {})
nome = f"{athlete.get('firstname', '')} {athlete.get('lastname', '')}".strip()
if nome:
    st.success(f"✅ Conectado como **{nome}**")

# Botão de logout
if st.sidebar.button("🚪 Desconectar"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ------------------------------------------------------------
# BUSCAR ATIVIDADES
# ------------------------------------------------------------
with st.spinner("Carregando atividades do Strava..."):
    try:
        activities_raw = get_all_activities(st.session_state["access_token"])
        df = activities_to_dataframe(activities_raw)
    except Exception as e:
        st.error(f"Erro ao buscar atividades: {e}")
        st.stop()

if df.empty:
    st.warning("Nenhuma atividade encontrada na sua conta.")
    st.stop()

# ------------------------------------------------------------
# FILTROS NA SIDEBAR
# ------------------------------------------------------------
st.sidebar.header("Filtros")

# Filtro por tipo de esporte
tipos = sorted(df["sport_type"].dropna().unique().tolist())
tipos_selecionados = st.sidebar.multiselect(
    "Tipo de esporte",
    tipos,
    default=tipos
)

# Filtro por período
data_min = df["start_date_local"].min().date()
data_max = df["start_date_local"].max().date()

data_inicio = st.sidebar.date_input("Data de início", data_min)
data_fim = st.sidebar.date_input("Data de fim", data_max)

# Aplica filtros
df_filtrado = df[
    (df["sport_type"].isin(tipos_selecionados)) &
    (df["date"] >= data_inicio) &
    (df["date"] <= data_fim)
].copy()

if df_filtrado.empty:
    st.warning("Nenhuma atividade corresponde aos filtros selecionados.")
    st.stop()

# ------------------------------------------------------------
# MÉTRICAS PRINCIPAIS
# ------------------------------------------------------------
st.subheader("📊 Resumo do Período")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Atividades", len(df_filtrado))
with col2:
    st.metric("Distância Total", f"{df_filtrado['distance_km'].sum():.1f} km")
with col3:
    st.metric("Tempo Total", f"{df_filtrado['moving_time_h'].sum():.1f} h")
with col4:
    st.metric("Elevação Total", f"{df_filtrado['total_elevation_gain'].sum():.0f} m")

# ------------------------------------------------------------
# GRÁFICOS
# ------------------------------------------------------------
st.subheader("📈 Evolução dos Treinos")

# Distância por atividade ao longo do tempo
df_sorted = df_filtrado.sort_values("start_date_local")

fig_dist = {
    "data": [
        {
            "x": df_sorted["start_date_local"].tolist(),
            "y": df_sorted["distance_km"].tolist(),
            "type": "scatter",
            "mode": "lines+markers",
            "name": "Distância (km)",
            "line": {"color": "#FC4C02"}
        }
    ],
    "layout": {
        "title": "Distância por Atividade",
        "xaxis": {"title": "Data"},
        "yaxis": {"title": "Distância (km)"},
        "hovermode": "x unified"
    }
}
st.plotly_chart(fig_dist, use_container_width=True)

# Distribuição de distâncias
fig_hist = {
    "data": [
        {
            "x": df_filtrado["distance_km"].tolist(),
            "type": "histogram",
            "marker": {"color": "#FC4C02"},
            "nbinsx": 20
        }
    ],
    "layout": {
        "title": "Distribuição de Distâncias",
        "xaxis": {"title": "Distância (km)"},
        "yaxis": {"title": "Frequência"}
    }
}
st.plotly_chart(fig_hist, use_container_width=True)

# Pace médio por atividade (apenas corridas)
df_runs = df_filtrado[df_filtrado["sport_type"].isin(["Run", "TrailRun"])].copy()
if not df_runs.empty:
    st.subheader("🏃 Pace Médio (Corridas)")
    df_runs_sorted = df_runs.sort_values("start_date_local")
    
    fig_pace = {
        "data": [
            {
                "x": df_runs_sorted["start_date_local"].tolist(),
                "y": df_runs_sorted["pace_min_km"].tolist(),
                "type": "scatter",
                "mode": "lines+markers",
                "name": "Pace (min/km)",
                "line": {"color": "#FC4C02"}
            }
        ],
        "layout": {
            "title": "Pace por Corrida",
            "xaxis": {"title": "Data"},
            "yaxis": {"title": "Pace (min/km)", "autorange": "reversed"},
            "hovermode": "x unified"
        }
    }
    st.plotly_chart(fig_pace, use_container_width=True)

# ------------------------------------------------------------
# TABELA DETALHADA
# ------------------------------------------------------------
st.subheader("📋 Lista de Atividades")

df_exibir = df_filtrado[[
    "date", "name", "sport_type", "distance_km",
    "moving_time_min", "pace_min_km", "total_elevation_gain",
    "average_heartrate"
]].copy()

df_exibir.columns = [
    "Data", "Nome", "Esporte", "Distância (km)",
    "Tempo (min)", "Pace (min/km)", "Elevação (m)", "FC Média"
]

st.dataframe(
    df_exibir.sort_values("Data", ascending=False),
    use_container_width=True,
    hide_index=True
)