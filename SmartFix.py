import streamlit as st
import pandas as pd
import numpy_financial as npf
import locale
import matplotlib.pyplot as plt
from functions.calcs import calcular_valor_total, get_recomendacoes
from functions.helpers import columns_are_not_ok

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Problema opcional: dividir o codigo em alguns arquivos separados
#           por exemplo, funcoes, pagina1, pagina2
# WIP

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
        st.metric("Redução (R$) por mês", locale.currency((ganho_financeiro/20)))
    with col2_2:
        st.metric("Redução (R$) por ano", locale.currency((ganho_financeiro)))
    
    # Tabela
    df_tabela = df_recomendacoes[["phantom", "PN", "Price", "qtd_max", "valor_recomendado", "Reducao"]]
    st.write(df_tabela.query('Reducao!=0'))
    



    st.subheader('Gráfico')
    
    # Filtrar somente os que houveram recomendacao para o grafico
    df_graf = df_recomendacoes.query('Reducao!=0')
    
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

def pagina2(df_recomendacoes):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("80% do valor de estoque")
        df_classeA, df_classeB = calcular_valor_total(df_recomendacoes)
        st.write(df_classeA)
    with col2:
        st.subheader("20% do valor de estoque")
        st.write(df_classeB)
    
def pagina3():
    st.header('Adicionar ROI, Payback')
    st.write(npf.npv(0.085, [-250000] + [33000] * 24))
    st.write(npf.irr([-250000] + [33000] * 24))
    
def manual():
    st.write('WIP')
    
def main():
    # Problema: eu gostaria de deixar esse filtro no top, porem não consegui
    #   Ordem desejada dos 'filtros': Páginas, Carregar arquivo, Valor multa
    # Solucionado
    # Solução: não utilização de variáveis globais e locais para a mesma seção
    opcao_manual = st.sidebar.radio("Opções:", ["Manual", "Relatório"])
    pagina_selecionada = 'Página 1'
    
    # Se a opção "Relatório" for selecionada, expanda as opções de página
    if opcao_manual == "Relatório":
        with st.sidebar.expander("Páginas do Relatório", expanded = True):
            pagina_selecionada = st.radio("Selecione a página:", 
                                          ["Qtdes recomendadas", "Estoque AB", 
                                           "Indicadores financeiros"])

    
    # Adicionar um menu para carregar um novo dataset
    uploaded_file = st.sidebar.file_uploader("Carregar arquivo CSV", type=["csv"])

    # Definição de multa pelo usuário
    multa = st.sidebar.number_input("Valor da Multa (R$):", value=5000.00)

    # Ler o arquivo CSV carregado pelo usuario ou disponibilizar o salvo na pasta
    if uploaded_file is None:
        csv_file = "dados_vins.csv"
        df = pd.read_csv(csv_file)
    else:
        df = pd.read_csv(uploaded_file)
        if columns_are_not_ok(df):
            csv_file = "dados_vins.csv"
            df = pd.read_csv(csv_file)
            st.warning("As colunas do arquivo não são: 'X,phantom,vin,PN,Qtde,Price'")

    df['phantom']=df['phantom'].astype(str)
    df_recomendacoes = get_recomendacoes(df, multa)
        
    if pagina_selecionada == "Qtdes recomendadas":
        pagina1(df_recomendacoes)
    elif pagina_selecionada == "Estoque AB":
        pagina2(df_recomendacoes)
    elif pagina_selecionada == "Indicadores financeiros":
        pagina3()
    else:
        manual()


if __name__ == "__main__":
    main()
