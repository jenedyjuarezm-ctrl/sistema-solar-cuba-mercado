"""Dashboard interactivo de solineras con Streamlit."""
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE = Path(__file__).parent.parent
DATA = BASE / "data"

st.set_page_config(page_title="Solinera Dashboard", layout="wide", page_icon="☀️")


@st.cache_data
def cargar_encuestas():
    p = DATA / "clean" / "encuestas_consolidadas.parquet"
    if not p.exists():
        return pd.DataFrame()
    return pd.read_parquet(p)


@st.cache_data
def cargar_onei():
    p = DATA / "raw" / "externas" / "onei_anuario.csv"
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)


def main():
    st.title("☀️ Dashboard - Sistemas Fotovoltaicos en Cuba")
    st.markdown("**Proyecto de ciencia de datos 2020–2026**")

    df = cargar_encuestas()
    onei = cargar_onei()

    if df.empty and onei.empty:
        st.warning(
            "No hay datos cargados. Ejecuta primero:\n"
            "```\npython solineras/extraer_onei.py\npython solineras/consolidar.py\n```"
        )
        return

    st.sidebar.header("Filtros")
    if not df.empty and "tipo_entidad" in df.columns:
        tipos = ["Todos"] + df["tipo_entidad"].dropna().unique().tolist()
        tipo_sel = st.sidebar.selectbox("Tipo de entidad", tipos)
        if tipo_sel != "Todos":
            df = df[df["tipo_entidad"] == tipo_sel]

    if not df.empty and "ubicacion" in df.columns:
        provincias = ["Todas"] + sorted(df["ubicacion"].dropna().astype(str).unique().tolist())
        prov_sel = st.sidebar.selectbox("Ubicacion", provincias)
        if prov_sel != "Todas":
            df = df[df["ubicacion"] == prov_sel]

    st.sidebar.markdown(f"**Registros filtrados:** {len(df)}")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📈 Series temporales",
        "🕐 Patrones",
        "🔗 Correlaciones",
        "🧪 Avanzado",
        "🔮 Pronóstico",
        "🔋 Optimización",
        "📋 Datos",
    ])

    with tab1:
        st.header("Series temporales — ONEI 2020–2024")
        if not onei.empty:
            indicadores = onei["indicador"].unique().tolist()
            sel = st.selectbox("Indicador", indicadores)
            s = onei[onei["indicador"] == sel].sort_values("anio")
            fig = px.line(s, x="anio", y="valor", markers=True, title=sel)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("Patrones por tipo de entidad")
        if not df.empty and "tipo_entidad" in df.columns:
            vars_num = ["potencia_pico_kwp", "consumo_total_anual_kwh", "pr_promedio"]
            vars_num = [v for v in vars_num if v in df.columns]
            if vars_num:
                var = st.selectbox("Variable", vars_num)
                fig = px.box(df, x="tipo_entidad", y=var, color="tipo_entidad")
                st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("Correlaciones")
        if not df.empty:
            vars_num = df.select_dtypes(include="number").columns.tolist()
            if len(vars_num) >= 2:
                x = st.selectbox("Eje X", vars_num, index=0)
                y = st.selectbox("Eje Y", vars_num, index=1)
                color = "tipo_entidad" if "tipo_entidad" in df.columns else None
                fig = px.scatter(df, x=x, y=y, color=color)
                st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.header("Análisis avanzado")
        if not df.empty:
            st.subheader("Distribución de variables")
            var = st.selectbox("Variable numérica",
                               df.select_dtypes(include="number").columns.tolist(),
                               key="adv")
            fig = px.histogram(df, x=var, nbins=20)
            st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.header("Pronóstico")
        if not onei.empty:
            s = onei[onei["indicador"] == "eolica_fotovoltaica_gwh"].sort_values("anio")
            if len(s) >= 2:
                from sklearn.linear_model import LinearRegression
                import numpy as np
                X = s["anio"].values.reshape(-1, 1)
                y = s["valor"].values
                m = LinearRegression().fit(X, y)
                fut = np.array([[2025], [2026], [2027]])
                pred = m.predict(fut)
                st.write(f"R² = {m.score(X, y):.3f}")
                forecast = pd.DataFrame({"anio": [2025, 2026, 2027], "pronostico": pred})
                combined = pd.concat([
                    s[["anio", "valor"]].rename(columns={"valor": "pronostico"}),
                    forecast,
                ])
                fig = px.line(combined, x="anio", y="pronostico", markers=True)
                st.plotly_chart(fig, use_container_width=True)

    with tab6:
        st.header("Optimización de almacenamiento")
        st.info("Simulador: ajusta capacidad de batería para maximizar autoconsumo.")
        st.write("(Disponible cuando se implemente `optimizacion.py`)")

    with tab7:
        st.header("Datos crudos")
        if not df.empty:
            st.dataframe(df)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Descargar CSV", csv, "datos_filtrados.csv", "text/csv")
        else:
            st.info("No hay encuestas cargadas aún.")

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Proyecto académico — 2026**")


if __name__ == "__main__":
    main()
