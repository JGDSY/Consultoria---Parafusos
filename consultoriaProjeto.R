# Defina o caminho para o arquivo CSV
caminho <- "C:/Users/ ... /arquivo_modificado.csv"

# Leia o arquivo CSV
dados <- read.csv(caminho)

# Visualize os primeiros registros do dataframe
head(dados)

# Calcular a média e a variância da coluna 'Qtde' por cada valor distinto da coluna 'vin'
media_var_por_vin <- aggregate(Qtde ~ vin, data = dados, FUN = function(x) c(Media = mean(x), Variancia = var(x)))

# Visualizar o resultado da média e variância por vin
print(media_var_por_vin)

# Calcular a média e a variância da coluna 'Qtde' por cada tipo de 'PN'
media_var_por_PN <- aggregate(Qtde ~ PN, data = dados, FUN = function(x) c(Media = mean(x), Variancia = var(x)))

# Visualizar o resultado da média e variância por PN
print(media_var_por_PN)

#Média e variancia da PN
MPN<-mean(media_var_por_PN$Qtde[,"Media"])
VPN<-mean(media_var_por_PN$Qtde[,"Variancia"])

#Média e variancia da vin
Mvin<-mean(media_var_por_vin$Qtde[,"Media"])
Vvin<-mean(media_var_por_vin$Qtde[,"Variancia"])


# Teste t de Student para médias
t_test_mean <- t.test(media_var_por_PN$Qtde[, "Media"], media_var_por_vin$Qtde[, "Media"])

# Teste F de Fisher para variâncias
var_test <- var.test(media_var_por_PN$Qtde[, "Variancia"], media_var_por_vin$Qtde[, "Variancia"])

# Imprimir os resultados
print("Teste t de Student para médias:")
print(t_test_mean)

print("Teste F de Fisher para variâncias:")
print(var_test)


