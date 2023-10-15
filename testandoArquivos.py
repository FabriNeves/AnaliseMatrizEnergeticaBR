import pandas as pd
import matplotlib.pyplot as plt

# Especificar os tipos de dados para cada coluna
dtype_mapping = {
    'DatGeracaoConjuntoDados': str,
    'SigTipoGeracao': str,
    'QtdUsinasPeriodo': int,
    'MdaPotenciaInstaladaKW': str,  # Leitura como string
    'MesReferencia': int,
    'AnoReferencia': int
}

geracaoBR = pd.read_csv("./Dados/empreendimento-operacao-historico.csv", sep=';', dtype=dtype_mapping, decimal=',')

geracaoBR['Data'] = pd.to_datetime(geracaoBR['AnoReferencia'].astype(str) + '-' + geracaoBR['MesReferencia'].astype(str) + '-01')
geracaoBR['Data'] = geracaoBR['Data'].dt.strftime('%Y-%m-%d')

geracaoBR['MdaPotenciaInstaladaKW'] = geracaoBR['MdaPotenciaInstaladaKW'].str.replace(',', '.', regex=True).astype(float)

# Lista dos tipos de geração
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

# Crie uma nova coluna 'TipoGeracao' usando o mapeamento
geracaoBR['TipoGeracao'] = geracaoBR['SigTipoGeracao'].map(mapeamento_tipos)

# Exiba o DataFrame com a nova coluna
# print(geracaoBR.head())

print(geracaoBR.columns)



geracaoBR['MdaPotenciaInstaladaMW'] = geracaoBR['MdaPotenciaInstaladaKW']/1000
print(geracaoBR['MdaPotenciaInstaladaMW'])


