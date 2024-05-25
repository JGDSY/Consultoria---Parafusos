import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import locale
import matplotlib.pyplot as plt
from random import choice
from functions.formats import format_currency, format_perc
from functions.calcs import otimiza, calcular_valor_total, get_recomendacoes

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Problema opcional: dividir o codigo em alguns arquivos separados
#           por exemplo, funcoes, pagina1, pagina2

#
# Adicionar um campo de entrada para o valor da multa
multa = st.sidebar.number_input("Valor da Multa", value=5000)
    
# Adicionar um menu para carregar um novo dataset
uploaded_file = st.sidebar.file_uploader("Carregar arquivo CSV", type=["csv"])

# Ler o arquivo CSV carregado pelo usuario ou disponibilizar o salvo na pasta
if uploaded_file is None:
    csv_file = "dados_vins.csv"
    df = pd.read_csv(csv_file)
else:
    df = pd.read_csv(uploaded_file)
df['phantom']=df['phantom'].astype(str)
df_recomendacoes = get_recomendacoes(df, multa)

def pagina1():
    st.subheader("Dashboard com Tabela")
    
    # ganho_financeiro, quantidade de dinheiro economizada anualmente
    ganho_financeiro = (df_recomendacoes['Price'] * df_recomendacoes['Reducao']).sum()
    st.write('PN com qtde alterada:',
             str(df_recomendacoes.query('Reducao!=0').shape[0]),
             "<br>Redução em disposição de fixadores por dia: " +
             str(format_currency(ganho_financeiro/240))+
             "<br>Redução em disposição de fixadores por mês: " +
             str(format_currency(ganho_financeiro/20))+
             '<br>Redução em disposição de fixadores por ano: ' +
             str(format_currency(ganho_financeiro)),
             unsafe_allow_html=True)
    # um ano possue aproximadamente 240 dias uteis
    # um mes possue aproximadamente 20 dias uteis
    
    # Tabela
    df_tabela = df_recomendacoes.drop(columns=['Qtde', 'qtd_min', 'custo_esperado'])
    st.write(df_tabela.query('Reducao!=0'))
    




    st.subheader('Gráfico')
    
    # Filtrar somente os que houveram recomendacao para o grafico
    df_graf = df_tabela.query('Reducao!=0')
    
    # Flexibilizar o phantom e pn
    # Problema, defini phantom_exemplo e pn_exemplo duas vezes
    #   - uma para colocar um valor aleatório qualquer e outra para deixar o usuário escolher
    # provavelmente existe uma maneira melhor para fazer isso
    phantom_exemplo = df_graf.sample(1).iloc[0,0]
    phantom_exemplo = st.selectbox('Selecione uma phantom para filtrar', 
                          sorted(df_graf.query('Reducao!=0')['phantom'].unique()))
    pn_exemplo = df_graf.query('phantom==@phantom_exemplo').sample(1).iloc[0, 1]
    pn_exemplo = st.selectbox('Selecione um pn para filtrar', 
                          sorted(df_tabela.query('phantom==@phantom_exemplo')['PN'].unique()))
    
    # Pegar todas as quantidades em df através do filtro
    calculo = df.query('phantom==@phantom_exemplo & PN==@pn_exemplo')[['PN','Qtde','Price']]
    calculo = calculo.sort_values('Qtde').reset_index(drop = True)
    
    # Problema: acabei calculando todas as otimizações novamente
    # muito ineficaz eheheh
    espaco_busca = np.array(calculo['Qtde'])
    espaco_probs = np.array([np.sum(espaco_busca > x) 
                             for x in espaco_busca]) / espaco_busca.shape[0]
    calculo['Probs'] = espaco_probs
    
    calculo['Custo'] = multa * calculo['Probs'] + calculo['Price'] * (
        espaco_busca - np.mean(calculo['Probs'])) * (1 - calculo['Probs'])
    calculo['Custo'] = calculo['Custo'].round(2)
    calculo = calculo.sort_values('Qtde')
    
    calculo = calculo.groupby(['PN', 'Qtde'],
                              as_index = False).agg({'Custo':'mean', 
                                            'Probs': 'mean'})
    calculo['Categoria'] = calculo['Qtde'].astype(str)
    # calculo.sort_values('Custo', inplace=True)
    
    st.write(calculo)

    ######TESTE
    calculo = df_recomendacoes.merge(df, how="left", on= ['PN', 'phantom']).query('phantom==@phantom_exemplo & PN==@pn_exemplo').sort_values('Qtde_y')
    calculo['Categoria'] = calculo['Qtde_y'].astype(str)

    
    # Problema prioridade: além de recalcular tudo, em algumas vezes o cálculo difere
    # Exemplo phantom: 10847, PN: Parafuso 10x10 10.4
    #       funcao otimiza indica a qtde 176
    #       o meu calculo indica a qtde 234
    # (Renan suspeita que seja algo relacionado aos filtros)
    st.write(calculo.query('PN==@pn_exemplo'))
    st.write(df_recomendacoes.query('PN==@pn_exemplo'))
    
    # Problema
    # Esse gráfico está horrível, a idéia é mostrar:
    # 1- todas qtde possíveis para um determinado pn num determinado phantom
    #       mostradas como barras
    # 2- todos os 'custos financeiros' de cada qtde
    #       mostradas como pontos
    # 3- assinar qual a quantidade que de fato foi escolhida
    #       assinalado pela linha tracejada
    fig, ax = plt.subplots()
    
    # ax.bar(calculo['Categoria'], calculo['Qtde'], label='Qtde')
    ax.bar(calculo['Categoria'], calculo['Qtde_y'], label='Qtde')
    # Problema adicionar ax.scatter com um eixo y paralelo para a
    # as barras não ficarem tão pequenas
    # para contornar isso eu coloquei essa divisão por 15, mas é algo que não deverá permanecer    custo_esperado
    # ax.scatter(calculo['Categoria'], calculo['Custo']/15,
    #         label='Custos', color = 'r')
    ax.scatter(calculo['Categoria'], calculo['custo_esperado']/15,
            label='Custos', color = 'r')


    posicao = df_tabela.query('phantom==@phantom_exemplo & PN==@pn_exemplo')[
        'valor_recomendado'].sort_values().iloc[0]

    # print(df_tabela.query('phantom==@phantom_exemplo & PN==@pn_exemplo')[['phantom', 'PN',
    #     'valor_recomendado']])
        
    ax.axvline(x=str(posicao), color='r', linestyle='--', label='Recomendado')

    ax.set_xlabel('Categorias')
    ax.set_ylabel('Valores')
    ax.set_title('Gráfico Qtde vs Custo')
    
    ax.legend()
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)

def pagina2():
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
    st.write('Em construção')
    
def main():
    pagina_selecionada = 'Página 1'
    # Problema: eu gostaria de deixar esse filtro no top, porem não consegui
    #   Ordem desejada dos 'filtros': Páginas, Carregar arquivo, Valor multa
    opcao_manual = st.sidebar.radio("Opções:", ["Manual", "Relatório"])
    
    # Se a opção "Relatório" for selecionada, expanda as opções de página
    if opcao_manual == "Relatório":
        with st.sidebar.expander("Páginas do Relatório", expanded = True):
            pagina_selecionada = st.radio("Selecione a página:", 
                                          ["Qtdes recomendadas", "Estoque AB", 
                                           "Indicadores financeiros"])

        # Chama a função correspondente com base na página selecionada
        if pagina_selecionada == "Qtdes recomendadas":
            pagina1()
        elif pagina_selecionada == "Estoque AB":
            pagina2()
        else:
            pagina3()
    else:
        manual()
        


if __name__ == "__main__":
    main()
