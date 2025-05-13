import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime

# Configuración de página mejorada
st.set_page_config(
    page_title="Análisis de Sensores - Mi Ciudad",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Aplicación para análisis de datos de sensores ESP32"
    }
)

# CSS personalizado con tipografías y estilos mejorados
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Roboto:wght@300;400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif;
        color: #2c3e50;
    }
    
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
    }
    
    .stAlert {
        margin-top: 1rem;
        border-radius: 8px;
    }
    
    .st-b7 {
        background-color: #3498db !important;
    }
    
    .st-c0 {
        background-color: #2980b9 !important;
    }
    
    .stButton>button {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .stSelectbox, .stRadio, .stSlider {
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 8px 8px 0 0;
        background-color: #ecf0f1;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3498db;
        color: white;
    }
    
    .stDataFrame {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stMap {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stDownloadButton>button {
        background-color: #2ecc71 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado con logo y título
st.title('📊 Análisis de datos de Sensores en Mi Ciudad')
st.markdown("""
    <div style="background-color:#1c097a; padding:1rem; border-radius:8px; margin-bottom:1.5rem;">
    Esta aplicación permite analizar datos de temperatura y humedad
    recolectados por sensores ESP32 en diferentes puntos de la ciudad.
    </div>
""", unsafe_allow_html=True)

# Sidebar para navegación
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2933/2933245.png", width=80)
    st.title("Opciones")
    st.markdown("---")
    st.markdown("**Configuración general**")
    st.info("Seleccione un archivo CSV para comenzar el análisis")

# Crear datos de mapa para EAFIT
eafit_location = pd.DataFrame({
    'lat': [6.2006],
    'lon': [-75.5783],
    'location': ['Universidad EAFIT']
})

# Mostrar mapa con estilo mejorado
st.subheader("📍 Ubicación de los Sensores - Universidad EAFIT")
st.map(eafit_location, zoom=15)

# Cargador de archivos
uploaded_file = st.file_uploader('Seleccione archivo CSV', type=['csv'], help="Suba un archivo CSV con datos de sensores")

if uploaded_file is not None:
    try:
        # Cargar y procesar datos
        df1 = pd.read_csv(uploaded_file)
        
        # Renombrar columnas para simplificar
        column_mapping = {
            'temperatura {device="ESP32", name="Sensor 1"}': 'temperatura',
            'humedad {device="ESP32", name="Sensor 1"}': 'humedad'
        }
        df1 = df1.rename(columns=column_mapping)
        
        df1['Time'] = pd.to_datetime(df1['Time'])
        df1 = df1.set_index('Time')

        # Crear pestañas con estilo mejorado
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Visualización", "📊 Estadísticas", "🔍 Filtros", "🗺️ Información del Sitio"])

        with tab1:
            st.markdown("### 📈 Visualización de Datos")
            
            # Selector de variable
            variable = st.selectbox(
                "Seleccione variable a visualizar",
                ["temperatura", "humedad", "Ambas variables"],
                key="var_selector"
            )
            
            # Selector de tipo de gráfico
            chart_type = st.selectbox(
                "Seleccione tipo de gráfico",
                ["Línea", "Área", "Barra"],
                key="chart_selector"
            )
            
            # Crear gráfico basado en la selección
            if variable == "Ambas variables":
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### Temperatura (°C)")
                    if chart_type == "Línea":
                        st.line_chart(df1["temperatura"])
                    elif chart_type == "Área":
                        st.area_chart(df1["temperatura"])
                    else:
                        st.bar_chart(df1["temperatura"])
                
                with col2:
                    st.markdown("#### Humedad (%)")
                    if chart_type == "Línea":
                        st.line_chart(df1["humedad"])
                    elif chart_type == "Área":
                        st.area_chart(df1["humedad"])
                    else:
                        st.bar_chart(df1["humedad"])
            else:
                if chart_type == "Línea":
                    st.line_chart(df1[variable])
                elif chart_type == "Área":
                    st.area_chart(df1[variable])
                else:
                    st.bar_chart(df1[variable])

            # Mostrar datos crudos con toggle
            if st.checkbox('Mostrar datos crudos', key="raw_data_toggle"):
                st.dataframe(df1, height=300)

        with tab2:
            st.markdown("### 📊 Análisis Estadístico")
            
            # Selector de variable para estadísticas
            stat_variable = st.radio(
                "Seleccione variable para estadísticas",
                ["temperatura", "humedad"],
                horizontal=True,
                key="stat_radio"
            )
            
            # Resumen estadístico
            stats_df = df1[stat_variable].describe().to_frame().T
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(stats_df.style.format("{:.2f}"))
            
            with col2:
                # Métricas adicionales
                if stat_variable == "temperatura":
                    st.metric("Temperatura Promedio", 
                             f"{stats_df['mean'].values[0]:.2f}°C",
                             delta=f"{stats_df['mean'].values[0] - stats_df['50%'].values[0]:.2f}°C desde la mediana")
                    st.metric("Temperatura Máxima", f"{stats_df['max'].values[0]:.2f}°C")
                    st.metric("Temperatura Mínima", f"{stats_df['min'].values[0]:.2f}°C")
                else:
                    st.metric("Humedad Promedio", 
                             f"{stats_df['mean'].values[0]:.2f}%",
                             delta=f"{stats_df['mean'].values[0] - stats_df['50%'].values[0]:.2f}% desde la mediana")
                    st.metric("Humedad Máxima", f"{stats_df['max'].values[0]:.2f}%")
                    st.metric("Humedad Mínima", f"{stats_df['min'].values[0]:.2f}%")

        with tab3:
            st.markdown("### 🔍 Filtros de Datos")
            
            # Selector de variable para filtrar
            filter_variable = st.selectbox(
                "Seleccione variable para filtrar",
                ["temperatura", "humedad"],
                key="filter_select"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Filtro de valor mínimo
                min_val = st.slider(
                    f'Valor mínimo de {filter_variable}',
                    float(df1[filter_variable].min()),
                    float(df1[filter_variable].max()),
                    float(df1[filter_variable].mean()),
                    key="min_val"
                )
                
                filtrado_df_min = df1[df1[filter_variable] > min_val]
                st.write(f"**Registros con {filter_variable} superior a {min_val:.2f}{'°C' if filter_variable == 'temperatura' else '%'}**")
                st.dataframe(filtrado_df_min, height=250)
                
            with col2:
                # Filtro de valor máximo
                max_val = st.slider(
                    f'Valor máximo de {filter_variable}',
                    float(df1[filter_variable].min()),
                    float(df1[filter_variable].max()),
                    float(df1[filter_variable].mean()),
                    key="max_val"
                )
                
                filtrado_df_max = df1[df1[filter_variable] < max_val]
                st.write(f"**Registros con {filter_variable} inferior a {max_val:.2f}{'°C' if filter_variable == 'temperatura' else '%'}**")
                st.dataframe(filtrado_df_max, height=250)

            # Descargar datos filtrados
            st.markdown("---")
            st.markdown("**Exportar datos filtrados**")
            if st.button('Generar archivo para descarga', key="download_btn"):
                csv = filtrado_df_min.to_csv().encode('utf-8')
                st.download_button(
                    label="⬇️ Descargar CSV",
                    data=csv,
                    file_name='datos_filtrados.csv',
                    mime='text/csv',
                    key="download_csv"
                )

        with tab4:
            st.markdown("### 🗺️ Información del Sitio de Medición")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📍 Ubicación del Sensor")
                st.markdown("""
                    **Universidad EAFIT**  
                    - Latitud: 6.2006  
                    - Longitud: -75.5783  
                    - Altitud: ~1,495 metros sobre el nivel del mar  
                """)
                st.map(eafit_location, zoom=15)
            
            with col2:
                st.markdown("#### 🔧 Detalles del Sensor")
                st.markdown("""
                    - **Tipo:** ESP32  
                    - **Variables medidas:**  
                      * Temperatura (°C)  
                      * Humedad (%)  
                    - **Frecuencia de medición:** Según configuración  
                    - **Ubicación:** Campus universitario  
                    - **Precisión:**  
                      * Temperatura: ±0.5°C  
                      * Humedad: ±2%  
                """)
                st.image("https://cdn-icons-png.flaticon.com/512/3094/3094843.png", width=150)

    except Exception as e:
        st.error(f'Error al procesar el archivo: {str(e)}')
else:
    st.warning('Por favor, cargue un archivo CSV para comenzar el análisis.')
    
# Footer mejorado
st.markdown("""
    <div style="background-color:#2c3e50; color:white; padding:1.5rem; border-radius:8px; margin-top:2rem;">
        <p style="text-align:center; margin-bottom:0;">
            <strong>Desarrollado para el análisis de datos de sensores urbanos</strong><br>
            <small>Ubicación: Universidad EAFIT, Medellín, Colombia | © 2023</small>
        </p>
    </div>
""", unsafe_allow_html=True)
