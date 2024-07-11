from dash import Dash, html, dcc, Input, Output 
import plotly.express as px
import pandas as pd
# usei o 'os' pois foi a melhor ferramenta para rastrear as tabelas .xlsx
import os

app = Dash(__name__)

# utilizei para modificar as estruturas em HTML e aplicar a fonte
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Estatísticas de Desempenho</title>
        <link href="https://fonts.cdnfonts.com/css/florida-project" rel="stylesheet">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# utilizei para direcionar aos diretórios
file_path_turma = os.path.join(os.path.dirname(__file__), "tabela_desempenho_da_turma.xlsx")
file_path_estudante = os.path.join(os.path.dirname(__file__), "desempenho_estudante_turma.xlsx")

# usado para selecionar os dados da tabela
df_turma = pd.read_excel(file_path_turma)
df_estudante = pd.read_excel(file_path_estudante)

# gerador de gráficos
fig_turma = px.bar(df_turma, x="list", y=["hits", "parcial", "undone"],
                   barmode="group", title="Desempenho da Turma por Lista",
                   labels={"list": "Lista de Exercícios", "value": "Número de Submissões"},
                   template="plotly_white")

fig_estudante = px.line(df_estudante, x="user_id", y=["expressoes", "estrutura_de_decisao", "repeticao_condicional", "repeticao_contada", "vetores"],
                        title="Desempenho dos Estudantes por Categoria",
                        labels={"user_id": "ID do Estudante", "value": "Número de Acertos"},
                        template="plotly_white")

# dropdown na tabela 'user_id' e 'GERAL'
opcoes = list(df_estudante['user_id'].unique())
opcoes.append("GERAL")

# modificações em textos HTML
app.layout = html.Div(children=[
    html.H1(children='DataViewer inPacta: Desempenho dos Estudantes'),
    html.H2(children='Gráficos de Desempenho por Lista e por Estudante'),

    html.Div(children='''
        Obs: Os gráficos mostram o desempenho da turma e dos estudantes em diferentes listas de atividade estudantis.
    '''),

    dcc.Tabs([
        dcc.Tab(label='Desempenho da Turma', children=[
            dcc.Graph(
                id='grafico_desempenho_turma',
                figure=fig_turma
            )
        ]),
        dcc.Tab(label='Desempenho por Estudantes', children=[
            dcc.Dropdown(opcoes, value='GERAL', id='lista_estudantes'),
            dcc.Graph(
                id='grafico_desempenho_estudantes',
                figure=fig_estudante
            )
        ]),
    ])
], className='custom-container')

# callback para modificar o gráfico dos estudantes
@app.callback(
    Output('grafico_desempenho_estudantes', 'figure'),
    Input('lista_estudantes', 'value')
)
def update_output(value):
    if value == "GERAL":
        fig = px.line(df_estudante, x="user_id", y=["expressoes", "estrutura_de_decisao", "repeticao_condicional", "repeticao_contada", "vetores"],
                      title="Desempenho dos Estudantes por Categoria",
                      labels={"user_id": "ID do Estudante", "value": "Número de Acertos"},
                      template="plotly_white")
    else:
        tabela_filtrada = df_estudante.loc[df_estudante['user_id'] == value, :]
        fig = px.line(tabela_filtrada, x="user_id", y=["expressoes", "estrutura_de_decisao", "repeticao_condicional", "repeticao_contada", "vetores"],
                      title=f"Desempenho do Estudante {value}",
                      labels={"user_id": "ID do Estudante", "value": "Número de Acertos"},
                      template="plotly_white")
    return fig

# usado para inicializar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
