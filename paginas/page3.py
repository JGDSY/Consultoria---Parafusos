import streamlit as st
import pandas as pd

def pagina3(df_recomendacoes):
    ganho_financeiro = (df_recomendacoes['Price'] * df_recomendacoes['Reducao']).sum()
    
    roi = (ganho_financeiro - 140000) / 1400
    payback = 140000 / (ganho_financeiro / 12)

    st.header('Indicadores Financeiros')

    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.metric("ROI", f"{round(roi, 2)}%")
    with col1_2:
        st.metric("Payback", f"{round(payback, 2)} meses")