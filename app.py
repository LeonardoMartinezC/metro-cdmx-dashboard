"""
=============================================================
 Metro CDMX · Dashboard de Ciencia de Datos
 Afluencia Diaria Desglosada 2021–2026
=============================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import re
from datetime import datetime, timedelta

# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Metro CDMX · Dashboard",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CSS / ESTILOS PREMIUM
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-card:    #111827;
    --bg-card2:   #1a2035;
    --accent1:    #6366f1;
    --accent2:    #8b5cf6;
    --accent3:    #06b6d4;
    --accent4:    #10b981;
    --accent5:    #f59e0b;
    --text-main:  #f1f5f9;
    --text-muted: #94a3b8;
    --border:     rgba(99,102,241,0.25);
    --glow:       0 0 30px rgba(99,102,241,0.20);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-main);
}

.main .block-container { padding: 1.5rem 2rem 2rem 2rem; }

/* ─── KPI CARDS ─── */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.kpi-card {
    background: linear-gradient(135deg, var(--bg-card), var(--bg-card2));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    box-shadow: var(--glow);
    transition: transform .25s, box-shadow .25s;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 140px; height: 140px;
    border-radius: 50%;
    opacity: 0.08;
    background: var(--glow-color, var(--accent1));
}
.kpi-card:hover { transform: translateY(-4px); box-shadow: 0 8px 40px rgba(99,102,241,0.30); }
.kpi-label { font-size: .72rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: var(--text-muted); margin-bottom: .5rem; }
.kpi-value { font-size: 2.1rem; font-weight: 800; letter-spacing: -1px; background: var(--grad, linear-gradient(90deg,#6366f1,#8b5cf6)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.kpi-sub   { font-size: .78rem; color: var(--text-muted); margin-top: .35rem; }
.kpi-icon  { font-size: 2rem; position: absolute; top: 1.2rem; right: 1.4rem; opacity: .55; }

/* ─── SECTION TITLE ─── */
.section-title {
    font-size: 1.25rem; font-weight: 700;
    background: linear-gradient(90deg, #6366f1, #06b6d4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 1.5rem 0 .75rem; border-left: 3px solid #6366f1; padding-left: .6rem;
}

/* ─── TABS ─── */
.stTabs [data-baseweb="tab-list"] { gap: .5rem; background: transparent; border-bottom: 1px solid var(--border); }
.stTabs [data-baseweb="tab"] {
    background: transparent; color: var(--text-muted);
    border: 1px solid transparent; border-radius: 10px 10px 0 0;
    padding: .6rem 1.2rem; font-weight: 500; font-size: .88rem;
    transition: all .2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(139,92,246,0.1));
    color: #6366f1 !important; border-color: var(--border);
}

/* ─── SIDEBAR ─── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #1a2035) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] label { color: var(--text-muted) !important; font-size:.82rem; font-weight:600; }
section[data-testid="stSidebar"] .stSelectbox>div>div,
section[data-testid="stSidebar"] .stMultiSelect>div>div {
    background: #1e293b !important; border: 1px solid var(--border) !important; color: var(--text-main) !important;
}

/* ─── CHARTS ─── */
.plot-container.plotly { border-radius: 12px; overflow: hidden; }

/* ─── STAT BADGE ─── */
.stat-badge {
    display: inline-block; padding: .25rem .75rem; border-radius: 99px;
    background: rgba(99,102,241,.15); color: #818cf8;
    font-size: .78rem; font-weight: 600; border: 1px solid rgba(99,102,241,.3);
    margin: .2rem;
}

/* ─── ANOMALY LEGEND ─── */
.anomaly-legend { background: rgba(239,68,68,.1); border: 1px solid rgba(239,68,68,.3);
    border-radius: 10px; padding: .9rem 1.2rem; margin: .5rem 0; font-size:.85rem; }

/* scrollbar */
::-webkit-scrollbar { width: 5px; } 
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--accent1); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────────────────────
CSV_PATH     = os.path.join(os.path.dirname(__file__), "afluenciastc_desglosado_06_2026.csv")
MAPPING_PATH = os.path.join(os.path.dirname(__file__), "mapping.json")

LINE_COLORS = {
    "Línea 1":  "#e63e47", "Línea 2":  "#004a97", "Línea 3":  "#007a43",
    "Línea 4":  "#6ccae0", "Línea 5":  "#fbcf09", "Línea 6":  "#e1001a",
    "Línea 7":  "#f07200", "Línea 8":  "#009352", "Línea 9":  "#52016f",
    "Línea 12": "#b5a23b", "Línea A":  "#9a1c6e", "Línea B":  "#bdbdbd",
}

MESES_ES = {
    "Enero":1,"Febrero":2,"Marzo":3,"Abril":4,"Mayo":5,"Junio":6,
    "Julio":7,"Agosto":8,"Septiembre":9,"Octubre":10,"Noviembre":11,"Diciembre":12
}
DIAS_ES = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]

# ─────────────────────────────────────────────────────────────
# CARGA DE DATOS (CACHEADA)
# ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="🔄 Cargando datos del Metro CDMX…")
def load_data():
    with open(MAPPING_PATH, "r", encoding="utf-8") as f:
        mapping = json.load(f)
    station_map = mapping.get("stations", {})
    line_map    = mapping.get("lines",    {})
    coords      = mapping.get("coordinates", {})

    chunks = []
    with open(CSV_PATH, "r", encoding="utf-8", errors="replace") as fh:
        for chunk in pd.read_csv(fh, chunksize=200_000):
            chunk["fecha"]    = pd.to_datetime(chunk["fecha"], errors="coerce")
            chunk["estacion"] = chunk["estacion"].map(lambda x: station_map.get(str(x), str(x)))
            chunk["linea"]    = chunk["linea"].map(lambda x: line_map.get(str(x), str(x)))
            chunks.append(chunk)

    df = pd.concat(chunks, ignore_index=True)
    df.dropna(subset=["fecha"], inplace=True)
    df["anio"]          = df["fecha"].dt.year
    df["mes_num"]       = df["fecha"].dt.month
    df["dia_semana"]    = df["fecha"].dt.dayofweek          # 0=Lun
    df["dia_semana_es"] = df["dia_semana"].map(lambda x: DIAS_ES[x])
    df["tipo_dia"]      = df["dia_semana"].map(lambda x: "Fin de semana" if x >= 5 else "Día laboral")
    df["afluencia"]     = pd.to_numeric(df["afluencia"], errors="coerce").fillna(0).astype(int)
    return df, coords

df, coords = load_data()

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1rem 0 .5rem;'>
        <div style='font-size:2.5rem;'>🚇</div>
        <div style='font-size:1.1rem;font-weight:800;background:linear-gradient(90deg,#6366f1,#06b6d4);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>Metro CDMX</div>
        <div style='font-size:.72rem;color:#64748b;letter-spacing:1px;'>DASHBOARD · 2021–2026</div>
    </div>
    <hr style='border-color:rgba(99,102,241,0.2);margin:.5rem 0 1rem;'>
    """, unsafe_allow_html=True)

    años = sorted(df["anio"].unique())
    sel_años = st.multiselect("📅 Año", años, default=años, key="años")

    lineas = sorted(df["linea"].unique())
    sel_lineas = st.multiselect("🚉 Línea", lineas, default=lineas, key="lineas")

    tipos_pago = sorted(df["tipo_pago"].unique())
    sel_pago = st.multiselect("💳 Tipo de pago", tipos_pago, default=tipos_pago, key="pago")

    st.markdown("<hr style='border-color:rgba(99,102,241,0.2);margin:1rem 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.72rem;color:#64748b;text-align:center;'>Datos: Portal de Datos Abiertos CDMX</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FILTRADO
# ─────────────────────────────────────────────────────────────
mask = (
    df["anio"].isin(sel_años) &
    df["linea"].isin(sel_lineas) &
    df["tipo_pago"].isin(sel_pago)
)
dff = df[mask].copy()

if dff.empty:
    st.warning("⚠️ No hay datos con los filtros seleccionados.")
    st.stop()

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:.5rem 0 1rem;'>
    <h1 style='font-size:2rem;font-weight:800;margin:0;
       background:linear-gradient(90deg,#6366f1,#06b6d4,#10b981);
       -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
       🚇 Afluencia del Metro CDMX
    </h1>
    <p style='color:#64748b;font-size:.9rem;margin:.3rem 0 0;'>
       Análisis de datos · 2021–2026 · Sistema de Transporte Colectivo
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Inicio & KPIs",
    "🔍 Análisis Exploratorio",
    "🤖 Clustering",
    "📈 Pronóstico",
    "🚨 Anomalías",
])

# ══════════════════════════════════════════════════════════════
# TAB 1: KPIs + MAPA
# ══════════════════════════════════════════════════════════════
with tab1:
    total_pax       = dff["afluencia"].sum()
    linea_top       = dff.groupby("linea")["afluencia"].sum().idxmax()
    estacion_top    = dff.groupby("estacion")["afluencia"].sum().idxmax()
    pax_por_dia     = dff.groupby("fecha")["afluencia"].sum().mean()
    dias_disponibles = dff["fecha"].nunique()

    st.markdown("""
    <div class='kpi-grid'>
      <div class='kpi-card' style='--glow-color:#6366f1;--grad:linear-gradient(90deg,#6366f1,#8b5cf6)'>
        <div class='kpi-icon'>🧑‍🤝‍🧑</div>
        <div class='kpi-label'>Pasajeros totales</div>
        <div class='kpi-value'>{:,.0f}M</div>
        <div class='kpi-sub'>en la selección actual</div>
      </div>
      <div class='kpi-card' style='--glow-color:#06b6d4;--grad:linear-gradient(90deg,#06b6d4,#0ea5e9)'>
        <div class='kpi-icon'>🏆</div>
        <div class='kpi-label'>Línea más popular</div>
        <div class='kpi-value' style='font-size:1.4rem'>{}</div>
        <div class='kpi-sub'>mayor afluencia acumulada</div>
      </div>
      <div class='kpi-card' style='--glow-color:#10b981;--grad:linear-gradient(90deg,#10b981,#34d399)'>
        <div class='kpi-icon'>📍</div>
        <div class='kpi-label'>Estación más concurrida</div>
        <div class='kpi-value' style='font-size:1.2rem'>{}</div>
        <div class='kpi-sub'>mayor flujo de pasajeros</div>
      </div>
      <div class='kpi-card' style='--glow-color:#f59e0b;--grad:linear-gradient(90deg,#f59e0b,#fb923c)'>
        <div class='kpi-icon'>📅</div>
        <div class='kpi-label'>Promedio diario</div>
        <div class='kpi-value'>{:,.0f}K</div>
        <div class='kpi-sub'>{:,} días en el período</div>
      </div>
    </div>
    """.format(
        total_pax / 1e6,
        linea_top,
        estacion_top,
        pax_por_dia / 1e3,
        dias_disponibles,
    ), unsafe_allow_html=True)

    # ─── MAPA INTERACTIVO ───
    st.markdown("<div class='section-title'>🗺️ Mapa de Afluencia por Estación</div>", unsafe_allow_html=True)

    station_afl = (
        dff.groupby("estacion")["afluencia"]
        .sum()
        .reset_index()
        .rename(columns={"estacion": "station", "afluencia": "total"})
    )
    station_afl["lat"] = station_afl["station"].map(lambda s: coords.get(s, {}).get("lat", None))
    station_afl["lon"] = station_afl["station"].map(lambda s: coords.get(s, {}).get("lon", None))
    station_afl.dropna(subset=["lat", "lon"], inplace=True)
    station_afl["millones"] = (station_afl["total"] / 1e6).round(2)

    # Add line colour info
    dff_line = dff.groupby(["estacion","linea"])["afluencia"].sum().reset_index()
    station_line = dff_line.loc[dff_line.groupby("estacion")["afluencia"].idxmax()][["estacion","linea"]].rename(columns={"estacion":"station"})
    station_afl = station_afl.merge(station_line, on="station", how="left")
    station_afl["color"] = station_afl["linea"].map(lambda l: LINE_COLORS.get(l, "#6366f1"))

    fig_map = go.Figure()
    for linea, grp in station_afl.groupby("linea"):
        fig_map.add_trace(go.Scattermapbox(
            lat=grp["lat"], lon=grp["lon"],
            mode="markers",
            marker=dict(
                size=np.sqrt(grp["total"] / grp["total"].max()) * 36 + 6,
                color=LINE_COLORS.get(linea, "#6366f1"),
                opacity=0.85,
                sizemode="diameter",
            ),
            text=grp.apply(lambda r: f"<b>{r['station']}</b><br>{r['linea']}<br>{r['millones']:.2f}M pasajeros", axis=1),
            hovertemplate="%{text}<extra></extra>",
            name=linea,
        ))

    fig_map.update_layout(
        mapbox=dict(style="carto-darkmatter", center={"lat": 19.41, "lon": -99.14}, zoom=10.5),
        paper_bgcolor="#0a0e1a", plot_bgcolor="#0a0e1a",
        font_color="#f1f5f9",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=500,
        legend=dict(orientation="v", x=1.01, y=1, bgcolor="rgba(17,24,39,.9)",
                    bordercolor="rgba(99,102,241,.3)", borderwidth=1, font_size=11),
        showlegend=True,
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # ─── EVOLUCIÓN ANUAL ───
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='section-title'>📅 Afluencia Mensual por Año</div>", unsafe_allow_html=True)
        monthly = (dff.groupby(["anio","mes_num"])["afluencia"].sum() / 1e6).reset_index()
        monthly.columns = ["Año","Mes","Millones"]
        fig_month = px.line(monthly, x="Mes", y="Millones", color="Año",
                            color_discrete_sequence=["#6366f1","#06b6d4","#10b981","#f59e0b","#f43f5e","#a855f7"],
                            markers=True, template="plotly_dark",
                            labels={"Millones":"Millones de pasajeros","Mes":"Mes"})
        fig_month.update_xaxes(tickvals=list(range(1,13)),
                               ticktext=["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"])
        fig_month.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827",
                                 font_color="#f1f5f9", legend_title_text="Año", height=320,
                                 margin={"t":10,"b":10,"l":10,"r":10})
        st.plotly_chart(fig_month, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-title'>💳 Distribución por Tipo de Pago</div>", unsafe_allow_html=True)
        pago_df = dff.groupby("tipo_pago")["afluencia"].sum().reset_index()
        fig_pie = px.pie(pago_df, names="tipo_pago", values="afluencia",
                         color_discrete_sequence=["#6366f1","#06b6d4","#10b981"],
                         hole=0.55, template="plotly_dark")
        fig_pie.update_traces(textinfo="percent+label", textfont_size=12,
                               marker=dict(line=dict(color="#0a0e1a", width=2)))
        fig_pie.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827",
                               font_color="#f1f5f9", showlegend=True, height=320,
                               margin={"t":10,"b":10,"l":10,"r":10},
                               legend=dict(orientation="v"))
        st.plotly_chart(fig_pie, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# TAB 2: EDA
# ══════════════════════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-title'>🏆 Top 10 Estaciones Más Concurridas</div>", unsafe_allow_html=True)
        top10_est = (dff.groupby("estacion")["afluencia"].sum().nlargest(10) / 1e6).reset_index()
        top10_est.columns = ["Estación","Millones"]
        top10_est = top10_est.sort_values("Millones")
        fig_top_est = px.bar(top10_est, x="Millones", y="Estación", orientation="h",
                             color="Millones", color_continuous_scale=["#312e81","#6366f1","#06b6d4"],
                             text=top10_est["Millones"].map(lambda v: f"{v:.1f}M"),
                             template="plotly_dark")
        fig_top_est.update_traces(textposition="outside")
        fig_top_est.update_coloraxes(showscale=False)
        fig_top_est.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827",
                                   font_color="#f1f5f9", height=380,
                                   margin={"t":10,"b":10,"l":10,"r":10})
        st.plotly_chart(fig_top_est, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>🚇 Afluencia Total por Línea</div>", unsafe_allow_html=True)
        linea_total = (dff.groupby("linea")["afluencia"].sum() / 1e6).reset_index()
        linea_total.columns = ["Línea","Millones"]
        linea_total = linea_total.sort_values("Millones")
        linea_total["color"] = linea_total["Línea"].map(lambda l: LINE_COLORS.get(l,"#6366f1"))
        fig_linea = px.bar(linea_total, x="Millones", y="Línea", orientation="h",
                           color="Línea", color_discrete_map=LINE_COLORS,
                           text=linea_total["Millones"].map(lambda v: f"{v:.0f}M"),
                           template="plotly_dark")
        fig_linea.update_traces(textposition="outside")
        fig_linea.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827",
                                 font_color="#f1f5f9", height=380, showlegend=False,
                                 margin={"t":10,"b":10,"l":10,"r":10})
        st.plotly_chart(fig_linea, use_container_width=True)

    # ─── DÍAS DE LA SEMANA ───
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("<div class='section-title'>📆 Afluencia Promedio por Día de la Semana</div>", unsafe_allow_html=True)
        dia_avg = dff.groupby(["fecha","dia_semana","dia_semana_es"])["afluencia"].sum().reset_index()
        dia_avg = dia_avg.groupby(["dia_semana","dia_semana_es"])["afluencia"].mean().reset_index()
        dia_avg = dia_avg.sort_values("dia_semana")
        dia_avg["afluencia_k"] = dia_avg["afluencia"] / 1e3
        fig_dia = px.bar(dia_avg, x="dia_semana_es", y="afluencia_k",
                         color="afluencia_k",
                         color_continuous_scale=["#312e81","#6366f1","#a78bfa"],
                         text=dia_avg["afluencia_k"].map(lambda v: f"{v:.0f}K"),
                         template="plotly_dark",
                         labels={"dia_semana_es":"Día","afluencia_k":"Miles de pasajeros"})
        fig_dia.update_traces(textposition="outside")
        fig_dia.update_coloraxes(showscale=False)
        fig_dia.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827",
                               font_color="#f1f5f9", height=330,
                               margin={"t":10,"b":10,"l":10,"r":10})
        st.plotly_chart(fig_dia, use_container_width=True)

    with col4:
        st.markdown("<div class='section-title'>🗃️ Treemap · Afluencia por Línea y Estación</div>", unsafe_allow_html=True)
        treemap_df = (dff.groupby(["linea","estacion"])["afluencia"].sum() / 1e6).reset_index()
        treemap_df.columns = ["Línea","Estación","Millones"]
        fig_tree = px.treemap(treemap_df, path=["Línea","Estación"], values="Millones",
                              color="Millones", color_continuous_scale=["#1e1b4b","#6366f1","#06b6d4","#10b981"],
                              template="plotly_dark")
        fig_tree.update_layout(paper_bgcolor="#111827", font_color="#f1f5f9", height=330,
                                margin={"t":10,"b":10,"l":10,"r":10})
        st.plotly_chart(fig_tree, use_container_width=True)

    # ─── HEATMAP SEMANA × MES ───
    st.markdown("<div class='section-title'>🌡️ Mapa de Calor · Día de Semana vs Mes</div>", unsafe_allow_html=True)
    hm = dff.groupby(["dia_semana","mes_num"])["afluencia"].mean().reset_index()
    hm_pivot = hm.pivot(index="dia_semana", columns="mes_num", values="afluencia")
    hm_pivot.index = [DIAS_ES[i] for i in hm_pivot.index]
    meses_tick = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
    hm_pivot.columns = [meses_tick[c-1] for c in hm_pivot.columns]
    fig_hm = px.imshow(hm_pivot, color_continuous_scale="Inferno",
                       labels={"color":"Pasajeros promedio"}, template="plotly_dark", aspect="auto")
    fig_hm.update_layout(paper_bgcolor="#111827", font_color="#f1f5f9", height=300,
                          margin={"t":10,"b":10,"l":10,"r":10})
    st.plotly_chart(fig_hm, use_container_width=True)

    # ─── LABORAL vs FINDE ───
    st.markdown("<div class='section-title'>⚖️ Días Laborales vs Fines de Semana</div>", unsafe_allow_html=True)
    tipo_anio = dff.groupby(["anio","tipo_dia"])["afluencia"].sum().reset_index()
    tipo_anio["Millones"] = tipo_anio["afluencia"] / 1e6
    fig_lf = px.bar(tipo_anio, x="anio", y="Millones", color="tipo_dia",
                    barmode="group",
                    color_discrete_map={"Día laboral":"#6366f1","Fin de semana":"#f59e0b"},
                    template="plotly_dark",
                    labels={"anio":"Año","Millones":"Millones de pasajeros","tipo_dia":"Tipo de día"})
    fig_lf.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827",
                          font_color="#f1f5f9", height=320,
                          margin={"t":10,"b":10,"l":10,"r":10})
    st.plotly_chart(fig_lf, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# TAB 3: CLUSTERING (K-Means + PCA en puro NumPy)
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-title'>🤖 Clustering de Estaciones</div>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color:#94a3b8;font-size:.88rem;'>
    Agrupamos las estaciones según su <b>perfil de uso</b>: distribución por día de la semana
    y por tipo de pago. Usamos K-Means y PCA implementados en <b>NumPy puro</b>.
    </p>""", unsafe_allow_html=True)

    col_ctrl, _ = st.columns([1,3])
    with col_ctrl:
        n_clusters = st.slider("Número de clusters", 2, 8, 4, key="n_clust")

    # ── Feature matrix ──────────────────────────────────────
    @st.cache_data(show_spinner=False)
    def build_features(dff_hash):
        df_feat = dff.copy()
        # Day-of-week profile (% of each day per station)
        dow = df_feat.groupby(["estacion","dia_semana"])["afluencia"].sum().unstack(fill_value=0)
        dow = dow.div(dow.sum(axis=1), axis=0)
        dow.columns = [f"dow_{c}" for c in dow.columns]

        # Payment type profile
        pago = df_feat.groupby(["estacion","tipo_pago"])["afluencia"].sum().unstack(fill_value=0)
        pago = pago.div(pago.sum(axis=1), axis=0)

        X = pd.concat([dow, pago], axis=1).fillna(0)
        return X

    X_feat = build_features(hash(str(dff.shape)))
    stations_idx = X_feat.index.tolist()
    Xn = X_feat.values.astype(float)

    # ── PCA (manual) ────────────────────────────────────────
    def pca_manual(X, n_components=2):
        Xc = X - X.mean(axis=0)
        cov = np.cov(Xc.T)
        evals, evecs = np.linalg.eigh(cov)
        idx = np.argsort(evals)[::-1]
        evecs = evecs[:, idx]
        return Xc @ evecs[:, :n_components]

    # ── K-Means (manual) ────────────────────────────────────
    def kmeans_manual(X, k, max_iter=300, n_init=5, seed=42):
        best_inertia, best_labels = None, None
        rng = np.random.default_rng(seed)
        for _ in range(n_init):
            centers = X[rng.choice(len(X), k, replace=False)]
            for _ in range(max_iter):
                dists = np.linalg.norm(X[:, None] - centers[None, :], axis=2)
                labels = dists.argmin(axis=1)
                new_centers = np.array([X[labels == c].mean(axis=0) if (labels == c).any() else centers[c] for c in range(k)])
                if np.allclose(centers, new_centers): break
                centers = new_centers
            inertia = sum(np.sum((X[labels == c] - centers[c])**2) for c in range(k))
            if best_inertia is None or inertia < best_inertia:
                best_inertia, best_labels = inertia, labels.copy()
        return best_labels

    with st.spinner("Calculando clusters…"):
        labels = kmeans_manual(Xn, n_clusters)
        pcs = pca_manual(Xn, 2)

    cluster_df = pd.DataFrame({
        "Estación": stations_idx,
        "PC1": pcs[:, 0],
        "PC2": pcs[:, 1],
        "Cluster": [f"Cluster {l+1}" for l in labels],
    })
    # Enrich with line info
    station_linea = dff.groupby("estacion")["linea"].agg(lambda x: x.value_counts().index[0]).to_dict()
    cluster_df["Línea"] = cluster_df["Estación"].map(lambda s: station_linea.get(s,""))

    palette = ["#6366f1","#06b6d4","#10b981","#f59e0b","#f43f5e","#a855f7","#84cc16","#fb923c"]
    fig_clust = px.scatter(cluster_df, x="PC1", y="PC2", color="Cluster",
                           hover_data={"Estación": True, "Línea": True, "PC1": False, "PC2": False},
                           color_discrete_sequence=palette,
                           template="plotly_dark",
                           labels={"PC1":"Componente Principal 1","PC2":"Componente Principal 2"})
    fig_clust.update_traces(marker=dict(size=9, opacity=0.88, line=dict(width=0.5, color="#0a0e1a")))
    fig_clust.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827",
                             font_color="#f1f5f9", height=450,
                             margin={"t":10,"b":10,"l":10,"r":10},
                             legend=dict(bgcolor="rgba(17,24,39,.9)", bordercolor="rgba(99,102,241,.3)", borderwidth=1))
    st.plotly_chart(fig_clust, use_container_width=True)

    # ─── Perfiles de clusters ───
    st.markdown("<div class='section-title'>📋 Perfil de Clusters</div>", unsafe_allow_html=True)
    profile_df = X_feat.copy()
    profile_df["Cluster"] = [f"Cluster {l+1}" for l in labels]

    dow_cols  = [c for c in profile_df.columns if c.startswith("dow_")]
    pago_cols = [c for c in profile_df.columns if not c.startswith("dow_") and c != "Cluster"]

    cluster_profile = profile_df.groupby("Cluster")[dow_cols + pago_cols].mean()
    cluster_profile.columns = (
        [f"% {DIAS_ES[int(c.split('_')[1])]}" for c in dow_cols] +
        [f"% {c}" for c in pago_cols]
    )
    cluster_profile_pct = (cluster_profile * 100).round(1)

    # Count stations per cluster
    count_map = profile_df["Cluster"].value_counts().to_dict()
    cluster_profile_pct.insert(0, "# Estaciones", [count_map.get(idx, 0) for idx in cluster_profile_pct.index])

    st.dataframe(cluster_profile_pct.style.background_gradient(cmap="Blues", subset=[c for c in cluster_profile_pct.columns if "%" in c]),
                 use_container_width=True)

    # ─── Estaciones por cluster ───
    with st.expander("🔍 Ver estaciones por cluster"):
        for cl in sorted(cluster_df["Cluster"].unique()):
            sts = cluster_df[cluster_df["Cluster"] == cl]["Estación"].tolist()
            badges = " ".join(f"<span class='stat-badge'>{s}</span>" for s in sts)
            st.markdown(f"**{cl}** ({len(sts)} estaciones)", unsafe_allow_html=False)
            st.markdown(badges, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 4: PRONÓSTICO
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-title'>📈 Pronóstico de Afluencia Diaria</div>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color:#94a3b8;font-size:.88rem;'>
    Modelo de <b>Suavizamiento Exponencial Triple (Holt-Winters)</b> con estacionalidad semanal,
    entrenado sobre la serie diaria de afluencia total en la selección.
    </p>""", unsafe_allow_html=True)

    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        horizonte = st.slider("Días a pronosticar", 7, 60, 14, key="horiz")

    # Daily series
    daily = dff.groupby("fecha")["afluencia"].sum().reset_index().sort_values("fecha")
    daily.columns = ["fecha","afluencia"]
    daily = daily.set_index("fecha").asfreq("D").fillna(method="ffill")

    if len(daily) < 30:
        st.warning("Se necesitan al menos 30 días de datos para el pronóstico.")
    else:
        try:
            from statsmodels.tsa.holtwinters import ExponentialSmoothing

            split_n = max(14, horizonte)
            train = daily.iloc[:-split_n]
            test  = daily.iloc[-split_n:]

            model = ExponentialSmoothing(
                train["afluencia"],
                trend="add",
                seasonal="add",
                seasonal_periods=7,
                damped_trend=True,
            ).fit(optimized=True, use_brute=False)

            # Forecast full test horizon + additional future points
            n_future = len(test) + horizonte
            forecast_vals = model.forecast(n_future)
            forecast_idx  = pd.date_range(train.index[-1] + timedelta(days=1), periods=n_future, freq="D")
            forecast_series = pd.Series(forecast_vals.values, index=forecast_idx)

            # Confidence intervals (±1.5 sigma from residuals)
            sigma = (train["afluencia"] - model.fittedvalues).std()
            fc_low  = forecast_series - 1.64 * sigma
            fc_high = forecast_series + 1.64 * sigma

            # Metrics on test
            y_true = test["afluencia"].values
            y_pred = forecast_series.iloc[:len(test)].values
            mae  = np.mean(np.abs(y_true - y_pred))
            rmse = np.sqrt(np.mean((y_true - y_pred)**2))
            mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-9))) * 100

            # KPIs
            c1, c2, c3 = st.columns(3)
            c1.metric("MAE",  f"{mae:,.0f} pax", help="Error Absoluto Medio")
            c2.metric("RMSE", f"{rmse:,.0f} pax", help="Raíz del Error Cuadrático Medio")
            c3.metric("MAPE", f"{mape:.1f}%",     help="Error Porcentual Absoluto Medio")

            # Chart
            fig_fc = go.Figure()
            # Training
            fig_fc.add_trace(go.Scatter(x=train.index[-90:], y=train["afluencia"].iloc[-90:],
                                         name="Histórico", line=dict(color="#6366f1", width=1.5)))
            # Test actual
            fig_fc.add_trace(go.Scatter(x=test.index, y=test["afluencia"],
                                         name="Real (validación)", line=dict(color="#10b981", width=2)))
            # Fitted
            fig_fc.add_trace(go.Scatter(x=train.index[-90:], y=model.fittedvalues.iloc[-90:],
                                         name="Ajuste modelo", line=dict(color="#f59e0b", width=1.5, dash="dot")))
            # Forecast
            fig_fc.add_trace(go.Scatter(x=forecast_series.index, y=forecast_series.values,
                                         name="Pronóstico", line=dict(color="#f43f5e", width=2.5)))
            # Confidence interval
            fig_fc.add_trace(go.Scatter(
                x=list(forecast_series.index) + list(forecast_series.index[::-1]),
                y=list(fc_high.values) + list(fc_low.values[::-1]),
                fill="toself", fillcolor="rgba(244,63,94,0.12)",
                line=dict(color="rgba(244,63,94,0)"),
                name="IC 90%", showlegend=True,
            ))
            fig_fc.update_layout(
                paper_bgcolor="#111827", plot_bgcolor="#111827",
                font_color="#f1f5f9", height=420,
                xaxis_title="Fecha", yaxis_title="Pasajeros",
                margin={"t":10,"b":10,"l":10,"r":10},
                legend=dict(bgcolor="rgba(17,24,39,.9)", bordercolor="rgba(99,102,241,.3)", borderwidth=1),
                hovermode="x unified",
            )
            st.plotly_chart(fig_fc, use_container_width=True)

            # Table of upcoming forecast
            future_only = forecast_series.iloc[len(test):len(test)+horizonte]
            ft_df = pd.DataFrame({
                "Fecha": future_only.index.strftime("%Y-%m-%d"),
                "Pronóstico": future_only.values.astype(int),
                "Límite inf.": fc_low.iloc[len(test):len(test)+horizonte].values.astype(int),
                "Límite sup.": fc_high.iloc[len(test):len(test)+horizonte].values.astype(int),
            })
            with st.expander("📋 Ver tabla de pronóstico"):
                st.dataframe(ft_df.set_index("Fecha"), use_container_width=True)

        except Exception as e:
            st.error(f"Error al entrenar el modelo: {e}")


# ══════════════════════════════════════════════════════════════
# TAB 5: ANOMALÍAS
# ══════════════════════════════════════════════════════════════
with tab5:
    st.markdown("<div class='section-title'>🚨 Detección de Anomalías</div>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color:#94a3b8;font-size:.88rem;'>
    Identificamos días con afluencia <b>inusualmente baja o alta</b> usando
    <b>z-score</b> sobre una ventana rodante de 30 días.
    </p>""", unsafe_allow_html=True)

    col_a1, col_a2 = st.columns([1,3])
    with col_a1:
        z_thresh = st.slider("Umbral z-score", 1.5, 4.0, 2.5, step=0.1, key="zthresh")

    daily_all = dff.groupby("fecha")["afluencia"].sum().reset_index().sort_values("fecha")
    daily_all.columns = ["fecha","afluencia"]

    # Rolling stats
    daily_all["roll_mean"] = daily_all["afluencia"].rolling(30, min_periods=7).mean()
    daily_all["roll_std"]  = daily_all["afluencia"].rolling(30, min_periods=7).std()
    daily_all["zscore"]    = (daily_all["afluencia"] - daily_all["roll_mean"]) / (daily_all["roll_std"] + 1)
    daily_all["anomaly"]   = daily_all["zscore"].abs() > z_thresh

    n_anom = daily_all["anomaly"].sum()
    normal  = daily_all[~daily_all["anomaly"]]
    anomaly = daily_all[daily_all["anomaly"]]

    # ─── Chart ───
    fig_anom = go.Figure()
    fig_anom.add_trace(go.Scatter(x=daily_all["fecha"], y=daily_all["roll_mean"],
                                   name="Media móvil 30d", line=dict(color="#6366f1", width=1.5, dash="dash")))
    fig_anom.add_trace(go.Scatter(x=normal["fecha"], y=normal["afluencia"],
                                   name="Normal", mode="lines",
                                   line=dict(color="#10b981", width=1.2), opacity=0.7))
    fig_anom.add_trace(go.Scatter(x=anomaly["fecha"], y=anomaly["afluencia"],
                                   name="Anomalía", mode="markers",
                                   marker=dict(color="#ef4444", size=10, symbol="circle-open",
                                               line=dict(color="#ef4444", width=2))))
    # Shade ±z region
    fig_anom.add_trace(go.Scatter(
        x=list(daily_all["fecha"]) + list(daily_all["fecha"][::-1]),
        y=list((daily_all["roll_mean"] + z_thresh * daily_all["roll_std"])) +
          list((daily_all["roll_mean"] - z_thresh * daily_all["roll_std"])[::-1]),
        fill="toself", fillcolor="rgba(99,102,241,0.08)",
        line=dict(color="rgba(99,102,241,0)"), name=f"Banda ±{z_thresh}σ",
    ))
    fig_anom.update_layout(
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        font_color="#f1f5f9", height=420,
        xaxis_title="Fecha", yaxis_title="Pasajeros",
        margin={"t":10,"b":10,"l":10,"r":10},
        legend=dict(bgcolor="rgba(17,24,39,.9)", bordercolor="rgba(99,102,241,.3)", borderwidth=1),
        hovermode="x unified",
    )
    st.plotly_chart(fig_anom, use_container_width=True)

    # ─── Métricas ───
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Días anómalos detectados", f"{n_anom:,}")
    col_m2.metric("% del total de días", f"{100*n_anom/max(1,len(daily_all)):.1f}%")
    col_m3.metric("Afluencia mínima anómala", f"{int(anomaly['afluencia'].min()):,}" if len(anomaly) > 0 else "N/A")

    # ─── Tabla de anomalías ───
    if len(anomaly) > 0:
        st.markdown("<div class='section-title'>📋 Días con Comportamiento Inusual</div>", unsafe_allow_html=True)
        anom_table = anomaly[["fecha","afluencia","zscore","roll_mean"]].copy()
        anom_table.columns = ["Fecha","Afluencia","Z-Score","Media móvil"]
        anom_table["Fecha"] = anom_table["Fecha"].dt.strftime("%Y-%m-%d")
        anom_table["Z-Score"] = anom_table["Z-Score"].round(2)
        anom_table["Media móvil"] = anom_table["Media móvil"].astype(int)
        anom_table["Desv. %"] = ((anom_table["Afluencia"] - anom_table["Media móvil"]) / (anom_table["Media móvil"]+1) * 100).round(1)
        anom_table = anom_table.sort_values("Fecha")

        st.dataframe(
            anom_table.set_index("Fecha")
                      .style.map(lambda v: "color:#ef4444;font-weight:600" if isinstance(v, float) and abs(v) > z_thresh else "", subset=["Z-Score"]),
            use_container_width=True,
            height=300,
        )

        # ─── Contexto histórico ───
        st.markdown("<div class='section-title'>📰 Contexto de Anomalías</div>", unsafe_allow_html=True)
        known_events = {
            "2021-01": "🦠 COVID-19: Restricciones ene/feb 2021",
            "2021-12": "🎄 Vacaciones diciembre 2021",
            "2022-04": "✝️ Semana Santa 2022",
            "2022-09": "🎉 Fiestas Patrias Sept 2022",
            "2023-04": "✝️ Semana Santa 2023",
            "2023-09": "🎉 Fiestas Patrias Sept 2023",
            "2024-01": "🎆 Año Nuevo 2024",
            "2024-04": "✝️ Semana Santa 2024",
            "2024-12": "🎄 Vacaciones diciembre 2024",
            "2025-04": "✝️ Semana Santa 2025",
            "2025-12": "🎄 Vacaciones diciembre 2025",
            "2026-01": "🎆 Año Nuevo 2026",
        }
        st.markdown("""
        <div class='anomaly-legend'>
        Las anomalías detectadas suelen coincidir con:<br>
        """ + " &nbsp;".join(f"<span class='stat-badge'>{v}</span>" for v in known_events.values()) + """
        </div>""", unsafe_allow_html=True)

    # ─── Z-score distribution ───
    st.markdown("<div class='section-title'>📊 Distribución de Z-Scores</div>", unsafe_allow_html=True)
    fig_hist = px.histogram(daily_all.dropna(subset=["zscore"]), x="zscore",
                             nbins=50, color_discrete_sequence=["#6366f1"],
                             template="plotly_dark",
                             labels={"zscore":"Z-Score","count":"Frecuencia"})
    fig_hist.add_vline(x= z_thresh, line_color="#ef4444", line_dash="dash", annotation_text=f"+{z_thresh}σ")
    fig_hist.add_vline(x=-z_thresh, line_color="#ef4444", line_dash="dash", annotation_text=f"-{z_thresh}σ")
    fig_hist.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827",
                            font_color="#f1f5f9", height=280,
                            margin={"t":30,"b":10,"l":10,"r":10})
    st.plotly_chart(fig_hist, use_container_width=True)
