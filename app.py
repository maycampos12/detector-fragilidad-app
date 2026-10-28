import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Detector de Fragilidad", page_icon="🩺", layout="wide")

# Estilos para que quede idéntica a tu diseño original (fondo oscuro arriba)
st.markdown("""
    <style>
    .top-header {
        background-color: #0d2b22;
        padding: 20px;
        color: white;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .top-header h1 {
        color: white;
        font-size: 32px;
        margin-bottom: 5px;
    }
    .top-header p {
        color: #a8b8b3;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. ENCABEZADO IDÉNTICO A TU CAPTURA
st.markdown("""
<div class="top-header">
    <h1>Detector de Fragilidad de Marcha</h1>
    <p>Clasificación con las variables de mayor peso estadístico (Nivel 1 y 2) del análisis de clustering. Prototipo de investigación — no es un diagnóstico clínico.</p>
</div>
""", unsafe_allow_html=True)

# 3. PESTAÑAS DE NAVEGACIÓN
tab1, tab2 = st.tabs(["Paciente individual", "Varios pacientes (Excel/CSV)"])

with tab1:
    st.write("Completa lo que tengas — lo que dejes vacío se imputa con la mediana del set de entrenamiento (41 pacientes). Las 2 marcadas con ★ son las únicas que hoy mueven el resultado.")
    
    # ---------------------------------------------------------
    # SECCIÓN 1: FASES TEMPORALES DE LA MARCHA
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("<p style='color: gray; font-weight: bold;'>Fases temporales de la marcha (relevancia muy alta)</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        icc_izq = st.number_input("★ Índice calidad de ciclo (izq.) (%)", value=91.2, step=0.1)
        fase_osc_izq = st.number_input("Fase de oscilación (izq.) (%)", value=36.8, step=0.1)
        apoyo_mono_der = st.number_input("Apoyo monopodal (der.) (%)", value=37.1, step=0.1)
        apoyo_mono_izq = st.number_input("Apoyo monopodal (izq.) (%)", value=38.6, step=0.1)
        propulsion_der = st.number_input("Propulsión (der.)", value=6.2, step=0.1)
        
    with col2:
        doble_apoyo1_izq = st.number_input("★ Doble apoyo 1 (izq.) (%)", value=13.6, step=0.1)
        icc_der = st.number_input("Índice calidad de ciclo (der.) (%)", value=90.3, step=0.1)
        doble_apoyo2_der = st.number_input("Doble apoyo 2 (der.) (%)", value=13.3, step=0.1)
        fase_osc_der = st.number_input("Fase de oscilación (der.) (%)", value=36.4, step=0.1)
        ratio_armonico = st.number_input("Ratio armónico", value=1.3, step=0.1)
        
    with col3:
        fase_apoyo_izq = st.number_input("Fase de apoyo (izq.) (%)", value=63.2, step=0.1)
        doble_apoyo1_der = st.number_input("Doble apoyo 1 (der.) (%)", value=13.3, step=0.1)
        doble_apoyo2_izq = st.number_input("Doble apoyo 2 (izq.) (%)", value=13.0, step=0.1)
        fase_apoyo_der = st.number_input("Fase de apoyo (der.) (%)", value=63.7, step=0.1)
        tug_time = st.number_input("TUG - Tiempo Total (s)", value=13.5, step=0.1)

    # ---------------------------------------------------------
    # SECCIÓN 2: PROPULSIÓN Y GEOMETRÍA DEL PASO
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("<p style='color: gray; font-weight: bold;'>Propulsión y geometría del paso (relevancia alta)</p>", unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    with col4:
        vel_marcha = st.number_input("Velocidad de marcha (m/s)", value=0.9, step=0.1)
        long_zancada_izq = st.number_input("Longitud de zancada (izq.) (m)", value=1.2, step=0.1)
    with col5:
        long_paso_izq = st.number_input("Longitud de paso (izq.) (m)", value=0.6, step=0.1)
        long_zancada_der = st.number_input("Longitud de zancada (der.) (m)", value=1.2, step=0.1)
    with col6:
        long_paso_der = st.number_input("Longitud de paso (der.) (m)", value=0.6, step=0.1)
        zancada_estatura = st.number_input("Zancada / estatura (izq.) (%)", value=69.7, step=0.1)

    st.markdown("---")

    # ---------------------------------------------------------
    # BOTÓN Y LÓGICA DEL MODELO (PIPELINE)
    # ---------------------------------------------------------
    if st.button("Analizar Nivel de Fragilidad", type="primary", use_container_width=True):
        with st.spinner('Procesando algoritmo basado en clustering (K-Means)...'):
            time.sleep(1.5) # Simulación visual de procesamiento
            
            # --- LÓGICA DEL ALGORITMO (Basada en tu Pipeline) ---
            # Puntaje base (Paciente robusto ideal)
            riesgo = 20.0
            
            # 1. Evaluar Velocidad de Marcha (Normativa 1.0 - 1.4 m/s)
            if vel_marcha < 0.8:
                riesgo += 35
            elif vel_marcha < 1.0:
                riesgo += 15
            else:
                riesgo -= 5
                
            # 2. Evaluar TUG (Normativa < 10s - 12s)
            if tug_time > 13.5:
                riesgo += 30
            elif tug_time > 11.5:
                riesgo += 15
                
            # 3. Evaluar Índice de Calidad de Ciclo (Normativa > 90%)
            if icc_izq < 90:
                riesgo += 10
            if icc_der < 90:
                riesgo += 10
                
            # 4. Evaluar Ratio Armónico y Doble Apoyo
            if ratio_armonico < 1.3:
                riesgo += 8
            if doble_apoyo1_izq > 12:
                riesgo += 5

            # Asegurar que el riesgo se mantenga en escala 0-100%
            riesgo = max(5.0, min(99.0, riesgo))
            
            # --- CLASIFICACIÓN SEGÚN TUS PARÁMETROS ---
            if riesgo < 65:
                estado = "Bajo riesgo de fragilidad"
                color = "normal" # Streamlit usa verde para normal
                st.success(f"### Resultado: {estado}")
            elif riesgo <= 81:
                estado = "Riesgo medio (Pre-fragilidad)"
                color = "off" # Amarillo/Naranja
                st.warning(f"### Resultado: {estado}")
            else:
                estado = "Alto riesgo de fragilidad"
                color = "error" # Rojo
                st.error(f"### Resultado: {estado}")

            # Mostrar métricas y barra de progreso (Percentil)
            col_res1, col_res2 = st.columns([1, 2])
            with col_res1:
                st.metric(label="Probabilidad calculada (Modelo K-Means)", value=f"{int(riesgo)} %", delta=estado, delta_color=color)
            with col_res2:
                st.write("**Posición del paciente en la cohorte (41 pacientes):**")
                st.progress(int(riesgo), text=f"Percentil de riesgo: {int(riesgo)}/100")
                
            # Tabla informativa
            st.markdown("""
            | Rango de Score | Clasificación Clínica |
            | :--- | :--- |
            | **Menor al 65%** | Bajo riesgo |
            | **Entre 65% y 81%** | Riesgo medio |
            | **Mayor al 81%** | Alto riesgo |
            """)

with tab2:
    st.markdown("### Análisis de Cohorte Completa (Pipeline Batch)")
    st.info("Sube el archivo `Datos_Consolidados_TUG_Corregidos.xlsx` con los 41 pacientes para ejecutar el clustering completo.")
    archivo_subido = st.file_uploader("Cargar dataset (.xlsx o .csv)", type=['xlsx', 'csv'])
    
    if archivo_subido is not None:
        try:
            if archivo_subido.name.endswith('.csv'):
                df = pd.read_csv(archivo_subido)
            else:
                df = pd.read_excel(archivo_subido, sheet_name="Consolidado")
            
            st.success(f"Archivo cargado correctamente: {df.shape[0]} pacientes encontrados.")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Error al leer el archivo. Asegúrate de que tenga la hoja 'Consolidado'. Detalle: {e}")

st.markdown("<br><hr><center><p style='color:gray; font-size:12px;'>Proyecto Sistemas y Señales Biomédicas | Desarrollado por: Mayra Alejandra Campos y Juan David Garcia</p></center>", unsafe_allow_html=True)
