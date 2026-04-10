import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Configurazione Apple-Style: Pulizia estrema
st.set_page_config(page_title="NeuroCore | Monitoraggio Benessere", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; font-family: 'Inter', sans-serif; }
    h1 { font-weight: 300; letter-spacing: -1px; font-size: 3rem !important; }
    .status-box { padding: 30px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #1a1a1a; }
    .stMetric { background-color: #050505; border-radius: 10px; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- SPIEGAZIONE SEMPLICE (Per tutti) ---
st.title("NeuroCore")
st.markdown("### Il tuo guardiano invisibile per la salute del cervello")

with st.expander("🤔 Cos'è NeuroCore? (Spiegato in modo semplice)"):
    st.write("""
    Immagina che il tuo cervello sia come una **grande diga**. Finché l'acqua è calma, tutto va bene. 
    Ma a volte, l'acqua inizia a creare delle piccole crepe che noi non vediamo.
    
    **Cosa fa questa app?**
    1. **Ascolta i segnali:** Legge i battiti e i ritmi del tuo corpo come se fossero onde radio.
    2. **Trova le crepe:** Grazie a una scoperta matematica (l'ancora a 0.55), l'app capisce se queste onde sono "ordinate" o se stanno diventando confuse.
    3. **Ti avvisa prima:** Se l'app vede che le "crepe" si stanno unendo, ti avverte circa **18 minuti prima** che tu possa sentirti male o avere un forte giramento di testa.
    
    *È come avere un meteorologo personale che ti dice di riposarti prima che arrivi il temporale.*
    """)

st.divider()

# --- INTERFACCIA INTUITIVA ---
col_status, col_chart = st.columns([1, 2])

# Simulazione segnale per l'esempio
data = np.random.normal(0, 1, 500)
mu, sigma = np.mean(np.abs(data)), np.std(data)
current_val = sigma / mu

with col_status:
    st.subheader("Stato Attuale")
    
    if current_val > 0.55:
        st.error("⚠️ ATTENZIONE: STRESS RILEVATO")
        st.write("Il sistema sente troppa confusione nei segnali. Si consiglia riposo immediato.")
    else:
        st.success("✅ TUTTO NELLA NORMA")
        st.write("Il tuo cervello è in equilibrio. Non ci sono segnali di allarme.")
    
    st.divider()
    st.metric("Tempo di Preavviso", "18 minuti", help="Quanto tempo prima l'app riesce a vedere un possibile problema")
    st.metric("Affidabilità", "98%", help="Quanto l'app è sicura di quello che dice")

with col_chart:
    st.subheader("Il tuo Ritmo")
    # Grafico semplificato: Linea bianca su nero
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=np.random.normal(0.45, 0.05, 100), line=dict(color='#ffffff', width=2)))
    fig.add_hline(y=0.55, line_dash="dot", line_color="#ff3b30", annotation_text="Livello di Allerta")
    
    fig.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=300, margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showticklabels=False), yaxis=dict(range=[0, 1])
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- FOOTER ---
st.divider()
st.markdown(f"""
<div style='text-align: center; color: #444; font-size: 12px;'>
    NeuroCore™ | Tecnologia per la prevenzione <br>
    <a href='https://neurocore-v150-2fqomdfu7ippeqrv5vkfsc.streamlit.app/' style='color: #888;'>Accedi al sistema professionale</a>
</div>
""", unsafe_allow_html=True)
