import streamlit as st
from functions.calcs import calcular_valor_total

def pagina2(df_recomendacoes):
    df_classeA, df_classeB = calcular_valor_total(df_recomendacoes)
    
    st.subheader("80% do valor de estoque")
    st.write(df_classeA)

    st.subheader("20% do valor de estoque")
    st.write(df_classeB)