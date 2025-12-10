# ==========================================================
# SIMULADOR INTERACTIVO DE RESPUESTA SÍSMICA SDOF
# Optimizado para Streamlit Cloud
# Sistema de Un Grado de Libertad
# ==========================================================

import streamlit as st
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Configuración de página
st.set_page_config(
    page_title="Simulador Sísmico SDOF",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    .stMetric:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    div[data-testid="stExpander"] {
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# ===========================================
# Función Ricker para simular pulsos sísmicos
# ===========================================
def ricker(t, t0, f0):
    """Wavelet Ricker para simular pulsos sísmicos realistas"""
    tau = t - t0
    a = (np.pi * f0 * tau)**2
    return (1 - 2*a) * np.exp(-a)

# =============================
# Encabezado profesional
# =============================
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.title("🏢 Simulador de Respuesta Sísmica SDOF")
    st.markdown("**Sistema de Un Grado de Libertad - Análisis Dinámico de Estructuras**")
with col2:
    st.markdown("### 📊")
    st.caption("Análisis Científico")
with col3:
    # Link al visualizador web (actualizar con tu URL de GitHub Pages)
    st.markdown("### 🎬")
    st.markdown("[Ver Animación →](https://andrix1515.github.io/TERREMOTO/simulator.html)", 
                unsafe_allow_html=True)

# =============================
# Panel de controles (sidebar)
# =============================
with st.sidebar:
    st.header("⚙️ Parámetros del Sistema")
    
    st.subheader("🏗️ Estructura")
    m = st.slider("Masa (kg)", 0.1, 10.0, 1.0, 0.1, 
                  help="Masa de la estructura en kilogramos")
    c = st.slider("Amortiguamiento (N·s/m)", 0.0, 5.0, 0.5, 0.1,
                  help="Coeficiente de amortiguamiento viscoso")
    k = st.slider("Rigidez (N/m)", 1.0, 100.0, 20.0, 1.0,
                  help="Rigidez lateral de la estructura")
    
    st.divider()
    
    st.subheader("🌊 Onda Sísmica")
    T = st.slider("Duración (s)", 5, 60, 20, 5,
                  help="Duración total de la simulación")
    intensidad = st.slider("Intensidad del sismo", 0.1, 3.0, 1.0, 0.1,
                          help="Factor de amplitud de la onda")
    
    st.divider()
    
    # Parámetros dinámicos calculados
    omega_n = np.sqrt(k/m)
    freq_nat = omega_n / (2*np.pi)
    periodo = 2*np.pi / omega_n
    c_critic = 2 * np.sqrt(m * k)
    zeta = c / c_critic
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Freq. Natural", f"{freq_nat:.2f} Hz", help="Frecuencia natural del sistema")
    with col2:
        st.metric("Período", f"{periodo:.2f} s", help="Período natural de vibración")
    
    st.metric("Razón de Amort.", f"{zeta:.3f}", 
              delta="Crítico" if abs(zeta - 1.0) < 0.05 else ("Subamort." if zeta < 1 else "Sobreamort."))

# =============================
# Generar sismo sintético realista
# =============================
@st.cache_data
def generar_sismo(T, intensidad, seed=0):
    """Genera un acelerograma sintético realista"""
    dt = 0.01
    t = np.arange(0, T, dt)
    
    # Superposición de wavelets Ricker para simular movimiento sísmico complejo
    acc = (
        0.8 * ricker(t, T/3 - 5, 1.0)
        + 1.2 * ricker(t, T/3, 2.5)
        + 0.6 * ricker(t, T/3 + 5, 4.0)
        + 0.3 * ricker(t, T/2, 1.2)
        + 0.4 * ricker(t, 2*T/3, 3.0)
    )
    
    # Envolvente de amplitud (más realista)
    env = np.exp(-((t - T/2) / (T/4)) ** 2)
    acc *= env
    
    # Agregar ruido sísmico de fondo
    np.random.seed(seed)
    acc += 0.05 * np.random.randn(len(t))
    
    # Normalizar y escalar
    acc = acc / max(abs(acc)) * (0.6 * intensidad)
    
    return t, acc

# =============================
# Resolver la ecuación del SDOF
# =============================
@st.cache_data
def resolver_sdof(m, c, k, T, acc_ground):
    """Resuelve la ecuación diferencial del SDOF"""
    dt = 0.01
    t = np.arange(0, T, dt)
    F_t = -m * acc_ground  # Fuerza sísmica
    
    def modelo_sdof(ti, y):
        """Ecuación diferencial: m·ẍ + c·ẋ + k·x = F(t)"""
        x, v = y
        Fi = np.interp(ti, t, F_t)
        a = (Fi - c * v - k * x) / m
        return [v, a]
    
    try:
        y0 = [0, 0]
        sol = solve_ivp(modelo_sdof, [0, T], y0, t_eval=t, method='RK45', max_step=0.01)
        x = sol.y[0]
        v = sol.y[1]
        a = np.gradient(v, dt)
        
        # Calcular energías
        E_cinetica = 0.5 * m * v**2
        E_potencial = 0.5 * k * x**2
        E_total = E_cinetica + E_potencial
        
        return t, x, v, a, E_cinetica, E_potencial, E_total
    except Exception as e:
        st.error(f"Error al resolver la ecuación diferencial: {e}")
        return None

# =============================
# Generar y resolver
# =============================
with st.spinner('🔄 Calculando respuesta sísmica...'):
    t, acc = generar_sismo(T, intensidad)
    resultado = resolver_sdof(m, c, k, T, acc)

if resultado is None:
    st.error("No se pudo calcular la respuesta. Ajusta los parámetros.")
    st.stop()

t, x, v, a_struct, E_cinetica, E_potencial, E_total = resultado

# =============================
# Mostrar resultados
# =============================

# Pestañas para organizar contenido
tab1, tab2, tab3, tab4 = st.tabs(["📊 Respuestas Temporales", "⚡ Energía", "📈 Comparativa", "ℹ️ Info Técnica"])

with tab1:
    st.subheader("Respuestas en el Dominio del Tiempo")
    
    # Fila 1: Acelerograma y Desplazamiento
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🌊 Acelerograma del Sismo")
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        ax1.plot(t, acc, color='#FF6B6B', linewidth=1.5, label='Aceleración del suelo')
        ax1.fill_between(t, acc, alpha=0.3, color='#FF6B6B')
        ax1.set_xlabel("Tiempo (s)", fontsize=11)
        ax1.set_ylabel("Aceleración (m/s²)", fontsize=11)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close()
    
    with col2:
        st.markdown("##### 📐 Desplazamiento de la Estructura")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(t, x*1000, color='#4ECDC4', linewidth=2, label='Desplazamiento')
        ax2.fill_between(t, x*1000, alpha=0.2, color='#4ECDC4')
        ax2.set_xlabel("Tiempo (s)", fontsize=11)
        ax2.set_ylabel("Desplazamiento (mm)", fontsize=11)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()
    
    # Fila 2: Velocidad y Aceleración
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🔄 Velocidad de la Estructura")
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        ax3.plot(t, v*1000, color='#95E1D3', linewidth=1.5)
        ax3.fill_between(t, v*1000, alpha=0.2, color='#95E1D3')
        ax3.set_xlabel("Tiempo (s)", fontsize=11)
        ax3.set_ylabel("Velocidad (mm/s)", fontsize=11)
        ax3.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()
    
    with col2:
        st.markdown("##### ⚡ Aceleración de la Estructura")
        fig4, ax4 = plt.subplots(figsize=(10, 4))
        ax4.plot(t, a_struct, color='#F38181', linewidth=1.5)
        ax4.fill_between(t, a_struct, alpha=0.2, color='#F38181')
        ax4.set_xlabel("Tiempo (s)", fontsize=11)
        ax4.set_ylabel("Aceleración (m/s²)", fontsize=11)
        ax4.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close()

with tab2:
    st.subheader("⚡ Evolución de Energía en el Sistema")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig5, ax5 = plt.subplots(figsize=(12, 5))
        ax5.plot(t, E_cinetica, label='Energía Cinética', linewidth=2, color='#3498db')
        ax5.plot(t, E_potencial, label='Energía Potencial', linewidth=2, color='#2ecc71')
        ax5.plot(t, E_total, label='Energía Total', linewidth=2.5, color='#e74c3c', linestyle='--')
        ax5.set_xlabel("Tiempo (s)", fontsize=12)
        ax5.set_ylabel("Energía (J)", fontsize=12)
        ax5.legend(loc='best', fontsize=11)
        ax5.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig5)
        plt.close()
    
    with col2:
        st.metric("Energía Cinética Máx.", f"{np.max(E_cinetica):.4f} J")
        st.metric("Energía Potencial Máx.", f"{np.max(E_potencial):.4f} J")
        st.metric("Energía Total Máx.", f"{np.max(E_total):.4f} J")
        st.info("💡 La energía total incluye disipación por amortiguamiento")

with tab3:
    st.subheader("📊 Comparativa: Entrada vs Salida")
    
    fig6, (ax6a, ax6b) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Normalizar para comparación
    acc_norm = acc / np.max(np.abs(acc))
    x_norm = x / np.max(np.abs(x))
    
    ax6a.plot(t, acc, label='Aceleración del suelo', linewidth=1.5, alpha=0.8, color='#FF6B6B')
    ax6a.fill_between(t, acc, alpha=0.2, color='#FF6B6B')
    ax6a.set_ylabel("Aceleración (m/s²)", fontsize=11)
    ax6a.legend(loc='best')
    ax6a.grid(True, alpha=0.3)
    
    ax6b.plot(t, x*1000, label='Desplazamiento estructura', linewidth=2, color='#4ECDC4')
    ax6b.fill_between(t, x*1000, alpha=0.2, color='#4ECDC4')
    ax6b.set_xlabel("Tiempo (s)", fontsize=11)
    ax6b.set_ylabel("Desplazamiento (mm)", fontsize=11)
    ax6b.legend(loc='best')
    ax6b.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig6)
    plt.close()

with tab4:
    st.markdown("### 📐 Información Técnica del Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Ecuación Diferencial
        $$m \\ddot{x} + c \\dot{x} + k x = -m \\cdot a_{ground}(t)$$
        
        Donde:
        - **m**: Masa de la estructura (kg)
        - **c**: Amortiguamiento viscoso (N·s/m)
        - **k**: Rigidez lateral (N/m)
        - **x**: Desplazamiento relativo (m)
        - **a_ground(t)**: Aceleración del suelo
        """)
    
    with col2:
        st.markdown(f"""
        #### Parámetros Dinámicos Calculados
        - **Frecuencia Natural**: ω_n = {omega_n:.3f} rad/s ({freq_nat:.3f} Hz)
        - **Período Natural**: T = {periodo:.3f} s
        - **Amortiguamiento Crítico**: c_c = {c_critic:.3f} N·s/m
        - **Razón de Amortiguamiento**: ζ = {zeta:.3f}
        - **Tipo**: {"Subamortiguado" if zeta < 1 else "Críticamente amortiguado" if zeta == 1 else "Sobreamortiguado"}
        """)
    
    st.markdown("""
    #### Método de Integración
    Se utiliza el método de **Runge-Kutta de orden 4-5 (RK45)** para resolver 
    numéricamente la ecuación diferencial con alta precisión y paso adaptativo.
    
    #### Generación de Sismo Sintético
    El acelerograma se genera mediante **superposición de wavelets Ricker** con diferentes
    frecuencias y tiempos de arribo, simulando un evento sísmico realista.
    """)

# =============================
# Estadísticas y resumen
# =============================
st.divider()
st.subheader("📋 Resumen de Resultados")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Desplazamiento Máximo",
        f"{np.max(np.abs(x))*1000:.2f} mm",
        delta=f"±{np.max(np.abs(x))*1000:.2f} mm"
    )

with col2:
    st.metric(
        "Velocidad Máxima",
        f"{np.max(np.abs(v))*1000:.2f} mm/s",
        delta=f"±{np.max(np.abs(v))*1000:.2f} mm/s"
    )

with col3:
    st.metric(
        "Aceleración Máxima",
        f"{np.max(np.abs(a_struct)):.2f} m/s²",
        delta=f"±{np.max(np.abs(a_struct)):.2f} m/s²"
    )

with col4:
    st.metric(
        "Energía Total Máxima",
        f"{np.max(E_total):.4f} J"
    )

# =============================
# Footer
# =============================
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🔬 Simulador educativo de dinámica estructural")
with col2:
    st.caption("📊 Análisis de respuesta sísmica SDOF")
with col3:
    st.caption(f"v1.0 - {T}s @ {intensidad:.1f}x intensidad")

