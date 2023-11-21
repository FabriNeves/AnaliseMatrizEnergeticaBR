import pandas as pd
import plotly.express as px

dtype_mapping = {
    'DatGeracaoConjuntoDados': str,
    'SigTipoGeracao': str,
    'QtdUsinasPeriodo': int,
    'MdaPotenciaInstaladaKW': str,
    'MesReferencia': int,
    'AnoReferencia': int
}

geracaoBR = pd.read_csv("/content/drive/MyDrive/Ciencia de Dados/Analise setor Energia/AnaliseDadosMatrizEnergeticaBR/Dados/empreendimento-operacao-historico.csv", sep=';', dtype=dtype_mapping, decimal=',')

geracaoBR['Data'] = pd.to_datetime(geracaoBR['AnoReferencia'].astype(str) + '-' + geracaoBR['MesReferencia'].astype(str) + '-01')
geracaoBR['Data'] = geracaoBR['Data'].dt.strftime('%Y-%m-%d')

geracaoBR['MdaPotenciaInstaladaKW'] = geracaoBR['MdaPotenciaInstaladaKW'].str.replace(',', '.', regex=True).astype(float)


tiposDeGeracao = geracaoBR['SigTipoGeracao'].unique()

mapeamento_tipos = {
    'PCH': 'Pequena Central Hidrelétrica',
    'UHE': 'Usina Hidrelétrica',
    'CGH': 'Central Geradora Hidrelétrica',
    'UTE': 'Usina Termelétrica',
    'UTN': 'Usina Termonuclear',
    'EOL': 'Central Geradora Eólica',
    'UFV': 'Central Geradora Solar Fotovoltaica',
    'CGU': 'Central Geradora Undi-elétrica'
}


geracaoBR['TipoGeracao'] = geracaoBR['SigTipoGeracao'].map(mapeamento_tipos)

print(geracaoBR.columns)

geracaoBR['MdaPotenciaInstaladaMW'] = geracaoBR['MdaPotenciaInstaladaKW']/1000

geracaoBR = geracaoBR.sort_values(by='Data')



# display(geracaoBR)

import plotly.express as px


fig = px.line(geracaoBR, x='Data', y='MdaPotenciaInstaladaMW', color='TipoGeracao',
              labels={'MdaPotenciaInstaladaMW': 'Potência Instalada (MW)'}, title='Potência Instalada')
fig.show()

tipos = geracaoBR['SigTipoGeracao'].unique()

dadosPizza = {'Tipo': [], 'PotInstalada': []}

for tipo in tipos:
    temp = geracaoBR[geracaoBR['SigTipoGeracao'] == tipo]
    ultimoValor = temp['MdaPotenciaInstaladaMW'].iloc[-1]
    dadosPizza['Tipo'].append(tipo)
    dadosPizza['PotInstalada'].append(ultimoValor)

df_dados_pizza = pd.DataFrame(dadosPizza)

df_dados_pizza['TipoGeracaoNome'] = df_dados_pizza['Tipo'].map(mapeamento_tipos)

print(df_dados_pizza)

pizza = px.pie(df_dados_pizza, names='TipoGeracaoNome', values='PotInstalada', title='Percentual da matriz energética do Brasil (MW)')
pizza.show()


# Imprimir o valor da terceira linha da coluna 'MdaPotenciaInstaladaKW'
valor_terceira_linha = geracaoBR.loc[2, 'MdaPotenciaInstaladaKW']
print(f"Valor da terceira linha em MdaPotenciaInstaladaKW: {valor_terceira_linha}")

# Obter tipos de geração únicos
tipos_de_geracao = geracaoBR['SigTipoGeracao'].unique()

# Iterar sobre os tipos de geração
for tipo in tipos_de_geracao:
    # Filtrar o DataFrame para o tipo de geração
    df_filtrado_tipo = geracaoBR.loc[geracaoBR['SigTipoGeracao'] == tipo]

    # Converter a coluna 'Data' para o formato datetime se ainda não estiver no formato adequado
    df_filtrado_tipo['Data'] = pd.to_datetime(df_filtrado_tipo['Data'])

    # Calcular a média por ano
    media_por_ano_tipo = df_filtrado_tipo.groupby('AnoReferencia')['MdaPotenciaInstaladaMW'].mean().reset_index()

    # Calcular a variação em relação ao ano anterior
    media_por_ano_tipo['Variacao'] = media_por_ano_tipo['MdaPotenciaInstaladaMW'].pct_change() * 100

    # Imprimir o resultado para o tipo de geração atual
    print(f"\nVariação Anual da Média de Potência Instalada ({tipo}) em relação ao ano anterior:")
    print(media_por_ano_tipo)

    # Criar um gráfico de barras da variação usando Plotly Express
    fig_tipo = px.bar(media_por_ano_tipo, x='AnoReferencia', y='Variacao',
                      labels={'Variacao': 'Variação em %'},
                      title=f'Variação Anual da Média de Potência Instalada ({tipo}) em relação ao ano anterior')
    fig_tipo.show()
