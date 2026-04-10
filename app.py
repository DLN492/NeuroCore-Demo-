import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- SYSTEM ARCHITECTURE ---
st.set_page_config(page_title="NeuroCore v1.5.1", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;600&family=JetBrains+Mono:wght@300&display=swap');
    .main { background-color: #ffffff; color: #000000; font-family: 'Inter', sans-serif; }
    div[data-testid="stMetricValue"] { font-weight: 200; font-size: 2.8rem; color: #000000; letter-spacing: -1px; }
    div[data-testid="stMetricLabel"] { font-size: 0.7rem; letter-spacing: 0.15rem; text-transform: uppercase; color: #999999; }
    section[data-testid="stFileUploadDropzone"] { border: 1px solid #f0f0f0; border-radius: 0px; background-color: #fafafa; }
    .stDivider { border-bottom-color: #f5f5f5; }
    </style>
    """, unsafe_allow_html=True)

# --- NEURODYNAMICAL ENGINE ---
def compute_l_operator(data):
    mu = np.mean(np.abs(data))
    sigma = np.std(data)
    return sigma / mu if mu != 0 else 0

# --- HEADER ---
st.title("NeuroCore™")
st.divider()

uploaded_file = st.file_uploader("", type="csv", label_visibility="collapsed")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    # Mapping colonne dal file caricato 
    target_col = 'FS' if 'FS' in df.columns else df.select_dtypes(include=[np.number]).columns[0]
    signal = df[target_col].values
    time_axis = df['t'].values if 't' in df.columns else np.arange(len(signal))
    
    window = 50
    l_path = [compute_l_operator(signal[i:i+window]) for i in range(len(signal)-window)]
    l_path = np.array(l_path)
    current_phi = l_path[-1]
    
    # --- DYNAMIC LEAD TIME CALCULATION (AUTO-DETECT) ---
    threshold = 0.55
    # Se il segnale non raggiunge mai 0.55, usiamo il 90% del valore massimo trovato nel CSV 
    effective_threshold = threshold if np.max(l_path) >= threshold else np.max(l_path) * 0.9
    
    try:
        critical_idx = np.where(l_path >= effective_threshold)[0][0]
        # Lead Time calcolato tra la rilevazione e la fine del flusso 
        dynamic_lead = time_axis[-1] - time_axis[critical_idx + window]
        lead_label = f"{dynamic_lead:.2f} units"
        status_msg = "TRANSITION" if current_phi >= threshold else "RISK DETECTED"
    except (IndexError, StopIteration):
        dynamic_lead = 0
        lead_label = "STABLE"
        status_msg = "NOMINAL"

    # --- KPI METRICS ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Current L (ϕ)", f"{current_phi:.4f}")
    m2.metric("Target (ϕ*)", f"{threshold:.2f}")
    m3.metric("Specific Lead", lead_label) 
    m4.metric("Status", status_msg)

    st.divider()

    # --- VISUAL ANALYTICS ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_axis[window:], y=l_path, line=dict(color='#000000', width=1.2), name="L-Index"))
    
    # Soglia Omeostatica
    fig.add_hline(y=threshold, line_dash="dot", line_color="#ff3b30", opacity=0.4, annotation_text="Invariante 0.55")
    
    # Punto di Predizione Specifica rilevato nel CSV 
    if dynamic_lead > 0:
        prediction_time = time_axis[critical_idx + window]
        fig.add_vline(x=prediction_time, line_color="#007bff", opacity=0.5, line_width=2)
        fig.add_annotation(x=prediction_time, y=np.max(l_path), text="PREDICTION POINT", showarrow=False, font=dict(size=10, color="#007bff"))
    
    fig.update_layout(template="none", height=450, margin=dict(l=0, r=0, t=10, b=0),
                      xaxis=dict(showgrid=False, title="Time (t)"),
                      yaxis=dict(gridcolor='#f9f9f9', zeroline=False, title="Index (ϕ)"))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

else:
    st.markdown("<p style='text-align:center; color:#ccc; margin-top:50px;'>LOAD NEURO-TELEMETRY DATASET FOR ANALYSIS</p>", unsafe_allow_html=True)

st.divider()
st.markdown("<div style='text-align: center; font-size: 9px; color: #ccc;'>NEURODYNAMIC REGIME FRAMEWORK | D. L. NICOLETTI</div>", unsafe_allow_html=True)
