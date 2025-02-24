from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np

def file_path(path):
    new_path = os.path.join(os.path.dirname(__file__), path)
    return new_path

def calc_q1(data):
    data.sort()
    n = len(data)
    if (n - 1) % 2 == 1:
        return data[n//4]
    else:
        return (data[(n//4)] + data[(n-1)//4]) / 2

def calc_q3(data):
    data.sort()
    n = len(data)
    if (n - 1) % 2 == 1:
        return data[(n*3)//4]
    else:
        return (data[((n*3)//4)] + data[((n*3)-1)//4]) / 2

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]    

def box_plot(header):
    path_metrics = os.path.join(os.path.dirname(__file__), "../data/2023.1/metrics_tempo.csv")
    metrics_time = pd.read_csv(path_metrics)
    total_time = list(metrics_time[header].dropna())
    total_time.sort()
    q1 = calc_q1(total_time)
    q3 = calc_q3(total_time)
    iqr = (q3 - q1)
    limite_superior = q3 + iqr * 1.5
    indice = total_time.index(int(find_nearest(total_time, limite_superior)))    
    del total_time[indice:]

    for i in range(len(total_time)):
        total_time[i] = ((total_time[i]/1000)/60)/60

    return total_time

x_data = [f"Lista {i}" for i in range(1, 16)]
y_data = [box_plot(f"tempo_total_gasto_list_id{str(i).zfill(2)}") for i in range(1, 16)]
# for i in range(1, 16):
#     if i < 10:
#        i = "0" + str(i)
#     y_data.append(box_plot(f"tempo_total_gasto_list_id{i}"))
fig = go.Figure()
for xd, yd in zip(x_data, y_data):
    fig.add_trace(go.Box(
        y=yd, 
        name=xd,
        ))
fig.update_layout(yaxis_title='Horas', template='plotly_dark', title='Tempo de realização das listas',)

layout_path = os.path.join(os.path.dirname(__file__), "assets/layout.html")
path_turma = os.path.join(os.path.dirname(__file__), "../data/2023.1/desempenho_da_turma.csv")
path_submissoes = os.path.join(os.path.dirname(__file__), "../data/2023.1/submissoes_por_dia.csv")

df_turma = pd.read_csv(path_turma)
df_submissoes = pd.read_csv(path_submissoes, dayfirst=True, parse_dates=[0])

df_turma_long = df_turma.melt(id_vars='list', value_vars=['hits', 'parcial', 'undone'])
df_turma_long['status'] = df_turma_long['variable'].map({'hits': 'Concluído', 'parcial': 'Incompleto', 'undone': 'Pendente'})

fig_turma = px.bar(df_turma_long, x="list", y="value",
                   color="status",
                   title="Desempenho da Turma por Lista",
                   labels={"list": "Lista de Exercícios", "value": "Número de Submissões", "status": "Status"},
                   template="plotly_dark"
                   )
fig_submissoes = px.line(df_submissoes, x="data", y="qnt_de_submissoes",
                         title="Número de Submissões por Dia",
                         labels={"data": "Data", "qnt_de_submissoes": "Número de Submissões"},
                         template="plotly_dark")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = [
    html.Div(className='side-bar', children=[
        html.Div(className='logo', children=[
            html.Img(src=app.get_asset_url('dataviewer-logo.png'), alt='Logo'),
            html.H2('Dashboard Dataviewer'),
        ]),
        html.Div(className='semestre', children=[
            html.H3('Semestre'),
            html.A('2023.1', className='active'),
            html.A('2023.2'),
            html.A('2024.1'),
            html.A('2024.2'),
        ]),
        html.Div(className='turma', children=[
            html.H3('Turma'),
            html.A('Turma 01'),
            html.A('Turma 02'),
        ]),
    ]),

    html.Div(className='content', children=[
        html.Div(children=[
            dcc.Graph(id='desempenho_turma', figure=fig_turma)
        ]),
        html.Div(className='six columns',children=[
            dcc.Graph(id='tempo_estudantes', figure=fig)
        ]),
        html.Div(className='five columns', children=[
                dcc.Graph(id='submissoes_por_dia', figure=fig_submissoes
            )
        ])
    ]),
]

if __name__ == '__main__':
    app.run(debug=True)
