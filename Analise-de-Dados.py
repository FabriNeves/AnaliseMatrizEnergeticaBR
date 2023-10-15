import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Carregue os dados do CSV
geracaoBR = pd.read_csv("./Dados/empreendimento-operacao-historico.csv", sep=';')

# Crie a nova coluna 'Data' combinando 'MesReferencia' e 'AnoReferencia'
geracaoBR['Data'] = pd.to_datetime(geracaoBR['AnoReferencia'].astype(str) + '-' + geracaoBR['MesReferencia'].astype(str) + '-01')
geracaoBR['Data'] = geracaoBR['Data'].dt.strftime('%Y-%m-%d')

# Crie uma aplicação web Flask-Dash
app = dash.Dash(__name__) 

# Layout da aplicação web
app.layout = html.Div([
    dcc.Dropdown(
        id='tipo-geracao-dropdown',
        options=[{'label': tipo, 'value': tipo} for tipo in geracaoBR['SigTipoGeracao'].unique()],
        value=geracaoBR['SigTipoGeracao'].unique()[0]
    ),
    dcc.Graph(id='geracao-graph')
])

@app.callback(
    Output('geracao-graph', 'figure'),
    [Input('tipo-geracao-dropdown', 'value')]
)
def update_graph(selected_tipo):
    data_filtrada = geracaoBR[geracaoBR['SigTipoGeracao'] == selected_tipo]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_filtrada['Data'], y=data_filtrada['QtdUsinasPeriodo'], mode='lines', name=f'Quantidade de Usinas de {selected_tipo}'))
    fig.update_layout(
        title=f'Quantidade de Usinas de {selected_tipo} ao longo dos Anos',
        xaxis=dict(title='Data'),
        yaxis=dict(title='Quantidade de Usinas')
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
