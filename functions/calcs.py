import numpy as np
import locale
import pandas as pd

def otimiza(qtde, price, multa):
    espaco_busca = np.sort(np.array(qtde))
    espaco_probs = (
        np.array([np.sum(espaco_busca > x) for x in espaco_busca]) 
        / espaco_busca.shape[0]
    )

    espaco_resultado = (
        multa * espaco_probs 
        + price * (espaco_busca - np.mean(espaco_busca)) * (1 - espaco_probs)
    )

    index_x = np.argmin(espaco_resultado)

    return {'qtd_min': espaco_busca[0], 
            'qtd_max': espaco_busca[-1],
            'valor_recomendado': espaco_busca[index_x],
            'custo_esperado': espaco_resultado[index_x],
            'quantidade': espaco_busca,
            'custos': espaco_resultado
            }

def calcular_valor_total(df):
    
    df['Total'] = (df['qtd_max'] - df['valor_recomendado']) * df['Price']
    df = df.groupby('PN').agg({'Total':'sum'})
    df = df.sort_values(by='Total', ascending=False)
    
    # Percentual acumulado para dividir o df
    valor_total = df['Total'].sum().round(decimals=2)
    df['Perc'] = (100*df['Total']/valor_total).round(decimals=2)
    df['Perc_Acum'] = df['Perc'].cumsum()
    
    # Problema: não é a melhor opção pois agora a coluna Total será string
    # Não é problema: trata-se de variável local sem impacto global
    df['Total'] = df['Total'].map(lambda x: locale.currency(x, grouping=True))
    
    dfA = df.query('Perc_Acum<=80')
    dfB = df.query('Perc_Acum>80')
    
    return dfA, dfB

def get_recomendacoes(df, multa):
    df_precos = df.groupby('PN').agg({'Price':'mean'})
    df_qtd = df.groupby(['phantom', 'PN']).agg({'Qtde':lambda x: list(x)}).reset_index()
    df_qtd_preco = pd.merge(left=df_qtd, right=df_precos, on='PN', how='left')
    
    resultados = pd.DataFrame(
        df_qtd_preco.apply(lambda x: otimiza(x['Qtde'], x['Price'], multa), axis=1).to_list()
    )

    df_recomendacoes = pd.concat([df_qtd_preco, resultados], axis=1)
    
    df_recomendacoes['Reducao'] = df_recomendacoes['qtd_max'] - df_recomendacoes['valor_recomendado']
    df_recomendacoes = df_recomendacoes.sort_values(by='Reducao', ascending=False)

    return df_recomendacoes