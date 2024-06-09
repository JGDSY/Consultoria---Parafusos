import streamlit as st
import pandas as pd
import locale
from functions.calcs import get_recomendacoes
from functions.helpers import columns_are_not_ok
from paginas import pagina1, pagina2, pagina3, manual

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
# def manual():
#     st.write('WIP')
    
def main():
    opcao_manual = st.sidebar.radio("Opções:", ["Manual", "Relatório"])
    pagina_selecionada = 'Página 1'
    
    # Se a opção "Relatório" for selecionada, expanda as opções de página
    if opcao_manual == "Relatório":
        with st.sidebar.expander("Páginas do Relatório", expanded = True):
            pagina_selecionada = st.radio("Selecione a página:", 
                                          ["Recomendações: KPIs e Gráficos", 
                                           "Estoque AB", 
                                           "ROI e Payback"])

    
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
        
    if pagina_selecionada == "Recomendações: KPIs e Gráficos":
        pagina1(df_recomendacoes)
    elif pagina_selecionada == "Estoque AB":
        pagina2(df_recomendacoes)
    elif pagina_selecionada == "ROI e Payback":
        pagina3(df_recomendacoes)
    else:
        manual()


if __name__ == "__main__":
    main()
