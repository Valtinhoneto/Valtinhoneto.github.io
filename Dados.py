import pandas as pd
import plotly.express as px

# Carregar os dados
df = pd.read_csv('Tabela.csv')

# Verificar e corrigir espaços nos nomes das colunas
df.columns = df.columns.str.strip()

# Calcular a média de satisfação para as questões (QUEST 1 a QUEST 26)
quest_columns = [col for col in df.columns if col.startswith('QUEST')]
df['media_satisfacao'] = df[quest_columns].mean(axis=1)

# Gráfico de barras mostrando a satisfação média por categoria (Sexo, por exemplo)
barras = px.bar(
    df.groupby('Sexo')['media_satisfacao'].mean().reset_index(),
    x='Sexo', y='media_satisfacao',
    labels={'media_satisfacao': 'Média de Satisfação'},
    title='Média de Satisfação por Sexo',
    color='Sexo',
    color_continuous_scale='Viridis'
)

# Gráfico de pizza mostrando a distribuição de pessoas por sexo
pizza = px.pie(
    df, names='Sexo', title='Distribuição de Sexo na População',
    hole=.3,  # Adiciona o efeito de "donut"
    color_discrete_sequence=px.colors.sequential.RdBu
)

# Exportar para HTML
barras.write_html('barras.html')
pizza.write_html('pizza.html')
