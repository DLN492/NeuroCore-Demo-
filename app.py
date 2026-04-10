import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Minimal System Configuration
st.set_page_config(page_title="NeuroCore", layout="wide", initial_sidebar_state="collapsed")

# Ultra-Light Apple Aesthetics
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;600&display=swap');
    
    .main { background-color: #ffffff; color: #000000; font-family: 'Inter', sans-serif; }
    .stMetric { border-bottom: 1px solid #eeeeee; padding: 10px 0px; }
    div[data-testid="stMetricValue"] { font-weight: 200; font-size: 2.5rem; color: #000000; }
    div[data-testid="stMetricLabel"] { font-size: 0.7rem; letter-spacing: 0.1rem; text-transform: uppercase; color: #999999; }
    
    /* File Uploader Custom Style */
    section[data-testid="stFileUploadDropzone"] {
        border: 1px dashed #dddddd;
        border-radius: 0px;
        background-color: #fafafa;
    }
    
    .stDivider { border-bottom-color: #f0f0f0; }
    h2 { font-weight: 200; letter-spacing: -1px; }
    </style>
    """, unsafe_allow_html=True)

# Core Engine
def l_operator(data):
    return np.std(data) / np.mean(np.abs(data)) if np.mean(np.abs(data)) != 0 else 0

# Header
c1, c2 = st.columns([8, 2])
with c1:
    st.title("NeuroCore™")
with c2:
    st.markdown("<br><p style='text-align:right; font-size:10px; color:#ccc;'>BUILD 6D59BD8D</p>", unsafe_allow_html=True)

st.divider()

# Input Layer
uploaded_file = st.file_uploader("", type="csv", label_visibility="collapsed")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    signal = df.iloc[:, 0].values
else:
    signal = np.random.normal(10, 2, 1000) # Baseline Default

# Metrics Layer
m1, m2, m3 = st.columns(3)
k_val = l_operator(signal[-100:])
m1.metric("L-INDEX", f"{k_val:.4f}")
m2.metric("TARGET", "0.5500")
m3.metric("STATUS", "CRITICAL" if k_val >= 0.55 else "STABLE")

# Visual Analytics Layer
fig = go.Figure()
fig.add_trace(go.Scatter(
    y=[l_operator(signal[i:i+50]) for i in range(len(signal)-50)],
    line=dict(color='#000000', width=1),
    hoverinfo='none'
))
fig.add_hline(y=0.55, line_dash="dot", line_color="#ff3b30", line_width=1)

fig.update_layout(
    template="none",
    margin=dict(l=0, r=0, t=20, b=0),
    height=450,
    xaxis=dict(showgrid=False, visible=False),
    yaxis=dict(showgrid=True, gridcolor='#f0f0f0', zeroline=False),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Terminal Footer
st.divider()
st.markdown("""
<div style='display: flex; justify-content: space-between; font-size: 9px; color: #bbb; letter-spacing: 1px;'>
    <span>NEURO-STABILITY INVARIANT ANALYSIS</span>
    <span><a href='https://neurocore-v150-2fqomdfu7ippeqrv5vkfsc.streamlit.app/' style='color:#bbb; text-decoration:none;'>REMOTE INSTANCE 1.5.0</a></span>
</div>
""", unsafe_allow_html=True)
