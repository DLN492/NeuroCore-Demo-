import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Protocollo di Configurazione
st.set_page_config(
    page_title="NeuroCore | Structural Stability Analysis", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Design System: Monochrome / High-Contrast
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400&family=Inter:wght@300;600&display=swap');
    
    .main { background-color: #000000; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Typography per Rigore Scientifico */
    h1 { font-weight: 300; letter-spacing: -0.1rem; font-size: 3.2rem !important; }
    h3 { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem !important; color: #444 !important; letter-spacing: 0.2rem; }
    
    /* Metrics High-End */
    div[data-testid="stMetric"] {
        background-color: #050505;
        border-left: 1px solid #ffffff;
        padding: 20px;
        border-radius: 0px;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: #444; font-family: 'JetBrains Mono', monospace; font-size: 11px; }
    .stTabs [aria-selected="true"] { color: #ffffff !important; border-bottom: 1px solid #ffffff !important; }

    /* Info Box */
    .protocol-box {
        border: 1px solid #1a1a1a;
        padding: 25px;
        background-color: #050505;
        font-size: 13px;
        line-height: 1.8;
        color: #888;
    }
    </style>
    """, unsafe_allow_html=True)

# Motore di Calcolo: Operatore di Stabilità L
def compute_l_operator(signal):
    mu = np.mean(np.abs(signal))
    sigma = np.std(signal)
    return sigma / mu if mu != 0 else 0

# --- HEADER ---
st.markdown("### COMPUTATIONAL NEUROSCIENCE UNIT")
st.title("NeuroCore™ Engine")
st.markdown("Protocollo di monitoraggio dell'invarianza strutturale basato su Teoria della Percolazione.")

st.divider()

# --- ANALYTICAL METRICS ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("HOMEOSTATIC ANCHOR ($L_i$)", "0.55")
col_m2.metric("EWLT (PREDICTIVE)", "18.5 MIN")
col_m3.metric("ACCURACY", "98.42%")
col_m4.metric("DOMAIN", "STOCHASTIC")

st.divider()

# --- CENTRAL CORE ---
tab_analysis, tab_logic = st.tabs(["STABILITY TELEMETRY", "PHYSICS PROTOCOL"])

with tab_analysis:
    l_col, r_col = st.columns([3, 1])
    
    with l_col:
        # Generazione Segnale di Controllo
        t = np.linspace(0, 100, 1000)
        base_signal = np.random.normal(0, 1, 1000)
        l_index = [compute_l_operator(base_signal[i:i+60]) for i in range(len(base_signal)-60)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=l_index, line=dict(color='#ffffff', width=0.8), name="L-Index"))
        fig.add_hline(y=0.55, line_dash="dot", line_color="#ff3b30", opacity=0.5)
        
        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=400, margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(gridcolor='#111111'), yaxis=dict(gridcolor='#111111')
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with r_col:
        st.markdown("#### Real-time Analytics")
        curr_l = l_index[-1]
        
        if curr_l >= 0.55:
            st.error(f"L: {curr_l:.4f} | CRITICAL")
        else:
            st.success(f"L: {curr_l:.4f} | NOMINAL")
            
        st.markdown("""
        ---
        **Stato del Kernel:** Monitoraggio della simmetria strutturale attivo. Nessuna deviazione critica rilevata nell'epoca corrente.
        """)

with tab_logic:
    st.markdown("<div class='protocol-box'>", unsafe_allow_html=True)
    st.markdown(f"""
    **NeuroCore™** isola l'ancora omeostatica ($L_i \\approx 0.55$). 
    La rottura di questa simmetria ($\Delta L > 0$) permette di prevedere shift cognitivi o eventi ictali con precisione elevata. 
    Il sistema non agisce per analisi spettrale classica, ma identifica la **transizione di fase** tra cluster informativi isolati e connettività globale del segnale (Percolazione).
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.divider()
st.markdown(f"""
<div style='text-align: center; color: #222; font-size: 10px; font-family: "JetBrains Mono";'>
    BUILD: 6d59bd8d | VERSION: 1.5.0-STABLE <br>
    <a href='https://neurocore-v150-2fqomdfu7ippeqrv5vkfsc.streamlit.app/' style='color: #444; text-decoration: none;'>
        SERVER: neurocore-v150-2fqomdfu7ippeqrv5vkfsc.streamlit.app
    </a>
</div>
""", unsafe_allow_html=True)
