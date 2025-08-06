import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# # dev
API_URL = "http://localhost:8000/metrics-list"

# # prod
# API_URL = "https://tech-challenge-fase-1-gabrielrm366244.onrender.com/metrics-list/"

st.set_page_config(page_title="API Metrics Dashboard", layout="wide")

# Link para documentação da API no topo, com target _blank para abrir em nova aba
st.markdown(
    '<a href="/docs" target="_blank" style="font-size:18px;">📖 Documentação da API</a>',
    unsafe_allow_html=True,
)

st.title("📊 API Metrics Dashboard")

# Fetch metrics data
with st.spinner("Carregando dados..."):
    response = requests.get(API_URL)
    if response.status_code != 200:
        st.error(f"Erro ao buscar métricas: {response.status_code}")
        st.stop()

    data = response.json()
    df = pd.DataFrame(data)

if df.empty:
    st.warning("Nenhuma métrica disponível.")
    st.stop()

# Conversões e novos campos
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["duration_ms"] = df["duration"] * 1000  # em milissegundos

# Sidebar filtros
with st.sidebar:
    st.header("Filtros")
    method_filter = st.multiselect(
        "Métodos HTTP",
        options=df["method"].unique(),
        default=df["method"].unique(),
        help="Filtre pelos métodos HTTP das requisições",
    )
    status_filter = st.multiselect(
        "Códigos de Status",
        options=sorted(df["status_code"].unique()),
        default=sorted(df["status_code"].unique()),
        help="Filtre pelos códigos de status HTTP",
    )
    st.markdown("---")
    st.caption(f"Total registros: {len(df):,}")

df_filtered = df[
    (df["method"].isin(method_filter)) & (df["status_code"].isin(status_filter))
]

# Métricas principais
total_requests = len(df_filtered)
error_5xx = df_filtered[df_filtered["status_code"] >= 500]
error_5xx_count = len(error_5xx)
error_5xx_pct = (error_5xx_count / total_requests * 100) if total_requests > 0 else 0

latency_mean = df_filtered["duration_ms"].mean()
latency_median = df_filtered["duration_ms"].median()
latency_max = df_filtered["duration_ms"].max()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total de Requisições", f"{total_requests:,}")
col2.metric("Erros 5xx", f"{error_5xx_count:,} ({error_5xx_pct:.1f}%)")
col3.metric("Latência Média", f"{latency_mean:.2f} ms")
col4.metric("Latência Mediana", f"{latency_median:.2f} ms")
col5.metric("Latência Máxima", f"{latency_max:.2f} ms")

# Gráfico: Hits por rota
st.subheader("📈 Hits por Rota")
hits_by_path = df_filtered["path"].value_counts().reset_index()
hits_by_path.columns = ["path", "hits"]
fig_hits = px.bar(
    hits_by_path,
    x="path",
    y="hits",
    text="hits",
    height=400,
    labels={"path": "Rota", "hits": "Número de Hits"},
    title="Número de Requisições por Rota",
)
fig_hits.update_traces(texttemplate="%{text:,}", textposition="outside")
fig_hits.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_hits, use_container_width=True)

# Gráfico: Distribuição dos códigos de status
st.subheader("📊 Distribuição dos Códigos de Status HTTP")
status_counts = df_filtered["status_code"].value_counts().reset_index()
status_counts.columns = ["status_code", "count"]
fig_status = px.pie(
    status_counts,
    values="count",
    names="status_code",
    title="Proporção dos Códigos de Status HTTP",
    hole=0.4,
)
st.plotly_chart(fig_status, use_container_width=True)

# Gráfico: Latência média por rota
st.subheader("⏱️ Latência Média por Rota")
latency_by_path = df_filtered.groupby("path")["duration_ms"].mean().reset_index()
fig_latency = px.bar(
    latency_by_path,
    x="path",
    y="duration_ms",
    text_auto=".2f",
    height=400,
    labels={"path": "Rota", "duration_ms": "Latência Média (ms)"},
    title="Latência Média (ms) por Rota",
)
fig_latency.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_latency, use_container_width=True)

# Gráfico: Evolução temporal de requests
st.subheader("📅 Requests ao longo do Tempo")
df_time = (
    df_filtered.set_index("timestamp").resample("1min").count()["id"].reset_index()
)
fig_time = px.line(
    df_time,
    x="timestamp",
    y="id",
    markers=True,
    height=400,
    labels={"timestamp": "Timestamp", "id": "Número de Requests"},
    title="Número de Requisições por Minuto",
)
st.plotly_chart(fig_time, use_container_width=True)
