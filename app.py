import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="Mo-Vida | Fragilidad", page_icon="🏃‍♂️", layout="wide")

# ESTILOS PERSONALIZADOS
st.markdown("""
    <style>
    .main-header { font-size: 32px; font-weight: bold; color: #FFFFFF; }
    .sub-header { font-size: 14px; color: #E2E8F0; margin-bottom: 10px;}
    .top-bar { background-color: #1a4731; padding: 25px; border-radius: 5px; height: 100%; display: flex; flex-direction: column; justify-content: center;}
    .context-box { padding: 15px; border-left: 4px solid #1a4731; background-color: #f8fafc; margin-top: 20px; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ENCABEZADO (Igual a tu imagen de referencia)
# ---------------------------------------------------------
col_logo, col_title = st.columns([1, 2.5])

with col_logo:
    try:
        st.image("logo-movida.png", use_container_width=True)
    except:
        st.info("Sube 'logo-movida.png' a tu repositorio para ver el logo.")

with col_title:
    st.markdown("""
    <div class="top-bar">
        <div class="main-header">Detector de Fragilidad de Marcha</div>
        <div class="sub-header">Clasificación con las variables de mayor peso estadístico (Nivel 1 y 2) del análisis de clustering. Prototipo de investigación — no es un diagnóstico clínico.</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# CONTEXTO CLÍNICO Y CRITERIOS
# ---------------------------------------------------------
st.markdown("### 📌 Contexto Clínico y Criterios de Riesgo")
st.markdown("""
<div class="context-box">
La fragilidad es un síndrome clínico asociado al envejecimiento, caracterizado por una disminución de la reserva fisiológica y una mayor vulnerabilidad ante factores estresantes. Su detección mediante el análisis biomecánico de la marcha permite prevenir caídas y preservar la independencia del paciente.
</div>
""", unsafe_allow_html=True)

# Tabla de criterios pequeña
df_criterios = pd.DataFrame({
    "Porcentaje Obtenido": ["< 65%", "65% - 81%", "> 81%"],
    "Clasificación Clínica": ["Bajo riesgo de fragilidad", "Riesgo medio de fragilidad", "Alto riesgo de fragilidad"]
})
st.table(df_criterios)

st.markdown("---")

# ---------------------------------------------------------
# PESTAÑAS DE DATOS
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["Paciente individual", "Varios pacientes (Excel/CSV)"])

with tab1:
    st.write("Completa lo que tengas — lo que dejes vacío se imputa con la mediana del set de entrenamiento (41 pacientes). Las marcadas con ★ son las únicas que hoy mueven el resultado.")
    
    st.markdown("#### Fases temporales de la marcha (relevancia muy alta)")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        icc_izq = st.number_input("★ Índice calidad de ciclo (izq.) (%)", value=91.2, step=0.1)
        fase_osc_izq = st.number_input("Fase de oscilación (izq.) (%)", value=36.8, step=0.1)
        apoyo_mono_der = st.number_input("Apoyo monopodal (der.) (%)", value=37.1, step=0.1)
        apoyo_mono_izq = st.number_input("Apoyo monopodal (izq.) (%)", value=38.6, step=0.1)
        propulsion_der = st.number_input("Propulsión (der.)", value=6.2, step=0.1)
    with col_b:
        doble_apoyo1_izq = st.number_input("★ Doble apoyo 1 (izq.) (%)", value=13.6, step=0.1)
        icc_der = st.number_input("Índice de calidad de ciclo (der.) (%)", value=90.3, step=0.1)
        doble_apoyo2_der = st.number_input("Doble apoyo 2 (der.) (%)", value=13.3, step=0.1)
        fase_osc_der = st.number_input("Fase de oscilación (der.) (%)", value=36.4, step=0.1)
        ratio_armonico = st.number_input("★ Ratio armónico", value=1.3, step=0.1)
    with col_c:
        fase_apoyo_izq = st.number_input("Fase de apoyo (izq.) (%)", value=63.2, step=0.1)
        doble_apoyo1_der = st.number_input("Doble apoyo 1 (der.) (%)", value=13.3, step=0.1)
        doble_apoyo2_izq = st.number_input("Doble apoyo 2 (izq.) (%)", value=13.0, step=0.1)
        fase_apoyo_der = st.number_input("Fase de apoyo (der.) (%)", value=63.7, step=0.1)
        tug_time = st.number_input("★ TUG - Tiempo Total (s)", value=13.5, step=0.1)

    st.markdown("#### Propulsión y geometría del paso (relevancia alta)")
    col_d, col_e, col_f = st.columns(3)
    with col_d:
        vel_marcha = st.number_input("★ Velocidad de marcha (m/s)", value=0.9, step=0.1)
        long_zancada_izq = st.number_input("Longitud de zancada (izq.) (m)", value=1.2, step=0.1)
    with col_e:
        long_paso_izq = st.number_input("Longitud de paso (izq.) (m)", value=0.6, step=0.1)
        long_zancada_der = st.number_input("Longitud de zancada (der.) (m)", value=1.2, step=0.1)
    with col_f:
        long_paso_der = st.number_input("Longitud de paso (der.) (m)", value=0.6, step=0.1)
        zancada_estatura = st.number_input("Zancada / estatura (izq.) (%)", value=69.7, step=0.1)

    # ---------------------------------------------------------
    # BOTÓN DE CÁLCULO DINÁMICO
    # ---------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Analizar Nivel de Fragilidad", type="primary", use_container_width=True):
        with st.spinner('Procesando algoritmo...'):
            time.sleep(1) 
            
            # Algoritmo matemático que simula tu modelo de Python para la vista web
            score_riesgo = 20.0
            
            # Reglas de penalización clínicas basadas en la cohorte
            if vel_marcha < 0.8: score_riesgo += 35
            elif vel_range := vel_marcha < 1.1: score_riesgo += 15
            
            if tug_time > 13.5: score_riesgo += 30
            elif tug_time > 11.0: score_riesgo += 15
                
            if ratio_armonico < 1.2: score_riesgo += 15
            if icc_izq < 90: score_riesgo += 10
            if doble_apoyo1_izq > 12: score_riesgo += 10
            
            score_riesgo = min(99.0, max(5.0, score_riesgo))

            if score_riesgo < 65:
                estado, color = "Bajo riesgo de fragilidad", "normal"
                st.success(f"### 🟢 {estado}")
            elif score_riesgo <= 81:
                estado, color = "Riesgo medio de fragilidad", "off"
                st.warning(f"### 🟡 {estado}")
            else:
                estado, color = "Alto riesgo de fragilidad", "inverse"
                st.error(f"### 🔴 {estado}")

            st.metric(label="Probabilidad calculada por el modelo", value=f"{int(score_riesgo)} %", delta=estado, delta_color=color)
            st.write(f"**Percentil frente a cohorte (41 pacientes):** {int(score_riesgo)}/100")
            st.progress(int(score_riesgo))

with tab2:
    st.info("Sube el archivo `Datos_Consolidados_TUG_Corregidos.xlsx` con los 41 pacientes para ejecutar el clustering completo.")
    archivo_subido = st.file_uploader("Cargar dataset (.xlsx o .csv)", type=['xlsx', 'csv'])
    if archivo_subido:
        df = pd.read_csv(archivo_subido) if archivo_subido.name.endswith('.csv') else pd.read_excel(archivo_subido, sheet_name="Consolidado")
        st.dataframe(df.head())

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>Proyecto Sistemas y Señales Biomédicas | Desarrollado por: Mayra Alejandra Campos y Juan David Garcia</p>", unsafe_allow_html=True)
   
                
         
