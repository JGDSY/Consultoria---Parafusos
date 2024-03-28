import pandas as pd
from scipy.stats import ttest_ind, bartlett
from statistics import mean, variance

# Defina o caminho para o arquivo CSV
caminho = "/arquivo_modificado.csv"

# Leia o arquivo CSV
dados = pd.read_csv(caminho)

# Visualize os primeiros registros do dataframe
print(dados.head())

# Calcular a média e a variância da coluna 'Qtde' por cada valor distinto da coluna 'vin'
media_var_por_vin = dados.groupby('vin')['Qtde'].agg(Media=lambda x: mean(x), Variancia=lambda x: variance(x)).reset_index()

# Visualizar o resultado da média e variância por vin
print(media_var_por_vin)

# Calcular a média e a variância da coluna 'Qtde' por cada tipo de 'PN'
media_var_por_PN = dados.groupby('PN')['Qtde'].agg(Media=lambda x: mean(x), Variancia=lambda x: variance(x)).reset_index()

# Visualizar o resultado da média e variância por PN
print(media_var_por_PN)

# Média e variancia da PN
MPN = media_var_por_PN['Media'].mean()
VPN = media_var_por_PN['Variancia'].mean()

# Média e variancia da vin
Mvin = media_var_por_vin['Media'].mean()
Vvin = media_var_por_vin['Variancia'].mean()

# Teste t de Student para médias
t_stat, t_p_value = ttest_ind(media_var_por_PN['Media'], media_var_por_vin['Media'], equal_var=False)

# Teste de Bartlett para igualdade de variâncias
bartlett_stat, bartlett_p_value = bartlett(media_var_por_PN['Variancia'], media_var_por_vin['Variancia'])

# Imprimir os resultados
print("Teste t de Student para médias:")
print(f"Estatística t: {t_stat}\np-valor: {t_p_value}")

print("\nTeste de Bartlett para igualdade de variâncias:")
print(f"Estatística de Bartlett: {bartlett_stat}\np-valor: {bartlett_p_value}")