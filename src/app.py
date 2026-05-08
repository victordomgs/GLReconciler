import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(__file__))
from agent import detectar_breaks, analizar_con_claude
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="GL Reconciler Demo", page_icon="🏦", layout="wide")
st.title("🏦 GL Reconciler — Agente de Conciliación")
st.caption("Demo · Powered by Claude")

st.subheader("1. Carga los extractos")
col1, col2 = st.columns(2)
with col1:
    banco_file = st.file_uploader("Extracto bancario (CSV)", type="csv")
with col2:
    gl_file = st.file_uploader("Libro mayor GL (CSV)", type="csv")

if banco_file and gl_file:
    os.makedirs("data", exist_ok=True)
    banco_path = "data/upload_banco.csv"
    gl_path    = "data/upload_gl.csv"
    with open(banco_path, "wb") as f: f.write(banco_file.read())
    with open(gl_path,    "wb") as f: f.write(gl_file.read())

    st.subheader("2. Breaks detectados")
    resultado = detectar_breaks(banco_path, gl_path)

    if resultado["n_breaks"] == 0:
        st.success("✅ Sin breaks. Conciliación limpia.")
    else:
        st.error(f"⚠️ {resultado['n_breaks']} breaks detectados")
        df_breaks = pd.DataFrame(resultado["breaks"])
        st.dataframe(df_breaks, use_container_width=True)

        st.subheader("3. Análisis del agente")
        if st.button("🤖 Analizar con Claude", type="primary"):
            with st.spinner("El agente está analizando los breaks..."):
                analisis = analizar_con_claude(resultado)
            st.markdown(analisis)

            st.subheader("4. Decisión")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ Aprobar y cerrar conciliación", use_container_width=True):
                    st.success("Conciliación aprobada y registrada.")
            with col_b:
                if st.button("🔺 Escalar a director financiero", use_container_width=True):
                    st.warning("Breaks escalados. Se ha notificado al responsable.")
else:
    st.info("👆 Sube los dos archivos CSV para comenzar. Puedes usar los sintéticos de /data")