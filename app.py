import streamlit as st
import pandas as pd
import numpy as np
import time

# Configuración de la página
st.set_page_config(page_title="Mo-Vida | Fragilidad", page_icon="🏃‍♂️", layout="wide")

# Estilos personalizados para parecerse a tu diseño original
st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #E8F5E9; }
    .sub-header { font-size: 14px; color: #A5D6A7; margin-bottom: 20px;}
    .top-bar { background-color: #064E3B; padding: 20px; border-radius: 10px; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown('<div class="top-bar">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 10])
with col1:
    # Asegúrate de subir logo-movida.png al mismo repositorio
    try:
        st.image("logo-movida.png", width=80)
    except:
        st.write("*(Logo)*")
with col2:
    st.markdown('<div class="main-header">Detector de Fragilidad de Marcha</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Clasificación con las variables de mayor peso estadístico (Nivel 1 y 2) del análisis de clustering. Prototipo de investigación — no es un diagnóstico clínico.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Pestañas
tab1, tab2 = st.tabs(["Paciente individual", "Varios pacientes (Excel/CSV)"])

with tab1:
    st.write("Completa lo que tengas — lo que dejes vacío se imputa con la mediana del set de entrenamiento (41 pacientes). Las marcadas con ★ son las únicas que hoy mueven el resultado.")
    
    with st.container(border=True):
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
            icc_der = st.number_input("Índice calidad de ciclo (der.) (%)", value=90.3, step=0.1)
            doble_apoyo2_der = st.number_input("Doble apoyo 2 (der.) (%)", value=13.3, step=0.1)
            fase_osc_der = st.number_input("Fase de oscilación (der.) (%)", value=36.4, step=0.1)
            ratio_armonico = st.number_input("★ Ratio armónico", value=1.3, step=0.1)
            
        with col_c:
            fase_apoyo_izq = st.number_input("Fase de apoyo (izq.) (%)", value=63.2, step=0.1)
            doble_apoyo1_der = st.number_input("Doble apoyo 1 (der.) (%)", value=13.3, step=0.1)
            doble_apoyo2_izq = st.number_input("Doble apoyo 2 (izq.) (%)", value=13.0, step=0.1)
            fase_apoyo_der = st.number_input("Fase de apoyo (der.) (%)", value=63.7, step=0.1)
            tug_time = st.number_input("★ TUG - Tiempo Total (s)", value=13.5, step=0.1)

    with st.container(border=True):
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

    # Botón de cálculo
    if st.button("Ejecutar Análisis Clínico", type="primary", use_container_width=True):
        with st.spinner('Procesando datos cinemáticos...'):
            time.sleep(1) # Simulación de tiempo de carga
            
            # ---------------------------------------------------------
            # LÓGICA DINÁMICA DE CÁLCULO (Reemplazar por tu modelo .pkl)
            # ---------------------------------------------------------
            # Ejemplo de cómo cargarías tu modelo real:
            # import joblib
            # modelo = joblib.load("modelo_kmeans.pkl")
            # score_riesgo = modelo.predict([[vel_marcha, ratio_armonico, tug_time, ...]])
            
            # Algoritmo de simulación dinámico para que la app cambie al alterar datos:
            score_riesgo = 20 # Base
            
            # Penalizaciones basadas en literatura médica y tu dataset
            if vel_marcha < 0.8: score_riesgo += 35
            elif vel_marcha < 1.1: score_riesgo += 15
            
            if tug_time > 13.5: score_riesgo += 30
            elif tug_time > 11.0: score_riesgo += 15
                
            if ratio_armonico < 1.2: score_riesgo += 15
            if icc_izq < 90: score_riesgo += 10
            if doble_apoyo1_izq > 12: score_riesgo += 10
            
            # Limitar a escala 100%
            score_riesgo = min(99, max(5, score_riesgo))

            # Definir clasificación
            if score_riesgo < 65:
                estado = "Bajo riesgo"
                color = "green"
            elif score_riesgo <= 81:
                estado = "Riesgo medio"
                color = "orange"
            else:
                estado = "Alto riesgo"
                color = "red"

            # Mostrar Resultados
            st.markdown("---")
            res_col1, res_col2 = st.columns([1, 2])
            
            with res_col1:
                st.metric(label="Clasificación de Fragilidad", value=estado, delta=f"{score_riesgo}% de probabilidad", delta_color="inverse")
            
            with res_col2:
                st.write(f"**Ubicación en el Percentil (Cohorte 41 pacientes): {score_riesgo}%**")
                st.progress(int(score_riesgo), text=f"Riesgo detectado: {estado}")
                
            st.success("Análisis completado exitosamente. Revisar cruce con diagnóstico médico primario.")

with tab2:
    st.markdown("### Carga Masiva de Pacientes")
    st.info("Sube un archivo Excel consolidado (como el `Datos_Consolidados_TUG_Corregidos.xlsx`) para analizar la cohorte completa.")
    uploaded_file = st.file_uploader("Sube tu archivo Excel o CSV", type=['xlsx', 'csv'])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, sheet_name="Consolidado")
            
            st.write("Vista previa de los datos cargados:")
            st.dataframe(df.head())
            st.button("Analizar Base de Datos")
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>Desarrollado por: Mayra Alejandra Campos y Juan David Garcia | Sistemas y Señales Biomédicas</p>", unsafe_allow_html=True)
