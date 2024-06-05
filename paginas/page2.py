import streamlit as st
from functions.calcs import calcular_valor_total

def pagina2(df_recomendacoes):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("80% do valor de estoque")
        df_classeA, df_classeB = calcular_valor_total(df_recomendacoes)
        st.write(df_classeA)
    with col2:
        st.subheader("20% do valor de estoque")
        st.write(df_classeB)