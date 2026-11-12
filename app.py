from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Evasão em cursos EAD", page_icon="📉", layout="wide")

DADOS = Path(__file__).parent / "dados" / "evasao_ead.csv"


@st.cache_data
def carregar_dados() -> pd.DataFrame:
    df = pd.read_csv(DADOS, parse_dates=["data_matricula"])
    df["ano_mes"] = df["data_matricula"].dt.to_period("M").dt.to_timestamp()
    return df


df = carregar_dados()

# ---------- Filtros ----------
st.sidebar.header("Filtros")

periodo = st.sidebar.date_input(
    "Período de matrícula",
    value=(df["data_matricula"].min(), df["data_matricula"].max()),
    min_value=df["data_matricula"].min(),
    max_value=df["data_matricula"].max(),
)
areas = st.sidebar.multiselect(
    "Área do curso", sorted(df["area_curso"].unique()), default=sorted(df["area_curso"].unique())
)
ingressos = st.sidebar.multiselect(
    "Modalidade de ingresso",
    sorted(df["modalidade_ingresso"].unique()),
    default=sorted(df["modalidade_ingresso"].unique()),
)
bolsa = st.sidebar.radio("Bolsa", ["todos", "sim", "nao"], horizontal=True)

filtrado = df[df["area_curso"].isin(areas) & df["modalidade_ingresso"].isin(ingressos)]
if len(periodo) == 2:
    inicio, fim = pd.Timestamp(periodo[0]), pd.Timestamp(periodo[1])
    filtrado = filtrado[filtrado["data_matricula"].between(inicio, fim)]
if bolsa != "todos":
    filtrado = filtrado[filtrado["possui_bolsa"] == bolsa]

# ---------- Cabeçalho e KPIs ----------
st.title("📉 Evasão em cursos a distância")
st.caption("Matrículas de 01/01/2022 a 30/06/2025 · evasão = saída antes de concluir o primeiro ano")

if filtrado.empty:
    st.warning("Nenhuma matrícula para os filtros selecionados.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Matrículas", f"{len(filtrado):,}".replace(",", "."))
c2.metric("Taxa de evasão", f"{filtrado['evadiu'].mean():.1%}")
c3.metric("Acessos (30d), média", f"{filtrado['num_acessos_30d'].mean():.1f}")
c4.metric("Atividades entregues, média", f"{filtrado['num_atividades_entregues'].mean():.1f}")

# ---------- Abas ----------
aba_tempo, aba_perfil, aba_engaj = st.tabs(["Evolução", "Perfil", "Engajamento"])

with aba_tempo:
    mensal = filtrado.groupby("ano_mes").agg(taxa=("evadiu", "mean"), n=("evadiu", "size")).reset_index()
    fig = px.line(mensal, x="ano_mes", y="taxa", markers=True, labels={"ano_mes": "Mês de matrícula", "taxa": "Taxa de evasão"})
    fig.update_yaxes(tickformat=".0%")
    # tutoria ativa implantada em fev/2024
    fig.add_vline(x=pd.Timestamp("2024-02-01").timestamp() * 1000, line_dash="dash", annotation_text="Tutoria ativa")
    st.plotly_chart(fig, width="stretch")

with aba_perfil:
    col_a, col_b = st.columns(2)
    dimensao = col_a.selectbox(
        "Evasão por", ["area_curso", "modalidade_ingresso", "turno_preferencial", "possui_bolsa", "uf"]
    )
    por_dim = filtrado.groupby(dimensao)["evadiu"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(por_dim, x=dimensao, y="evadiu", labels={"evadiu": "Taxa de evasão"})
    fig.update_yaxes(tickformat=".0%")
    col_a.plotly_chart(fig, width="stretch")

    fig = px.histogram(filtrado, x="idade", color=filtrado["evadiu"].map({0: "Permaneceu", 1: "Evadiu"}), barmode="overlay", opacity=0.6)
    fig.update_layout(legend_title_text="")
    col_b.plotly_chart(fig, width="stretch")

with aba_engaj:
    metrica = st.selectbox(
        "Métrica de engajamento",
        ["num_acessos_30d", "tempo_plataforma_h_30d", "num_atividades_entregues", "nota_media_atividades", "num_mensagens_forum"],
    )
    fig = px.box(filtrado, x=filtrado["evadiu"].map({0: "Permaneceu", 1: "Evadiu"}), y=metrica, labels={"x": ""})
    st.plotly_chart(fig, width="stretch")

with st.expander("Ver dados"):
    st.dataframe(filtrado.drop(columns="ano_mes"), width="stretch")
