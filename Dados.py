import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Carregar os dados
df = pd.read_csv('Tabela.csv')

# Verificar e corrigir espaços nos nomes das colunas
df.columns = df.columns.str.strip()

# Calcular a média de satisfação para as questões (QUEST 1 a QUEST 26)
quest_columns = [col for col in df.columns if col.startswith('QUEST')]
df['media_satisfacao'] = df[quest_columns].mean(axis=1)

# Criar a aplicação Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard Interativo de Satisfação da População", style={'text-align': 'center'}),

    # Dropdown para seleção de categoria de visualização
    html.Div([
        html.Label("Selecione uma Categoria:"),
        dcc.Dropdown(
            id='categoria',
            options=[
                {'label': 'Raça/Cor', 'value': 'Raça/Cor'},
                {'label': 'Sexo', 'value': 'Sexo'},
                {'label': 'Comorbidades', 'value': 'Comorbidades'},
                {'label': 'Naturalidade', 'value': 'Naturalidade'}
            ],
            value='Sexo'  # Valor inicial
        ),
    ], style={'width': '50%', 'margin': 'auto'}),

    html.Div([
        dcc.Graph(id='grafico_satisfacao_barras'),
        dcc.Graph(id='grafico_satisfacao_pizza')
    ])
])

# Callback para atualizar os gráficos com base na seleção de categoria
@app.callback(
    [Output('grafico_satisfacao_barras', 'figure'),
     Output('grafico_satisfacao_pizza', 'figure')],
    [Input('categoria', 'value')]
)
def update_graphs(categoria):
    # Gráfico de barras mostrando a satisfação média por categoria
    barras = px.bar(
        df.groupby(categoria)['media_satisfacao'].mean().reset_index(),
        x=categoria, y='media_satisfacao',
        labels={'media_satisfacao': 'Média de Satisfação'},
        title=f'Média de Satisfação por {categoria}',
        color=categoria,
        color_continuous_scale='Viridis'
    )

    # Gráfico de pizza mostrando a distribuição de pessoas por categoria
    pizza = px.pie(
        df, names=categoria, title=f'Distribuição de {categoria} na População',
        hole=.3,  # Adiciona o efeito de "donut"
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    return barras, pizza

# Rodar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
