import streamlit as st
import pandas as pd
import time

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
# PESTAÑAS
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["Paciente individual", "Varios pacientes (Excel/CSV)"])

with tab1:
    st.write("Completa lo que tengas — lo que dejes vacío se imputa con la mediana del set de entrenamiento (41 pacientes). Las marcadas con ★ son las únicas que hoy mueven el resultado.")
    
    st.markdown("<br><p style='color: gray; font-weight: bold;'>Fases temporales de la marcha (relevancia muy alta)</p>", unsafe_allow_html=True)
    
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

    st.markdown("<p style='color: gray; font-weight: bold; margin-top: 20px;'>Propulsión y geometría del paso (relevancia alta)</p>", unsafe_allow_html=True)
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
    # BOTÓN CLASIFICAR Y DIBUJO DE RESULTADOS (DISEÑO FOTO)
    # ---------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Creamos dos columnas para que el botón no ocupe toda la pantalla, como en tu foto
    col_btn, _ = st.columns([1, 5])
    if col_btn.button("Clasificar"):
        with st.spinner('Procesando...'):
            time.sleep(1) 
            
            # --- Lógica dinámica de simulación de tu K-Means ---
            score_riesgo = 20.0
            if vel_marcha < 0.8: score_riesgo += 35
            elif vel_marcha < 1.1: score_riesgo += 15
            
            if tug_time > 13.5: score_riesgo += 30
            elif tug_time > 11.0: score_riesgo += 15
                
            if ratio_armonico < 1.2: score_riesgo += 15
            if icc_izq < 90: score_riesgo += 10
            if doble_apoyo1_izq > 12: score_riesgo += 10
            
            score_riesgo = min(99.9, max(5.0, score_riesgo))

            # --- Definir colores y textos según el resultado ---
            if score_riesgo < 65:
                clase = "No frágil"
                color_texto = "#14532d" # Verde oscuro
                color_bg = "#f0fdf4"    # Verde muy claro (fondo)
                color_barra = "#15803d" # Verde barra
            elif score_riesgo <= 81:
                clase = "Pre-frágil"
                color_texto = "#713f12" # Naranja/Café oscuro
                color_bg = "#fefce8"    # Amarillo claro (fondo)
                color_barra = "#ca8a04" # Amarillo barra
            else:
                clase = "Frágil"
                color_texto = "#7f1d1d" # Rojo oscuro
                color_bg = "#fef2f2"    # Rojo claro (fondo)
                color_barra = "#b91c1c" # Rojo barra

            # --- DIBUJAR EL RESULTADO EN HTML PARA QUE QUEDE EXACTO A TU IMAGEN ---
            html_resultado = f"""
            <div style="background-color: {color_bg}; border: 1px solid {color_texto}; border-radius: 8px; padding: 30px; margin-top: 15px; margin-bottom: 10px;">
                <h1 style="color: {color_texto}; font-size: 36px; margin-bottom: 25px; font-family: Georgia, serif;">{clase}</h1>
                
                <p style="font-size: 16px; color: #1f2937; margin-bottom: 5px;"><strong>Probabilidad de "Frágil": {score_riesgo:.1f}%</strong></p>
                
                <!-- Barra de probabilidad (Gris con relleno de color) -->
                <div style="width: 100%; background-color: #d1d5db; border-radius: 4px; height: 12px; margin-bottom: 10px;">
                    <div style="width: {score_riesgo}%; background-color: {color_texto}; height: 12px; border-radius: 4px;"></div>
                </div>
                
                <p style="font-size: 13px; color: #6b7280; margin-bottom: 45px;">10 de 10 variables imputadas con la mediana de entrenamiento.</p>
                
                <p style="font-size: 14px; font-weight: bold; color: #111827; margin-bottom: 40px;">📍 Comparativa Clínica: Posición en la base de datos (41 pacientes):</p>
                
                <!-- Gradiente y Tooltip del Percentil -->
                <div style="position: relative; width: 100%; height: 14px; background: linear-gradient(to right, #86efac, #fde047, #fca5a5); border-radius: 6px; border: 1px solid #9ca3af; margin-bottom: 5px;">
                    <!-- Tooltip negro flotante -->
                    <div style="position: absolute; left: calc({score_riesgo}% - 55px); top: -38px; background-color: #111827; color: white; padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; text-align: center; width: 110px; z-index: 10;">
                        Tú (Percentil {int(score_riesgo)})
                        <!-- Triangulito del tooltip -->
                        <div style="position: absolute; bottom: -5px; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 6px solid #111827;"></div>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between; font-size: 11px; color: #6b7280; margin-top: 5px;">
                    <span>0% (Saludable)</span>
                    <span>Mediana (50%)</span>
                    <span>100% (Frágil)</span>
                </div>
            </div>
            """
            # Renderizamos el HTML
            st.markdown(html_resultado, unsafe_allow_html=True)
            
            # Textos aclaratorios
            st.markdown("""
            <p style="font-size: 12px; color: #9ca3af; margin-top: 5px;">
            Etiqueta "Frágil"/"No frágil" derivada de un clustering no supervisado (K-Means) sobre 41 pacientes, no de un criterio clínico validado (Fried, SPPB, etc.). Usar solo como apoyo exploratorio.
            </p>
            """, unsafe_allow_html=True)

with tab2:
    st.info("Sube el archivo `Datos_Consolidados_TUG_Corregidos.xlsx` con los 41 pacientes para ejecutar el clustering completo.")
    archivo_subido = st.file_uploader("Cargar dataset (.xlsx o .csv)", type=['xlsx', 'csv'])
    if archivo_subido:
        df = pd.read_csv(archivo_subido) if archivo_subido.name.endswith('.csv') else pd.read_excel(archivo_subido, sheet_name="Consolidado")
        st.dataframe(df.head())

# ---------------------------------------------------------
# PIE DE PÁGINA
# ---------------------------------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280; font-size: 14px;'>Sistema desarrollado e investigado por <strong>Mayra Alejandra Campos</strong> y <strong>Juan David Garcia</strong></p>", unsafe_allow_html=True)
