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

# Salvar os gráficos como strings HTML
barras_html = barras.to_html(full_html=False, include_plotlyjs='cdn')
pizza_html = pizza.to_html(full_html=False, include_plotlyjs='cdn')

# Salvar o conteúdo em arquivos para incorporar no index.html
with open('barras_html.txt', 'w') as f:
    f.write(barras_html)

with open('pizza_html.txt', 'w') as f:
    f.write(pizza_html)

print("Gráficos salvos como strings HTML.")
