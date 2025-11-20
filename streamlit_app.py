import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- CONFIGURACIÓN DE LA PÁGINA WEB ---
st.set_page_config(page_title="DiDIA-BA | Diagnóstico Docente IA", layout="wide")

# --- BARRA LATERAL (CARGA DE DATOS) ---
st.sidebar.header("📂 Carga de Datos")
st.sidebar.info("Sube el CSV con las respuestas de los docentes para alimentar el motor de diagnóstico.")

# Función para descargar plantilla (ayuda al usuario a saber el formato)
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# --- 1. GENERACIÓN DE DATOS (SIMULADOS O CARGADOS) ---

# Función para generar datos simulados (se usa si no hay CSV)
def get_simulated_data():
    data = {
        'ID_Docente': range(1, 51),
        'Rol': np.random.choice(['Docente Aula', 'Directivo', 'Coordinador'], 50),
        # Escala 1-5 (Competencias UNESCO)
        'Comp_Etica': np.random.randint(1, 4, 50),
        'Comp_Tecnica': np.random.randint(2, 5, 50),
        # Escala 1-5 (Límites a la Domesticación)
        'Reticencia_Miedo': np.random.randint(3, 6, 50),
        'Austeridad_Tiempo': np.random.randint(4, 6, 50),
        'Uso_Obligado_Vigilancia': np.random.randint(1, 4, 50),
        'Apropiacion_Uso': np.random.randint(1, 4, 50)
    }
    return pd.DataFrame(data)

# Widget para subir archivo
uploaded_file = st.sidebar.file_uploader("Subir archivo CSV", type=["csv"])

# Lógica de Carga
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("✅ Datos cargados correctamente")
        
        # Validación simple de columnas requeridas
        required_columns = ['Reticencia_Miedo', 'Austeridad_Tiempo', 'Uso_Obligado_Vigilancia', 'Apropiacion_Uso', 'Comp_Etica', 'Comp_Tecnica']
        if not all(col in df.columns for col in required_columns):
            st.error(f"El CSV debe contener las siguientes columnas: {required_columns}")
            st.stop()
            
    except Exception as e:
        st.sidebar.error(f"Error al leer el archivo: {e}")
        df = get_simulated_data() # Fallback a simulados si falla
else:
    # Si no hay archivo, usamos la simulación
    df = get_simulated_data()
    st.sidebar.warning("⚠️ Usando datos simulados (Demo)")
    
    # Botón para descargar la plantilla de ejemplo
    csv_template = convert_df(df)
    st.sidebar.download_button(
        label="📥 Descargar Plantilla CSV de Ejemplo",
        data=csv_template,
        file_name="plantilla_didia_ba.csv",
        mime="text/csv",
    )

# --- COMIENZO DEL DASHBOARD ---

st.title("🤖 DiDIA-BA: Brújula de Apropiación Docente")
st.markdown(f"""
**Dispositivo de Diagnóstico Institucional basado en el Modelo de Apropiación .**
Este tablero analiza las barreras de *Austeridad, Reticencia y Usos Obligados* para recomendar políticas de formación.
*Datos analizados: {len(df)} docentes.*
""")
st.markdown("---")

# --- 2. MOTOR DE PROCESAMIENTO (Cálculo de Indicadores) ---
avg_reticencia = df['Reticencia_Miedo'].mean()
avg_austeridad = df['Austeridad_Tiempo'].mean()
avg_usos_obligados = df['Uso_Obligado_Vigilancia'].mean()
indice_apropiacion = df['Apropiacion_Uso'].mean() * 20 

# --- 3. DASHBOARD INTERACTIVO ---

# KPIs Principales
col1, col2, col3, col4 = st.columns(4)
col1.metric("Puntaje de Apropiación", f"{indice_apropiacion:.1f}%", "Nivel General")
col2.metric("Nivel de Reticencia", f"{avg_reticencia:.1f}/5", "Barrera Ética/Miedo", delta_color="inverse")
col3.metric("Nivel de Austeridad", f"{avg_austeridad:.1f}/5", "Barrera Recursos/Tiempo", delta_color="inverse")
col4.metric("Nivel de Usos Obligados", f"{avg_usos_obligados:.1f}/5", "Barrera Control", delta_color="inverse")

# Gráficos
c1, c2 = st.columns((2, 1))

with c1:
    st.subheader("Mapa de Límites a la Domesticación")
    limites_data = pd.DataFrame({
        'Límite': ['Reticencia (Miedo/Ética)', 'Austeridad (Recursos/Tiempo)', 'Usos Obligados (Control)'],
        'Intensidad': [avg_reticencia, avg_austeridad, avg_usos_obligados]
    })
    # Gráfico de barras con colores personalizados
    fig = px.bar(limites_data, x='Límite', y='Intensidad', color='Intensidad', 
                 range_y=[0,5], color_continuous_scale='RdYlGn_r', title="Barreras detectadas (Escala 1-5)")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Brecha de Competencias")
    competencias_data = pd.DataFrame({
        'Area': ['Ética (UNESCO)', 'Técnica (UNESCO)', 'Pedagógica (UNESCO)'],
        # Agregamos una métrica simulada extra para que el radar se vea mejor (triángulo)
        'Nivel Promedio': [df['Comp_Etica'].mean(), df['Comp_Tecnica'].mean(), (df['Comp_Tecnica'].mean() + df['Comp_Etica'].mean())/2] 
    })
    
    # Usamos bar_polar que es la función correcta
    fig2 = px.bar_polar(competencias_data, r='Nivel Promedio', theta='Area', range_r=[0,5], template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

# --- 4. MOTOR DE RECOMENDACIÓN (Lógica del TIF) ---
st.markdown("---")
st.subheader("🤖 Motor de Recomendación de Políticas (DiDIA AI)")

def generar_recomendacion(austeridad, reticencia, obligados):
    # Lógica de priorización basada en tus hallazgos
    if austeridad >= 4.0:
        return """
        **🔴 DIAGNÓSTICO CRÍTICO: AUSTERIDAD (Estructural)**
        Los docentes reportan falta severa de tiempo o recursos. Cualquier capacitación extra será rechazada si no se libera tiempo primero.
        
        **RECOMENDACIÓN DE POLÍTICA:**
        1. **Infraestructura:** Garantizar acceso a versiones pagas o equipos.
        2. **Tiempo Protegido:** Reducir carga administrativa usando IA para liberar 2hs semanales dedicadas a experimentación.
        """
    elif reticencia >= 4.0:
        return """
        **🟠 DIAGNÓSTICO CRÍTICO: RETICENCIA (Cultural)**
        Existe un fuerte temor al plagio, a la pérdida de control del aula o a la desprofesionalización.
        
        **RECOMENDACIÓN DE POLÍTICA:**
        1. **Talleres de Sensibilización:** Enfocados en "IA como Copiloto" y no como reemplazo.
        2. **Debate Ético:** Espacios institucionales para definir normas de integridad académica.
        """
    elif obligados >= 4.0:
        return """
        **🟡 DIAGNÓSTICO CRÍTICO: USOS OBLIGADOS (Vigilancia)**
        Los docentes perciben la tecnología como una herramienta de control administrativo.
        
        **RECOMENDACIÓN DE POLÍTICA:**
        1. **Cambio de Narrativa:** Desvincular la IA de procesos de presentismo/control.
        2. **Incentivos Positivos:** Premiar la innovación pedagógica en lugar de vigilar el cumplimiento.
        """
    else:
        return """
        **🟢 ESTADO SALUDABLE**
        La institución tiene un buen nivel de apropiación.
        **RECOMENDACIÓN:** Avanzar al Nivel 3 (Crear) del marco UNESCO: fomentar que los docentes creen sus propios bots o recursos personalizados.
        """

if st.button('Generar Diagnóstico y Recomendación'):
    recommendation = generar_recomendacion(avg_austeridad, avg_reticencia, avg_usos_obligados)
    st.info("Analizando patrones en los datos cargados...")
    st.markdown(recommendation)

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("Desarrollado para el TIF: 'Indagación sobre el Impacto de la IAG en Docentes de Nivel Medio CABA'.")
