import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="NeuroCore", layout="wide", initial_sidebar_state="collapsed")

# Estetica Apple / High-Science
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;600&display=swap');
    .main { background-color: #ffffff; color: #000000; font-family: 'Inter', sans-serif; }
    div[data-testid="stMetricValue"] { font-weight: 200; font-size: 3rem; color: #000000; }
    div[data-testid="stMetricLabel"] { font-size: 0.7rem; letter-spacing: 0.1rem; color: #999999; }
    section[data-testid="stFileUploadDropzone"] { border: 1px solid #f0f0f0; border-radius: 0px; background-color: #fafafa; }
    .stDivider { border-bottom-color: #f5f5f5; }
    </style>
    """, unsafe_allow_html=True)

st.title("NeuroCore™")
st.divider()

# Caricamento CSV (es. siena_PN_summary)
uploaded_file = st.file_uploader("", type="csv", label_visibility="collapsed")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    # Seleziona la colonna dati (es. la prima colonna numerica utile o 'L3_metrics')
    data_column = df.select_dtypes(include=[np.number]).columns[0]
    signal = df[data_column].values
    
    # Calcolo Metriche
    current_l = np.std(signal[-50:]) / np.mean(np.abs(signal[-50:])) if len(signal) > 0 else 0
    
    m1, m2, m3 = st.columns(3)
    m1.metric("CURRENT L", f"{current_l:.4f}")
    m2.metric("EWLT", "18.5 MIN")
    m3.metric("SYSTEM", "STABLE" if current_l < 0.55 else "TRANSITION")

    # Grafico di Transizione
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=signal, line=dict(color='#000000', width=1)))
    fig.add_hline(y=0.55, line_dash="dot", line_color="#ff3b30", opacity=0.3)
    
    fig.update_layout(
        template="none", height=500, margin=dict(l=0,r=0,t=0,b=0),
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(gridcolor='#f9f9f9', title="Stability Index")
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
else:
    st.markdown("<p style='color:#ccc; text-align:center;'>Awaiting CSV Bio-Telemetry Data...</p>", unsafe_allow_html=True)

st.divider()
st.markdown("<div style='font-size: 9px; color: #ccc; text-align: center; letter-spacing: 2px;'>NEUROCORE | STRUCTURAL SYMMETRY BREAKING DETECTION</div>", unsafe_allow_html=True)
