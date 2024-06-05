import streamlit as st
import locale
import matplotlib.pyplot as plt

def pagina1(df_recomendacoes):
    st.subheader("Dashboard com Tabela")
    
    # ganho_financeiro, quantidade de dinheiro economizada anualmente
    ganho_financeiro = (df_recomendacoes['Price'] * df_recomendacoes['Reducao']).sum()
    # um ano possui aproximadamente 240 dias uteis
    # um mes possui aproximadamente 20 dias uteis
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.metric("PNs alterados", str(df_recomendacoes.query('Reducao!=0').shape[0]))
    with col1_2:
        st.metric("Redução (R$) por dia", locale.currency((ganho_financeiro/240)))

    col2_1, col2_2 = st.columns(2)
    with col2_1:
        st.metric("Redução (R$) por mês", locale.currency((ganho_financeiro/12)))
    with col2_2:
        st.metric("Redução (R$) por ano", locale.currency((ganho_financeiro)))
    
    # Tabela
    df_tabela = df_recomendacoes[["phantom", "PN", "Price", "qtd_max", "valor_recomendado", "Reducao"]]
    st.write(df_tabela.query('Reducao!=0'))
    

    
    # Filtrar somente os que houveram recomendacao para o grafico
    df_graf = df_recomendacoes.query('Reducao!=0')
    if len(df_graf) > 0:
        st.subheader('Gráfico de Otimização de Valores')
        
        # Seleção de Phanton e PN
        phantom_exemplo = st.selectbox('Selecione uma phantom para filtrar', 
                                       sorted(df_graf.query('Reducao!=0')['phantom'].unique()))
        pn_exemplo = st.selectbox('Selecione um PN para filtrar', 
                                  sorted(df_graf.query('phantom==@phantom_exemplo')['PN'].unique()))
        
        # Problema prioridade: além de recalcular tudo, em algumas vezes o cálculo difere
        # Solução: sem recálculos. Reaproveitamento do método já utilizado.
    
        fig, ax = plt.subplots()

        df_recomendacoes_filtro = df_recomendacoes.query('phantom==@phantom_exemplo & PN==@pn_exemplo')

        quantidade = df_recomendacoes_filtro['quantidade'].iloc[0]
        custos = df_recomendacoes_filtro['custos'].iloc[0]

        ax.bar(
            [str(quant) for quant in quantidade], 
            custos, 
            label='quantidade'
        )
        
        posicao = df_recomendacoes_filtro['valor_recomendado'].iloc[0]
            
        ax.axvline(x=str(posicao), color='r', linestyle='--', label='Recomendado')

        ax.set_xlabel('Quantidade')
        ax.set_ylabel('Valores (R$)')
        ax.set_title(f'Gráfico Qtde vs Custo (phantom {phantom_exemplo}: {pn_exemplo})')
        
        ax.legend()
        
        st.pyplot(fig)