from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import os

def file_path(path):
    new_path = os.path.join(os.path.dirname(__file__), path)
    return new_path

path_turma = os.path.join(os.path.dirname(__file__), "../data/2023.1/desempenho_da_turma.csv")

df_turma = pd.read_csv(path_turma)

df_turma_long = df_turma.melt(id_vars='list', value_vars=['hits', 'parcial', 'undone'])
df_turma_long['status'] = df_turma_long['variable'].map({'hits': 'Concluído', 'parcial': 'Incompleto', 'undone': 'Pendente'})

fig_turma = px.bar(df_turma_long, x="list", y="value",
                   color="status",
                   title="Desempenho da Turma por Lista",
                   labels={"list": "Lista de Exercícios", "value": "Número de Submissões", "status": "Status"},
                   template="plotly_dark")


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

app.layout = [
    html.H1(children='Dashboard Dataviewer', style={'textAlign':'center'}),
    dcc.Graph(id='desempenho_turma', figure=fig_turma)
]

if __name__ == '__main__':
    app.run(debug=True)
