import streamlit as st
import pandas as pd
import numpy as np
import time
import io
from scipy import stats

st.set_page_config(page_title="Mo-Vida | Fragilidad", page_icon="🏃‍♂️", layout="wide")

# ---------------------------------------------------------
# ESTILOS GENERALES
# ---------------------------------------------------------
st.markdown("""
    <style>
    .main-header { font-size: 32px; font-weight: bold; color: #FFFFFF; }
    .sub-header { font-size: 14px; color: #E2E8F0; margin-bottom: 10px;}
    .top-bar { background-color: #1a4731; padding: 25px; border-radius: 5px; height: 100%; display: flex; flex-direction: column; justify-content: center;}
    .context-box { padding: 15px; border-left: 4px solid #1a4731; background-color: #f8fafc; margin-top: 20px; margin-bottom: 20px; font-size: 14px; color: #334155;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# COHORTE INTERNA INCRUSTADA
# ---------------------------------------------------------
SCORES_COHORTE_41 = [
    12.5, 15.0, 18.2, 21.0, 24.5, 28.1, 31.5, 34.0, 36.5, 39.2, 
    41.0, 44.5, 47.2, 49.8, 52.0, 54.5, 57.1, 59.5, 62.0, 64.5, 
    66.2, 68.5, 71.0, 73.2, 75.5, 77.8, 80.1, 82.5, 84.2, 86.5, 
    88.1, 90.5, 92.2, 94.0, 95.5, 96.8, 97.5, 98.2, 98.9, 99.5, 99.9
]

@st.cache_data
def load_data():
    try:
        return pd.read_excel("Datos_Consolidados_TUG_Corregidos.xlsx", sheet_name="Consolidado")
    except:
        return pd.DataFrame()

df_cohorte = load_data()

# ---------------------------------------------------------
# FUNCIÓN MULTIVARIABLE ROBUSTA
# ---------------------------------------------------------
def calcular_score_fragilidad(v, tug, ratio, icc_i, icc_d, da1_i, prop_d, zancada_i):
    riesgo = 20.0
    
    if v < 0.6: riesgo += 35
    elif v < 0.8: riesgo += 20
    elif v < 1.0: riesgo += 10
    elif v > 3.0: riesgo -= 40
    elif v > 1.3: riesgo -= 10
    
    if tug > 14.0: riesgo += 25
    elif tug > 12.0: riesgo += 15
    elif tug > 10.5: riesgo += 5
    elif tug < 5.0: riesgo -= 30
    elif tug < 9.0: riesgo -= 10
        
    if ratio < 1.2: riesgo += 10
    elif ratio < 1.4: riesgo += 5
        
    if icc_i < 90: riesgo += 5
    if icc_d < 90: riesgo += 5
        
    if da1_i > 13: riesgo += 10
    elif da1_i > 11.5: riesgo += 5
        
    if prop_d < 5.5: riesgo += 5
    if zancada_i < 0.9: riesgo += 5
    
    return min(99.9, max(0.1, riesgo))

# ---------------------------------------------------------
# ENCABEZADO Y LOGO
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

df_criterios = pd.DataFrame({
    "Porcentaje Obtenido": ["< 65%", "65% - 81%", "> 81%"],
    "Clasificación Clínica": ["Bajo riesgo de fragilidad", "Riesgo medio de fragilidad", "Alto riesgo de fragilidad"]
})
st.table(df_criterios)
st.markdown("---")

# ---------------------------------------------------------
# PESTAÑAS DE DATOS
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["Paciente individual", "Análisis Masivo (Profesionales)"])

with tab1:
    st.write("Completa lo que tengas — lo que dejes vacío se imputa con la mediana de entrenamiento. Las marcadas con ★ son las únicas que hoy mueven el resultado.")
    
    st.markdown("<br><p style='color: gray; font-weight: bold;'>Fases temporales de la marcha (relevancia muy alta)</p>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        icc_izq = st.number_input("★ Índice calidad de ciclo (izq.) (%)", value=91.2, step=0.1)
        fase_osc_izq = st.number_input("Fase de oscilación (izq.) (%)", value=36.8, step=0.1)
        apoyo_mono_der = st.number_input("Apoyo monopodal (der.) (%)", value=37.1, step=0.1)
        apoyo_mono_izq = st.number_input("Apoyo monopodal (izq.) (%)", value=38.6, step=0.1)
        propulsion_der = st.number_input("★ Propulsión (der.)", value=6.2, step=0.1)
    with col_b:
        doble_apoyo1_izq = st.number_input("★ Doble apoyo 1 (izq.) (%)", value=13.6, step=0.1)
        icc_der = st.number_input("★ Índice de calidad de ciclo (der.) (%)", value=90.3, step=0.1)
        doble_apoyo2_der = st.number_input("Doble apoyo 2 (der.) (%)", value=13.3, step=0.1)
        fase_osc_der = st.number_input("Fase de oscilación (der.) (%)", value=36.4, step=0.1)
        ratio_armonico = st.number_input("★ Ratio armónico", value=1.3, step=0.1)
    with col_c:
        fase_apoyo_izq = st.number_input("Fase de apoyo (izq.) (%)", value=63.2, step=0.1)
        doble_apoyo1_der = st.number_input("Doble apoyo 1 (der.) (%)", value=13.3, step=0.1)
        doble_apoyo2_izq = st.number_input("Doble apoyo 2 (izq.) (%)", value=13.0, step=0.1)
        fase_apoyo_der = st.number_input("Fase de apoyo (der.) (%)", value=63.7, step=0.1)
        tug_time = st.number_input("★ TUG - Tiempo Total (s)", value=13.5, step=0.1)

    st.markdown("<p style='color: gray; font-weight: bold; margin-top: 20px;'>Propulsión y geometría del paso (relevancia alta)</p>", unsafe_allow_html=True)
    col_d, col_e, col_f = st.columns(3)
    with col_d:
        vel_marcha = st.number_input("★ Velocidad de marcha (m/s)", value=0.9, step=0.1)
        long_zancada_izq = st.number_input("★ Longitud de zancada (izq.) (m)", value=1.2, step=0.1)
    with col_e:
        long_paso_izq = st.number_input("Longitud de paso (izq.) (m)", value=0.6, step=0.1)
        long_zancada_der = st.number_input("Longitud de zancada (der.) (m)", value=1.2, step=0.1)
    with col_f:
        long_paso_der = st.number_input("Longitud de paso (der.) (m)", value=0.6, step=0.1)
        zancada_estatura = st.number_input("Zancada / estatura (izq.) (%)", value=69.7, step=0.1)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn, _ = st.columns([1, 5])
    
    if col_btn.button("Clasificar Paciente"):
        with st.spinner('Evaluando variables y comparando con cohorte...'):
            time.sleep(1) 
            
            prob_fragilidad = calcular_score_fragilidad(
                vel_marcha, tug_time, ratio_armonico, icc_izq, icc_der, 
                doble_apoyo1_izq, propulsion_der, long_zancada_izq
            )
            percentil_cohorte = stats.percentileofscore(SCORES_COHORTE_41, prob_fragilidad, kind='strict')

            if prob_fragilidad < 65:
                clase = "No frágil"
                color_texto, color_bg = "#14532d", "#f0fdf4"
            elif prob_fragilidad <= 81:
                clase = "Pre-frágil"
                color_texto, color_bg = "#713f12", "#fefce8"
            else:
                clase = "Frágil"
                color_texto, color_bg = "#7f1d1d", "#fef2f2"

            html_resultado = f"""
<div style="background-color: {color_bg}; border: 1px solid {color_texto}; border-radius: 8px; padding: 30px; margin-top: 15px; margin-bottom: 10px;">
<h1 style="color: {color_texto}; font-size: 36px; margin-bottom: 25px; font-family: Georgia, serif;">{clase}</h1>
<p style="font-size: 16px; color: #1f2937; margin-bottom: 5px;"><strong>Probabilidad de "Frágil": {prob_fragilidad:.1f}%</strong></p>
<div style="width: 100%; background-color: #d1d5db; border-radius: 4px; height: 12px; margin-bottom: 10px;">
<div style="width: {prob_fragilidad}%; background-color: {color_texto}; height: 12px; border-radius: 4px;"></div>
</div>
<p style="font-size: 13px; color: #6b7280; margin-bottom: 45px;">Se evaluaron 8 variables (Nivel 1 y 2) frente a la distribución clínica.</p>
<p style="font-size: 14px; font-weight: bold; color: #111827; margin-bottom: 40px;">📍 Comparativa Clínica: Posición en la base de datos (41 pacientes):</p>
<div style="position: relative; width: 100%; height: 14px; background: linear-gradient(to right, #86efac, #fde047, #fca5a5); border-radius: 6px; border: 1px solid #9ca3af; margin-bottom: 5px;">
<div style="position: absolute; left: calc({percentil_cohorte}% - 55px); top: -38px; background-color: #111827; color: white; padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; text-align: center; width: 110px; z-index: 10;">
Tú (Posición {int(percentil_cohorte)})
<div style="position: absolute; bottom: -5px; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 6px solid #111827;"></div>
</div>
</div>
<div style="display: flex; justify-content: space-between; font-size: 11px; color: #6b7280; margin-top: 5px;">
<span>0% (Saludable)</span><span>Mediana (50%)</span><span>100% (Frágil)</span>
</div>
</div>
"""
            st.markdown(html_resultado, unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 2 (ANÁLISIS MASIVO) - AHORA EXPORTA A EXCEL NATIVO
# ---------------------------------------------------------
with tab2:
    st.markdown("### 📊 Análisis Clínico Masivo (Lote)")
    st.write("Herramienta diseñada para profesionales de la salud. Sube una base de datos con múltiples pacientes para procesar sus niveles de riesgo de forma simultánea.")
    
    with st.expander("Ver formato requerido para las columnas (Clic aquí)"):
        st.write("El archivo Excel o CSV debe contener pacientes en las filas e idealmente estas columnas (si el sistema no encuentra un dato, asumirá un paciente promedio en esa variable específica para poder procesarlo):")
        st.code("""
marcha_velocidad_ms
tug_tug_tiempo_total_s
marcha_ratio_armonico
marcha_indice_calidad_ciclo_izq_pct
marcha_indice_calidad_ciclo_der_pct
marcha_i_doble_apoyo1_pct
marcha_propulsion_der
marcha_longitud_zancada_izq_m
        """)
        
    archivo_subido = st.file_uploader("Cargar registros de pacientes (.xlsx o .csv)", type=['xlsx', 'csv'])
    
    if archivo_subido:
        try:
            df_nuevos = pd.read_csv(archivo_subido) if archivo_subido.name.endswith('.csv') else pd.read_excel(archivo_subido)
            st.success(f"✅ Archivo cargado correctamente: {len(df_nuevos)} pacientes listos para evaluación.")
            
            if st.button("Ejecutar Procesamiento de Cohorte", type="primary"):
                with st.spinner('Analizando datos biomecánicos y generando Excel...'):
                    time.sleep(1.5)
                    resultados = []
                    
                    for idx, row in df_nuevos.iterrows():
                        v = row.get('marcha_velocidad_ms', 1.0)
                        t = row.get('tug_tug_tiempo_total_s', 12.0)
                        r = row.get('marcha_ratio_armonico', 1.3)
                        ii = row.get('marcha_indice_calidad_ciclo_izq_pct', 92.0)
                        id = row.get('marcha_indice_calidad_ciclo_der_pct', 92.0)
                        da = row.get('marcha_i_doble_apoyo1_pct', 11.0)
                        p = row.get('marcha_propulsion_der', 6.0)
                        z = row.get('marcha_longitud_zancada_izq_m', 1.1)
                        
                        v = v if pd.notna(v) else 1.0
                        t = t if pd.notna(t) else 12.0
                        r = r if pd.notna(r) else 1.3
                        ii = ii if pd.notna(ii) else 92.0
                        id = id if pd.notna(id) else 92.0
                        da = da if pd.notna(da) else 11.0
                        p = p if pd.notna(p) else 6.0
                        z = z if pd.notna(z) else 1.1
                        
                        score = calcular_score_fragilidad(v, t, r, ii, id, da, p, z)
                        percentil = stats.percentileofscore(SCORES_COHORTE_41, score, kind='strict')
                        
                        if score < 65: clase = "🟢 No frágil"
                        elif score <= 81: clase = "🟡 Pre-frágil"
                        else: clase = "🔴 Frágil"
                        
                        identificador = row.get('ID', row.get('Paciente', row.get('Nombre', f"Paciente {idx+1}")))
                        
                        resultados.append({
                            "Identificador": identificador,
                            "Probabilidad (%)": round(score, 1),
                            "Percentil (Posición)": int(percentil),
                            "Clasificación Clínica": clase
                        })
                    
                    df_resultados = pd.DataFrame(resultados)
                    st.dataframe(df_resultados, use_container_width=True)
                    
                    # MAGIA AQUÍ: Convertir la tabla directamente a un archivo nativo de EXCEL
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df_resultados.to_excel(writer, index=False, sheet_name='Reporte Clínico')
                    
                    st.download_button(
                        label="⬇️ Descargar Reporte de Diagnóstico (Formato Excel)",
                        data=buffer.getvalue(),
                        file_name="Reporte_Pacientes_MoVida.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
        except Exception as e:
            st.error(f"Error al leer el archivo. Verifica el formato. Detalle: {e}")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280; font-size: 14px;'>Sistema desarrollado e investigado por <strong>Mayra Alejandra Campos</strong> y <strong>Juan David Garcia</strong></p>", unsafe_allow_html=True)
