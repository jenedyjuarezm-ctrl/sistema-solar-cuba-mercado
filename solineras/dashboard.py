"""
Dashboard interactivo verificado para el análisis de energía solar en Cuba.
Ejecutar con: streamlit run solineras/dashboard.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Análisis Solar Cuba", page_icon="☀️", layout="wide")

BASE = Path(__file__).parent.parent
DATA = BASE / "data"

@st.cache_data
def cargar_datos():
    enc, onei, nasa = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    p_enc = DATA / "clean" / "encuestas_consolidadas.parquet"
    if p_enc.exists(): enc = pd.read_parquet(p_enc)
    
    p_onei = DATA / "clean" / "onei_generacion.parquet"
    if p_onei.exists(): onei = pd.read_parquet(p_onei)
    
    p_nasa = DATA / "clean" / "nasa_power_limpio.parquet"
    if p_nasa.exists(): nasa = pd.read_parquet(p_nasa)
    
    return enc, onei, nasa

def main():
    st.title("☀️ Transición Energética en Cuba (2020-2026)")
    st.markdown("Análisis de la adopción solar y la crisis eléctrica.")
    
    df, onei, nasa = cargar_datos()
    
    if df.empty and onei.empty:
        st.error("⚠️ No se encontraron datos. Ejecuta `python solineras/run_all.py` primero.")
        return

    # Sidebar
    st.sidebar.header("Filtros")
    if not df.empty:
        tipos = ["Todos"] + df["tipo_entidad"].unique().tolist()
        tipo_sel = st.sidebar.selectbox("Tipo de Entidad", tipos)
        if tipo_sel != "Todos":
            df = df[df["tipo_entidad"] == tipo_sel]
        st.sidebar.markdown(f"**Registros filtrados:** {len(df)}")

    # Pestañas
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Entrevistas (Campo)", 
        "📈 Crisis (ONEI)", 
        "🔗 Clima y Correlaciones (NASA)",
        "📋 Tabla de Datos"
    ])

    # --- TAB 1: ENTREVISTAS ---
    with tab1:
        st.header("Resultados de la Investigación de Campo")
        if not df.empty:
            # Limpiar nulos solo para graficar
            df_plot = df.dropna(subset=['potencia_pico_kwp', 'capacidad_baterias_kwh'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Potencia Instalada (kWp)")
                fig1 = px.box(df_plot, x="tipo_entidad", y="potencia_pico_kwp", color="tipo_entidad")
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                st.subheader("Baterías (kWh)")
                fig2 = px.box(df_plot, x="tipo_entidad", y="capacidad_baterias_kwh", color="tipo_entidad")
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No hay datos de entrevistas.")

    # --- TAB 2: SERIES TEMPORALES (ONEI) ---
    with tab2:
        st.header("Evolución del Sistema Eléctrico Nacional (2020-2022)")
        if not onei.empty:
            # CORRECCIÓN: Usamos dos gráficos separados porque las escalas son muy diferentes
            st.subheader("Generación Total (GW·h)")
            fig_total = px.line(onei, x="anio", y="gen_total_gwh", markers=True, color_discrete_sequence=['#2a6f97'])
            st.plotly_chart(fig_total, use_container_width=True)
            
            st.subheader("Generación Fotovoltaica (GW·h)")
            fig_fv = px.line(onei, x="anio", y="gen_fv_gwh", markers=True, color_discrete_sequence=['#f4a900'])
            st.plotly_chart(fig_fv, use_container_width=True)
            
            st.info("Nota: La generación total cayó drásticamente (-17%), mientras la FV se mantuvo estable.")
        else:
            st.info("No hay datos de la ONEI.")

    # --- TAB 3: CORRELACIONES (NASA) ---
    with tab3:
        st.header("El impacto del clima (NASA)")
        if not nasa.empty and not onei.empty:
            # 1. Agrupar NASA por año
            nasa_anual = nasa.groupby('anio').agg({
                'irradiancia_kwh_m2': 'mean',
                'temperatura_c': 'mean'
            }).reset_index()
            
            # 2. Cruzar con ONEI
            df_corr = onei.merge(nasa_anual, on='anio')
            
            st.subheader("Relación: Irradiancia vs Generación Total")
            fig4 = px.scatter(df_corr, x="irradiancia_kwh_m2", y="gen_total_gwh", 
                              text="anio", size=[100]*len(df_corr), color_discrete_sequence=['#2ca02c'])
            fig4.update_traces(textposition='top center')
            st.plotly_chart(fig4, use_container_width=True)
            
            st.subheader("Temperatura Promedio por Mes (2020-2024)")
            # CORRECCIÓN: Ordenar los meses cronológicamente para que no se vea desordenado
            meses = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
            nasa['mes'] = pd.Categorical(nasa['mes'], categories=meses, ordered=True)
            nasa_mes = nasa.groupby('mes', observed=True).mean(numeric_only=True).reset_index()
            
            fig5 = px.bar(nasa_mes, x="mes", y="temperatura_c", color_discrete_sequence=['#d62728'])
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.info("Faltan datos de la NASA o la ONEI para hacer la correlación.")

    # --- TAB 4: TABLA DE DATOS ---
    with tab4:
        st.header("Dataset Consolidado")
        if not df.empty:
            st.dataframe(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar CSV", csv, "datos_cuba.csv", "text/csv")
        else:
            st.info("No hay datos para mostrar.")

if __name__ == "__main__":
    main()
