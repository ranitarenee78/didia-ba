import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- CONFIGURACIÓN DE LA PÁGINA WEB ---
st.set_page_config(page_title="DiDIA-BA | Diagnóstico Docente IA", layout="wide")

# Título y Contexto Académico
st.title("🤖 DiDIA-BA: Brújula de Apropiación Docente")
st.markdown("""
**Dispositivo de Diagnóstico Institucional basado en el Modelo de Apropiación (Sandoval/Cabello).**
Este tablero analiza las barreras de *Austeridad, Reticencia y Usos Obligados* para recomendar políticas de formación.
""")
st.markdown("---")

# --- 1. BASE DE DATOS (Simulación de Datos Recolectados) ---
# En un caso real, esto se conectaría a un Google Sheet en vivo.
@st.cache_data
def load_data():
    # Simulamos 50 respuestas de docentes de una institución ficticia en CABA
    data = {
        'ID_Docente': range(1, 51),
        'Rol': np.random.choice(['Docente Aula', 'Directivo', 'Coordinador'], 50),
        # Escala 1-5 (Competencias UNESCO)
        'Comp_Etica': np.random.randint(1, 4, 50), # Bajo dominio ético simulado
        'Comp_Tecnica': np.random.randint(2, 5, 50),
        # Escala 1-5 (Límites a la Domesticación - Sandoval)
        'Reticencia_Miedo': np.random.randint(3, 6, 50), # Alta reticencia
        'Austeridad_Tiempo': np.random.randint(4, 6, 50), # Alta falta de tiempo
        'Uso_Obligado_Vigilancia': np.random.randint(1, 4, 50),
        'Apropiacion_Uso': np.random.randint(1, 4, 50)
    }
    return pd.DataFrame(data)

df = load_data()

# --- 2. MOTOR DE PROCESAMIENTO (Cálculo de Indicadores) ---
# Calculamos los promedios institucionales para el diagnóstico
avg_reticencia = df['Reticencia_Miedo'].mean()
avg_austeridad = df['Austeridad_Tiempo'].mean()
avg_usos_obligados = df['Uso_Obligado_Vigilancia'].mean()
indice_apropiacion = df['Apropiacion_Uso'].mean() * 20  # Convertir a porcentaje (escala 100)

# --- 3. DASHBOARD INTERACTIVO (Visualización) ---

# KPIs Principales
col1, col2, col3, col4 = st.columns(4)
col1.metric("Puntaje de Apropiación", f"{indice_apropiacion:.1f}%", "-5% vs Mes Anterior")
col2.metric("Nivel de Reticencia", f"{avg_reticencia:.1f}/5", "Alerta Alta", delta_color="inverse")
col3.metric("Nivel de Austeridad (Tiempo)", f"{avg_austeridad:.1f}/5", "Crítico", delta_color="inverse")
col4.metric("Muestra", f"{len(df)} Docentes")

# Gráficos
c1, c2 = st.columns((2, 1))

with c1:
    st.subheader("Mapa de Límites a la Domesticación")
    # Datos para el gráfico de radar o barras
    limites_data = pd.DataFrame({
        'Límite': ['Reticencia (Miedo/Ética)', 'Austeridad (Recursos/Tiempo)', 'Usos Obligados (Control)'],
        'Intensidad': [avg_reticencia, avg_austeridad, avg_usos_obligados]
    })
    fig = px.bar(limites_data, x='Límite', y='Intensidad', color='Intensidad', 
                 range_y=[0,5], color_continuous_scale='Reds', title="Barreras detectadas según Modelo Sandoval")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Brecha de Competencias")
    # Comparativa con UNESCO
    competencias_data = pd.DataFrame({
        'Area': ['Ética (UNESCO)', 'Técnica (UNESCO)'],
        'Nivel Promedio': [df['Comp_Etica'].mean(), df['Comp_Tecnica'].mean()]
    })
    fig2 = px.bar_polar(competencias_data, r='Nivel Promedio', theta='Area', range_r=[0,5], title="Brecha de Competencias (Radar)")
    st.plotly_chart(fig2, use_container_width=True)

# --- 4. MOTOR DE RECOMENDACIÓN (Simulación IA) ---
st.markdown("---")
st.subheader("🤖 Motor de Recomendación de Políticas (DiDIA AI)")

def generar_recomendacion(austeridad, reticencia):
    # Lógica algorítmica basada en los hallazgos de tu TIF
    if austeridad > 4.0:
        return """
        **DIAGNÓSTICO:** Se detecta una barrera crítica de **Austeridad de Tiempo** [Maximiliano]. 
        Los docentes no se niegan a usar IA, pero carecen de espacio material.
        
        **RECOMENDACIÓN DE POLÍTICA:**
        1. **Liberación de Carga:** Utilizar IA administrativa para reducir en un 20% el tiempo burocrático.
        2. **Inversión:** Proveer licencias institucionales (evitar la desigualdad de acceso detectada en el caso 'Julieta').
        """
    elif reticencia > 4.0:
        return """
        **DIAGNÓSTICO:** Predomina la **Reticencia Pedagógica/Ética** [Emilia/Paula]. 
        Existe temor a la desprofesionalización o al plagio.
        
        **RECOMENDACIÓN DE POLÍTICA:**
        1. **Formación Ética:** Taller obligatorio basado en el eje 'Human-Centered AI' de UNESCO.
        2. **Redefinición de Roles:** Jornadas institucionales para co-diseñar protocolos de evaluación con IA.
        """
    else:
        return "La institución muestra niveles saludables de apropiación. Se sugiere profundizar en usos creativos."

if st.button('Generar Diagnóstico y Recomendación'):
    recommendation = generar_recomendacion(avg_austeridad, avg_reticencia)
    st.success("Análisis completado con éxito.")
    st.markdown(recommendation)

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("Desarrollado para el TIF: 'Indagación sobre el Impacto de la IAG en Docentes de Nivel Medio CABA'.")
